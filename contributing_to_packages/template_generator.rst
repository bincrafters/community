Generating Template Content
----------------------
Bincrafters is actively developing a generator script in python to streamline the bootstrapping of repositories for recipes. 

https://github.com/bincrafters/conan-readme-generator

Please try to use the bincrafter’s README generator to generate a README.md and LICENSE.md for your conan recipe repository.  

To install it, clone the repository and use pip to install it locally:

.. code:: bash

    git clone https://github.com/bincrafters/conan-readme-generator
    cd conan-readme-generator
    pip install .

You need a working “git” installation in your environment PATH.

To use it you need to:

-  ``cd your-conan-recipe-project``
-  optionally checkout the branch you want to generate a README.md for.
-  Just execute: ``conan-readme-generator``

Note that a valid conan recipe (conanfile.py) must be present in the
directory you execute the generator in.

Also be aware that the generator will overwrite your existing README.md.

Apart from the README.md generated, a LICENSE.md file with an MIT
license will be generated. Remember to rerun ``conan-readme-generator``
if you make changes to your recipe or you add CI to your repository. You
can also use your own template (see the command line options with
``conan-readme-generator --help``.

The generator will automatically add to your README.md suitable Appveyor
and Travis badges, provided this is setup properly.
