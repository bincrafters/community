
find_path(PORTAUDIO_INCLUDE_DIR NAMES portaudio.h PATHS ${CONAN_INCLUDE_DIRS_PORTAUDIO})
find_library(PORTAUDIO_LIBRARY NAMES ${CONAN_LIBS_PORTAUDIO} PATHS ${CONAN_LIB_DIRS_PORTAUDIO})

IF(CMAKE_SYSTEM_NAME STREQUAL "Linux")
   SET(EXTRA_LIBS rt m asound pthread)
ENDIF()

macro(ADD_OSX_FRAMEWORK fwname)
    find_library(FRAMEWORK_${fwname}
                NAMES ${fwname}
                PATHS ${CMAKE_OSX_SYSROOT}/System/Library
                PATH_SUFFIXES Frameworks
                NO_DEFAULT_PATH)
    if( ${FRAMEWORK_${fwname}} STREQUAL FRAMEWORK_${fwname}-NOTFOUND)
        message(ERROR ": Framework ${fwname} not found")
    else()
        set(EXTRA_LIBS ${EXTRA_LIBS} "${FRAMEWORK_${fwname}}/${fwname}")
        message(STATUS "Framework ${fwname} found at ${FRAMEWORK_${fwname}}")
    endif()
endmacro(ADD_OSX_FRAMEWORK)

if(APPLE)
   # This frameworks are needed for macos: http://portaudio.com/docs/v19-doxydocs/compile_mac_coreaudio.html
   ADD_OSX_FRAMEWORK(CoreServices)
   ADD_OSX_FRAMEWORK(Carbon)
   ADD_OSX_FRAMEWORK(AudioUnit)
   ADD_OSX_FRAMEWORK(AudioToolbox)
   ADD_OSX_FRAMEWORK(CoreAudio)
endif(APPLE)

set(PORTAUDIO_INCLUDE_DIRS ${PORTAUDIO_INCLUDE_DIR})
set(PORTAUDIO_LIBRARIES ${PORTAUDIO_LIBRARY} ${EXTRA_LIBS})

mark_as_advanced(PORTAUDIO_LIBRARY PORTAUDIO_INCLUDE_DIR)

message("** Portaudio found by Conan!")
set(PORTAUDIO_FOUND TRUE)
message("   - libraries:  ${PORTAUDIO_LIBRARIES}")
message("   - includes:  ${PORTAUDIO_INCLUDE_DIRS}")

