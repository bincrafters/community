#include <iostream>
#include <fluidsynth.h>

int main()
{
    std::cout << "FluidSynth version:" << fluid_version_str() << std::endl;
    return 0;
}
