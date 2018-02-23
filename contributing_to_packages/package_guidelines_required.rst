LICENSE.md
-------------------

The policy has on LICENSE has changed recently. Bincrafters recipe files should always be MIT license, and that is what should exist in the repository in a file by the name ``LICENSE.md``.  See the section below 

CMakeLists.txt  
-------------------
The template repository now features `CMakeLists.txt` template, which is listed in an `export` in the template `conanfile.txt`.  This is a wrapper that should be used when building all libraries which use CMake for the build, even when it has no dependencies.  You can tweak and add flags in this file, but most times it just serves to enforce the "Conan-managed" settings and attributes during the build.  If the target library does not use CMake, delete this file and remote the import of the Cmake helper from the `conanfile.py`.


conanfile.py
-------------------

We have conventions for most of the fields of ``conanfile.py``.

url
==========

Always use the URL of the git repo of the recipe, not the original lilbrary. 


homepage
==========

Always use the URL of the original library.

name  
==========

As of December, use only lowercase letters in package names moving forward.  We will be renaming old packages to be all-lowercase. 

version
==========

Always use the version of the upstream package. There are some challenges in some cases, such as those which lack semver, or those that are currently un-released.  Strategies for these cases are described below. 

Packages without official releases
---------------------------------------

The notation shown below is used for publishing packages where the original library does not make official releases. Thus we use a datestamp to show when the package was created:

::

    gsl_microsoft/20171020@bincrafters/stable

Packages without semantic versioning
----------------------------------------

The same notation is used for publishing packages where the original library does have official releases, but does not use semantic versioning. In this case, the version number is the one provided from the original library. In the case of msys2_installer, the library happens to use a datestamp:

::

    msys2_installer/20161025@bincrafters/stable 

        
Conan “latest” version convention
----------------------------------------

In some cases a version alias of “latest” is added to packages. Users
can reference this version in requirements as shown in the example below
to get the latest release without specifying a specific version or
range:

::

    msys2_installer/latest@bincrafters/stable


**Note that using the latest alias will cause your projects to download and use an updated version as soon as it becomes available. Such library updates can potentially be breaking, so users should consider this before referencing the latest alias in a project.**

settings

==============
    
settings.compiler
--------------------------

Windows does not necessarily imply Visual Studio, there are at least GCC
(e.g. MinGW) and Clang for Windows. Thus, don’t write conditions like:

.. code:: python

    if self.settings.os == "Windows": 
        self.run("cl")

write instead:

.. code:: python

    if self.settings.compiler == "Visual Studio": 
        self.run("cl")

settings.arch
--------------------------

Don’t assume there are only two architectures like x86 and x64, there are at least many variations of ARM (even on Windows, yes) so don’t write conditions like:

.. code:: python

    flags = "-m32" if self.settings.arch = 'x86' else = "-m64"

write instead:

.. code:: python

    flags = {'x86': '-m32', 'x86_64': '-m64'}.get(str(self.settings.arch))

settings - restrictions
---------------------------------

Don’t restrict operating system and arch with the following strategy,
even though I think this is in the Conan documentation as a suggestion.
It turns out that this prevents cross-building scenarios.

.. code:: python

    settings = {"os" : ["Windows", "Macos", "Linux"], "arch" : ["x86_64"]}
	
Instead, do this: 

.. code:: python

    def config_options(self):
        # Checking against self.settings.* would prevent cross-building profiles from working
        if tools.detected_architecture() != "x86_64":
            raise Exception("Unsupported Architecture.  This package currently only supports x86_64.")
        if platform.system() not in ["Windows", "Darwin", "Linux"]:
            raise Exception("Unsupported System. This package currently only support Linux/Darwin/Windows")

options
=============

options - fPIC for Linux
------------------------------------

At a certain point, we realized we should be adding fPIC option for many packages which we did not consider before.  So, please check with the team in slack if you're not sure whether or not you need fPIC. 
 
In order to add fPIC options, modify your **conanfile.py** by adding highlighted lines:

.. code:: python

   options = {"shared": [True, False], "fPIC": [True, False]}
   default_options = "shared=False", "fPIC=True"

also, you’ll need **configure** method to skip fPIC for Visual Studio
(if your recipe supports MSVC, of course):

.. code:: python

        def configure(self):
            if self.settings.compiler == 'Visual Studio':
                del self.options.fPIC

For CMake-based projects, modify your ``build()`` method:

.. code:: python

       def build_cmake(self):
           cmake = CMake(self, generator='Ninja')
           if self.settings.compiler != 'Visual Studio':
               cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC

For autotools-based project, you may just need:

.. code:: python

   if self.settings.compiler != 'Visual Studio':
       env_build.fpic = self.options.fPIC

Or alternatively, if configure provides **–with-pic** option:

.. code:: python

   if self.settings.compiler != 'Visual Studio' and self.options.fPIC:
       configure_args.append('--with-pic')

	   
source() method
===============

-  Favor ``tools.get()`` on an archive over git clone. 
-  With github, even if there are no github releases, use the "Download as Zip" url. 
-  Most times you can use a ``.tar.gz`` for windows and linux
-  Validate checksums when they are provided by upstream, pass as parameter to ``tools.get()``
-  We have a convention now: rename the directory that gets extracted or downloaded to ``source_subfolder``. This simplifies several elements in our standard recipes. There’s a feature request in progress to add a param to ``tools.get()`` to automate this.

build() method
================

Don't do `cmake.install()` in the the `build()` method.  The problem is that if/when users just want to try to re-run the `package()` method for some reason, it won't have the desired effect.  

So, don't do this: 

.. code:: python

    def build(self):
        cmake = CMake(self)
		cmake.configure()
		cmake.build()
		cmake.install()
		
	def package(self):
		pass

Do this instead: 

.. code:: python

    def build(self):
        cmake = CMake(self)
		cmake.configure()
		cmake.build()

    def package(self):
        cmake = CMake(self)
		cmake.install()
		
		
package() method
================

Don’t do ``with tools.chdir("sources")``, it doesn’t do what you want it to.

If you're building a CMake project, do `cmake.install()` in the `package()` method (see notes above under `build()` method). 

test_package
================

Our standard for test_package are nice in that you only need to change ``test_package.cpp`` contents in most cases. The ``conanfile.py`` and ``CMakeLists.txt`` are made to be generic. Special circumstances might require some changes to the other files such as for C only libraries, but try to avoid if possible.

Please write the actual minimum contents of a file you can to prove that ``include`` and linking works. Do not use examples from the author, do not test that methods do the right thing. Do not use a test framework, even Catch. Just use a ``main()`` method that gets fun from the ``test()`` method in ``conanfile.py``.