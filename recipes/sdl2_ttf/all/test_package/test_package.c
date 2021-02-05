#include <SDL2/SDL_ttf.h>

#include <stdio.h>

int main(int argc, char **argv)
{
    if (TTF_Init() == -1) {
        fprintf(stderr, "Failed to initialize TTF: %s\n", SDL_GetError());
        return 1;
    }

    TTF_Font *font = TTF_OpenFont(FONT_PATH, 16);

    if (font == NULL) {
        fprintf(stderr, "Failed to load font: %s\n", SDL_GetError());
        return 1;
    }

    printf("SDL2_ttf is working!\n");

    return 0;
}
