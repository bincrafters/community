from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.definitions['WITH_WINDOW'] = self.options['sfml'].window
        cmake.definitions['WITH_GRAPHICS'] = self.options['sfml'].graphics
        cmake.definitions['WITH_AUDIO'] = self.options['sfml'].audio
        cmake.definitions['WITH_NETWORK'] = self.options['sfml'].network
        cmake.configure()
        cmake.build()

    def test(self):
        bin_path = os.path.join("bin", "test_package")
        self.run(bin_path, run_environment=True)
