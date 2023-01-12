from conans import ConanFile, tools
import os 


class TestPackageConan(ConanFile):

    settings = "os", "arch"

    def test(self):
        if not tools.cross_building(self):
            self.run("%s --version" % os.environ["LD"], run_environment=True)
