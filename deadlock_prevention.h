#ifndef DEADLOCK_PREVENTION_H
#define DEADLOCK_PREVENTION_H

#include <vector>

class DeadlockPrevention {
public:
    DeadlockPrevention(int processes, int resources);
    void setAvailableResources(const std::vector<int>& available);
    void setMaxNeed(const std::vector<std::vector<int>>& maxNeed);
    void setAllocation(const std::vector<std::vector<int>>& allocation);
    bool requestResources(int processID, const std::vector<int>& request);
    bool isSafeState(std::vector<int>& safeSequence);

private:
    int processes;
    int resources;
    std::vector<int> available;
    std::vector<std::vector<int>> maxNeed;
    std::vector<std::vector<int>> allocation;
    std::vector<std::vector<int>> need;
};

#endif // DEADLOCK_PREVENTION_H