import tkinter as tk
from tkinter import messagebox
import threading

class BankersAlgorithmGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Banker's Algorithm Simulator")

        self.num_processes = 5
        self.num_resources = 3

        self.create_widgets()

    def create_widgets(self):
        self.allocation_entries = []
        self.max_entries = []

        tk.Label(self.master, text="Allocation Matrix", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.master, text="Maximum Matrix", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10, pady=5)

        allocation_frame = tk.Frame(self.master)
        allocation_frame.grid(row=1, column=0, padx=10)
        max_frame = tk.Frame(self.master)
        max_frame.grid(row=1, column=1, padx=10)

        for i in range(self.num_processes):
            row_entries_alloc = []
            row_entries_max = []
            for j in range(self.num_resources):
                entry_alloc = tk.Entry(allocation_frame, width=5, justify='center')
                entry_alloc.grid(row=i, column=j, padx=2, pady=2)
                row_entries_alloc.append(entry_alloc)

                entry_max = tk.Entry(max_frame, width=5, justify='center')
                entry_max.grid(row=i, column=j, padx=2, pady=2)
                row_entries_max.append(entry_max)
            self.allocation_entries.append(row_entries_alloc)
            self.max_entries.append(row_entries_max)

        tk.Label(self.master, text="Available Resources", font=("Arial", 10)).grid(row=2, column=0, columnspan=2)
        self.available_entries = []
        available_frame = tk.Frame(self.master)
        available_frame.grid(row=3, column=0, columnspan=2)
        for i in range(self.num_resources):
            entry = tk.Entry(available_frame, width=5, justify='center')
            entry.grid(row=0, column=i, padx=2, pady=2)
            self.available_entries.append(entry)

        self.run_button = tk.Button(self.master, text="Run Banker's Algorithm", command=self.run_thread)
        self.run_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.safe_sequence_label = tk.Label(self.master, text="", font=("Arial", 12), fg="blue")
        self.safe_sequence_label.grid(row=5, column=0, columnspan=2)

        self.finished_frame = tk.Frame(self.master)
        self.finished_frame.grid(row=6, column=0, columnspan=2, pady=5)

    def run_thread(self):
        for widget in self.finished_frame.winfo_children():
            widget.destroy()
        self.safe_sequence_label.config(text="")
        threading.Thread(target=self.run_simulation).start()

    def run_simulation(self):
        try:
            allocation = [[int(entry.get()) for entry in row] for row in self.allocation_entries]
            maximum = [[int(entry.get()) for entry in row] for row in self.max_entries]
            available = [int(entry.get()) for entry in self.available_entries]
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers in all fields.")
            return

        need = [[maximum[i][j] - allocation[i][j] for j in range(self.num_resources)] for i in range(self.num_processes)]

        finish = [False] * self.num_processes
        safe_sequence = []

        while len(safe_sequence) < self.num_processes:
            allocated_in_this_round = False
            for i in range(self.num_processes):
                if not finish[i] and all(need[i][j] <= available[j] for j in range(self.num_resources)):
                    for j in range(self.num_resources):
                        available[j] += allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(i)
                    allocated_in_this_round = True
                    break
            if not allocated_in_this_round:
                messagebox.showerror("Deadlock Detected", "The system is not in a safe state!")
                return

        self.master.after(0, lambda: self.display_sequence(safe_sequence))

    def display_sequence(self, sequence):
        self.safe_sequence_label.config(text="\u2705 Safe sequence found: " + " -> ".join([f"P{p}" for p in sequence]))
        self.animate_safe_sequence(sequence)

    def animate_safe_sequence(self, sequence, index=0):
        if index < len(sequence):
            process = sequence[index]
            label = tk.Label(self.finished_frame, text=f"P{process}: Finished", bg="lightgreen", font=("Arial", 10), width=20)
            label.pack(pady=2)
            self.master.after(1000, lambda: self.animate_safe_sequence(sequence, index + 1))

if __name__ == "__main__":
    root = tk.Tk()
    app = BankersAlgorithmGUI(root)
    root.mainloop()
