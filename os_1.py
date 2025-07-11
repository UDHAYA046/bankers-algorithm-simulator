# Copyright (C) 2025 UDHAYA046
# This program is licensed under GPLv3. See LICENSE file for details.
# Unauthorized use without preserving this notice is a license violation.


def get_matrix_input(rows, cols, name):
    print(f"\nEnter the {name} matrix values row-wise (space-separated):")
    matrix = []
    for i in range(rows):
        while True:
            try:
                row = list(map(int, input(f"{name}[{i}]: ").strip().split()))
                if len(row) != cols:
                    raise ValueError
                matrix.append(row)
                break
            except ValueError:
                print(f"Please enter exactly {cols} integers.")
    return matrix

def is_safe_state(processes, avail, max_demand, allocation):
    n = len(processes)
    m = len(avail)
    need = [[max_demand[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    finish = [False] * n
    safe_seq = []
    work = avail[:]

    while len(safe_seq) < n:
        allocated = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                safe_seq.append(processes[i])
                finish[i] = True
                allocated = True
        if not allocated:
            return False, []
    return True, safe_seq

def main():
    print("=== Banker's Algorithm Simulator ===")

    n = int(input("Enter the number of processes: "))
    m = int(input("Enter the number of resource types: "))

    processes = list(range(n))

    allocation = get_matrix_input(n, m, "Allocation")
    max_demand = get_matrix_input(n, m, "Max")
    
    while True:
        try:
            available = list(map(int, input(f"\nEnter Available resources (space-separated, {m} values): ").strip().split()))
            if len(available) != m:
                raise ValueError
            break
        except ValueError:
            print(f"Please enter exactly {m} integers.")

    safe, sequence = is_safe_state(processes, available, max_demand, allocation)
    
    print("\n=== Results ===")
    if safe:
        print("System is in a SAFE state.")
        print("Safe sequence:", ' -> '.join([f'P{p}' for p in sequence]))
    else:
        print("System is NOT in a safe state (Deadlock possibility).")

if __name__ == "__main__":
    main()
