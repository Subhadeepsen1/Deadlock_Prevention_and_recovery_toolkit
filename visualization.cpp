#include "visualization.h"

Visualization::Visualization(int width, int height)
: window(sf::VideoMode(width, height), "Resource Allocation Graph") {}

void Visualization::drawGraph(const std::unordered_map<std::string, sf::Vector2f>& nodes,
                               const std::unordered_map<std::string, sf::Color>& colors,
                               const std::unordered_map<std::string, std::string>& edges) {

   window.clear();

   // Draw nodes
   for (const auto& node : nodes) {
       sf::CircleShape circle(20); // Node radius 
       circle.setPosition(node.second);
       circle.setFillColor(colors.at(node.first));
       window.draw(circle);
   }

   // Draw edges
   for (const auto& edge : edges) { 
       sf:Vertex line[] =
       { 
           sf:Vertex(nodes.at(edge.first), sf:Color(255, 255, 255)),
           sf:Vertex(nodes.at(edge.second), sf:Color(255, 255, 255))
       };
       window.draw(line, 2, sf:Lines); 
   }

   window.display();
}