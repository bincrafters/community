Using Packages
==============

Bincrafters is posting new packages and/or versions to our public Conan repository every week. We've provided some instructions below for users who wish to start using them.

Installing Conan
------------------------------------------------
If you do not have Conan installed, please refer to the official Conan installation instructions.

`Conan Installation Instructions <http://conanio.readthedocs.io/en/latest/installation.html>`_

Adding the Bincrafters repository as a "Conan Remote"
-----------------------------------------------------

By default, Conan will only search for packages from the two central repositories hosted and moderated by Conan.io staff: "conan-center" and "conan-transit".  Bincrafters packages are hosted in a separate Conan repository which is also hosted by Bintray, but which is managed by the Bincrafters team.  To start using any of the Bincrafters packages, simply run the command below:

.. code-block:: bash

	$ conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan

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

Conan "latest" version convention
------------------------------------------------
In some cases a version alias of "latest" is added to packages (`Conan Alias feature Explained <http://docs.conan.io/en/latest/reference/commands/misc/alias.html?highlight=alias/>`_).  Users can reference this version in requirements as shown in the example below to get the latest release without specifying a specific version or range:

.. code-block:: bash

	msys2_installer/latest@bincrafters/stable

*Note that using the `latest` alias will cause your projects to download and use an updated version as soon as it becomes available.  Such library updates can potentially be breaking, so users should consider this before referencing the `latest` alias in a project.*

Prerelease packages
------------------------------------------------
Another notation is used for publishing packages that are in a pre-release status or containing a critical bug fix which is not yet officially released by the author.  The sources for these packages are usually pulled from a named Github branch, so the branch name is included.  Also, despite not being part of a release yet, in order to allow for proper handling of semantic versioning the package will have a proper version number, which will be that of the next major release (even though it's not out yet).  An example of this notation is:

.. code-block:: bash

	boost_beast/1.66.0@bincrafters/git-develop

Much like testing, packages in these types of channels are considered volatile and not fit for production use.  When the next release of the package occurs, users testing this package should immediately switch to the stable branch.  After one month has passed with an official release, these pre-release packages are subject to removeal from the repository.

