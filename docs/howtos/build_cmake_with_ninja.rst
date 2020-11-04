Build CMake project with ninja
---------------------------------------------

in order to build CMake project with ninja, add the following into the
**conanfile.py**:

::

       def build(self):
            if self.settings.compiler == 'Visual Studio':
                with tools.vcvars(self.settings, force=True, filter_known_paths=False):
                    self.build_cmake()
            else:
                self.build_cmake()

        def build_cmake(self):
            cmake = CMake(self, generator='Ninja')

also, the following is needed in **build.py**:

::

    from bincrafters import build_template_default


    def add_build_requires(builds):
        return map(add_required_installers, builds)


    def add_required_installers(build):
        installers = ['ninja/1.9.1@bincrafters/stable']
        build.build_requires.update({"*": installers})
        return build


    if __name__ == "__main__":

        builder = build_template_default.get_builder()

        builder.items = add_build_requires(builder.items)

        builder.run()

in order to build locally, you need ninja_installer in your profile.
first, create new profile for ninja:

``conan profile new --detect``

then put the following into the profile (*$HOME/.conan/profiles/ninja)*:

::

    [build_requires]
    ninja_installer/1.8.2@bincrafters/stable

then to build locally with ninja run:

``conan create . bincrafters/testing -p ninja``
