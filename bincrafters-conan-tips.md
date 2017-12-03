Bincrafter's Conan Tips
=======================

*Practical day to day conan usage. This guide is always a work in progress.*

Introduction
------------

Conan is a very powerful tool that greatly diminishes project setup time. When used exclusively, it also shortens configuration files considerably, automating builds and improving maintainability at the same time. Bincrafters members are software developers who use conan regularly. We are not professional "packagers" but, since we package open source libraries for our own use, we have come together to create a common pool of high quality packages for ourselves and the rest of the conan community, and also to learn from each other and increase our efficiency and quality of work by establishing a set of good common practices.

This guide is not a replacement for the [conan documentation](http://docs.conan.io/en/latest/). As a matter of fact, it often references it. Its purpose is to help you navigate learning conan and advance quickly without getting lost in the details. It is based on our experience of doing so ourselves and the insights we have developed while packaging, testing and using various libraries in our own projects. It is probably a good idea to read it sequentially if you have just started out with conan. On the other hand, if you are a more experienced user, it may be best to just skim through the titles and go directly to the tips that catch your attention.

Tip 1: Set up conan with virtualenv
-----------------------------------
One of the first things you will do when starting out with conan is of course installing it. On the [download page](https://www.conan.io/downloads) you will notice that there are various ways to do that: installation programs, from source code, from pypi or even from homebrew on MacOS. We suggest setting up conan under virtualenv, using pip. It may seem simpler to just run a setup wizard, but this method will make updating to the latest conan version a breeze, and that is something that is needed quite often. Once you have installed python and virtualenv on your system, do the following:

	virtualenv vconan --no-site-packages
	
You have created your virtual environment. Every time you need to activate it, you need to do the following on Linux and MacOS. Do that now:

	source vconan/bin/activate
	
Note that, on Windows, things are a little different:

	.\vconan\scripts\activate
	
Your virtual environment is now activated. Notice that its name appears in parentheses in front of your command prompt.

Make sure you have the latest version of pip installed in your virtual environment:

	pip install --upgrade pip
	
Then install conan:

	pip install conan
	
That's all! Let's run a conan command:

	conan --version
	
In order to deactivate the virtual environment (thus no longer being able to run conan), do the following:

	deactivate
	
Conan has now been set up with virtualenv. And since virtualenv makes it so easy, it is a good idea to make sure you have the latest version of pip and conan every time you activate it:

	source/vconan/bin/activate or .\vconan\scripts\activate
	pip install --upgrade pip
	pip install --upgrade conan

*You may have noticed that we have made no reference to homebrew. You can certainly use homebrew as the conan download page suggests if you have a Mac, but we wanted to make the point that you do not have to. MacOS/OSX comes with Python preinstalled and you can install virtualenv directly there with easy_install and sudo*: `sudo pip easy_install virtualenv`

Tip 2: If you don't already have it, install cmake
--------------------------------------------------

This is not a cmake installation guide, so we assume you know how to install cmake on your system.

On Windows, remember to put the `bin` directory of cmake in the PATH environment variable, so that you can run it from the command line and so that conan can find it.

On Linux and on a Mac it will just work, only if you install it with homebrew in the latter case. If you have a Mac and prefer not to use homebrew, just install cmake from the distributable availabe at cmake.org, as an application. In that case however, you need to make it accessible from the command line. Create a directory called `bin` in your home directory. Edit the file .bash_profile in your home directory, or create it if it doesn't already exist. Then add the folling line to it:

	export PATH=$PATH:/Users/(your username)/bin
	
Create a symbolic link inside the bin directory pointing to the cmake executable, using the terminal:

	ln -s /Applications/CMake.app/Contents/bin/cmake /Users/(your username)/bin/cmake
	
If the terminal was already open when you were editing .bash_profile, shut it down completely (cmd + Q) and restart it.
	
You should now be able to execute cmake from the terminal, no matter which directory you are in. Try it:

	cmake --version
	
Tip 3: Conan does not need cmake. You probably do though. Understand what conan is.
--------------------------------------------------------------------------------------

Conan is not so much a build system but rather a package management system that drastically reduces the steps needed to reference existing libraries that have been packaged with it. It is architected in a way that allows it to interact with and encapsulate any compiler / build system like cmake, autotools, Visual Studio, MinGW or Xcode. In that sense, cmake is not a prerequisite when using conan. You will find however that many conan packages use cmake, either for building the library they contain itself, or for building the test that ensures that the library works.

So conan's added value is not so much in proposing a new build configuration but the production and easy consumption of cross-platform packages, each containing a library, information about its dependencies on other libraries, a "recipe" for building it and binaries corresponding to various os architectures. You reference a conan package by listing it in your project's recipe. When you build your project with conan, it first checks which packages your have referenced. It downloads and sets up their binaries for you in a local cache, which can be reused across projects. If your cpu architecture and build options cannot match a precompiled binary, the package's recipe is used to compile it on your machine before storing it in the local cache. The same is repeated for packages referenced by the packages you have referenced, together with their own dependencies, etc.

When comparing conan to other existing tools, we have heard some people say that it reminds them of homebrew for the Mac, or apt, yum or npm on Linux. However we tend to think that it is more similar to package managers that exist in other ecosystems, like nuget for .Net or maven for the JVM.
