from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import os

required_conan_version = ">=1.33.0"


class PortaudioConan(ConanFile):
    name = "portaudio"
    topics = ("portaudio", "audio", "recording", "playing")
    description = "PortAudio is a free, cross-platform, open-source, audio I/O library"
    url = "https://github.com/bincrafters/community"
    homepage = "http://www.portaudio.com"
    license = "MIT"
    exports = ["CMakeLists.txt"]
    generators = ["cmake"]

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_alsa": [True, False],
        "with_jack": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_alsa": False,
        "with_jack": False
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None

    def validate(self):
        if self.settings.compiler == "apple-clang" and tools.Version(self.settings.compiler.version) < "11":
            raise ConanInvalidConfiguration("This recipe does not support Apple-Clang versions < 11")

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.settings.os == "Windows":
            self.options.remove("fPIC")
        if self.settings.os != "Linux":
            self.options.remove("with_alsa")
            self.options.remove("with_jack")

    def requirements(self):
        if self.settings.os == "Linux":
            if self.options.with_alsa:
                self.requires("libalsa/1.1.9")

    def system_requirements(self):
        if self.settings.os == "Linux":
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                installer.install("libasound2-dev") 
                if self.options.with_jack:
                    installer.install("libjack-dev")
            elif tools.os_info.with_yum:
                installer = tools.SystemPackageTool()
                installer.install("alsa-lib-devel")
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    installer.install("glibmm24.i686")
                    installer.install("glibc-devel.i686")
                if self.options.with_jack:
                    installer.install("jack-audio-connection-kit-devel")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["PA_BUILD_STATIC"] = not self.options.shared
            self._cmake.definitions["PA_BUILD_SHARED"] = self.options.shared
            self._cmake.definitions["PA_USE_JACK"] = self.options.get_safe("with_jack", False)
            if self.options.get_safe("with_alsa", False): # with_alsa=False just makes portaudio use the Linux distro's alsa
                                                          # as a workaround to the fact that conancenter's alsa does not work,
                                                          # at least some of the time (no devices detected by portaudio)
                self._cmake.definitions["PA_USE_ALSA"] = True
            self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE*", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))
        # tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        # tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        # TODO: Add components with > 19.7, because the next release will most likely have major changes for their CMake setup
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(["CoreAudio", "AudioToolbox", "AudioUnit", "CoreServices", "Carbon"])

        if self.settings.os == "Windows" and self.settings.compiler == "gcc" and not self.options.shared:
            self.cpp_info.system_libs.extend(["winmm", "setupapi"])

        if self.settings.os == "Linux" and not self.options.shared:
            self.cpp_info.system_libs.extend(["m", "pthread", "asound"])
            if self.options.with_jack:
                self.cpp_info.system_libs.append("jack")
