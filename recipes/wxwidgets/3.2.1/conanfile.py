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

    def source(self):
        get(
            self, 
            **self.conan_data["sources"][self.version], 
            strip_root=True, 
        )

    def layout(self):
        cmake_layout(self, build_folder="build_subforlder")

    def build(self):
        cmake = CMake(self)
        cmake.configure()

        # wxWidgets CMake use $<CONFIG> generator expressions
        # when configuring include directories (e.g. mswu and mswud), 
        # thus if only build/install Debug, CMake will complain for missing
        # Release folder (e.g. mswu); if only build/install Release, CMake
        # will complain for missing Debug folder (e.g. mswud).
        cmake.build(build_type="Debug")
        cmake.build(build_type="Release")

    def package(self):
        cmake = CMake(self)
        cmake.install(build_type="Debug")
        cmake.install(build_type="Release")

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "none")
        self.cpp_info.builddirs.append(os.path.join("lib", "cmake", "wxWidgets"))
