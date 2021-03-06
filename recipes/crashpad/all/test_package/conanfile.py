from conans import ConanFile, CMake, tools, RunEnvironment
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        test_env_dir = "test_env"
        tools.mkdir(test_env_dir)
        bin_path = os.path.join("bin", "test_package")
        handler_exe = "crashpad_handler.exe" if self.settings.os == "Windows" else "crashpad_handler"
        handler_bin_path = os.path.join(self.deps_cpp_info['crashpad'].rootpath, "bin", handler_exe)
        self.run("%s %s/db %s" % (bin_path, test_env_dir, handler_bin_path), run_environment=True)
