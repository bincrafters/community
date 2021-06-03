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
        shutil.copy(
            src=os.path.join(self.source_folder, "1_packet.pcap"),
            dst=os.path.abspath("."),
        )
        bin_path = os.path.join("bin", "test_package")
        self.run(bin_path, run_environment=True)
