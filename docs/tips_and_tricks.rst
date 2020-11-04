Bincrafter's Conan Tips
=======================

*Practical day to day Conan usage. This guide is always a work in progress.*

Introduction
------------

Conan is a very powerful tool that greatly diminishes project setup time. When used exclusively, it also shortens configuration files considerably, automating builds and improving maintainability at the same time. Bincrafters have come together to create a common pool of high quality packages for ourselves and the rest of the Conan community, and also to learn from each other and increase our efficiency and quality of work by establishing a set of good common practices.

This guide is not a replacement for the [Conan documentation](http://docs.conan.io/en/latest/). As a matter of fact, it often references it. The purpose of this wiki is to explain Bincrafters specific topics.


Tip: Conan does not need CMake. You probably do though. Understand what Conan is.
--------------------------------------------------------------------------------------

Conan is not so much a build system but rather a package management system that drastically reduces the steps needed to reference existing libraries that have been packaged with it. It is architected in a way that allows it to interact with and encapsulate any compiler / build system like cmake, autotools, Visual Studio, MinGW or Xcode. In that sense, cmake is not a prerequisite when using conan. You will find however that many conan packages use cmake, either for building the library they contain itself, or for building the test that ensures that the library works.

So conan's added value is not so much in proposing a new build configuration but the production and easy consumption of cross-platform packages, each containing a library, information about its dependencies on other libraries, a "recipe" for building it and binaries corresponding to various os architectures. You reference a conan package by listing it in your project's recipe. When you build your project with conan, it first checks which packages your have referenced. It downloads and sets up their binaries for you in a local cache, which can be reused across projects. If your cpu architecture and build options cannot match a precompiled binary, the package's recipe is used to compile it on your machine before storing it in the local cache. The same is repeated for packages referenced by the packages you have referenced, together with their own dependencies, etc.

When comparing conan to other existing tools, we have heard some people say that it reminds them of homebrew for the Mac, or apt, yum or dnf on Linux. However we tend to think that it is more similar to package managers that exist in other ecosystems, like nuget for .Net or maven for the JVM.
