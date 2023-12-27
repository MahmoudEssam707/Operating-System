import customtkinter as ctk


def SecondChance(num_frames, ref_string):
    # Initialize memory frames and reference bits
    frames = [None] * num_frames
    ref_bits = [0] * num_frames

    # Initialize page fault count and clock hand
    page_faults = 0
    clock_hand = 0

    # Handle each reference in the string
    for ref in ref_string:
        found = False

        # Search for the page in memory frames
        for i in range(num_frames):
            if frames[i] == ref:
                # Set reference bit to 1 and skip replacement
                ref_bits[i] = 1
                found = True
                break

        # Page fault if not found
        if not found:
            page_faults += 1

            # Replace using Second Chance algorithm
            while True:
                # Give second chance if reference bit is 1
                if ref_bits[clock_hand] == 1:
                    ref_bits[clock_hand] = 0
                    clock_hand = (clock_hand + 1) % num_frames
                else:
                    # Replace page and update frame and bit
                    frames[clock_hand] = ref
                    ref_bits[clock_hand] = 1
                    clock_hand = (clock_hand + 1) % num_frames
                    break

    # Get the result as a string
    result_str = f"Page faults: {page_faults}\nMemory frames: {frames} with reference bits: {ref_bits}"

    # Insert the result into the text area
    text_result.insert(ctk.END, result_str + "\n")


# Create the main application window
root = ctk.CTk()
root.title("Second Chance Page Replacement Algorithm")

# Label and Entry for the number of memory frames
lbl_frames = ctk.CTkLabel(root, text="Number of Memory Frames:")
lbl_frames.pack(pady=5)
entry_frames = ctk.CTkEntry(root)
entry_frames.pack(pady=5)

# Label and Entry for the reference string
lbl_ref_string = ctk.CTkLabel(root, text="Reference String (separated by spaces):")
lbl_ref_string.pack(pady=5)
entry_ref_string = ctk.CTkEntry(root)
entry_ref_string.pack(pady=5)

# Text area to display the result
text_result = ctk.CTkTextbox(root, width=300, height=100)
text_result.pack(pady=10)


# Function to execute the algorithm when the button is clicked
def run_algorithm():
    try:
        num_frames = int(entry_frames.get())
        ref_string = entry_ref_string.get().split()
        SecondChance(num_frames, ref_string)
    except ValueError:
        text_result.insert(
            ctk.END, "Please enter valid numeric input for memory frames.\n"
        )


# Button to run the algorithm
btn_run = ctk.CTkButton(root, text="Run Algorithm", command=run_algorithm)
btn_run.pack(pady=10)

# Start the Tkinter event loop
root.geometry('350x350')
root.mainloop()


