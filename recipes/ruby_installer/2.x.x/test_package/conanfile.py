import os
from conans import ConanFile


class RubyInstallerTestConan(ConanFile):
    settings = "os", "arch", "build_type", "arch"
    generators = "txt"

    def build(self):
        pass

    def test(self):
        self.run("ruby -v", run_environment=True)
        self.run("ruby -e \"puts 'hello'\"", run_environment=True)
        self.run("ruby -e \"require 'date';puts Date.today\" --disable-gems", run_environment=True)
