build.py
--------

The standard for this file is fully generic and requires no modifications between libraries. Of course, some libraries are special, but it’s very helpful for libraries to use the generic template when possible.

–build missing
==============

Do not use ``--build missing`` in your ``build.py`` files. This is not the default for a reason. It might be useful to turn this on temporarily for testing, but it should not be left turned on in ``build.py``
long-term.

filtering builds
================

Please pull out filter logic into a separate function which return bools, and use python’s “filter” method. Example:

.. code:: python

    def _is_valid_abi(build):
        compiler = build.settings['compiler']
        version = build.settings['compiler.version']
        libcxx = build.settings['compiler.libcxx']
        if compiler == 'gcc' and float(version) > 5:
            return libcxx == 'libstdc++11'
        return True

And then in the ``if __name__ == "__main__":`` block:

.. code:: python

        builder.add_common_builds(shared_option_name=name + ":shared")
        if get_os() == "Linux":
            builder.builds = filter(_is_valid_abi, builder.builds)

appveyor.yml
------------

The standard for this file is fully generic and requires no modifications between libraries. Of course, some libraries are special, but it’s very helpful for libraries to use the generic template when possible.

.travis.yml
-----------

The standard for this file is fully generic and requires no modifications between libraries. Of course, some libraries are special, but it’s very helpful for libraries to use the generic template when
possible.

LICENSE.md
------------

The policy has on LICENSE has changed recently. Bincrafters recipe files should always be MIT license, and that is what should exist in the repository in a file by the name ``LICENSE.md``.  See the section below 

CMakeLists.txt  
------------
The template repository now features `CMakeLists.txt` template, which is listed in an `export` in the template `conanfile.txt`.  This is a wrapper that should be used when building all libraries which use CMake for the build, even when it has no dependencies.  You can tweak and add flags in this file, but most times it just serves to enforce the "Conan-managed" settings and attributes during the build.  If the target library does not use CMake, delete this file and remote the import of the Cmake helper from the `conanfile.py`.


conanfile.py
===============

We have conventions for most of the fields of ``conanfile.py``.

url
----

Always use the URL of the git repo of the recipe, not the original lilbrary. 


name  
-------

As of December, use only lowercase letters in package names moving forward.  We will be renaming old packages to be all-lowercase. 

version
---------

Always use the version of the upstream package. There are some challenges in some cases, such as those which lack semver, or those that are currently un-released.  Strategies for these cases are described below. 

Packages without official releases
----------------------------------

The notation shown below is used for publishing packages where the original library does not make official releases. Thus we use a datestamp to show when the package was created:

::

    gsl_microsoft/20171020@bincrafters/stable

Packages without semantic versioning
------------------------------------

The same notation is used for publishing packages where the original library does have official releases, but does not use semantic versioning. In this case, the version number is the one provided from the original library. In the case of msys2_installer, the library happens to use a datestamp:

::

    msys2_installer/20161025@bincrafters/stable 

        
Conan “latest” version convention
---------------------------------

In some cases a version alias of “latest” is added to packages. Users
can reference this version in requirements as shown in the example below
to get the latest release without specifying a specific version or
range:

::

    msys2_installer/latest@bincrafters/stable


**Note that using the latest alias will cause your projects to download and use an updated version as soon as it becomes available. Such library updates can potentially be breaking, so users should consider this before referencing the latest alias in a project.**

    
settings.compiler
~~~~~~~~~~~~~~~~~

Windows does not necessarily imply Visual Studio, there are at least GCC
(e.g. MinGW) and Clang for Windows. Thus, don’t write conditions like:

.. code:: python

    if self.settings.os == "Windows": 
        self.run("cl")

write instead:

.. code:: python

    if self.settings.compiler == "Visual Studio": 
        self.run("cl")

settings.arch
~~~~~~~~~~~~~

Don’t assume there are only two architectures like x86 and x64, there are at least many variations of ARM (even on Windows, yes) so don’t write conditions like:

.. code:: python

    flags = "-m32" if self.settings.arch = 'x86' else = "-m64"

write instead:

.. code:: python

    flags = {'x86': '-m32', 'x86_64': '-m64'}.get(str(self.settings.arch))

settings - restrictions
~~~~~~~~~~~~~~~~~~~~~~~

Don’t restrict operating system and arch with the following strategy,
even though I think this is in the Conan documentation as a suggestion.
It turns out that this prevents cross-building scenarios.

.. code:: python

    settings = {"os" : ["Windows", "Macos", "Linux"], "arch" : ["x86_64"]}
	
Instead, do this: 

.. code:: python

    def config_options(self):
        # Checking against self.settings.* would prevent cross-building profiles from working
        if tools.detected_architecture() != "x86_64":
            raise Exception("Unsupported Architecture.  This package currently only supports x86_64.")
        if platform.system() not in ["Windows", "Darwin", "Linux"]:
            raise Exception("Unsupported System. This package currently only support Linux/Darwin/Windows")

source() method
===============

#. Favor ``tools.get()`` on an archive over git clone. 
#  With github, even if there are no github releases, use the "Download as Zip" url. 
#. Most times you can use a ``.tar.gz`` for windows and linux
#. Validate checksums when they are provided by upstream, pass as parameter to ``tools.get()``
#. We have a convention now: rename the directory that gets extracted or downloaded to “sources”. This simplifies several elements in our standard recipes. There’s a feature request in progress to add a param to ``tools.get()`` to automate this.

package() method
================

Don’t do ``with tools.chdir("sources")``, it doesn’t do what you want it to.

Badges
======

Please try to add the following banners after you’ve got the recipe mostly working: 
* Bintray - The badge URL should have at the end:  `...\_latest` 
* Appveyor - The badge URL should have at the end (example): `github/bincrafters/conan-lzma?svg=true` 
* Travis - The badge URL should have at the end (example):  `bincrafters/conan-lzma.svg`

|[![Download](https://api.bintray.com/packages/bincrafters/public-conan/lzma%3Abincrafters/images/download.svg)](https://bintray.com/bincrafters/public-conan/lzma%3Abincrafters/_latestVersion)|[![Build status](https://ci.appveyor.com/api/projects/status/github/bincrafters/conan-lzma?svg=true)](https://ci.appveyor.com/project/BinCrafters/conan-lzma)|[![Build Status](https://travis-ci.org/bincrafters/conan-lzma.svg)](https://travis-ci.org/bincrafters/conan-lzma)|

test_package
------------

Our standard for test_package are nice in that you only need to change ``test_package.cpp`` contents in most cases. The ``conanfile.py`` and ``CMakeLists.txt`` are made to be generic. Special circumstances might require some changes to the other files such as for C only libraries, but try to avoid if possible.

Please write the actual minimum contents of a file you can to prove that ``include`` and linking works. Do not use examples from the author, do not test that methods do the right thing. Do not use a test framework, even Catch. Just use a ``main()`` method that gets fun from the ``test()`` method in ``conanfile.py``.