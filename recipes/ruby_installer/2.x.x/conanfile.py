import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment

required_conan_version = ">=1.33.0"


class RubyInstallerConan(ConanFile):
    name = "ruby_installer"
    license = "Ruby"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/community"
    homepage = "https://www.ruby-lang.org"
    description = "Ruby is an interpreted, high-level, general-purpose programming language"
    topics = ("installer", "ruby", "gem")
    _autotools = None

    @property
    def _api_version(self):
        return "2.7.0"

    @property
    def _rubyinstaller_release(self):
        return "1"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def package_id(self):
        del self.info.settings.compiler

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("zlib/1.2.11")

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("7zip/19.00")
        else:
            self.build_requires("openssl/1.1.1l")

    def source(self):
        sha256 = "8925a95e31d8f2c81749025a52a544ea1d05dad18794e6828709268b92e55338"
        source_url = "https://cache.ruby-lang.org"
        tools.get("{}/pub/ruby/{}/ruby-{}.tar.gz".format(
            source_url,
            self.version.rpartition(".")[0],
            self.version), sha256=sha256)
        extracted_folder = "ruby-" + self.version
        os.rename(extracted_folder, self._source_subfolder)

    def _configure_autotools(self):
        if not self._autotools:
            self._autotools = AutoToolsBuildEnvironment(self)
            args = [
                "--disable-install-doc",
                "--with-out-ext=gdbm,pty,readline,syslog",
                "--without-gmp",
                "--enable-load-relative",
                "--with-openssl-dir={}".format(self.deps_cpp_info["openssl"]
                                                   .rootpath)
            ]
            self._autotools.configure(args=args, configure_dir=self._source_subfolder)
        return self._autotools

    def _configure_installer(self):
        # Extract binaries into a directory called "ruby"
        arch = {"x86": "x86",
                "x86_64": "x64"}[str(self.settings.arch)]
        name = "RubyInstaller-{}-{}".format(self.version, self._rubyinstaller_release)
        folder = "{}-{}".format(name.lower(), arch)
        url = "https://github.com/oneclick/rubyinstaller2/releases/download/{}/{}.7z".format(
            name, folder)
        tools.download(url, "ruby.7z")
        self.run("7z x {}".format("ruby.7z"), run_environment=True)
        tools.rmdir(self._source_subfolder)
        os.rename(folder, self._source_subfolder)
        # Remove non-standard defaults directory
        tools.rmdir(os.path.join(self._source_subfolder, "lib", "ruby", self._api_version, "rubygems", "defaults"))

    def build(self):
        if self.settings.os == "Windows":
            self._configure_installer()
        else:
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        if self.settings.os == "Windows":
            self.copy("*", src=self._source_subfolder, symlinks=True, excludes="LICENSE.txt")
            self.copy("LICENSE.txt", dst="licenses", src=self._source_subfolder)
        else:
            self.copy("COPYING", dst="licenses", src=self._source_subfolder)
            self.copy("LEGAL", dst="licenses", src=self._source_subfolder)
            self.copy("GPL", dst="licenses", src=self._source_subfolder)
            autotools = self._configure_autotools()
            autotools.install()
            tools.rmdir(os.path.join(self.package_folder, "share"))
            tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)
