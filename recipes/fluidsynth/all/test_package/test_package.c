#include <stdio.h>
#include <fluidsynth.h>

int main()
{
    printf("FluidSynth version: %s\n", fluid_version_str());
    return 0;
}
