Strategy for deprecating packages
=================================

There are some possible scenarios where the deprecation of a particular package is necessary, among them are:

**Official Support**

The official upstream is now available on Conan Center and the same package is maintained by Bincrafters

**EOF**

The official upstream just archived a project that is maintained by Bincrafters

When some situation like this occurs, Bincrafters needs to update the package status to **deprecated**.
Bincrafters will keep that version of the package on Github and Bintray, however it will no longer be maintained or supported.

Steps to deprecate a package now officially supported by the upstream
---------------------------------------------------------------------

Here is a list of what should be done to deprecate a package:

1) Create a new branch version following the latest upstream version

The version should be distributed as Conan package by both as a soft transition.

2) Show warning message on ``configure`` method about the deprecation:

.. code:: python

    def configure(self):
        self.output.warn("[DEPRECATED] Package foo/bincrafters is being deprecated. Change yours to require foo/author instead")

3) Alias_ to the new project reference:

.. code:: python

    from conans import ConanFile

    class AliasConanfile(ConanFile):
        alias = "project/0.1.0@author/stable"

4) Add warning message in the README file:

.. code:: text

    ## Package Deprecation Notice

    The author of this library has taken ownership of the public Conan package for this library, which can be found at the following links:

    https://github.com/<author>/<project>
    https://bintray.com/<author>/<remote>/<reference>

    Bincrafters will keep this version of the package on Github and Bintray, however it will no longer be maintained or supported.
    Users are advised to update their projects to use the official Conan package maintained by the library author immediately.

5) Update Github project description:

.. code:: text

    [DEPRECATED] Conan recipes for <project>

6) Archive Github repository:

    https://help.github.com/articles/archiving-repositories/

7) Update Bintray package description:

.. code:: text

    [DEPRECATED] <project description>

8) Add **deprecated** image to Bintray project logo:

.. figure:: .images/deprecated.png

Examples
--------

There are some projects already deprecated and could be used as example:

* PEGTL_
* Catch2_

Discussion
----------

If you are interested to understand how we created this flow, please visit the related issue_ page.

.. _issue: https://github.com/bincrafters/community/issues/546
.. _PEGTL: https://github.com/bincrafters/conan-pegtl
.. _Catch2: https://github.com/bincrafters/conan-catch2
.. _Alias: https://docs.conan.io/en/latest/reference/commands/misc/alias.html