cmake_minimum_required(VERSION 2.8.12)
project(sdl2_mixer)

include(conanbuildinfo.cmake)
conan_basic_setup()

macro(add_music_option type)
  option(${type} "${type} music support" OFF)
  message(STATUS "${type} ${${type}}")
  if(${${type}})
    add_definitions("-DMUSIC_${type}")
    if(${${type}_DYNAMIC})
      add_definitions("-D${type}_DYNAMIC")
    endif()
  endif()
endmacro()

add_music_option(CMD)
add_music_option(WAV)
add_music_option(FLAC)
add_music_option(OGG)
add_music_option(OPUS)
add_music_option(MP3_MPG123)
add_music_option(MP3_MAD)
add_music_option(MOD_MIKMOD)
add_music_option(MOD_MODPLUG)
add_music_option(MID_NATIVE)
add_music_option(MID_FLUIDSYNTH)
add_music_option(MID_TINYMIDI)

if(${MID_NATIVE})

set(NATIVE_MIDI_SOURCES
source_subfolder/native_midi/native_midi_common.c
source_subfolder/native_midi/native_midi_common.h
source_subfolder/native_midi/native_midi_haiku.cpp
source_subfolder/native_midi/native_midi_mac.c
source_subfolder/native_midi/native_midi_macosx.c
source_subfolder/native_midi/native_midi_win32.c
)

set(NATIVE_MIDI_HEADERS
source_subfolder/native_midi/native_midi.h
)

endif()

set(SOURCES
source_subfolder/effect_position.c
source_subfolder/effect_stereoreverse.c
source_subfolder/effects_internal.c
source_subfolder/load_aiff.c
source_subfolder/load_voc.c
source_subfolder/mixer.c
source_subfolder/music.c
source_subfolder/music_cmd.c
source_subfolder/music_flac.c
source_subfolder/music_fluidsynth.c
source_subfolder/music_mad.c
source_subfolder/music_mikmod.c
source_subfolder/music_modplug.c
source_subfolder/music_mpg123.c
source_subfolder/music_nativemidi.c
source_subfolder/music_ogg.c
source_subfolder/music_opus.c
source_subfolder/music_timidity.c
source_subfolder/music_wav.c
${NATIVE_MIDI_SOURCES}
)

set(HEADERS
source_subfolder/effects_internal.h
source_subfolder/load_aiff.h
source_subfolder/load_voc.h
source_subfolder/mixer.h
source_subfolder/music.h
source_subfolder/music_cmd.h
source_subfolder/music_flac.h
source_subfolder/music_fluidsynth.h
source_subfolder/music_mad.h
source_subfolder/music_mikmod.h
source_subfolder/music_modplug.h
source_subfolder/music_mpg123.h
source_subfolder/music_nativemidi.h
source_subfolder/music_ogg.h
source_subfolder/music_opus.h
source_subfolder/music_timidity.h
source_subfolder/music_wav.h
${NATIVE_MIDI_HEADERS}
)

add_library(${PROJECT_NAME} ${SOURCES} ${HEADERS})

target_include_directories(${PROJECT_NAME} PRIVATE "source_subfolder")

if(${MID_NATIVE})
  target_include_directories(${PROJECT_NAME} PRIVATE "source_subfolder/native_midi")
endif()

target_link_libraries(${PROJECT_NAME} PRIVATE ${CONAN_LIBS})
set_target_properties(${PROJECT_NAME} PROPERTIES PUBLIC_HEADER source_subfolder/SDL_mixer.h)

if(${BUILD_SHARED_LIBS})
  target_compile_definitions(${PROJECT_NAME} PRIVATE DLL_EXPORT)
endif()

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION "lib"
  LIBRARY DESTINATION "lib"
  RUNTIME DESTINATION "bin"
  PUBLIC_HEADER DESTINATION "include/SDL2"
)
