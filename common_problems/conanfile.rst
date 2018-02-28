Common Conanfile Problems
==========================

Header-Only Libraries 
====================

There are a few occasional problems to be aware of for header-only libraries.  Below we describe some of them along with the special handling needed to deal with them. 

CMake
---------------------------- 

While header-only libraries don't need to be "built", many header-only libraries still use CMake to define an install target.  In these cases, it's better to use ``cmake.install()`` than manually capture ``.h`` files, as sometimes it generates and installs ``findXXX.cmake`` files which we want. 

Using Conan's CMake Helper with a header-only library presents a bit of a quandry, because the helper requires a compiler to be defined, and the convention is to remove the compiler setting (along with all other settings) from header-only recipes. 

package_id() method
---------------------------- 

Often times, header-only libraries need to define information in the ``package_id()`` method which depends on the conanfile settings of ``"os", "arch", "compiler", "build_type"``.  However, the convention is to remove all settings from header-only recipes.  So, in these cases, your recipe should feature all the normal settings of ``"os", "arch", "compiler", "build_type"``, but use the standard ``self.info.header_only()`` at the very end of the ``package_id()`` method. A good example is defined here: 

http://docs.conan.io/en/latest/howtos/header_only.html#with-unit-tests


Cygwin Builds on Windows 
---------------------------- 

Set ``short_paths=True`` in all recipe's for libraries which need to be built with Cygwin for Windows. The reason for this is that spaces in some users profile path will cause build of the recipe to fail. Using ``short_paths=True`` avoids the problem completely. 