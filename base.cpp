#include <iostream>
#include <vector>
#include <string>

using std::cin;
using std::cout;
using std::vector;
using std::string;

class DeadlockManager {
    struct ProcessState {
        vector<int> max_need;
        vector<int> allocated;
        vector<int> remaining_need;
    };

    vector<int> available_resources;
    vector<ProcessState> processes;
    vector<vector<int>> allocation_graph;

public:
    void initialize() {
        int num_processes, num_resources;
        cout << "Number of processes and resources: ";
        cin >> num_processes >> num_resources;

        cout << "\nAvailable resources (" << num_resources << " values): ";
        available_resources.resize(num_resources);
        for (int& res : available_resources) cin >> res;

        processes.resize(num_processes);
        for (int i = 0; i < num_processes; ++i) {
            cout << "\nProcess " << i << " details:\n";
            cout << "- Maximum needs: ";
            processes[i].max_need.resize(num_resources);
            for (int& val : processes[i].max_need) cin >> val;

            cout << "- Current allocations: ";
            processes[i].allocated.resize(num_resources);
            processes[i].remaining_need = processes[i].max_need;
            
            for (int& alloc : processes[i].allocated) {
                cin >> alloc;
                if (alloc < 0) {
                    cout << "Error: Negative allocation not allowed\n";
                    exit(1);
                }
            }

            // Calculate remaining needs
            for (int j = 0; j < num_resources; ++j) {
                processes[i].remaining_need[j] -= processes[i].allocated[j];
                if (processes[i].remaining_need[j] < 0) {
                    cout << "Error: Allocation exceeds maximum need\n";
                    exit(1);
                }
            }
        }
        build_allocation_graph();
    }

    void request_resources(int process_id, const vector<int>& request) {
        if (process_id < 0 || process_id >= processes.size()) {
            cout << "Invalid process ID\n";
            return;
        }

        if (!is_safe_request(process_id, request)) {
            cout << "Request denied: Unsafe state\n";
            return;
        }

        // Tentatively allocate resources
        for (size_t i = 0; i < request.size(); ++i) {
            available_resources[i] -= request[i];
            processes[process_id].allocated[i] += request[i];
            processes[process_id].remaining_need[i] -= request[i];
        }

        cout << "Resources allocated successfully\n";
        rebuild_graph_and_check();
    }

private:
    bool is_safe_request(int pid, const vector<int>& request) const {
        const auto& process = processes[pid];
        for (size_t i = 0; i < request.size(); ++i) {
            if (request[i] > process.remaining_need[i] || 
                request[i] > available_resources[i]) {
                return false;
            }
        }
        return check_system_safety(pid, request);
    }

    bool check_system_safety(int pid, vector<int> request) const {
        // Simplified safety check implementation
        auto temp_available = available_resources;
        auto temp_need = processes[pid].remaining_need;
        
        for (size_t i = 0; i < request.size(); ++i) {
            temp_available[i] -= request[i];
            temp_need[i] -= request[i];
        }

        vector<bool> finished(processes.size(), false);
        bool progress = true;

        while (progress) {
            progress = false;
            for (size_t i = 0; i < processes.size(); ++i) {
                if (!finished[i] && can_fulfill(processes[i].remaining_need, temp_available)) {
                    for (size_t j = 0; j < temp_available.size(); ++j) {
                        temp_available[j] += processes[i].allocated[j];
                    }
                    finished[i] = true;
                    progress = true;
                }
            }
        }

        for (bool f : finished) if (!f) return false;
        return true;
    }

    bool can_fulfill(const vector<int>& need, const vector<int>& available) const {
        for (size_t i = 0; i < need.size(); ++i) {
            if (need[i] > available[i]) return false;
        }
        return true;
    }

    void build_allocation_graph() {
        allocation_graph.clear();
        const int total_nodes = processes.size() + available_resources.size();
        allocation_graph.resize(total_nodes, vector<int>(total_nodes, 0));

        for (size_t p = 0; p < processes.size(); ++p) {
            for (size_t r = 0; r < available_resources.size(); ++r) {
                if (processes[p].allocated[r] > 0) {
                    allocation_graph[p][processes.size() + r] = 1;
                }
                if (processes[p].remaining_need[r] > 0) {
                    allocation_graph[processes.size() + r][p] = 1;
                }
            }
        }
    }

    void rebuild_graph_and_check() {
        build_allocation_graph();
        if (detect_cycles()) {
            recover_from_deadlock();
        }
    }

    bool detect_cycles() {
        vector<bool> visited(allocation_graph.size(), false);
        vector<bool> stack(allocation_graph.size(), false);

        for (size_t i = 0; i < allocation_graph.size(); ++i) {
            if (check_cycle_dfs(i, visited, stack)) {
                cout << "Deadlock detected in the system!\n";
                return true;
            }
        }
        return false;
    }

    bool check_cycle_dfs(int node, vector<bool>& visited, vector<bool>& stack) {
        if (!visited[node]) {
            visited[node] = true;
            stack[node] = true;

            for (size_t neighbor = 0; neighbor < allocation_graph[node].size(); ++neighbor) {
                if (allocation_graph[node][neighbor]) {
                    if (!visited[neighbor] && check_cycle_dfs(neighbor, visited, stack)) {
                        return true;
                    } else if (stack[neighbor]) {
                        return true;
                    }
                }
            }
        }
        stack[node] = false;
        return false;
    }

    void recover_from_deadlock() {
        cout << "Initiating recovery...\n";
        // Reset all allocations
        for (auto& process : processes) {
            for (size_t r = 0; r < available_resources.size(); ++r) {
                available_resources[r] += process.allocated[r];
                process.allocated[r] = 0;
                process.remaining_need[r] = process.max_need[r];
            }
        }
        build_allocation_graph();
    }

public:
    void display_state() const {
        cout << "\nCurrent System State:\n";
        cout << "Available resources: ";
        for (int res : available_resources) cout << res << " ";
        
        cout << "\nProcess States:\n";
        for (size_t i = 0; i < processes.size(); ++i) {
            cout << "Process " << i << " | Allocated: ";
            for (int a : processes[i].allocated) cout << a << " ";
            cout << "| Remaining Needs: ";
            for (int n : processes[i].remaining_need) cout << n << " ";
            cout << "\n";
        }
    }
};

int main() {
    DeadlockManager manager;
    manager.initialize();
    manager.display_state();

    string choice;
    do {
        int pid;
        vector<int> request;

        cout << "\nEnter process ID: ";
        cin >> pid;
        
        cout << "Enter resource request (space-separated values): ";
        int val;
        while (cin >> val) {
            request.push_back(val);
            if (cin.peek() == '\n') break;
        }

        manager.request_resources(pid, request);
        manager.display_state();

        cout << "\nMake another request? (y/n): ";
        cin >> choice;
    } while (choice == "y" || choice == "Y");

    return 0;
}
