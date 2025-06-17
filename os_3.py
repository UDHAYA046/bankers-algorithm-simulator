import tkinter as tk
from tkinter import messagebox
import time
import threading

class BankersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banker's Algorithm Simulator")

        self.entries = []
        self.process_labels = []
        self.step_text = tk.StringVar()

        self.setup_inputs()

    def setup_inputs(self):
        tk.Label(self.root, text="Number of Processes:").grid(row=0, column=0)
        self.num_processes_entry = tk.Entry(self.root)
        self.num_processes_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Number of Resources:").grid(row=1, column=0)
        self.num_resources_entry = tk.Entry(self.root)
        self.num_resources_entry.grid(row=1, column=1)

        tk.Button(self.root, text="Submit", command=self.create_matrix_inputs).grid(row=2, column=0, columnspan=2)

    def create_matrix_inputs(self):
        try:
            self.n = int(self.num_processes_entry.get())
            self.m = int(self.num_resources_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")
            return

        self.clear_widgets(from_row=3)

        self.allocation_entries = []
        self.max_entries = []
        self.available_entries = []

        tk.Label(self.root, text="Allocation Matrix").grid(row=3, column=0)
        tk.Label(self.root, text="Max Matrix").grid(row=3, column=1)

        for i in range(self.n):
            alloc_row = []
            max_row = []
            for j in range(self.m):
                alloc_entry = tk.Entry(self.root, width=4)
                alloc_entry.grid(row=4 + i, column=j)
                alloc_row.append(alloc_entry)

                max_entry = tk.Entry(self.root, width=4)
                max_entry.grid(row=4 + i, column=j + self.m + 1)
                max_row.append(max_entry)

            self.allocation_entries.append(alloc_row)
            self.max_entries.append(max_row)

        tk.Label(self.root, text="Available Resources:").grid(row=5 + self.n, column=0)
        for j in range(self.m):
            avail_entry = tk.Entry(self.root, width=4)
            avail_entry.grid(row=5 + self.n, column=1 + j)
            self.available_entries.append(avail_entry)

        tk.Button(self.root, text="Run Banker's Algorithm", command=self.run_simulation_thread).grid(row=6 + self.n, column=0, columnspan=2)

        self.step_label = tk.Label(self.root, textvariable=self.step_text, font=("Arial", 12), fg="blue")
        self.step_label.grid(row=7 + self.n, column=0, columnspan=5)

    def clear_widgets(self, from_row):
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) >= from_row:
                widget.destroy()

    def run_simulation_thread(self):
        thread = threading.Thread(target=self.run_simulation)
        thread.start()

    def run_simulation(self):
        allocation = [[int(entry.get()) for entry in row] for row in self.allocation_entries]
        max_demand = [[int(entry.get()) for entry in row] for row in self.max_entries]
        available = [int(entry.get()) for entry in self.available_entries]

        need = [[max_demand[i][j] - allocation[i][j] for j in range(self.m)] for i in range(self.n)]
        finish = [False] * self.n
        safe_sequence = []

        for lbl in self.process_labels:
            lbl.destroy()
        self.process_labels.clear()

        row_offset = 8 + self.n
        for i in range(self.n):
            lbl = tk.Label(self.root, text=f"P{i}: Waiting", font=("Arial", 10), bg="lightgray", width=20)
            lbl.grid(row=row_offset + i, column=0, columnspan=3, pady=2)
            self.process_labels.append(lbl)

        while len(safe_sequence) < self.n:
            executed = False
            for i in range(self.n):
                if not finish[i] and all(need[i][j] <= available[j] for j in range(self.m)):
                    self.step_text.set(f"🔄 Executing Process P{i}")
                    self.update_process_label(i, "Executing", "yellow")
                    self.root.update()
                    time.sleep(1)

                    for j in range(self.m):
                        available[j] += allocation[i][j]

                    finish[i] = True
                    safe_sequence.append(i)
                    self.update_process_label(i, "Finished", "lightgreen")
                    self.step_text.set(f"✅ Process P{i} completed. Available: {available}")
                    self.root.update()
                    time.sleep(1)
                    executed = True
                    break

            if not executed:
                self.step_text.set("❌ No safe sequence found. System is in deadlock.")
                self.root.update()
                return

        self.step_text.set(f"✅ Safe sequence found: {' -> '.join(['P'+str(p) for p in safe_sequence])}")

    def update_process_label(self, index, state, color):
        self.process_labels[index].config(text=f"P{index}: {state}", bg=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = BankersGUI(root)
    root.mainloop()
