import tkinter as tk
from tkinter import messagebox

class BankersGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banker's Algorithm Simulator")

        # Number of Processes and Resources input
        self.processes_label = tk.Label(root, text="Enter Number of Processes:")
        self.processes_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.processes_entry = tk.Entry(root)
        self.processes_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.resources_label = tk.Label(root, text="Enter Number of Resources:")
        self.resources_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.resources_entry = tk.Entry(root)
        self.resources_entry.grid(row=1, column=1, padx=10, pady=5)

        # Button to generate the matrices
        self.generate_button = tk.Button(root, text="Generate Matrices", command=self.generate_matrices)
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Step label for progress display
        self.step_label = tk.Label(root, text="Step-by-Step Progress:")
        self.step_label.grid(row=3, column=0, columnspan=2, pady=10)

    def generate_matrices(self):
        # Get the number of processes and resources
        try:
            self.processes = int(self.processes_entry.get())
            self.resources = int(self.resources_entry.get())
        except ValueError:
            # Handle non-integer input
            messagebox.showerror("Input Error", "Please enter valid integers for processes and resources.")
            return

        # Clear any previous matrices if they exist
        for widget in self.root.winfo_children():
            widget.grid_forget()

        # Create Allocation Frame
        alloc_frame = tk.LabelFrame(self.root, text="Allocation Matrix", padx=10, pady=10)
        alloc_frame.grid(row=4, column=0, padx=10, pady=10)

        # Create column headers for Allocation Matrix
        for j in range(self.resources):
            tk.Label(alloc_frame, text=chr(65 + j)).grid(row=0, column=j + 1)

        self.allocation_entries = []
        for i in range(self.processes):
            row_entries = []
            tk.Label(alloc_frame, text=f"P{i}").grid(row=i + 1, column=0)  # Process label
            for j in range(self.resources):
                entry = tk.Entry(alloc_frame, width=5)
                entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                row_entries.append(entry)
            self.allocation_entries.append(row_entries)

        # Create Max Frame
        max_frame = tk.LabelFrame(self.root, text="Maximum Matrix", padx=10, pady=10)
        max_frame.grid(row=4, column=1, padx=10, pady=10)

        # Create column headers for Maximum Matrix
        for j in range(self.resources):
            tk.Label(max_frame, text=chr(65 + j)).grid(row=0, column=j + 1)

        self.max_entries = []
        for i in range(self.processes):
            row_entries = []
            tk.Label(max_frame, text=f"P{i}").grid(row=i + 1, column=0)
            for j in range(self.resources):
                entry = tk.Entry(max_frame, width=5)
                entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                row_entries.append(entry)
            self.max_entries.append(row_entries)

        # Create Available Frame
        avail_frame = tk.LabelFrame(self.root, text="Available Resources", padx=10, pady=10)
        avail_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.available_entries = []
        for j in range(self.resources):
            tk.Label(avail_frame, text=chr(65 + j)).grid(row=0, column=j)
            entry = tk.Entry(avail_frame, width=5)
            entry.grid(row=1, column=j, padx=5, pady=5)
            self.available_entries.append(entry)

        # Run Button
        run_button = tk.Button(self.root, text="Run Banker's Algorithm", command=self.run_simulation)
        run_button.grid(row=6, column=0, columnspan=2, pady=10)

    def run_simulation(self):
        # Read the matrices from the input fields
        allocation = [[int(self.allocation_entries[i][j].get()) for j in range(self.resources)] for i in range(self.processes)]
        maximum = [[int(self.max_entries[i][j].get()) for j in range(self.resources)] for i in range(self.processes)]
        available = [int(self.available_entries[j].get()) for j in range(self.resources)]

        # Calculate the Need Matrix
        need = [[maximum[i][j] - allocation[i][j] for j in range(self.resources)] for i in range(self.processes)]

        # Initialize work and finish arrays
        work = available[:]
        finish = [False] * self.processes
        safe_sequence = []

        # Step-by-step progress display
        self.step_label.config(text="Step-by-Step Progress:")
        self.update_matrices(allocation, maximum, need, work, safe_sequence, step="Initial State")

        # Banker's Algorithm to check for safe state
        while len(safe_sequence) < self.processes:
            made_progress = False
            for i in range(self.processes):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(self.resources)):
                    # Process i can finish
                    safe_sequence.append(i)
                    finish[i] = True
                    # Update work by adding the allocation of the completed process
                    work = [work[j] + allocation[i][j] for j in range(self.resources)]
                    made_progress = True
                    self.update_matrices(allocation, maximum, need, work, safe_sequence, step=f"Process P{i} finishes")
                    break
            
            if not made_progress:
                # If no progress is made, the system is in an unsafe state
                messagebox.showinfo("Result", "The system is in an unsafe state!")
                return
        
        # If we get here, the system is in a safe state
        messagebox.showinfo("Result", f"The system is in a safe state! Safe sequence: {safe_sequence}")

    def update_matrices(self, allocation, maximum, need, work, safe_sequence, step):
        """
        Function to update the matrices and display them along with the step in Banker's Algorithm
        """
        # Clear the previous matrices and update the label
        self.step_label.config(text=f"Step-by-Step Progress: {step}")

        # Recreate the Allocation Matrix
        alloc_frame = tk.LabelFrame(self.root, text="Allocation Matrix", padx=10, pady=10)
        alloc_frame.grid(row=7, column=0, padx=10, pady=10)

        for j in range(self.resources):
            tk.Label(alloc_frame, text=chr(65 + j)).grid(row=0, column=j + 1)

        for i in range(self.processes):
            tk.Label(alloc_frame, text=f"P{i}").grid(row=i + 1, column=0)
            for j in range(self.resources):
                tk.Label(alloc_frame, text=str(allocation[i][j])).grid(row=i + 1, column=j + 1)

        # Recreate the Max Matrix
        max_frame = tk.LabelFrame(self.root, text="Maximum Matrix", padx=10, pady=10)
        max_frame.grid(row=7, column=1, padx=10, pady=10)

        for j in range(self.resources):
            tk.Label(max_frame, text=chr(65 + j)).grid(row=0, column=j + 1)

        for i in range(self.processes):
            tk.Label(max_frame, text=f"P{i}").grid(row=i + 1, column=0)
            for j in range(self.resources):
                tk.Label(max_frame, text=str(maximum[i][j])).grid(row=i + 1, column=j + 1)

        # Recreate the Need Matrix
        need_frame = tk.LabelFrame(self.root, text="Need Matrix", padx=10, pady=10)
        need_frame.grid(row=8, column=0, padx=10, pady=10)

        for j in range(self.resources):
            tk.Label(need_frame, text=chr(65 + j)).grid(row=0, column=j + 1)

        for i in range(self.processes):
            tk.Label(need_frame, text=f"P{i}").grid(row=i + 1, column=0)
            for j in range(self.resources):
                tk.Label(need_frame, text=str(need[i][j])).grid(row=i + 1, column=j + 1)

        # Work Vector display
        work_frame = tk.LabelFrame(self.root, text="Work Vector", padx=10, pady=10)
        work_frame.grid(row=9, column=0, columnspan=2, pady=10)
        
        tk.Label(work_frame, text="Work = ").grid(row=0, column=0)
        tk.Label(work_frame, text=str(work)).grid(row=0, column=1)

        # Safe Sequence Display
        safe_frame = tk.LabelFrame(self.root, text="Safe Sequence", padx=10, pady=10)
        safe_frame.grid(row=10, column=0, columnspan=2, pady=10)
        
        tk.Label(safe_frame, text="Safe Sequence = ").grid(row=0, column=0)
        tk.Label(safe_frame, text=str(safe_sequence)).grid(row=0, column=1)

root = tk.Tk()
app = BankersGUI(root)
root.mainloop()
