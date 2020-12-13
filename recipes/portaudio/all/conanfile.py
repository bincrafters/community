import os
from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools

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
        "with_jack":  [True, False]
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        "with_alsa":  True,
        "with_jack":  True
    }
    exports = ["FindPortaudio.cmake", "CMakeLists.txt"]
    exports_sources = ["patches/*.diff"]

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
        os.rename("portaudio", self.sources_folder)

    def patch_source(self):
        if self.settings.os == "Macos":
            tools.replace_in_file(os.path.join(self.sources_folder, "configure"), 'mac_sysroot="-isysroot `xcodebuild -version -sdk macosx10.12 Path`"',
"""
mac_sysroot="-isysroot `xcodebuild -version -sdk macosx10.12 Path`"
elif xcodebuild -version -sdk macosx10.13 Path >/dev/null 2>&1 ; then
                 mac_version_min="-mmacosx-version-min=10.4"
                 mac_sysroot="-isysroot `xcodebuild -version -sdk macosx10.13 Path`"
elif xcodebuild -version -sdk macosx10.14 Path >/dev/null 2>&1 ; then
                 mac_version_min="-mmacosx-version-min=10.4"
                 mac_sysroot="-isysroot `xcodebuild -version -sdk macosx10.14 Path`"

"""
                        )
            tools.replace_in_file(os.path.join(self.sources_folder, "configure"), "Could not find 10.5 to 10.12 SDK.", "Could not find 10.5 to 10.14 SDK.")
        elif self.settings.os == "Windows" and self.settings.compiler == "gcc":
            tools.replace_in_file(os.path.join(self.sources_folder, "CMakeLists.txt"), 'OPTION(PA_USE_WDMKS "Enable support for WDMKS" ON)', 'OPTION(PA_USE_WDMKS "Enable support for WDMKS" OFF)')
            tools.replace_in_file(os.path.join(self.sources_folder, "CMakeLists.txt"), 'OPTION(PA_USE_WDMKS_DEVICE_INFO "Use WDM/KS API for device info" ON)', 'OPTION(PA_USE_WDMKS_DEVICE_INFO "Use WDM/KS API for device info" OFF)')
            tools.replace_in_file(os.path.join(self.sources_folder, "CMakeLists.txt"), 'OPTION(PA_USE_WASAPI "Enable support for WASAPI" ON)', 'OPTION(PA_USE_WASAPI "Enable support for WASAPI" OFF)')


    def build(self):
        for p in self.conan_data["patches"][self.version]:
            tools.patch(**p)
        self.patch_source()

        if self.settings.os == "Linux" or self.settings.os == "Macos":
            env = AutoToolsBuildEnvironment(self)
            env.fpic = self.options.fPIC
            args = []
            if self.settings.os == "Macos" and self.settings.compiler == "apple-clang":
                args.append("--disable-mac-universal")
            elif self.settings.os == "Linux":
                args.append("--with-alsa" if self.options.with_alsa else "--without-alsa")
                args.append("--with-jack" if self.options.with_jack else "--without-jack")
                if self.options.with_alsa:
                    env.flags.extend("-I%s" % p for p in self.deps_cpp_info["libalsa"].include_paths) # env.include_paths does not seem to work here
            env.configure(configure_dir=self.sources_folder, args=args)
            if self.settings.os == "Macos" and self.settings.compiler == "apple-clang":
                env.make()
            else:
                env.make(target = "lib/libportaudio.la")
            if self.settings.os == "Macos" and self.options.shared:
                self.run('cd lib/.libs && for filename in *.dylib; do install_name_tool -id $filename $filename; done')
        else:
            cmake = CMake(self)
            cmake.definitions["MSVS"] = self.settings.compiler == "Visual Studio"
            cmake.definitions["PA_BUILD_STATIC"] = not self.options.shared
            cmake.definitions["PA_BUILD_SHARED"] = self.options.shared
            cmake.configure()
            cmake.build()

    def package(self):
        self.copy("FindPortaudio.cmake", ".", ".")
        self.copy("*.h", dst="include", src=os.path.join(self.sources_folder, "include"))
        self.copy(pattern="LICENSE*", dst="licenses", src=self.sources_folder,  ignore_case=True, keep_path=False)

        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self.copy(pattern="*.lib", dst="lib", keep_path=False)
                if self.options.shared:
                    self.copy(pattern="*.dll", dst="bin", keep_path=False)
                self.copy(pattern="*.pdb", dst="bin", keep_path=False)
            else:
                if self.options.shared:
                    self.copy(pattern="*.dll.a", dst="lib", keep_path=False)
                    self.copy(pattern="*.dll", dst="bin", keep_path=False)
                else:
                    self.copy(pattern="*static.a", dst="lib", keep_path=False)

        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", src=os.path.join( "lib", ".libs"))
                else:
                    self.copy(pattern="*.so*", dst="lib", src=os.path.join( "lib", ".libs"))
            else:
                self.copy("*.a", dst="lib", src=os.path.join("lib", ".libs"))


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(["CoreAudio","AudioToolbox","AudioUnit","CoreServices","Carbon"])

        if self.settings.os == "Windows" and self.settings.compiler == "gcc" and not self.options.shared:
            self.cpp_info.system_libs.append('winmm')

        if self.settings.os == "Linux" and not self.options.shared:
            self.cpp_info.system_libs.extend(['m', 'pthread'])
            if self.options.with_jack:
                self.cpp_info.system_libs.append('jack')
