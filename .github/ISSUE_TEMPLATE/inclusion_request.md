---
name: 'Package Inclusion Request'
about: 'Request Library for the inclusion into Bincrafters'
title: 'Inclusion Request: <LIBRARY NAME>'
labels: Packaging
---

### Package Details
  * Package Name: **libpng**
  * Operating Systems+versions: **Linux Ubuntu 16.04, Ubuntu 18.04, Windows, macOS**
  * Compiler support: **gcc-5.4, gcc6, clang7**
  * Conan recipe repository: **https://github.com/bincrafters/conan-libpng**

### Inclusion request
  * Fill all checkboxes with x if you agree with the statement or if it applies to your Conan recipe
  * [ ] I want that my Conan recipe is getting included into the Bincrafters organisation
  * [ ] I understand that if my request is accepted we are cloning your repository with all its history into Bincrafters, adapt some configurations and meta data if needed, and publishing it under the Bincrafters name and accounts
  * [ ] I have used the Bincrafters templates to develop my Conan recipe - https://github.com/bincrafters/conan-templates
  * [ ] My Conan recipe and all parts of it are licensed under the MIT license - https://choosealicense.com/licenses/mit/
    * Bincrafters are releasing all recipes under MIT license. If you want to have your recipe within Bincrafters we kindly ask you to do the same
    * it is okay if your test_package contains code from the upstream project under the upstream project's license, as long as it is clearly mentioned within the test_package files
  * [ ] My Conan recipe covers (at least) the latest stable version which is available for the package
  * [ ] I know that my Conan recipe is working on all operating system and compilers mentioned above right now
    * if not: please provide here links to your CI platforms and / or build logs and describe the problems you encounter
  * [ ] I'm willing to help to maintain the recipe even after it is included into Bincrafters


### Checklist for the Bincrafters team
  * Ignore this if you are not part of the Bincrafters team
  * [ ] There is no such Conan package yet in conan-center, conan-community or Bincrafters
  * [ ] The project is either popular or deserves to be maintained for another good reason (we can't package every single project out there)
  * [ ] [bincrafters-conventions](https://github.com/bincrafters/bincrafters-conventions) reports no major complains; the recipe fulfills our general quality requirements and conventions
  * [ ] The recipe is cloned into our organisation; CI is enabled and configurated and succeeds
  * [ ] There is a branch protection rule for `stable/*` branches, which requires a pull request with at least one approval first before things can get published
  * Considering granding the inclusion request author push rights to the recipe repository (there is no guarantee that everyone is getting push rights, we decide this on a case-to-case base)
