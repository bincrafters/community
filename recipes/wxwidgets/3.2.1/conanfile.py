import os

from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMake
from conan.tools.files import get


class wxWidgetsConan(ConanFile):
    name = "wxwidgets"
    description = "wxWidgets is a C++ library that lets developers create applications for Windows, macOS, " \
                  "Linux and other platforms with a single code base."
    topics = ("conan", "wxwidgets", "gui", "ui")
    url = "https://github.com/bincrafters/conan-wxwidgets"
    homepage = "https://www.wxwidgets.org"
    license = "wxWidgets"
    generators = "CMakeDeps", "CMakeToolchain"
    settings = "os", "arch", "compiler", "build_type"

    options = {"shared": [True, False],
               "fPIC": [True, False],
               "unicode": [True, False],
               "compatibility": ["2.8", "3.0", "3.1"],
               "zlib": ["off", "sys", "zlib"],
               "png": ["off", "sys", "libpng"],
               "jpeg": ["off", "sys", "libjpeg", "libjpeg-turbo", "mozjpeg"],
               "tiff": ["off", "sys", "libtiff"],
               "expat": ["off", "sys", "expat"],
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
               "custom_enables": ["ANY"], # comma splitted list
               "custom_disables": ["ANY"]}
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

    _cmake = None

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
        if self.settings.os != 'Linux':
            del self.options.cairo

    def source(self):
        get(
            self, 
            **self.conan_data["sources"][self.version], 
            strip_root=True, 
        )

    def layout(self):
        cmake_layout(self, build_folder="build_subforlder")

    def build(self):
        cmake = self._configure_cmake()

        # wxWidgets CMake use $<CONFIG> generator expressions
        # when configuring include directories (e.g. mswu and mswud), 
        # thus if only build/install Debug, CMake will complain for missing
        # Release folder (e.g. mswu); if only build/install Release, CMake
        # will complain for missing Debug folder (e.g. mswud).
        cmake.build(build_type="Debug")
        cmake.build(build_type="Release")

    def package(self):
        cmake = self._configure_cmake()
        cmake.install(build_type="Debug")
        cmake.install(build_type="Release")

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "wxWidgets"))

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        cmake = CMake(self)

        # generic build options
        variables = {
            'wxBUILD_SHARED' : self.options.shared,
            'wxBUILD_SAMPLES' : 'OFF',
            'wxBUILD_TESTS' : 'OFF',
            'wxBUILD_DEMOS' : 'OFF',
            'wxBUILD_INSTALL' : True,
            'wxBUILD_COMPATIBILITY' : self.options.compatibility,
        }
        if self.settings.compiler == 'clang':
            variables['wxBUILD_PRECOMP'] = 'OFF'

        # platform-specific options
        if self.settings.compiler == 'msvc':
            variables['wxBUILD_USE_STATIC_RUNTIME'] = 'MT' in str(self.settings.compiler.runtime)
            variables['wxBUILD_MSVC_MULTIPROC'] = True
        if self.settings.os == 'Linux':
            # TODO : GTK3
            # cmake.definitions['wxBUILD_TOOLKIT'] = 'gtk3'
            variables['wxUSE_CAIRO'] = self.options.cairo
        # Disable some optional libraries that will otherwise lead to non-deterministic builds
        if self.settings.os != "Windows":
            variables['wxUSE_LIBSDL'] = 'OFF'
            variables['wxUSE_LIBICONV'] = 'OFF'
            variables['wxUSE_LIBNOTIFY'] = 'OFF'
            variables['wxUSE_LIBMSPACK'] = 'OFF'
            variables['wxUSE_LIBGNOMEVFS'] = 'OFF'

        variables['wxUSE_LIBPNG'] = 'sys' if self.options.png != 'off' else 'OFF'
        variables['wxUSE_LIBJPEG'] = 'sys' if self.options.jpeg != 'off' else 'OFF'
        variables['wxUSE_LIBTIFF'] = 'sys' if self.options.tiff != 'off' else 'OFF'
        variables['wxUSE_ZLIB'] = 'sys' if self.options.zlib != 'off' else 'OFF'
        variables['wxUSE_EXPAT'] = 'sys' if self.options.expat != 'off' else 'OFF'

        # wxWidgets features
        variables['wxUSE_UNICODE'] = self.options.unicode
        variables['wxUSE_SECRETSTORE'] = self.options.secretstore

        # wxWidgets libraries
        variables['wxUSE_AUI'] = self.options.aui
        variables['wxUSE_OPENGL'] = self.options.opengl
        variables['wxUSE_HTML'] = self.options.html
        variables['wxUSE_MEDIACTRL'] = self.options.mediactrl
        variables['wxUSE_PROPGRID'] = self.options.propgrid
        variables['wxUSE_DEBUGREPORT'] = self.options.debugreport
        variables['wxUSE_RIBBON'] = self.options.ribbon
        variables['wxUSE_RICHTEXT'] = self.options.richtext
        variables['wxUSE_SOCKETS'] = self.options.sockets
        variables['wxUSE_STC'] = self.options.stc
        variables['wxUSE_WEBVIEW'] = self.options.webview
        variables['wxUSE_XML'] = self.options.xml
        variables['wxUSE_XRC'] = self.options.xrc
        variables['wxUSE_HELP'] = self.options.help
        variables['wxUSE_WXHTML_HELP'] = self.options.html_help
        variables['wxUSE_URL'] = self.options.protocol
        variables['wxUSE_PROTOCOL'] = self.options.protocol
        variables['wxUSE_FS_INET'] = self.options.fs_inet

        for item in str(self.options.custom_enables).split(","):
            if len(item) > 0:
                variables[item] = True
        for item in str(self.options.custom_disables).split(","):
            if len(item) > 0:
                variables[item] = False

        cmake.configure(variables=variables)

        self._cmake = cmake
        return self._cmake
