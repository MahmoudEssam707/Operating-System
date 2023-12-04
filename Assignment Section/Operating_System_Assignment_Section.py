import pandas as pd
import tkinter as tk
from tkinter import Label, Entry, Button, Text
import matplotlib.pyplot as plt


class Process:
    def __init__(self, name, arrival, burst, priority):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst
        self.turnaround = 0
        self.waiting = 0
        self.start = -1
        self.finish = 0
        self.q = 0

    def execute(self, output_text):
        output_text.insert(
            tk.END, "At t = {}, {} entered the kernel\n".format(self.start, self.name)
        )
        self.remaining -= 1
        self.q -= 1


class MLQScheduler:
    @staticmethod
    def scheduling(processes, output_text):
        processes.sort(key=lambda p: p.arrival)
        high_queue = []
        medium_queue = []
        low_queue = []
        time = 0
        current = None

        while True:
            for p in processes:
                if p.arrival == time:
                    output_text.insert(
                        tk.END,
                        "At t = {}, {} arrived the queue {}\n".format(
                            time, p.name, p.priority
                        ),
                    )
                    if p.priority == 0:
                        high_queue.append(p)
                        p.q = 3
                    elif p.priority == 1:
                        medium_queue.append(p)
                        p.q = 2
                    else:
                        low_queue.append(p)

            if current and current.remaining == 0:
                output_text.insert(
                    tk.END,
                    "At t = {}, {} left the kernel and finished\n".format(
                        time, current.name
                    ),
                )
                current.finish = time
                current.turnaround = current.finish - current.arrival
                current.waiting = current.turnaround - current.burst
                current = None

            if current and current.q == 0:
                output_text.insert(
                    tk.END,
                    "At t = {}, {} left the kernel and entered the queue {}\n".format(
                        time, current.name, current.priority
                    ),
                )
                if current.priority == 0:
                    current.q = 3
                    high_queue.append(current)
                else:
                    current.q = 2
                    medium_queue.append(current)
                current = None

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

            if current:
                current.execute(output_text)

            time += 1

        MLQScheduler.print_output(processes, output_text)
        MLQScheduler.draw_gantt_chart(processes)

    @staticmethod
    def draw_gantt_chart(processes):
        fig, ax = plt.subplots(figsize=(8, 4))
        gantt_processes = [p.name for p in processes]
        gantt_start_times = [p.start for p in processes]
        gantt_durations = [p.burst for p in processes]

        for i, process in enumerate(gantt_processes):
            ax.barh(
                0,
                width=gantt_durations[i],
                left=gantt_start_times[i],
                label=f"{process}",
                color=f"C{i}",
            )
            ax.text(
                gantt_start_times[i] + gantt_durations[i] / 2,
                0,
                process,
                ha="center",
                va="center",
                color="white",
            )

        ax.set_xlabel("Time")
        ax.set_yticks([0])
        ax.set_yticklabels(["Combined Queues"])
        ax.set_title("Combined Queues Gantt Chart")
        ax.legend()

        plt.tight_layout()
        plt.show()

    @staticmethod
    def print_output(processes, output_text):
        total_waiting = sum(p.waiting for p in processes)
        average_waiting = total_waiting / len(processes)
        total_turnaround = sum(p.turnaround for p in processes)
        average_turnaround = total_turnaround / len(processes)

        output_text.insert(tk.END, "\nProcess\tTurnaround Time\tWaiting Time\n")
        for p in processes:
            output_text.insert(
                tk.END, "{}\t\t{}\t\t\t{}\n".format(p.name, p.turnaround, p.waiting)
            )

        output_text.insert(
            tk.END, "\nAverage Waiting Time: {:.4f}\n".format(average_waiting)
        )
        output_text.insert(
            tk.END, "Average Turnaround Time: {:.4f}\n".format(average_turnaround)
        )


# GUI functions
def get_process_input():
    name = name_entry.get()
    arrival = int(arrival_entry.get())
    burst = int(burst_entry.get())
    priority = int(priority_entry.get())
    return Process(name, arrival, burst, priority)


def on_add_process():
    processes.append(get_process_input())
    output_text.insert(tk.END, "Process added.\n")
    clear_input_fields()


def on_submit():
    if len(processes) > 0:
        MLQScheduler.scheduling(processes, output_text)
        processes.clear()
        output_text.insert(tk.END, "Scheduling completed.\n")
    else:
        output_text.insert(tk.END, "No processes to schedule.\n")


def clear_input_fields():
    name_entry.delete(0, tk.END)
    arrival_entry.delete(0, tk.END)
    burst_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)


# Tkinter GUI
root = tk.Tk()
root.title("MLQ Scheduling")

# Labels
Label(root, text="Process Name:").grid(row=0, column=0, sticky=tk.W)
Label(root, text="Arrival Time:").grid(row=1, column=0, sticky=tk.W)
Label(root, text="Burst Time:").grid(row=2, column=0, sticky=tk.W)
Label(root, text="Priority:").grid(row=3, column=0, sticky=tk.W)

# Entry fields for process input
name_entry = Entry(root)
name_entry.grid(row=0, column=1)
arrival_entry = Entry(root)
arrival_entry.grid(row=1, column=1)
burst_entry = Entry(root)
burst_entry.grid(row=2, column=1)
priority_entry = Entry(root)
priority_entry.grid(row=3, column=1)

# Buttons
add_process_button = Button(root, text="Add Process", command=on_add_process)
add_process_button.grid(row=4, column=0, columnspan=2, pady=5)

submit_button = Button(root, text="Submit", command=on_submit)
submit_button.grid(row=5, column=0, columnspan=2, pady=10)

# Output text area
output_text = Text(
    root, wrap=tk.WORD, height=15, width=60
)  # Increased height and width
output_text.grid(row=6, column=0, columnspan=2)

# Process list
processes = []

root.mainloop()
