from conans import ConanFile, CMake, tools
import os


class SfmlConan(ConanFile):
    name = 'sfml'
    description = 'Simple and Fast Multimedia Library'
    topics = ('sfml', 'multimedia')
    url = 'https://github.com/bincrafters/community'
    homepage = 'https://github.com/SFML/SFML'
    license = "ZLIB"
    exports_sources = ['CMakeLists.txt', 'patches/*']
    generators = 'cmake', 'cmake_find_package_multi'
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

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  strip_root=True, destination=self._source_subfolder)
        tools.rmdir(os.path.join(self._source_subfolder, "extlibs"))

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
        self._cmake.definitions['SFML_INSTALL_PKGCONFIG_FILES'] = False
        self._cmake.definitions['SFML_GENERATE_PDB'] = False
        if self.settings.os == "Macos":
            self._cmake.definitions['SFML_OSX_FRAMEWORK'] = "-framework AudioUnit"
        elif self.settings.compiler == 'Visual Studio':
            if self.settings.compiler.runtime == 'MT' or self.settings.compiler.runtime == 'MTd':
                self._cmake.definitions['SFML_USE_STATIC_STD_LIBS'] = True

        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        for p in self.conan_data["patches"][self.version]:
            tools.patch(**p)

        with tools.vcvars(self.settings, force=True, filter_known_paths=False) if self.settings.compiler == 'Visual Studio' else tools.no_op():
            cmake = self._configure_cmake()
        cmake.build()

    def package(self):
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
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))


    def _get_decorated_lib(self, name):
        suffix = '-s' if not self.options.shared else ''
        suffix += '-d' if self.settings.build_type == 'Debug' else ''
        return name + suffix

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "SFML"
        self.cpp_info.names["cmake_find_package_multi"] = "SFML"
        self.cpp_info.names["pkg_config"] = "SFML"

        self.cpp_info.components["sfml-system"].names["pkg_config"] = "system"
        self.cpp_info.components["sfml-system"].names["cmake_find_package"] = "system"
        self.cpp_info.components["sfml-system"].names["cmake_find_package_multi"] = "system"
        self.cpp_info.components["sfml-system"].libs = [self._get_decorated_lib("sfml-system")]
        if not self.options.shared:
            self.cpp_info.components["sfml-system"].defines = ['SFML_STATIC']
        if self.settings.os == 'Windows':
            self.cpp_info.components["sfml-system"].system_libs = ['winmm']
        elif self.settings.os == 'Linux':
            self.cpp_info.components["sfml-system"].system_libs = ['rt']
        elif self.settings.os == 'Android':
            self.cpp_info.components["sfml-system"].system_libs = ['android', 'log']
        if self.settings.os != 'Windows':
            self.cpp_info.components["sfml-system"].system_libs = ['pthread']

        if self.settings.os in ['Windows', 'Android', 'iOS']:
            sfml_main_suffix = '-d' if self.settings.build_type == 'Debug' else ''
            self.cpp_info.components["sfml-main"].libs = ["sfml-main" + sfml_main_suffix]
            if not self.options.shared:
                self.cpp_info.components["sfml-main"].defines = ['SFML_STATIC']
            if self.settings.os == 'Android':
                self.cpp_info.components["sfml-main"].libs.append(self._get_decorated_lib("sfml-activity"))
                self.cpp_info.components["sfml-main"].system_libs = ['android', 'log']

        if self.options.window or self.options.graphics:
            self.cpp_info.components["sfml-window"].names["pkg_config"] = "window"
            self.cpp_info.components["sfml-window"].names["cmake_find_package"] = "window"
            self.cpp_info.components["sfml-window"].names["cmake_find_package_multi"] = "window"
            self.cpp_info.components["sfml-window"].libs = [self._get_decorated_lib("sfml-window")]
            self.cpp_info.components["sfml-window"].requires = ["opengl::opengl", "sfml-system"]
            if self.settings.os in ['Linux', 'FreeBSD']:
                self.cpp_info.components["sfml-window"].requires.append('xorg::xorg')
            if not self.options.shared:
                self.cpp_info.components["sfml-window"].defines = ['SFML_STATIC']
            if self.settings.os == 'Windows':
                self.cpp_info.components["sfml-window"].system_libs = ['winmm', 'gdi32']
            if self.settings.os == 'Linux':
                self.cpp_info.components["sfml-window"].system_libs = ['udev']
            if self.settings.os == 'FreeBSD':
                self.cpp_info.components["sfml-window"].system_libs = ['usbhid']
            elif self.settings.os == "Macos":
                self.cpp_info.components["sfml-window"].frameworks['Foundation', 'AppKit', 'IOKit', 'Carbon']
                if not self.options.shared:
                    self.cpp_info.components["sfml-window"].exelinkflags.append("-ObjC")
                    self.cpp_info.components["sfml-window"].sharedlinkflags = self.cpp_info.components["sfml-window"].exelinkflags
            elif self.settings.os == "iOS":
                self.cpp_info.frameworks['Foundation', 'UIKit', 'CoreGraphics', 'QuartzCore', 'CoreMotion']
            elif self.settings.os == "Android":
                self.cpp_info.components["sfml-window"].system_libs = ['android']

        if self.options.graphics:
            self.cpp_info.components["sfml-graphics"].names["pkg_config"] = "graphics"
            self.cpp_info.components["sfml-graphics"].names["cmake_find_package"] = "graphics"
            self.cpp_info.components["sfml-graphics"].names["cmake_find_package_multi"] = "graphics"
            self.cpp_info.components["sfml-graphics"].libs = [self._get_decorated_lib("sfml-graphics")]
            self.cpp_info.components["sfml-graphics"].requires = ["freetype::freetype", "stb::stb", "sfml-window"]
            if not self.options.shared:
                self.cpp_info.components["sfml-graphics"].defines = ['SFML_STATIC']
            if self.settings.os == 'Linux':
                self.cpp_info.components["sfml-graphics"].system_libs = ['udev']

        if self.options.network:
            self.cpp_info.components["sfml-network"].names["pkg_config"] = "network"
            self.cpp_info.components["sfml-network"].names["cmake_find_package"] = "network"
            self.cpp_info.components["sfml-network"].names["cmake_find_package_multi"] = "network"
            self.cpp_info.components["sfml-network"].libs = [self._get_decorated_lib("sfml-network")]
            self.cpp_info.components["sfml-network"].requires = ["sfml-system"]
            if not self.options.shared:
                self.cpp_info.components["sfml-network"].defines = ['SFML_STATIC']
            if self.settings.os == 'Windows':
                self.cpp_info.components["sfml-network"].system_libs = ['ws2_32']

        if self.options.audio:
            self.cpp_info.components["sfml-audio"].names["pkg_config"] = "audio"
            self.cpp_info.components["sfml-audio"].names["cmake_find_package"] = "audio"
            self.cpp_info.components["sfml-audio"].names["cmake_find_package_multi"] = "audio"
            self.cpp_info.components["sfml-audio"].libs = [self._get_decorated_lib("sfml-audio")]
            self.cpp_info.components["sfml-audio"].requires = ["openal::openal", "flac::flac", "ogg::ogg", "vorbis::vorbis", "sfml-system"]
            if not self.options.shared:
                self.cpp_info.components["sfml-audio"].defines = ['SFML_STATIC']
            if self.settings.os == "Android":
                self.cpp_info.components["sfml-audio"].system_libs = ['android']
