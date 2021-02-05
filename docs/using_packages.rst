Using Packages
==============

Bincrafters is posting new packages and/or versions to our public Conan repository every week. We've provided some instructions below for users who wish to start using them.

Installing Conan
------------------------------------------------
If you do not have Conan installed, please refer to the official Conan installation instructions.

`Conan Installation Instructions <https://docs.conan.io/en/latest/installation.html>`_

Adding the Bincrafters repository as a "Conan Remote"
-----------------------------------------------------

By default, Conan will only search for packages in the central Conan Center repository.  Bincrafters packages are hosted in a separate Conan repository which is hosted on a JFrog Artifactory instance, which is managed by the Bincrafters team.  To start using any of the Bincrafters packages, run the command below:

.. code-block:: bash

	$ conan remote add bincrafters https://bincrafters.jfrog.io/artifactory/api/conan/public-conan


Please note, that your Conan client also needs to have revisions enabled. You can do this via

.. code-block:: bash

	$ conan config set general.revisions_enabled=1


Understanding Conan Channels
------------------------------------------------
Conan has a somewhat unique but valuable notion of channels embedded in the package names.  An example package name is:

.. code-block:: bash

	boost_system/1.64.0@bincrafters/stable

The channel name in this example is "stable".  This is a required field for every package, but it's a completely arbitrary string meaning that authors can put whatever they want.  Bincrafters follows a somewhat standard convention utilized by the Conan teams own packages, which features two possible channel values:  `testing` or `stable`.   Under almost all circumstances, users should prefer the`stable` channel if it exists.  In some cases, brand new packages may only feature a `testing` channel, but these packages would not be considered safe for general users anyway and are not supported.

Packages without official releases
------------------------------------------------
The notation shown below is used for publishing packages where the original library does not make official releases. Thus we use a datestamp to show when the package was created.  In order to create reproducable builds, we also "commit-lock" to the latest commit on that day, otherwise users would get inconsistent results over time when using `--build`.  The "Guidelines Support Library" from Microsoft is an example of a package for which we used this versioning:

.. code-block:: bash

	gsl_microsoft/20180102@bincrafters/stable

And here is a link to the recipe itself, showing how we do the "commit-lock":

https://github.com/bincrafters/conan-gsl_microsoft/blob/stable/20180102/conanfile.py#L11


Packages without semantic versioning
------------------------------------------------

The same notation is used for publishing packages where the original library does have official releases, but does not use semantic versioning. In this case, the version number is the one provided from the original library.  In the case of `msys2_installer`, the library happens to use a datestamp:

.. code-block:: bash

	msys2_installer/20161025@bincrafters/stable


Prerelease packages
------------------------------------------------
When there wasn't a stable release in the upstream projects for a long time, it might be okay to add a pre-release version. This could look like this:

.. code-block:: bash

	premake_installer/5.0.0-alpha14@bincrafters/stable
