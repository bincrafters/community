Requirements for packagers
==========================

Everybody needs their own accounts in each system:
#. github
#. appveyor
#. travis
#. bintray

Where to get Bincrafters Templates
===================================

https://github.com/bincrafters/conan-templates


Using Bincrafters Templates
===========================
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

Additional steps are required to build the package using CI services like TravisCI and Appveyor.  Those are documented below. 


General package workflow for Contributors
=========================================

#. Setup a github repo for the recipe under your own github account
#. In the Github "Website" field, add the URL to the original library homepage.
#. Copy the relevant files from **the relevant branch** of the templates repository above.
#. Use Bincrafters standard branch naming convention (testing/x.y.z)
#. Get help from the team via PR’s to your own github account
#. Add Bincrafters standard CI recipes and scripts
#. Activate the repo in your own appveyor and travis
#. Setup publishing to your own Bintray account
#. Open an issue on Bincrafters community, requesting package inclusion
#. Once approved, Bincrafters will clone your repo
#. To make a contribution to a project, you must fork it and submit a PR

General package workflow for Bincrafters members
================================================

#. Setup a github repo for the recipe under your own github account
#. In the Github "Website" field, add the URL to the original library homepage.
#. Copy the relevant files from **the relevant branch** of the templates repository above.
#. Use Bincrafters standard branch naming convention (testing/x.y.z)
#. Get help from the team via PR’s to your own github account
#. Add Bincrafters standard CI recipes and scripts
#. Activate the repo in your own appveyor and travis
#. Setup publishing to your own Bintray account
#. Once working and verified, create the equivalent repo in Bincrafters
#. Add the Bincrafters repo as a git remote and push
#. Have solvingj enable travis and appveyor on the repo
#. Get Bintray credentials added in CI: see:  :ref:`ci credentials`
#. Once the package appears on Bintray, add the metadata via Bintray UI
#. To make a contribution to a project, you must fork it and submit a PR
