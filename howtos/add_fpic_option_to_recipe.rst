Add fPIC option to a Conan Recipe
-------------------------------

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