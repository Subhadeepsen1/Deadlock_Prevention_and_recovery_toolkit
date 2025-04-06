def bankers_algorithm(allocation, need, available):
    num_processes, num_resources = need.shape
    work = available.copy()
    finish = [False] * num_processes
    safe_sequence = []

    while len(safe_sequence) < num_processes:
        found = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                work += allocation[i]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            return None
    return safe_sequence