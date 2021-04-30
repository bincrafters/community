import os
from conans import ConanFile, CMake, tools

class ConanRecipe(ConanFile):
    name = "portaudio"
    settings = "os", "compiler", "build_type", "arch"
    generators = ["cmake"]
    sources_folder = "sources"
    description = "Conan package for the Portaudio library"
    url = "https://github.com/bincrafters/conan-portaudio"
    license = "http://www.portaudio.com/license.html"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_alsa":  [True, False],
        "with_jack":  [True, False],
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        "with_alsa":  True,
        "with_jack":  True,
    }
    exports = ["CMakeLists.txt"]

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.settings.os == "Windows":
            self.options.remove("fPIC")
        if self.settings.os != "Linux":
            self.options.remove("with_alsa")
            self.options.remove("with_jack")

    def requirements(self):
        if self.settings.os == 'Linux':
            if self.options.with_alsa:
                self.requires('libalsa/1.1.9')

    def system_requirements(self):
        if self.settings.os == 'Linux':
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                if self.options.with_jack:
                    installer.install("libjack-dev")
            elif tools.os_info.with_yum:
                installer = tools.SystemPackageTool()
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    installer.install("glibmm24.i686")
                    installer.install("glibc-devel.i686")
                if self.options.with_jack:
                    installer.install("jack-audio-connection-kit-devel")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        # remove prefix 'v'
        os.rename(self.name + "-" + self.version[1:], self.sources_folder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["PA_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["PA_BUILD_SHARED"] = self.options.shared
        if self.settings.os == "Linux":
            cmake.definitions["PA_USE_ALSA"] = self.options.with_alsa
            cmake.definitions["PA_USE_JACK"] = self.options.with_jack
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(["CoreAudio","AudioToolbox","AudioUnit","CoreServices","CoreFoundation"])

        if self.settings.os == "Windows" and self.settings.compiler == "gcc" and not self.options.shared:
            self.cpp_info.system_libs.append('winmm')

        if self.settings.os == "Linux" and not self.options.shared:
            self.cpp_info.system_libs.extend(['m', 'pthread'])
            if self.options.with_jack:
                self.cpp_info.system_libs.append('jack')
