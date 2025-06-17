import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import json
import os

DATA_FILE = "banker_data.json"

class BankersAlgorithmGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Banker's Algorithm Simulator")

        self.num_processes = 5
        self.num_resources = 3

        self.allocation_entries = []
        self.max_entries = []
        self.available_entries = []

        self.create_main_layout()
        self.create_matrix_inputs()

    def create_main_layout(self):
        # Input for num processes/resources
        top_frame = tk.Frame(self.master)
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Processes:").grid(row=0, column=0)
        self.proc_entry = tk.Entry(top_frame, width=5)
        self.proc_entry.insert(0, "5")
        self.proc_entry.grid(row=0, column=1)

        tk.Label(top_frame, text="Resources:").grid(row=0, column=2)
        self.res_entry = tk.Entry(top_frame, width=5)
        self.res_entry.insert(0, "3")
        self.res_entry.grid(row=0, column=3)

        update_btn = tk.Button(top_frame, text="Update Matrix", command=self.update_matrix)
        update_btn.grid(row=0, column=4, padx=10)

        # Matrix frame
        self.matrix_frame = tk.Frame(self.master)
        self.matrix_frame.pack()

        # Button frame
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Run Banker's Algorithm", command=self.run_thread).pack(side='left', padx=5)
        tk.Button(button_frame, text="Save Dataset", command=self.save_data).pack(side='left', padx=5)
        tk.Button(button_frame, text="Reset", command=self.reset_fields).pack(side='left', padx=5)

        self.dataset_var = tk.StringVar()
        self.dataset_var.set("Select Dataset")

        self.dropdown = tk.OptionMenu(button_frame, self.dataset_var, "Select Dataset")
        self.dropdown.pack(side='left', padx=5)
        tk.Button(button_frame, text="Load", command=self.load_data).pack(side='left', padx=5)

        # Output display
        self.safe_sequence_label = tk.Label(self.master, text="", font=("Arial", 12), fg="blue")
        self.safe_sequence_label.pack(pady=5)

        self.finished_frame = tk.Frame(self.master)
        self.finished_frame.pack()

    def create_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.allocation_entries = []
        self.max_entries = []
        self.available_entries = []

        tk.Label(self.matrix_frame, text="Allocation Matrix", font=("Arial", 10, "bold")).grid(row=0, column=0)
        tk.Label(self.matrix_frame, text="Maximum Matrix", font=("Arial", 10, "bold")).grid(row=0, column=1)

        alloc_frame = tk.Frame(self.matrix_frame)
        alloc_frame.grid(row=1, column=0, padx=10)
        max_frame = tk.Frame(self.matrix_frame)
        max_frame.grid(row=1, column=1, padx=10)

        for i in range(self.num_processes):
            row_alloc = []
            row_max = []
            for j in range(self.num_resources):
                e1 = tk.Entry(alloc_frame, width=5, justify='center')
                e1.grid(row=i, column=j, padx=2, pady=2)
                row_alloc.append(e1)

                e2 = tk.Entry(max_frame, width=5, justify='center')
                e2.grid(row=i, column=j, padx=2, pady=2)
                row_max.append(e2)

            self.allocation_entries.append(row_alloc)
            self.max_entries.append(row_max)

        # Available resources
        tk.Label(self.matrix_frame, text="Available Resources", font=("Arial", 10)).grid(row=2, column=0, columnspan=2)
        avail_frame = tk.Frame(self.matrix_frame)
        avail_frame.grid(row=3, column=0, columnspan=2)

        for i in range(self.num_resources):
            e = tk.Entry(avail_frame, width=5, justify='center')
            e.grid(row=0, column=i, padx=2, pady=2)
            self.available_entries.append(e)

    def update_matrix(self):
        try:
            self.num_processes = int(self.proc_entry.get())
            self.num_resources = int(self.res_entry.get())
            if self.num_processes <= 0 or self.num_resources <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter positive integers for processes and resources.")
            return

        self.create_matrix_inputs()

    def run_thread(self):
        for widget in self.finished_frame.winfo_children():
            widget.destroy()
        self.safe_sequence_label.config(text="")
        threading.Thread(target=self.run_simulation).start()

    def run_simulation(self):
        try:
            alloc = [[int(e.get()) for e in row] for row in self.allocation_entries]
            maxm = [[int(e.get()) for e in row] for row in self.max_entries]
            avail = [int(e.get()) for e in self.available_entries]
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")
            return

        need = [[maxm[i][j] - alloc[i][j] for j in range(self.num_resources)] for i in range(self.num_processes)]
        finish = [False] * self.num_processes
        sequence = []

        while len(sequence) < self.num_processes:
            allocated = False
            for i in range(self.num_processes):
                if not finish[i] and all(need[i][j] <= avail[j] for j in range(self.num_resources)):
                    for j in range(self.num_resources):
                        avail[j] += alloc[i][j]
                    finish[i] = True
                    sequence.append(i)
                    allocated = True
                    break
            if not allocated:
                messagebox.showerror("Deadlock", "The system is not in a safe state.")
                return

        self.master.after(0, lambda: self.display_sequence(sequence))

    def display_sequence(self, sequence):
        self.safe_sequence_label.config(text="\u2705 Safe sequence: " + " → ".join([f"P{p}" for p in sequence]))
        self.animate_safe_sequence(sequence)

    def animate_safe_sequence(self, sequence, index=0):
        if index < len(sequence):
            p = sequence[index]
            label = tk.Label(self.finished_frame, text=f"P{p} Finished", bg="lightgreen", font=("Arial", 10), width=20)
            label.pack(pady=2)
            self.master.after(1000, lambda: self.animate_safe_sequence(sequence, index + 1))

    def reset_fields(self):
        for row in self.allocation_entries + self.max_entries:
            for e in row:
                e.delete(0, tk.END)
        for e in self.available_entries:
            e.delete(0, tk.END)
        self.safe_sequence_label.config(text="")
        for widget in self.finished_frame.winfo_children():
            widget.destroy()

    def save_data(self):
        name = simpledialog.askstring("Save Dataset", "Enter dataset name:")
        if not name:
            return

        try:
            alloc = [[int(e.get()) for e in row] for row in self.allocation_entries]
            maxm = [[int(e.get()) for e in row] for row in self.max_entries]
            avail = [int(e.get()) for e in self.available_entries]
        except ValueError:
            messagebox.showerror("Input Error", "All fields must contain valid integers.")
            return

        data = {
            "num_processes": self.num_processes,
            "num_resources": self.num_resources,
            "allocation": alloc,
            "maximum": maxm,
            "available": avail
        }

        all_data = {}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                all_data = json.load(f)

        all_data[name] = data
        with open(DATA_FILE, "w") as f:
            json.dump(all_data, f, indent=2)

        self.refresh_dataset_list()
        messagebox.showinfo("Saved", f"Dataset '{name}' saved successfully.")

    def refresh_dataset_list(self):
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)
        menu = self.dropdown["menu"]
        menu.delete(0, "end")
        for key in all_data:
            menu.add_command(label=key, command=lambda value=key: self.dataset_var.set(value))

    def load_data(self):
        name = self.dataset_var.get()
        if name == "Select Dataset":
            return

        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)

        data = all_data.get(name)
        if not data:
            return

        self.num_processes = data["num_processes"]
        self.num_resources = data["num_resources"]
        self.proc_entry.delete(0, tk.END)
        self.proc_entry.insert(0, str(self.num_processes))
        self.res_entry.delete(0, tk.END)
        self.res_entry.insert(0, str(self.num_resources))
        self.create_matrix_inputs()

        for i in range(self.num_processes):
            for j in range(self.num_resources):
                self.allocation_entries[i][j].delete(0, tk.END)
                self.allocation_entries[i][j].insert(0, data["allocation"][i][j])

                self.max_entries[i][j].delete(0, tk.END)
                self.max_entries[i][j].insert(0, data["maximum"][i][j])

        for j in range(self.num_resources):
            self.available_entries[j].delete(0, tk.END)
            self.available_entries[j].insert(0, data["available"][j])

if __name__ == "__main__":
    root = tk.Tk()
    app = BankersAlgorithmGUI(root)
    app.refresh_dataset_list()
    root.mainloop()
