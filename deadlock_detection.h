#ifndef DEADLOCK_DETECTION_H
#define DEADLOCK_DETECTION_H

#include <vector>

class DeadlockDetection {
public:
    DeadlockDetection(int processes, int resources);
    
    void setAllocation(const std::vector<std::vector<int>>& allocation);
    void setRequest(const std::vector<std::vector<int>>& request);
    
    bool detectDeadlock();

private:
    int processes;
    int resources;
    
    std::vector<std::vector<int>> allocation;
    std::vector<std::vector<int>> request;

    bool dfs(int node, std::vector<bool>& visited, std::vector<bool>& recStack);
};

#endif // DEADLOCK_DETECTION_H