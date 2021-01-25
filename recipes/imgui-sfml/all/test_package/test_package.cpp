#include "imgui.h"
#include "imgui-SFML.h"

#include <SFML/Window/Event.hpp>

int main() {
    sf::Event event; 
    ImGui::SFML::ProcessEvent(event);
    return 0;
}
