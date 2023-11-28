import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Process:
    # Setting up all needed details about data
    def __init__(self, name, arrival, burst, priority):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.turnaround = 0
        self.waiting = 0
        self.start = 0
        self.finish = 0
        self.q = 0


def MLQ(processes):
    # Sort all process
    processes.sort(key=lambda p: p.arrival)
    high_queue = []  # Round robin with quantum = 3, and it's priority = 0
    medium_queue = []  # Shortest Reamining time with quantum = 2, and it's priority = 1
    low_queue = []  # Shortest Job First without quantum , and it's priority = 2
    # Init starting time
    time = 0
    # Current Proccess
    current = None
    while True:
        for p in processes:
            # Setting Arrival time = Process current Arrival
            if p.arrival == time:
                print(f"At t = {time}, {p.name} arrived the queue {p.priority}")
                if p.priority == 0:
                    high_queue.append(p)
                    p.q = 3
                elif p.priority == 1:
                    medium_queue.append(p)
                    p.q = 2
                else:
                    low_queue.append(p)
        # Checking that reamining = 0 to remove value 
        if current and current.remaining == 0:
            print(f"At t = {time}, {current.name} left the kernel and finished")
            current.finish = time
            current.turnaround = current.finish - current.arrival
            current.waiting = current.turnaround - current.burst
            current = None
        # For Shortest Job First
        if current and current.q == 0:
            print(
                f"At t = {time}, {current.name} left the kernel and entered the queue {current.priority}"
            )
            if current.priority == 0:
                current.q = 3
                high_queue.append(current)
            else:
                current.q = 2
                medium_queue.append(current)
            current = None
        # Then it's done
        if not current:
            if high_queue:
                current = high_queue.pop(0)
            elif medium_queue:
                medium_queue.sort(key=lambda p: p.remaining)
                current = medium_queue.pop(0)
            elif low_queue:
                low_queue.sort(key=lambda p: p.burst)
                current = low_queue.pop(0)
            else:
                break

            if current.start == -1:
                current.start = time
            print(f"At t = {time}, {current.name} entered the kernel")

        current.remaining -= 1
        current.q -= 1
        time += 1

    print_output(processes)
    display_output_page(processes)


def display_output_page(processes):
    output_window = tk.Toplevel(root)
    output_window.title("MLQ Scheduler Output")

    # Gantt Chart
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_title("Gantt Chart")
    for process in processes:
        ax.barh(
            process.name,
            process.finish - process.start,
            left=process.start,
            color="blue",
        )
    ax.set_xlabel("Time")
    ax.set_yticks(range(len(processes)))
    ax.set_yticklabels([process.name for process in processes])
    canvas = FigureCanvasTkAgg(fig, master=output_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def submit_process():
    name = name_entry.get()
    arrival = int(arrival_entry.get())
    burst = int(burst_entry.get())
    priority = int(priority_entry.get())
    process = Process(name, arrival, burst, priority)
    processes.append(process)
    update_table()


def update_table():
    table.delete(*table.get_children())
    for process in processes:
        table.insert(
            "",
            "end",
            values=(process.name, process.arrival, process.burst, process.priority),
        )


def print_output(processes):
    # Total summation of watiting times
    total_waiting = sum(p.waiting for p in processes)
    # Divided by number of processes
    average_waiting = total_waiting / len(processes)
    data = {
        "Process": [p.name for p in processes],
        "Turnaround Time": [p.turnaround for p in processes],
        "Waiting Time": [p.waiting for p in processes],
    }
    # Calculating Average
    df = pd.DataFrame(data)
    print("Average Waiting Time: {:.4f}".format(average_waiting))


# Initialize the processes list globally
processes = []

# GUI setup
root = tk.Tk()
root.title("MLQ Scheduler")

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

name_label = tk.Label(input_frame, text="Process Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

arrival_label = tk.Label(input_frame, text="Arrival Time:")
arrival_label.grid(row=1, column=0, padx=5, pady=5)
arrival_entry = tk.Entry(input_frame)
arrival_entry.grid(row=1, column=1, padx=5, pady=5)

burst_label = tk.Label(input_frame, text="Burst Time:")
burst_label.grid(row=2, column=0, padx=5, pady=5)
burst_entry = tk.Entry(input_frame)
burst_entry.grid(row=2, column=1, padx=5, pady=5)

priority_label = tk.Label(input_frame, text="Priority:")
priority_label.grid(row=3, column=0, padx=5, pady=5)
priority_entry = tk.Entry(input_frame)
priority_entry.grid(row=3, column=1, padx=5, pady=5)

submit_button = tk.Button(input_frame, text="Submit", command=submit_process)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

# Table Frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

columns = ("Process Name", "Arrival Time", "Burst Time", "Priority")
table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=100)

table.pack()

# Run Button
run_button = tk.Button(root, text="Run MLQ Scheduler", command=lambda: MLQ(processes))
run_button.pack(pady=10)

root.mainloop()
