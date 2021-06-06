from conans import ConanFile, CMake
import os
import shutil


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        for file_name in ["1_packet.pcap", "wpcap.dll", "Packet.dll"]:
            shutil.copy(
                src=os.path.join(self.source_folder, file_name),
                dst=os.path.abspath("."),
            )
        bin_path = os.path.join("bin", "test_package")
        self.run(bin_path, run_environment=True)
