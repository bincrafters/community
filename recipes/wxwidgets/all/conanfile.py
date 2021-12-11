from conans import ConanFile, CMake, tools
import os


class wxWidgetsConan(ConanFile):
    name = "wxwidgets"
    description = "wxWidgets is a C++ library that lets developers create applications for Windows, macOS, " \
                  "Linux and other platforms with a single code base."
    topics = ("wxwidgets", "gui", "ui")
    url = "https://github.com/bincrafters/community"
    homepage = "https://www.wxwidgets.org"
    license = "wxWidgets"
    exports_sources = ["CMakeLists.txt", "patches/*"]
    generators = ["cmake", "cmake_find_package"]
    settings = "os", "arch", "compiler", "build_type"
    _cmake = None

    options = {"shared": [True, False],
               "fPIC": [True, False],
               "unicode": [True, False],
               "compatibility": ["2.8", "3.0", "3.1"],
               "zlib": ["off", "zlib"],
               "png": ["off", "libpng"],
               "jpeg": ["off", "libjpeg", "libjpeg-turbo", "mozjpeg"],
               "tiff": ["off", "libtiff"],
               "expat": ["off", "expat"],
               "secretstore": [True, False],
               "aui": [True, False],
               "opengl": [True, False],
               "html": [True, False],
               "mediactrl": [True, False],  # disabled by default as wxWidgets still uses deprecated GStreamer 0.10
               "propgrid": [True, False],
               "debugreport": [True, False],
               "ribbon": [True, False],
               "richtext": [True, False],
               "sockets": [True, False],
               "stc": [True, False],
               "webview": [True, False],
               "xml": [True, False],
               "xrc": [True, False],
               "cairo": [True, False],
               "help": [True, False],
               "html_help": [True, False],
               "url": [True, False],
               "protocol": [True, False],
               "fs_inet": [True, False],
               "custom_enables": "ANY", # comma splitted list
               "custom_disables": "ANY"}
    default_options = {
               "shared": False,
               "fPIC": True,
               "unicode": True,
               "compatibility": "3.0",
               "zlib": "zlib",
               "png": "libpng",
               "jpeg": "libjpeg",
               "tiff": "libtiff",
               "expat": "expat",
               "secretstore": True,
               "aui": True,
               "opengl": True,
               "html": True,
               "mediactrl": False,
               "propgrid": True,
               "debugreport": True,
               "ribbon": True,
               "richtext": True,
               "sockets": True,
               "stc": True,
               "webview": True,
               "xml": True,
               "xrc": True,
               "cairo": True,
               "help": True,
               "html_help": True,
               "url": True,
               "protocol": True,
               "fs_inet": True,
               "custom_enables": "",
               "custom_disables": ""
    }
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
        if self.settings.os != 'Linux':
            self.options.remove('cairo')

    def system_requirements(self):
        if self.settings.os == 'Linux' and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                packages = []
                if self.options.secretstore:
                    packages.append('libsecret-1-dev')
                if self.options.webview:
                    # TODO: Why is libsoup required?
                    # Can't find a reference in the docs
                    packages.extend(['libsoup2.4-dev',
                                     'libwebkit2gtk-4.0-dev'])
                if self.options.cairo:
                    packages.append("libcairo2-dev")
                for package in packages:
                    installer.install(package)

    def build_requirements(self):
        self.build_requires("ninja/1.10.2")

    def requirements(self):
        if self.settings.os == 'Linux':
            self.requires('xorg/system')
            self.requires("gtk/3.24.24")
            if self.options.opengl:
                self.requires('opengl/system')
        if self.options.png == 'libpng':
            self.requires('libpng/1.6.37')
        if self.options.jpeg == 'libjpeg':
            self.requires('libjpeg/9d')
        elif self.options.jpeg == 'libjpeg-turbo':
            self.requires('libjpeg-turbo/2.1.1')
        elif self.options.jpeg == 'mozjpeg':
            self.requires('mozjpeg/3.3.1')
        if self.options.tiff == 'libtiff':
            self.requires('libtiff/4.0.9')
        if self.options.zlib == 'zlib':
            self.requires('zlib/1.2.11')
        if self.options.expat == 'expat':
            self.requires('expat/2.4.1')
        # TODO: Does not work right now
        # if self.options.get_safe("cairo"):
        #    self.requires("cairo/1.17.4")
        if self.options.mediactrl:
            self.requires("gstreamer/1.19.2")
            self.requires("gst-plugins-base/1.19.2")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        cmake = CMake(self)

        # generic build options
        cmake.definitions['wxBUILD_SHARED'] = self.options.shared
        cmake.definitions['wxBUILD_SAMPLES'] = 'OFF'
        cmake.definitions['wxBUILD_TESTS'] = 'OFF'
        cmake.definitions['wxBUILD_DEMOS'] = 'OFF'
        cmake.definitions['wxBUILD_INSTALL'] = True
        cmake.definitions['wxBUILD_COMPATIBILITY'] = self.options.compatibility
        if self.settings.compiler == 'clang':
            cmake.definitions['wxBUILD_PRECOMP'] = 'OFF'

        # platform-specific options
        if self.settings.compiler == 'Visual Studio':
            cmake.definitions['wxBUILD_USE_STATIC_RUNTIME'] = 'MT' in str(self.settings.compiler.runtime)
            cmake.definitions['wxBUILD_MSVC_MULTIPROC'] = True
        if self.settings.os == 'Linux':
            cmake.definitions['wxBUILD_TOOLKIT'] = 'gtk3'
            cmake.definitions['wxUSE_CAIRO'] = self.options.cairo
        # Disable some optional libraries that will otherwise lead to non-deterministic builds
        if self.settings.os != "Windows":
            cmake.definitions['wxUSE_LIBSDL'] = 'OFF'
            cmake.definitions['wxUSE_LIBICONV'] = 'OFF'
            cmake.definitions['wxUSE_LIBNOTIFY'] = 'OFF'
            cmake.definitions['wxUSE_LIBMSPACK'] = 'OFF'
            cmake.definitions['wxUSE_LIBGNOMEVFS'] = 'OFF'

        cmake.definitions['wxUSE_LIBPNG'] = 'sys' if self.options.png != 'off' else 'OFF'
        cmake.definitions['wxUSE_LIBJPEG'] = 'sys' if self.options.jpeg != 'off' else 'OFF'
        cmake.definitions['wxUSE_LIBTIFF'] = 'sys' if self.options.tiff != 'off' else 'OFF'
        cmake.definitions['wxUSE_ZLIB'] = 'sys' if self.options.zlib != 'off' else 'OFF'
        cmake.definitions['wxUSE_EXPAT'] = 'sys' if self.options.expat != 'off' else 'OFF'

        # wxWidgets features
        cmake.definitions['wxUSE_UNICODE'] = self.options.unicode
        cmake.definitions['wxUSE_SECRETSTORE'] = self.options.secretstore

        # wxWidgets libraries
        cmake.definitions['wxUSE_AUI'] = self.options.aui
        cmake.definitions['wxUSE_OPENGL'] = self.options.opengl
        cmake.definitions['wxUSE_HTML'] = self.options.html
        cmake.definitions['wxUSE_MEDIACTRL'] = self.options.mediactrl
        cmake.definitions['wxUSE_PROPGRID'] = self.options.propgrid
        cmake.definitions['wxUSE_DEBUGREPORT'] = self.options.debugreport
        cmake.definitions['wxUSE_RIBBON'] = self.options.ribbon
        cmake.definitions['wxUSE_RICHTEXT'] = self.options.richtext
        cmake.definitions['wxUSE_SOCKETS'] = self.options.sockets
        cmake.definitions['wxUSE_STC'] = self.options.stc
        cmake.definitions['wxUSE_WEBVIEW'] = self.options.webview
        cmake.definitions['wxUSE_XML'] = self.options.xml
        cmake.definitions['wxUSE_XRC'] = self.options.xrc
        cmake.definitions['wxUSE_HELP'] = self.options.help
        cmake.definitions['wxUSE_WXHTML_HELP'] = self.options.html_help
        cmake.definitions['wxUSE_URL'] = self.options.protocol
        cmake.definitions['wxUSE_PROTOCOL'] = self.options.protocol
        cmake.definitions['wxUSE_FS_INET'] = self.options.fs_inet

        for item in str(self.options.custom_enables).split(","):
            if len(item) > 0:
                cmake.definitions[item] = True
        for item in str(self.options.custom_disables).split(","):
            if len(item) > 0:
                cmake.definitions[item] = False

        cmake.configure(build_folder=self._build_subfolder)

        self._cmake = cmake
        return self._cmake

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # copy setup.h
        self.copy(pattern='*setup.h', dst=os.path.join('include', 'wx'), src=os.path.join(self._build_subfolder, 'lib'),
                  keep_path=False)

        if self.settings.os == 'Windows':
            # copy wxrc.exe
            self.copy(pattern='*', dst='bin', src=os.path.join(self._build_subfolder, 'bin'), keep_path=False)
        else:
            # make relative symlink
            bin_dir = os.path.join(self.package_folder, 'bin')
            for x in os.listdir(bin_dir):
                filename = os.path.join(bin_dir, x)
                if os.path.islink(filename):
                    target = os.readlink(filename)
                    if os.path.isabs(target):
                        rel = os.path.relpath(target, bin_dir)
                        os.remove(filename)
                        os.symlink(rel, filename)

    def package_info(self):
        _version = tools.Version(self.version)
        version_suffix_major_minor = '-%s.%s' % (_version.major, _version.minor)
        unicode = 'u' if self.options.unicode else ''

        # wx no longer uses a debug suffix for non-windows platforms from 3.1.3 onwards
        use_debug_suffix = False
        if self.settings.build_type == 'Debug' and self.settings.os == 'Windows':
            use_debug_suffix = True

        debug = 'd' if use_debug_suffix else ''

        if self.settings.os == 'Linux':
            prefix = 'wx_'
            toolkit = 'gtk3'
            version = ''
            suffix = version_suffix_major_minor
        elif self.settings.os == 'Macos':
            prefix = 'wx_'
            toolkit = 'osx_cocoa'
            version = ''
            suffix = version_suffix_major_minor
        elif self.settings.os == 'Windows':
            toolkit = 'msw'
            if self.settings.compiler == 'Visual Studio':
                prefix = 'wx'
                version = '%s%s' % (_version.major, _version.minor)
                suffix = ''
            else:
                prefix = 'wx_'
                version = ''
                suffix = version_suffix_major_minor

        def base_library_pattern(library):
            return '{prefix}base{version}{unicode}{debug}_%s{suffix}' % library

        def library_pattern(library):
            return '{prefix}{toolkit}{version}{unicode}{debug}_%s{suffix}' % library

        libs = []
        if not self.options.shared:
            regex_suffix = '{debug}' if self.settings.os == "Windows" else '{suffix}'
            libs.append('wxregex{unicode}' + regex_suffix)
        libs.append('{prefix}base{version}{unicode}{debug}{suffix}')
        libs.append(library_pattern('core'))
        libs.append(library_pattern('adv'))
        if self.options.sockets:
            libs.append(base_library_pattern('net'))
        if self.options.xml:
            libs.append(base_library_pattern('xml'))
        if self.options.aui:
            libs.append(library_pattern('aui'))
        if self.options.opengl:
            libs.append(library_pattern('gl'))
        if self.options.html:
            libs.append(library_pattern('html'))
        if self.options.mediactrl:
            libs.append(library_pattern('media'))
        if self.options.propgrid:
            libs.append(library_pattern('propgrid'))
        if self.options.debugreport:
            libs.append(library_pattern('qa'))
        if self.options.ribbon:
            libs.append(library_pattern('ribbon'))
        if self.options.richtext:
            libs.append(library_pattern('richtext'))
        if self.options.stc:
            if not self.options.shared:
                scintilla_suffix = '{debug}' if self.settings.os == "Windows" else '{suffix}'
                libs.append('wxscintilla' + scintilla_suffix)
            libs.append(library_pattern('stc'))
        if self.options.webview:
            libs.append(library_pattern('webview'))
        if self.options.xrc:
            libs.append(library_pattern('xrc'))
        for lib in reversed(libs):
            self.cpp_info.libs.append(lib.format(prefix=prefix,
                                                 toolkit=toolkit,
                                                 version=version,
                                                 unicode=unicode,
                                                 debug=debug,
                                                 suffix=suffix))

        self.cpp_info.defines.append('wxUSE_GUI=1')
        if self.settings.build_type == 'Debug':
            self.cpp_info.defines.append('__WXDEBUG__')
        if self.options.shared:
            self.cpp_info.defines.append('WXUSINGDLL')
        if self.settings.os == 'Linux':
            self.cpp_info.defines.append('__WXGTK__')
            self.cpp_info.system_libs.extend(['dl', 'pthread', 'SM'])
        elif self.settings.os == 'Macos':
            self.cpp_info.defines.extend(['__WXMAC__', '__WXOSX__', '__WXOSX_COCOA__'])
            for framework in ['Carbon',
                              'Cocoa',
                              'AudioToolbox',
                              'OpenGL',
                              'AVKit',
                              'AVFoundation',
                              'Foundation',
                              'IOKit',
                              'ApplicationServices',
                              'CoreText',
                              'CoreGraphics',
                              'CoreServices',
                              'CoreMedia',
                              'Security',
                              'ImageIO',
                              'System',
                              'WebKit',
                              'QuartzCore']:
                self.cpp_info.frameworks.append(framework)
        elif self.settings.os == 'Windows':
            # see cmake/init.cmake
            compiler_prefix = {'Visual Studio': 'vc',
                               'gcc': 'gcc',
                               'clang': 'clang'}.get(str(self.settings.compiler))

            arch_suffix = '_x64' if self.settings.arch == 'x86_64' else ''
            lib_suffix = '_dll' if self.options.shared else '_lib'
            libdir = '%s%s%s' % (compiler_prefix, arch_suffix, lib_suffix)
            libdir = os.path.join('lib', libdir)
            self.cpp_info.bindirs.append(libdir)
            self.cpp_info.libdirs.append(libdir)
            self.cpp_info.defines.append('__WXMSW__')
            # disable annoying auto-linking
            self.cpp_info.defines.extend(['wxNO_NET_LIB',
                                          'wxNO_XML_LIB',
                                          'wxNO_REGEX_LIB',
                                          'wxNO_ZLIB_LIB',
                                          'wxNO_JPEG_LIB',
                                          'wxNO_PNG_LIB',
                                          'wxNO_TIFF_LIB',
                                          'wxNO_ADV_LIB',
                                          'wxNO_HTML_LIB',
                                          'wxNO_GL_LIB',
                                          'wxNO_QA_LIB',
                                          'wxNO_XRC_LIB',
                                          'wxNO_AUI_LIB',
                                          'wxNO_PROPGRID_LIB',
                                          'wxNO_RIBBON_LIB',
                                          'wxNO_RICHTEXT_LIB',
                                          'wxNO_MEDIA_LIB',
                                          'wxNO_STC_LIB',
                                          'wxNO_WEBVIEW_LIB'])
            self.cpp_info.system_libs.extend(['kernel32',
                                       'user32',
                                       'gdi32',
                                       'comdlg32',
                                       'winspool',
                                       'shell32',
                                       'comctl32',
                                       'ole32',
                                       'oleaut32',
                                       'imm32',
                                       'uuid',
                                       'wininet',
                                       'rpcrt4',
                                       'winmm',
                                       'advapi32',
                                       'wsock32'])
            # Link a few libraries that are needed when using gcc on windows
            if self.settings.compiler == 'gcc':
                self.cpp_info.system_libs.extend(['uxtheme',
                                           'version',
                                           'shlwapi',
                                           'oleacc'])
        if self.settings.compiler == 'Visual Studio':
            self.cpp_info.includedirs.append(os.path.join('include', 'msvc'))
        else:
            include_path = os.path.join("include", "wx{}".format(version_suffix_major_minor))
            self.cpp_info.includedirs = [include_path] + self.cpp_info.includedirs
