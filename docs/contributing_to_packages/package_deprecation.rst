Strategy for deprecating packages
=================================

There are some possible scenarios where the deprecation of a particular package is necessary, among them are:

**Official Support**

The official upstream is now available on Conan Center and the same package is maintained by Bincrafters

**EOF**

The official upstream just archived a project that is maintained by Bincrafters

When some situation like this occurs, Bincrafters needs to update the package status to **deprecated**.
Bincrafters will keep that version of the package on Github and Artifactory, however it will no longer be maintained or supported.

Discussion
----------

If you are interested to understand how we created this flow, please visit the related issue_ page.

.. _issue: https://github.com/bincrafters/community/issues/546
.. _PEGTL: https://github.com/bincrafters/conan-pegtl
.. _Catch2: https://github.com/bincrafters/conan-catch2
.. _Alias: https://docs.conan.io/en/latest/reference/commands/misc/alias.html
