#ifndef VISUALIZATION_H
#define VISUALIZATION_H

#include <SFML/Graphics.hpp>
#include <string>
#include <unordered_map>

class Visualization {
public:
    Visualization(int width, int height);
    
    void drawGraph(const std::unordered_map<std::string, sf::Vector2f>& nodes,
                   const std::unordered_map<std::string, sf::Color>& colors,
                   const std::unordered_map<std::string, std::string>& edges);
    
private:
    sf::RenderWindow window;
};

#endif // VISUALIZATION_H