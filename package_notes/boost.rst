Boost
-----

There are ~135 libraries in Boost, so obviously there are a few nuances related to the packages which users might want to know. We will continually update this page with usage-notes, limitations, and any unresolvable issues we discover or hear about from users.

boost_iostreams
===============

This package has optional dependencies on three compression libraries: *zlib*, *bzip2*, and *lzma*. Fortunately, we now have all three compression libraries in Conan Center, so we can support them as proper dependencies. The default conan setting for including support for these compressors in ``boost_iostreams`` is "enabled" (for example: ``use_zlib=True``), and our CI has precompiled iostreams with these defaults, so you should be able to use them all out of the box.

boost_regex
===========

This package has optional dependency on IBM's ICU library (International Components for Unicode).  The default conan setting for including support for ICU is "disabled", so if you want to use ICU with ``boost_regex``, you'll have to set the option ``boost_regex:use_icu=True``

boost_mpi
=========

The ``boost_mpi`` library has a hard dependency on a concrete implementation of MPI: namely OpenMPI on Linux and macOS, and MicrosoftMPI on Windows.  Bincrafters has recently completed an OpenMPI package, and is currently in the process of testing it with `boost_mpi`.  Using these packages together is considered experimental at this time, but we will certainly post an update when it's considered stable. The MicrosoftMPI package is also under R&D at this time, but that is a bit trickier, since it is released as an MSI which is difficult for Conan to manage.

boost_python
============

The ``boost_python`` library has a hard dependency on a local installation of Python.  As such, this package has many nuances.  By default, it will try to auto-detect and locate your python version and installation.  It also has options for overriding this detection and manually specifying these things.  More details to follow.

boost_fiber
===========

This library requires C++11, thus we do not build with MSVC12 on our CI.
This library cannot build on apple-clang 7.3 due to the error, so we have simply removed support for this compiler:
``thread-local storage is not supported for the current target``

boost_context
=============

This library requires C++11, thus we do not build with MSVC12 on our CI.


boost_coroutine
===============

This library requires C++11, thus we do not build with MSVC12 on our CI.


boost_log
=========

This library requires C++11, thus we do not build with MSVC12 on our CI.


boost_fiber
===========

This library does not build on xcode 7.3 because of the error below, so we've disabled it in CI.


.. code-block:: bash

	fiber/detail/spinlock_ttas.hpp:42:16: error: thread-local storage is not supported for the current target
			static thread_local std::minstd_rand generator{ std::random_device{}() };
				   ^
	2 errors generated.
	make[2]: *** [CMakeFiles/test_package.dir/test_package.cpp.o] Error 1


Stackoverflow Post: https://stackoverflow.com/questions/28094794/why-does-apple-clang-disallow-c11-thread-local-when-official-clang-supports