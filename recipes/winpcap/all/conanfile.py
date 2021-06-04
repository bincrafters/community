from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class WinpcapConan(ConanFile):
    name = "winpcap"
    settings = "os", "compiler", "build_type", "arch"
    description = "The WinPcap packet capture library."
    homepage = "https://www.winpcap.org/"
    url = "https://github.com/bincrafters/community"
    license = "Muliple"

    def configure(self):
        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration("WinPcap is only supported for Windows. For other operating systems, look for libpcap.")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])

    def package(self):
        lib_dir = "WpdPack/Lib"
        if self.settings.arch == "x86_64":
            lib_dir += "/x64"
        self.copy("*.lib", src=lib_dir, dst="lib", keep_path=False)
        self.copy("*.h", src="WpdPack/Include", dst="include")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
