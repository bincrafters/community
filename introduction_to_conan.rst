Introduction to Conan
=============

If you are new to Conan.io and want to learn about it, the Conan documentation should be your next stop. 

`Conan Documentation <https://conanio.readthedocs.io/en/latest/introduction.html>`_.

Here we simply provide a selective summary of Conan from our perspective as OSS packagers.

In the simplest terms, Conan is a package management platform for C and C++ which resembles a number of modern package managers from the ecosystems of other programming languages.  While it most closely resembles `Maven <https://en.wikipedia.org/wiki/Apache_Maven/>`_ and `Nuget <https://en.wikipedia.org/wiki/NuGet/>`_, it is unique in that it focuses on packaging "Native Binaries" and tackling the unique challenges associated with them.  

As a package manager, the most basic role that Conan performs is to provide a common package descriptor format for package authors.  In the case of Conan, the descriptor format is a python script with the default name of ``conanfile.py`` (known as the "Conanfile").  Generally speaking, the Conanfile contains the instructions for taking raw source code, compiling it into a binary format, and then storing it in a compressed archive format (a "Conan Package").  Crucially, the Conanfile also contains a list of other Conan Packages which are required for compilation, enabling authors to define a traditional "dependency tree" of Conan Packages.  Thus, the Conan Package format and associated metadata are tailored for distribution and re-use as a dependencies in other Conan projects.  In addition to the defining the Conanfile and Conan Package formats, the Conan platform features a client application which performs the role of executing the instructions and create the packages, and a Conan server application which provides an API for uploading and downloading packages between machines.  

Beyond these basic package management features, Conan has the following important characteristics: 

* A moderated and trusted central repository for OSS software
* Worfklow closely resembles other prevalent package managers 
* Cross-Platform and toolset agnostic
* Packages contain precompiled binaries
* Binaries are built on-demand if not available
* Binaries are stored in a local binary cache
* Designed to support both Enterprise and OSS workloads

For the Open-Source Software community, Conan has enabled a new experience for developing with C and C++.  Without a binary package manager like Conan, developers are required to manually compile all third-party libraries they wished to use in their projects on their development machine.  Naturally, this results in a vast number of developers performing the same redundant compilations of Open-Source libraries.  With Conan, a vast number of these redundant compilations can be avoided.  OSS developers working on C and C++ projects can now define the list of third-party library dependencies in their projects, and the Conan client can download precompiled binary versions of those libraries on-demand. 

In fact, the Linux ecosystem features a number of binary package managers which have historically addressed this problem to some degree. However, Conan is fundamentally different from these package managers in a few ways, most notably it's intention and ability to package and retrieve libraries for any operating systems from a single descriptor file (the Conanfile).  
