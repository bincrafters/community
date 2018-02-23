		
appveyor.yml
------------

The standard for this file is fully generic and requires no modifications between libraries. Of course, some libraries are special, but it’s very helpful for libraries to use the generic template when possible.

.travis.yml
-----------

The standard for this file is fully generic and requires no modifications between libraries. Of course, some libraries are special, but it’s very helpful for libraries to use the generic template when
possible.

Badges
-----------------

Please try to add the following banners after you’ve got the recipe mostly working:   

-  Bintray - The badge URL should have at the end:  `...\_latest` 
-  Appveyor - The badge URL should have at the end (example): `github/bincrafters/conan-lzma?svg=true` 
-  Travis - The badge URL should have at the end (example):  `bincrafters/conan-lzma.svg`


build.py
--------

The standard for this file is fully generic and requires no modifications between libraries. Of course, some libraries are special, but it’s very helpful for libraries to use the generic template when possible.

–build missing
==============

Do not use ``--build missing`` in your ``build.py`` files. This is not the default for a reason. It might be useful to turn this on temporarily for testing, but it should not be left turned on in ``build.py``
long-term.

filtering builds
================

In simple cases, please use python's `filter` method with a lambda.  If the condition is more than a line, break out the condition into a separate function which returns bool. If there are multiple conditions and it's a bit more complex, you should use the for comprehension as example provided on Conan Package Tools documentation. This method always works, it's just very verbose. 

Link to Conan Package Tools method: 

https://github.com/conan-io/conan-package-tools#filtering-the-configurations

Simpler Example using `filter()`:

.. code:: python

	from bincrafters import build_template_default

	if __name__ == "__main__":

		builder = build_template_default.get_builder()
		
		# Filter out (don't build) shared versions the lib
		builder.builds = filter(lambda build: build.options['somelib:shared'] == False , builder.items)
		
		builder.run()

Slightly more complex example of using `filter()`:

.. code:: python

	from bincrafters import build_template_default

    def _is_static_msvc_build(build):
        if build.options['somelib:shared'] == False and build.settings['compiler'] == 'Visual Studio':
            return False
		else:
			return True
		
	if __name__ == "__main__":

		builder = build_template_default.get_builder()
		
		# Filter out (don't build) shared versions the lib, but only for MSVC
		builder.builds = filter(_is_static_msvc_build , builder.items)
		
		builder.run()

