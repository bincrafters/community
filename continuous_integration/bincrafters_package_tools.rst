Introduction to Bincrafter Package Tools
========================================

To avoid code replication when using bincrafter-templates_ for each new Conan recipe, a pip package was developed to put all templates together.

Also, it is possible to create a multi package matrix running just few of code.

To install the package you only pip:

.. code-block:: bash

    pip install bincrafters-package-tools

After to install the package you will able to run any Bincrafters' template.

This next example runs all possible configuration, including **shared** option:

.. code:: python

    from bincrafters import build_template_default

        if __name__ == "__main__":
            builder = build_template_boost_default.get_builder()
            build.run()

The same block cloud represented by:

.. code:: python

    from conan.packager import ConanMultiPackager

        if __name__ == "__main__":
            builder = ConanMultiPackager()
            builder.add_common_builds(shared_option_name="foobar:shared")
            builder.run()

Also there is a header-only template:

.. code:: python

    from bincrafters import build_template_header_only

        if __name__ == "__main__":
            builder = build_template_header_only.get_builder()
            builder.run()

The Bincrafters package tools is not a replacement for Conan package tools, it is a wrapper, helping to solve build variables and execution steps.

Environment
-----------

If you are running Travis or Appveyor, you only need to set ``CONAN_PASSWORD`` and ``CONAN_LOGIN_USERNAME``. All other variables will be collect by your CI environment.

Contributing
------------

If you are interested to contribute, fix a bug or just read the code, visit the `project page`_.


.. _bincrafter-templates: https://github.com/bincrafters/conan-templates
.. _project page: https://github.com/bincrafters/bincrafters-package-tools
