# Copyright (C) 2025 UDHAYA046
# This program is licensed under GPLv3. See LICENSE file for details.
# Unauthorized use without preserving this notice is a license violation.


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import warnings

# Suppress specific warning related to missing glyph in the font
warnings.filterwarnings("ignore", message="Glyph 9989")

# ---------------------- USER INPUT SECTION ---------------------- #

n = int(input("Enter the number of processes: "))
m = int(input("Enter the number of resource types: "))

print("\nEnter the Allocation matrix (space separated values row-wise):")
allocation = []
for i in range(n):
    row = list(map(int, input(f"Allocation for P{i}: ").strip().split()))
    if len(row) != m:
        raise ValueError("Incorrect number of resource types.")
    allocation.append(row)

print("\nEnter the Max matrix (space separated values row-wise):")
max_demand = []
for i in range(n):
    row = list(map(int, input(f"Max for P{i}: ").strip().split()))
    if len(row) != m:
        raise ValueError("Incorrect number of resource types.")
    max_demand.append(row)

available = list(map(int, input("\nEnter Available resources (space separated): ").strip().split()))
if len(available) != m:
    raise ValueError("Incorrect number of resource types.")

processes = [f'P{i}' for i in range(n)]

# ---------------------- ALGORITHM SECTION ---------------------- #

def calculate_need(max_demand, allocation):
    return [[max_demand[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

def bankers_algorithm(allocation, max_demand, available):
    need = calculate_need(max_demand, allocation)
    work = available[:]
    finish = [False] * n
    safe_sequence = []

    while len(safe_sequence) < n:
        allocated = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                safe_sequence.append(i)
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                allocated = True
                break
        if not allocated:
            return False, []
    return True, safe_sequence

safe, sequence = bankers_algorithm(allocation, max_demand, available)
if not safe:
    print("\n🔴 System is NOT in a safe state.")
    exit()
else:
    print("\n🟢 System is in a safe state.")
    print("Safe Sequence:", ' -> '.join([f'P{i}' for i in sequence]))

# ---------------------- VISUALIZATION SECTION ---------------------- #

# Create a larger figure and adjust the size of the bars
fig, ax = plt.subplots(figsize=(12, 6))  # Larger figure for visibility
plt.title("Banker's Algorithm Safe Sequence Simulation", fontsize=14)

# Initialize bars for processes (thicker bars and more visible)
bars = ax.bar(processes, [0.1] * n, color='blue', width=0.6)  # Initial height set to a small value (0.1)

# Set up the text elements for available resources and status
status_text = ax.text(0.5, 1.15, '', ha='center', transform=ax.transAxes, fontsize=14)  # Move up
available_text = ax.text(0.5, -0.2, '', ha='center', transform=ax.transAxes, fontsize=12)  # Move down

current_available = available[:]

# Set proper y-axis limits for visibility
ax.set_ylim(0, 1)  # Set y-axis to ensure bars can be seen

# Update function for animation
def update(frame):
    for bar in bars:
        bar.set_color('blue')  # Reset all bars to blue

    if frame < len(sequence):
        pid = sequence[frame]
        bars[pid].set_color('green')  # Highlight the bar for the current process in green

        status_text.set_text(f'Executing Process P{pid}')
        
        # Update available resources after process execution
        global current_available
        for j in range(m):
            current_available[j] += allocation[pid][j]

        available_text.set_text(f'Available: {current_available}')
    else:
        status_text.set_text('Safe Sequence Completed ✅')
        available_text.set_text(f'Final Available: {current_available}')

# Create animation with proper frame updates
ani = animation.FuncAnimation(fig, update, frames=len(sequence) + 1, interval=1500, repeat=False)

# Adjust layout to avoid overlap
plt.tight_layout(pad=5.0)  # Adjust padding for better spacing

plt.show()
