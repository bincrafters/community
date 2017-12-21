Requirements for packagers
==========================

Everybody needs their own accounts in each system:
#. github 
#. appveyor
#. travis 
#. bintray

Where to get templates
======================

https://github.com/bincrafters/conan-templates

General package workflow
========================

#. Setup a github repo for the recipe under your own github account
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

