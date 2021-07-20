from conans import ConanFile, CMake, tools
import os


class SfmlConan(ConanFile):
    name = 'sfml'
    description = 'Simple and Fast Multimedia Library'
    topics = ('conan', 'sfml', 'multimedia')
    url = 'https://github.com/bincrafters/conan-sfml'
    homepage = 'https://github.com/SFML/SFML'
    license = "ZLIB"
    exports_sources = ['CMakeLists.txt', 'patches/*']
    generators = 'cmake'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
        'window': [True, False],
        'graphics': [True, False],
        'network': [True, False],
        'audio': [True, False],
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'window': True,
        'graphics': True,
        'network': True,
        'audio': True
    }
    _source_subfolder = 'source_subfolder'
    _build_subfolder = 'build_subfolder'

    _cmake = None

    def config_options(self):
        if self.settings.os == 'Windows':
            self.options.remove('fPIC')

    def configure(self):
        if self.options.graphics:
            self.options.window = True

    def requirements(self):
        if self.options.graphics:
            self.requires('freetype/2.10.4')
            self.requires('stb/20200203')
        if self.options.audio:
            self.requires('openal/1.21.0')
            self.requires('flac/1.3.3')
            self.requires('ogg/1.3.4')
            self.requires('vorbis/1.3.7')
        if self.options.window:
            if self.settings.os == 'Linux':
                self.requires('xorg/system')
            self.requires('opengl/system')

    def system_requirements(self):
        if self.settings.os == 'Linux' and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                packages = []
                if self.options.window:
                    packages.extend(['libudev-dev'])

                for package in packages:
                    installer.install(package)

    def build_requirements(self):
        if self.settings.os == 'Linux':
            if not tools.which('pkg-config'):
                self.build_requires('pkgconf/1.7.4')

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  strip_root=True, destination=self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions['SFML_DEPENDENCIES_INSTALL_PREFIX'] = self.package_folder
        self._cmake.definitions['SFML_MISC_INSTALL_PREFIX'] = self.package_folder
        self._cmake.definitions['SFML_BUILD_WINDOW'] = self.options.window
        self._cmake.definitions['SFML_BUILD_GRAPHICS'] = self.options.graphics
        self._cmake.definitions['SFML_BUILD_NETWORK'] = self.options.network
        self._cmake.definitions['SFML_BUILD_AUDIO'] = self.options.audio
        if self.settings.os == "Macos":
            self._cmake.definitions['SFML_OSX_FRAMEWORK'] = "-framework AudioUnit"
        elif self.settings.compiler == 'Visual Studio':
            if self.settings.compiler.runtime == 'MT' or self.settings.compiler.runtime == 'MTd':
                self._cmake.definitions['SFML_USE_STATIC_STD_LIBS'] = True

        extlibs_folder = os.path.join(self._source_subfolder, 'extlibs')
        ext_folder = os.path.join(self._source_subfolder, 'ext')
        os.rename(extlibs_folder, ext_folder)
        self._cmake.configure(build_folder=self._build_subfolder)
        os.rename(ext_folder, extlibs_folder)
        return self._cmake

    def build(self):
        for p in self.conan_data["patches"][self.version]:
            tools.patch(**p)

        with tools.vcvars(self.settings, force=True, filter_known_paths=False) if self.settings.compiler == 'Visual Studio' else tools.no_op():
            cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern='license.md', dst='licenses', src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        if self.settings.os == 'Macos' and self.options.shared and self.options.graphics:
            with tools.chdir(os.path.join(self.package_folder, 'lib')):
                suffix = '-d' if self.settings.build_type == 'Debug' else ''
                graphics_library = 'libsfml-graphics%s.%s.dylib' % (suffix, self.version)
                old_path = '@rpath/../Frameworks/freetype.framework/Versions/A/freetype'
                new_path = '@loader_path/../freetype.framework/Versions/A/freetype'
                command = 'install_name_tool -change %s %s %s' % (old_path, new_path, graphics_library)
                self.output.warn(command)
                self.run(command)

    def package_info(self):
        self.cpp_info.defines = ['SFML_STATIC'] if not self.options.shared else []

        suffix = '-s' if not self.options.shared else ''
        suffix += '-d' if self.settings.build_type == 'Debug' else ''
        sfml_main_suffix = '-d' if self.settings.build_type == 'Debug' else ''

        if self.options.graphics:
            self.cpp_info.libs.append('sfml-graphics' + suffix)
        if self.options.window:
            self.cpp_info.libs.append('sfml-window' + suffix)
        if self.options.network:
            self.cpp_info.libs.append('sfml-network' + suffix)
        if self.options.audio:
            self.cpp_info.libs.append('sfml-audio' + suffix)
        if self.settings.os == 'Windows':
            self.cpp_info.libs.append('sfml-main' + sfml_main_suffix)
        self.cpp_info.libs.append('sfml-system' + suffix)

        if not self.options.shared:
            if self.settings.os == 'Windows':
                if self.options.window:
                    self.cpp_info.system_libs.append('gdi32')
                if self.options.network:
                    self.cpp_info.system_libs.append('ws2_32')
                self.cpp_info.system_libs.append('winmm')
            elif self.settings.os == 'Linux':
                self.cpp_info.system_libs.append('pthread')
                if self.options.graphics:
                    self.cpp_info.system_libs.append('udev')
            elif self.settings.os == "Macos":
                if self.options.window:
                    self.cpp_info.frameworks.extend(['Cocoa', 'IOKit', 'Carbon'])
                self.cpp_info.exelinkflags.append("-ObjC")
                self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
