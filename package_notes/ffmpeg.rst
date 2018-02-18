ffmpeg
----------------------

FFmpeg is a very complex library, which has support and integration for many other C and C++ libraries.  For a Conan package, this means numerous options which control the optional dependencies it is compiled with.  Here are the current options available, with more to come over time. 

+-----------------+---------+-----------------+
| Option          | Default | Possible Values |
+=================+=========+=================+
| xcb             | True    | [True, False]   |
+-----------------+---------+-----------------+
| pulse           | True    | [True, False]   |
+-----------------+---------+-----------------+
| vorbis          | True    | [True, False]   |
+-----------------+---------+-----------------+
| lzma            | True    | [True, False]   |
+-----------------+---------+-----------------+
| iconv           | True    | [True, False]   |
+-----------------+---------+-----------------+
| bzlib           | True    | [True, False]   |
+-----------------+---------+-----------------+
| opus            | True    | [True, False]   |
+-----------------+---------+-----------------+
| avfoundation    | True    | [True, False]   |
+-----------------+---------+-----------------+
| shared          | False   | [True, False]   |
+-----------------+---------+-----------------+
| zmq             | True    | [True, False]   |
+-----------------+---------+-----------------+
| alsa            | True    | [True, False]   |
+-----------------+---------+-----------------+
| freetype        | False   | [True, False]   |
+-----------------+---------+-----------------+
| audiotoolbox    | True    | [True, False]   |
+-----------------+---------+-----------------+
| fPIC            | True    | [True, False]   |
+-----------------+---------+-----------------+
| videotoolbox    | True    | [True, False]   |
+-----------------+---------+-----------------+
| coreimage       | True    | [True, False]   |
+-----------------+---------+-----------------+
| appkit          | True    | [True, False]   |
+-----------------+---------+-----------------+
| openjpeg        | True    | [True, False]   |
+-----------------+---------+-----------------+
| securetransport | True    | [True, False]   |
+-----------------+---------+-----------------+
| vdpau           | True    | [True, False]   |
+-----------------+---------+-----------------+
| zlib            | True    | [True, False]   |
+-----------------+---------+-----------------+
| vda             | False   | [True, False]   |
+-----------------+---------+-----------------+
| vaapi           | True    | [True, False]   |
+-----------------+---------+-----------------+
| jack            | True    | [True, False]   |
+-----------------+---------+-----------------+