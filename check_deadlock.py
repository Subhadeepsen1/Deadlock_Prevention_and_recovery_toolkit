def check_deadlock(self):
    try:
        processes = self.processes
        resources = self.resources

        allocation = np.zeros((processes, resources), dtype=int)
        max_need = np.zeros((processes, resources), dtype=int)
        available = np.zeros(resources, dtype=int)

        # Extract allocation and max matrices
        for i in range(processes):
            for j in range(resources):
                allocation[i][j] = int(self.matrix_table.item(i * 3, j + 1).text())
                max_need[i][j] = int(self.matrix_table.item(i * 3 + 1, j + 1).text())

        # Extract available resources
        for j in range(resources):
            available[j] = int(self.matrix_table.item(processes * 3, j + 1).text())

        # Compute Need matrix
        need = max_need - allocation

        # Run Banker's Algorithm
        safe_sequence = self.bankers_algorithm(allocation, need, available)

        if safe_sequence:
            self.result_label.setText(f"✅ Safe Sequence: {' → '.join(f'P{p}' for p in safe_sequence)}")
            self.result_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.result_label.setText("❌ No Safe Sequence Found (System in Deadlock!)")
            self.result_label.setStyleSheet("color: red; font-weight: bold;")

    except ValueError:
        QMessageBox.critical(self, "Error", "Invalid matrix values. Please enter only numbers.")
