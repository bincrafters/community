#include <iostream>
#include <cstdlib>
#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>

int main(int argc, char *argv[])
{
    int audio_rate = MIX_DEFAULT_FREQUENCY;
    int audio_format = MIX_DEFAULT_FORMAT;
    int audio_channels = 2;
    bool under_ci = (std::getenv("CI") != NULL);
    if (SDL_Init(SDL_INIT_AUDIO) < 0)
        return under_ci ? 0 : -1;
    Mix_Init(MIX_INIT_FLAC | MIX_INIT_MOD | MIX_INIT_MP3 | MIX_INIT_OGG | MIX_INIT_MID | MIX_INIT_OPUS);

    if (Mix_OpenAudio(audio_rate, audio_format, audio_channels, 4096) < 0)
        return under_ci ? 0 : -3;

    const SDL_version * version = Mix_Linked_Version();
    std::cout << "SDL2_mixer version: ";
    std::cout << int(version->major) << ".";
    std::cout << int(version->minor) << ".";
    std::cout << int(version->patch) << std::endl;

    int num_chunk_decoders = Mix_GetNumChunkDecoders();
    std::cout << "chunk decoders:" << std::endl;
    for (int i = 0; i < num_chunk_decoders; ++i)
        std::cout << "\t" << Mix_GetChunkDecoder(i) << std::endl;
    int num_music_decoders = Mix_GetNumMusicDecoders();
    std::cout << "music decoders:" << std::endl;
    for (int i = 0; i < num_music_decoders; ++i)
        std::cout << "\t" << Mix_GetMusicDecoder(i) << std::endl;
    Mix_CloseAudio();
    Mix_Quit();
    return 0;
}
