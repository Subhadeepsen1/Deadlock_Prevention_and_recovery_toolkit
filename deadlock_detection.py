import numpy as np


class DeadlockDetection:
    def __init__(self):
        # Example input data
        self.allocation = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1], [0, 0, 2]])
        self.request = np.array([[0, 0, 0], [2, 0, 2], [0, 0, 0], [1, 0, 0], [0, 0, 2]])
        self.available = np.array([1, 1, 0])

    def run(self):
        deadlocked_processes = self.detect_deadlock()
        if deadlocked_processes:
            return f"Deadlock detected! Affected processes: {deadlocked_processes}"
        else:
            return "No deadlock detected."

    def detect_deadlock(self):
        n, m = self.allocation.shape
        work = np.copy(self.available)
        finish = np.zeros(n, dtype=bool)
        deadlocked_processes = []

        while True:
            allocated = False
            for i in range(n):
                if not finish[i] and all(self.request[i] <= work):
                    work += self.allocation[i]
                    finish[i] = True
                    allocated = True

            if not allocated:
                break

        for i in range(n):
            if not finish[i]:
                deadlocked_processes.append(i)

        return deadlocked_processes


if __name__ == "__main__":
    result = DeadlockDetection().run()
    print(result)
