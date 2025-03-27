#include "deadlock_detection.h"
#include <iostream>

DeadlockDetection::DeadlockDetection(int p, int r)
: processes(p), resources(r), allocation(p, std::vector<int>(r)), request(p, std::vector<int>(r)) {}

void DeadlockDetection::setAllocation(const std::vector<std::vector<int>>& alloc) {
    allocation = alloc;
}

void DeadlockDetection::setRequest(const std::vector<std::vector<int>>& req) {
    request = req;
}

bool DeadlockDetection::dfs(int node, std::vector<bool>& visited, std::vector<bool>& recStack) {
    visited[node] = true;
    recStack[node] = true;

    for (int neighbor : request[node]) { // Assuming request[node] contains indices of neighbors in RAG
        if (!visited[neighbor]) {
            if (dfs(neighbor, visited, recStack)) return true;
        } else if (recStack[neighbor]) return true;
    }

    recStack[node] = false;
    return false;
}

bool DeadlockDetection::detectDeadlock() {
    std::vector<bool> visited(processes, false);
    std::vector<bool> recStack(processes, false);

    for (int i = 0; i < processes; i++) {
        if (!visited[i]) {
            if (dfs(i, visited, recStack)) {
                return true; // Deadlock detected
            }
        }
    }
    
    return false; // No deadlocks detected
}