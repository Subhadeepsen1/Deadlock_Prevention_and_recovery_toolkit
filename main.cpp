#include "deadlock_detection.h"
#include "deadlock_prevention.h"
#include "visualization.h"
#include <iostream>
#include <unordered_map>
#include <thread>
#include <chrono>

void simulate(DeadlockPrevention& dpToolkit, Visualization& visualizer) {
   while (true) { 
       // Example user input handling and resource requests simulation

       int processID; 
       int resourceRequest[2]; 

       // Simulate user input or predefined requests here...
       
       if(dpToolkit.requestResources(processID, {resourceRequest[0], resourceRequest[1]})) { 
           // Update graph visualization based on successful allocation...
           visualizer.drawGraph(...); 
       } else { 
           // Handle unsuccessful requests...
           visualizer.drawGraph(...); 
       }

       // Sleep or wait before next iteration...
       std: this_thread.sleep_for(std:chrono seconds(1)); 
   }
}

int main() {
   const int numProcesses = 5; 
   const int numResources = 3;

   DeadlockPrevention dpToolkit(numProcesses,numResources); 
   dpToolkit.setAvailableResources({10 ,5 ,7}); 

   dpToolkit.setMaxNeed({{7 ,5 ,3}, {3 ,2 ,2}, {9 ,0 ,2}, {2 ,2 ,2}, {4 ,3 ,3}}); 
   dpToolkit.setAllocation({{0 ,1 ,0}, {2 ,0 ,0}, {3 ,0 ,2}, {2 ,1 ,1}, {0 ,0 ,2}}); 

   Visualization visualizer(800 ,600); 

   simulate(dpToolkit ,visualizer); 

   return 0; 
}