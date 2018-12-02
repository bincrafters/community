Template Content for Conan Packaging
-------------------------------------
Bincrafters has a repository containing all the template files you need for a Conan package including the following, among others:

- ``conanfile.py``
- ``build.py``
- ``README.md``
- ``LICENSE.md``
- ``appveyor.yml``
- ``.travis.yml``
- ``test_package\conanfile.py``
- ``test_package\CMakeLists.txt``
- ``test_package\test_package.cpp``

The process of using these templates is extremely simple: 

- Clone the templates repository. 
- Open each file in a text editor and familiarize yourself with the contents. 
- Perform the following find and replace operations manually
- ``conanfile.py`` : Evaluate every line of this file for possible replacement. 
- ``README.md`` : Replace all 6 instances of ``package_name`` with the name of your package. 
- ``test_package\CMakeLists.txt`` : If CMake is used by the project, no changes necessary, otherwise delete the file.
- ``test_package\test_package.cpp`` : Completely re-write the contents with a custom test for your package. 

That's it for editing the templates, all of the other template files have been generalized to the point where they do not need to be modified.  

Additional steps are required to build the package using CI services like TravisCI and Appveyor.  Those are documented here:  

`general-package-workflow-for-contributors <https://bincrafters.readthedocs.io/en/latest/contributing_to_packages/package_guidelines_faq.html#general-package-workflow-for-contributors>`_




