Introduction to Continuous Integration (CI)
==========================

One of the distinguishing characteristics between Conan.io and other package managers is that it can store a wide variety of precompiled binary packages for a wide variety of platforms. Below is a screenshot of a report from the ``conan search`` command for the common ZLIB package found in Conan Center, which demonstrates precisely what precompiled binary packages are available: 

http://docs.conan.io/en/latest/_images/search_binary_table.png

As you can see, there are over 100 precompiled binaries available for ZLIB.  We call these "package variants".  Each package variant is independently compiled from sources using the platforms and options shown in the table, and then uploaded to Bintray. So, how did ZLIB get recompiled over 100 times and uploaded to Bintray?

Continuous Integration (abbreviated CI) is the amazing build-automation technology which enables Conan packagers to prepare such a wide variety of package variants for Conan packages.  TravisCI and Appveyor are two cloud-based CI services which have been providing FREE continuous integration services for Open Source software for many years.  TravisCI provides Linux and MacOS builds, while Appveyor provides builds on Windows.  Bincrafters leverages these two services with virtually every Conan package we publish.  The one major exception to this rule is that CI is not needed for packages which contain header-only libraries. 

Learning about Continuous Integration
-------------------------------------------------

Unfortunately, creating and publishing Conan packages which contain the wide array of package variants needed by the OSS community is not trivial.  CI is a separate skillset not universally held by most C++ programmers, however it is required for creating Conan packages which are fit for publishing.  This was one of the key realizations which led to the formation of the Bincrafters team. By looking at the central Conan.io repository, we were able to seek out those community packagers which had demonstrated this skillset with their existing packages. In this way, we were able to assemble our initial team of capable packagers who could hit the ground running.  


Conan Package Tools
-------------------------------------------------

Using continuous integration to precompile a wide array of package variants for open-source C and C++ projects was clearly part of the founding vision of Conan.  While Conan itself has no native features relating to continuous integration, the Conan team developed a separate project known as "ConanPackageTools" to streamline the use of Conan with common continuous integration providers. 

https://github.com/conan-io/conan-package-tools

The ConanPackageTools project contains a bit of custom logic for a number of well-known CI platforms (including TravisCI and Appveyor).  To use ConanPackageTools, package authors can simply add a few trivial script files to their repositories which contain Conan recipes, and then add some boilerplate lines to their CI files which call these scripts. The key script function is called ``add_common_builds()``, which proceeds to compile, package, and upload a pre-defined set of the most common package variants to the Conan repository of your choosing. 

Docker
-------------------------------------------------

Docker is an integral part of ConanPackageTools.  The Conan team maintains a number of docker images designated and streamlined for building Conan packages.  You can read more about those images in the conan-package-tools github repository. 

Bincrafters CI Templates
-------------------------------------------------

The Bincrafters CI templates have actually evolved to the point where they can be added alongside a new Conan recipe without any modification.  In those cases, a package author can simply "enable" Appveyor and/or TravisCI on the github repository containing the recipe, and everything will be taken care of automatically.  This includes building the pre-defined set of 100+ package variants across MacOS, Linux, and Windows, and uploading them to the configured Conan repository. However, a great many packages require customizations to the Ci templates, so it's important for packagers to understand how they work to some degree.
