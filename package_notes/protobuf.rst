Google Protobuf
---------------

Google Protocol Buffers are a method of serializing structured data. It is useful in developing
programs to communicate with each other over a wire or for storing data.

As Protobuf is a complex project, we split it into a couple of packages, one package
installer only for *protoc* and one regular package for the libraries.

Protoc Installer
================
protoc-installer_ is a Conan package focused in provide only **protoc** application and CMake
files used to import macros, such as *protobuf_generate_cpp* and *protobuf_generate*. It does not
require any other package.

Protobuf
========
protobuf_ is a Conan package designed to distribute only Protobuf libraries, such as *libprotobuf*,
*libprotobuf-lite* and *libprotoc*. However, **protobuf** and **lite** are mutually related,
you should only bind one per configuration. It does not require **protoc** application to be used.

Protobuf Integration Test
=========================
There are many possible scenarios for Protobuf to be used, including embedded systems. When cross
building a project, you probably will need all prebuilt libraries for your target architecture, but
your protoc should be able to run on your host platform and generate all outputs.

protobuf-integration-test_ was created to simulate more elaborate, real-life cases, including the example above.
Because protoc and protobuf are independent of each other, only a simple Conan test package would
not be enough to reproduce some scenarios.

Both protoc-installer and protobuf have a trigger to start a new integration test when the stable
branch is updated. Read the Travis and Appveyor files to get more information.

.. figure:: .images/protobuf-testing.png

.. _protoc-installer: https://github.com/bincrafters/conan-protoc_installer
.. _protobuf: https://github.com/bincrafters/conan-protobuf
.. _protobuf-integration-test: https://github.com/bincrafters/protobuf-integration-test
