#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
from bincrafters import build_template_default

if __name__ == "__main__":

    if platform.system() == "Linux":
        command = os.environ["CONAN_DOCKER_ENTRY_SCRIPT"] + "; sudo apt-get -qq update && sudo apt-get -qq install -y python-minimal"
        builder = build_template_default.get_builder(docker_entry_script=command, pure_c=False)
    else:
        builder = build_template_default.get_builder(pure_c=False)

    builder.run()
    