from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit,
    QGridLayout, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import numpy as np
from algorithm import bankers_algorithm
from graph import show_resource_allocation_graph

class DeadlockToolkit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deadlock Prevention and Recovery Toolkit")
        self.setGeometry(100, 100, 1200, 750)
        self.setStyleSheet("background-color: #F8F9F9;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("🔄 Deadlock Prevention & Recovery Toolkit")
        self.title_label.setFont(QFont("Arial", 22, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #154360; padding: 10px;")
        layout.addWidget(self.title_label)

        grid_layout = QGridLayout()

        self.process_label = QLabel("Number of Processes:")
        self.process_entry = QLineEdit()
        grid_layout.addWidget(self.process_label, 0, 0)
        grid_layout.addWidget(self.process_entry, 0, 1)

        self.resource_label = QLabel("Number of Resources:")
        self.resource_entry = QLineEdit()
        grid_layout.addWidget(self.resource_label, 1, 0)
        grid_layout.addWidget(self.resource_entry, 1, 1)

        self.submit_button = QPushButton("Generate Table")
        self.submit_button.setStyleSheet("background-color: #3498DB; color: white; padding: 7px; border-radius: 5px;")
        self.submit_button.clicked.connect(self.generate_table)
        grid_layout.addWidget(self.submit_button, 2, 0, 1, 2)

        layout.addLayout(grid_layout)

        self.matrix_table = QTableWidget()
        self.matrix_table.setStyleSheet("background-color: white;")
        layout.addWidget(self.matrix_table)

        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("padding: 10px;")
        layout.addWidget(self.result_label)

        self.check_button = QPushButton("Analyze Deadlock")
        self.check_button.setStyleSheet("background-color: #2ECC71; color: white; padding: 7px; border-radius: 5px;")
        self.check_button.clicked.connect(self.analyze_deadlock)
        layout.addWidget(self.check_button)

        self.graph_button = QPushButton("Show Resource Allocation Graph")
        self.graph_button.setStyleSheet("background-color: #F39C12; color: white; padding: 7px; border-radius: 5px;")
        self.graph_button.clicked.connect(self.display_graph)
        layout.addWidget(self.graph_button)

        self.setLayout(layout)

    def generate_table(self):
        try:
            self.processes = int(self.process_entry.text())
            self.resources = int(self.resource_entry.text())
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid integers.")
            return

        self.matrix_table.setRowCount(self.processes * 3 + 1)
        self.matrix_table.setColumnCount(self.resources + 1)

        headers = ["P/R"] + [f"R{j}" for j in range(self.resources)]
        self.matrix_table.setHorizontalHeaderLabels(headers)

        for i in range(self.processes):
            self.matrix_table.setItem(i * 3, 0, QTableWidgetItem(f"P{i} Allocation"))
            self.matrix_table.setItem(i * 3 + 1, 0, QTableWidgetItem(f"P{i} Max"))
            self.matrix_table.setItem(i * 3 + 2, 0, QTableWidgetItem(f"P{i} Need"))
            for j in range(1, self.resources + 1):
                self.matrix_table.setItem(i * 3, j, QTableWidgetItem("0"))
                self.matrix_table.setItem(i * 3 + 1, j, QTableWidgetItem("0"))
                self.matrix_table.setItem(i * 3 + 2, j, QTableWidgetItem("0"))

        self.matrix_table.setItem(self.processes * 3, 0, QTableWidgetItem("Available"))
        for j in range(1, self.resources + 1):
            self.matrix_table.setItem(self.processes * 3, j, QTableWidgetItem("0"))

        self.matrix_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def analyze_deadlock(self):
        try:
            processes = self.processes
            resources = self.resources
            allocation = np.zeros((processes, resources), dtype=int)
            max_need = np.zeros((processes, resources), dtype=int)
            available = np.zeros(resources, dtype=int)

            for i in range(processes):
                for j in range(resources):
                    allocation[i][j] = int(self.matrix_table.item(i * 3, j + 1).text())
                    max_need[i][j] = int(self.matrix_table.item(i * 3 + 1, j + 1).text())
            for j in range(resources):
                available[j] = int(self.matrix_table.item(processes * 3, j + 1).text())

            need = max_need - allocation
            safe_sequence = bankers_algorithm(allocation, need, available)

            if safe_sequence:
                self.result_label.setText(f"✅ Safe Sequence: {' → '.join(f'P{p}' for p in safe_sequence)}")
                self.result_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.result_label.setText("❌ No Safe Sequence Found (System in Deadlock!)")
                self.result_label.setStyleSheet("color: red; font-weight: bold;")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_graph(self):
        show_resource_allocation_graph(self)