build.py
--------

The standard for this file is fully generic and requires no
modifications between libraries. Of course, some libraries are special,
but it’s very helpful for libraries to use the generic template when
possible.

–build missing
==============

Do not use ``--build missing`` in your ``build.py`` files. This is not
the default for a reason. It might be useful to turn this on temporarily
for testing, but it should not be left turned on in ``build.py``
long-term.

filtering builds
================

Please pull out filter logic into a separate function which return
bools, and use python’s “filter” method. Example:

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

The standard for this file is fully generic and requires no
modifications between libraries. Of course, some libraries are special,
but it’s very helpful for libraries to use the generic template when
possible.

.travis.yml
-----------

The standard for this file is fully generic and requires no
modifications between libraries. Of course, some libraries are special,
but it’s very helpful for libraries to use the generic template when
possible.

LICENSE
-------

The policy has on LICENSE has changed recently. Bincrafters recipe files
should always be MIT license, and that is what should exist in the
repository in a file by the name ``LICENSE.md``.

conanfile.py
------------

url
===

Always use the URL of the git repo of the recipe

version
=======

Always use the version of the upstream package. There are some
challenges in some cases, such as those which lack semver, or those that
are currently un-released.

Packages without official releases
----------------------------------

The notation shown below is used for publishing packages where the
original library does not make official releases. Thus we use a
datestamp to show when the package was created:

::

    `gsl_microsoft/20171020@bincrafters/stable`

Packages without semantic versioning
------------------------------------

The same notation is used for publishing packages where the original
library does have official releases, but does not use semantic
versioning. In this case, the version number is the one provided from
the original library. In the case of msys2_installer, the library
happens to use a datestamp:

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

\*\* Note that using the lates