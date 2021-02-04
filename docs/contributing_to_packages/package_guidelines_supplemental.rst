header only libraries
=====================

For header only libs, we don’t setup CI.

We publish manually using ``conan upload <package_ref> --all`` We do setup test_package, however we skipped for boost due to volume.

imports style
=============

Instead of: ``from conans.tools import download``

Please use: ``from conans import tools``

And then use qualified method calls on statics… so ``tools.download()``

For people new to conan, it’s not obvious where unqualified method calls are coming from.


package dependencies
====================

1. Do not use version ranges for OSS packages.  Previously, we had advised the use of version ranges for dependencies on Bincrafters packages rather than hardcoding version numbers.  We have since been advised by the Conan team that dependency resolution was much slower with ranges than otherwise.  Also, many community members were more interested in repeatable builds with reliable dependency tree's than automatic "most recent version" behavior.

2. Only use dependencies from conan-center or bincrafters. If you need a dependency which is in transit, or someone else’s repository, we need to copy it, standardize it, and re-publish it under bincrafters.

3. Always reference the ``stable`` branch of a dependency. There are exceptions, including Boost, and potentially Qt in the future, but use ``stable`` otherwise.

git submodules
==============

A proper package defines all of it’s dependencies via the Conan ``requirements`` mechanism. Unfortunately, for any package we might want to build, almost none of the dependencies will be in Conan Center, or even Bincrafters (yet).

Many C++ projects use git-submodules. While it is convenient to write the Conan package so that the ``source()`` method does a ``git clone --recurse``, it would be better to go forward and create a
Conan recipe and package for each dependency, and then return to the original package of interest once this effort is complete. This builds towards a better long-term future, because those little dependencies are very likely to show up in the dependency tree of numerous other future packages.

However, this is extremely time-consuming and overwhelming however when all you want to do is package “the library”. But, by working together as a team in concert, Bincrafters can actually tackle a library and all of it’s dependencies in potentially in a few hours. This is intended to be the packaging paradigm moving forward.
