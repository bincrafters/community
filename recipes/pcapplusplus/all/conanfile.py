from conans import ConanFile, tools, MSBuild, AutoToolsBuildEnvironment
from conans.errors import ConanInvalidConfiguration
import os


class PcapplusplusConan(ConanFile):
    name = "pcapplusplus"
    license = "Unlicense"
    description = "PcapPlusPlus is a multiplatform C++ library for capturing, parsing and crafting of network packets"
    topics = ("conan", "pcapplusplus", "pcap", "network", "security", "packet")
    url = "https://github.com/bincrafters/community"
    homepage = "https://github.com/seladb/PcapPlusPlus"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "immediate_mode": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "immediate_mode": False,
    }
    generators = "make", "visual_studio"

    _source_subfolder = "PcapPlusPlus"

    _vs_projects_to_build =[
        "Common++",
        "LightPcapNg",
        "Packet++",
        "Pcap++",
    ]

    def configure(self):
        if self.settings.os not in ["Windows", "Macos", "Linux"]:
            raise ConanInvalidConfiguration("%s is not supported" % self.settings.os)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
            del self.options.immediate_mode

    def requirements(self):
        if self.settings.os == 'Windows':
            self.requires("winpcap/4.1.3@bincrafters/stable")
            if self.settings.compiler == "Visual Studio":
                self.requires("pthreads4w/3.0.0")
        else:
            self.requires("libpcap/1.9.1")

    def source(self):
        sha256 = "b35150a8517d3e5d5d8d1514126e4e8e4688f0941916af4256214c013c06ff50"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self._source_subfolder + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            if self.settings.os == "Linux":
                libpcap_include_path = self.deps_cpp_info["libpcap"].include_paths[0]
                libpcap_lib_path = self.deps_cpp_info["libpcap"].lib_paths[0]
                config_command = ("./configure-linux.sh --libpcap-include-dir %s --libpcap-lib-dir %s" % (libpcap_include_path, libpcap_lib_path))
                if self.options.immediate_mode:
                    config_command += " --use-immediate-mode"

                self.run(config_command)

                env_build = AutoToolsBuildEnvironment(self)
                env_build.make()

            elif self.settings.os == "Macos":
                libpcap_include_path = self.deps_cpp_info["libpcap"].include_paths[0]
                libpcap_lib_path = self.deps_cpp_info["libpcap"].lib_paths[0]
                config_command = ("./configure-mac_os_x.sh --libpcap-include-dir %s --libpcap-lib-dir %s" % (libpcap_include_path, libpcap_lib_path))
                if self.options.immediate_mode:
                    config_command += " --use-immediate-mode"

                self.run(config_command)

                env_build = AutoToolsBuildEnvironment(self)
                env_build.make()

            elif self.settings.os == "Windows":
                if self.settings.compiler != "Visual Studio":
                    raise ConanInvalidConfiguration("Compiler %s is not supported" % self.settings.compiler)

                vs_version = "vs2015"
                if self.settings.compiler.version == "15":
                    vs_version = "vs2017"
                elif self.settings.compiler.version == "16":
                    vs_version = "vs2019"

                sln_file = "mk/%s/PcapPlusPlus.sln" % (vs_version)
                winpcap_path = self.deps_cpp_info["winpcap"].rootpath
                pthreads_path = self.deps_cpp_info["pthreads4w"].rootpath
                self.run("configure-windows-visual-studio.bat --vs-version %s --pcap-sdk %s --pthreads-home %s" % (vs_version, winpcap_path, pthreads_path))
                self.generate_directory_build_props_file()
                msbuild = MSBuild(self)
                msbuild.build(
                    sln_file,
                    targets=self._vs_projects_to_build,
                    use_env=False,
                    properties={"WholeProgramOptimization":"None"},
                )

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder, keep_path=False)
        self.copy("*.h", dst="include", src="PcapPlusPlus/Dist/header")
        self.copy("*.lib", dst="lib", src="PcapPlusPlus/Dist/", keep_path=False)
        self.copy("*.a", dst="lib", src="PcapPlusPlus/Dist/", keep_path=False)
        self.copy("*.pdb", dst="lib", src="PcapPlusPlus/Dist/", keep_path=False)
        self.copy("*", dst="bin", src="PcapPlusPlus/Dist/examples", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["Pcap++", "Packet++", "Common++"]
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
        if self.settings.os == "Windows":
            self.cpp_info.system_libs.append("Iphlpapi")
        if self.settings.os == "Macos":
            self.cpp_info.frameworks.append("CoreFoundation")
            self.cpp_info.frameworks.append("Security")
            self.cpp_info.frameworks.append("SystemConfiguration")

    def generate_directory_build_props_file(self):

        log_message = (
            "Generating Directory.Build.Props in the build directory which"
            "injects conan variables into all vcxproj files in the directory tree beneath it. "
            "https://docs.microsoft.com/en-us/visualstudio/msbuild/what-s-new-in-msbuild-15-0"
        )

        props_content = r"""<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
    <ImportGroup Label="PropertySheets">
        <Import Project="../conanbuildinfo.props" />
    </ImportGroup>
</Project>
"""
        self.output.warn(log_message)
        tools.save("Directory.Build.props", props_content)
