#include "imgui.h"
#include "imgui-SFML.h"

#include <SFML/Window/Event.hpp>

int main() {
    #ifdef IMGUI_SFML_VERSION_GREATER_THAN_2_3
    ImGui::SFML::Shutdown();
    #else
    sf::Event event; 
    ImGui::SFML::ProcessEvent(event);
    #endif
    return 0;
}
