from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class WinpcapConan(ConanFile):
    name = "winpcap"
    version = "4.1.2"
    settings = "os", "compiler", "build_type", "arch"
    description = "The WinPcap packet capture library."
    homepage = "https://www.winpcap.org/"
    url = "https://github.com/bincrafters/community"
    license = "Muliple"

    def configure(self):
        if self.settings.os != "Windows":
            raise ConanInvalidConfiguration("WinPcap is only supported for Windows. For other operating systems, look for libpcap.")

    def package(self):
        sha256 = "ea799cf2f26e4afb1892938070fd2b1ca37ce5cf75fec4349247df12b784edbd"
        winpcap_dev_pack_url = "https://www.winpcap.org/install/bin/WpdPack_4_1_2.zip"
        tools.get(winpcap_dev_pack_url, sha256=sha256)
        lib_dir = "WpdPack/Lib"
        if self.settings.arch == "x86_64":
            lib_dir += "/x64"
        self.copy("*.lib", src=lib_dir, dst="lib", keep_path=False)
        self.copy("*.h", src="WpdPack/Include", dst="include")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
