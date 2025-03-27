#include "deadlock_prevention.h"
#include <iostream>
#include <algorithm>

DeadlockPrevention::DeadlockPrevention(int p, int r) : processes(p), resources(r) {
    maxNeed.resize(processes, std::vector<int>(resources));
    allocation.resize(processes, std::vector<int>(resources));
    need.resize(processes, std::vector<int>(resources));
}

void DeadlockPrevention::setAvailableResources(const std::vector<int>& avail) {
    available = avail;
}

void DeadlockPrevention::setMaxNeed(const std::vector<std::vector<int>>& maxN) {
    maxNeed = maxN;
}

void DeadlockPrevention::setAllocation(const std::vector<std::vector<int>>& alloc) {
    allocation = alloc;
    
    // Calculate remaining need
    for (int i = 0; i < processes; ++i) {
        for (int j = 0; j < resources; ++j) {
            need[i][j] = maxNeed[i][j] - allocation[i][j];
        }
    }
}

bool DeadlockPrevention::requestResources(int processID, const std::vector<int>& request) {
    // Check if request is valid
    for (int i = 0; i < resources; ++i) {
        if (request[i] > need[processID][i] || request[i] > available[i]) {
            return false; // Invalid request
        }
    }

    // Temporarily allocate resources
    for (int i = 0; i < resources; ++i) {
        available[i] -= request[i];
        allocation[processID][i] += request[i];
        need[processID][i] -= request[i];
    }

    // Check if state is safe
    std::vector<int> safeSequence;
    if (isSafeState(safeSequence)) {
        return true; // Request granted
    } else {
        // Rollback changes if not safe
        for (int i = 0; i < resources; ++i) {
            available[i] += request[i];
            allocation[processID][i] -= request[i];
            need[processID][i] += request[i];
        }
        return false; // Request denied
    }
}

bool DeadlockPrevention::isSafeState(std::vector<int>& safeSequence) {
    std::vector<bool> finish(processes, false);
    std::vector<int> work = available;

    while (safeSequence.size() < processes) {
        bool foundProcess = false;

        for (int p = 0; p < processes; ++p) {
            if (!finish[p]) {
                bool canAllocate = true;

                for (int r = 0; r < resources; ++r) {
                    if (need[p][r] > work[r]) {
                        canAllocate = false;
                        break;
                    }
                }

                if (canAllocate) {
                    for (int r = 0; r < resources; ++r) {
                        work[r] += allocation[p][r];
                    }
                    finish[p] = true;
                    safeSequence.push_back(p);
                    foundProcess = true;
                }
            }
        }

        if (!foundProcess) { // No process could be allocated
            return false;
        }
    }

    return true; // Safe state found
}