import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit,
    QGridLayout, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class DeadlockToolkit(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deadlock Prevention and Recovery Toolkit")
        self.setGeometry(100, 100, 1200, 750)
        self.setStyleSheet("background-color: #F8F9F9;")
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.title_label = QLabel("🔄 Deadlock Prevention & Recovery Toolkit", self)
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
        self.submit_button.clicked.connect(self.get_input)
        grid_layout.addWidget(self.submit_button, 2, 0, 1, 2)
        
        layout.addLayout(grid_layout)
        
        self.matrix_table = QTableWidget()
        self.matrix_table.setStyleSheet("background-color: white;")
        layout.addWidget(self.matrix_table)
        
        self.result_label = QLabel("", self)
        self.result_label.setFont(QFont("Arial", 14))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("padding: 10px;")
        layout.addWidget(self.result_label)
        
        self.check_button = QPushButton("Analyze Deadlock")
        self.check_button.setStyleSheet("background-color: #2ECC71; color: white; padding: 7px; border-radius: 5px;")
        self.check_button.clicked.connect(self.check_deadlock)
        layout.addWidget(self.check_button)
        
        self.graph_button = QPushButton("Show Resource Allocation Graph")
        self.graph_button.setStyleSheet("background-color: #F39C12; color: white; padding: 7px; border-radius: 5px;")
        self.graph_button.clicked.connect(self.show_graph)
        layout.addWidget(self.graph_button)
        
        self.setLayout(layout)
    
    def get_input(self):
        try:
            self.processes = int(self.process_entry.text())
            self.resources = int(self.resource_entry.text())
            self.create_matrix_input()
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid numbers")
    
    def create_matrix_input(self):
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
    
    def check_deadlock(self):
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
            safe_sequence = self.bankers_algorithm(allocation, need, available)

            if safe_sequence:
                self.result_label.setText(f"✅ Safe Sequence: {' → '.join(f'P{p}' for p in safe_sequence)}")
                self.result_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.result_label.setText("❌ No Safe Sequence Found (System in Deadlock!)")
                self.result_label.setStyleSheet("color: red; font-weight: bold;")

        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid matrix values. Please enter only numbers.")
    
    def bankers_algorithm(self, allocation, need, available):
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
    
    def show_graph(self):
        G = nx.DiGraph()

        for i in range(self.processes):
            G.add_node(f"P{i}", color='blue')
        for j in range(self.resources):
            G.add_node(f"R{j}", color='red')

        allocation_edges = []
        request_edges = []

        for i in range(self.processes):
            for j in range(self.resources):
                allocated = int(self.matrix_table.item(i * 3, j + 1).text())
                requested = int(self.matrix_table.item(i * 3 + 2, j + 1).text())

                if allocated > 0:
                    allocation_edges.append((f"R{j}", f"P{i}"))
                if requested > 0:
                    request_edges.append((f"P{i}", f"R{j}"))

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color=['blue' if node.startswith('P') else 'red' for node in G.nodes()])
        nx.draw_networkx_edges(G, pos, edgelist=allocation_edges, edge_color="green", arrowstyle="->", width=2)
        nx.draw_networkx_edges(G, pos, edgelist=request_edges, edge_color="orange", arrowstyle="->", width=2, style="dashed")
        plt.title("Resource Allocation Graph\n(Green: Allocated, Orange: Requested)")
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeadlockToolkit()
    window.show()
    sys.exit(app.exec_())
