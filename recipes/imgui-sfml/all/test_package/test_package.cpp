#include "imgui.h"
#include "imgui-SFML.h"

#include <SFML/Window/Event.hpp>
#ifdef WITH_WINDOW
#include <SFML/Graphics/RenderWindow.hpp>
#endif

int main() {
    sf::Event event; 
    #ifdef WITH_WINDOW
    sf::RenderWindow window(sf::VideoMode(1, 1), "");
    ImGui::SFML::Init(window);
    ImGui::SFML::ProcessEvent(window, event);
    #else
    ImGui::SFML::ProcessEvent(event);
    #endif
    return 0;
}
