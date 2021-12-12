#include "imgui.h"
#include "imgui-SFML.h"

#include <SFML/Window/Event.hpp>
#include <SFML/Graphics/RenderWindow.hpp>

int main() {
    sf::Event event; 
    sf::RenderWindow window(sf::VideoMode(1, 1), "");
    ImGui::SFML::Init(window);
    ImGui::SFML::ProcessEvent(window, event);
    return 0;
}
