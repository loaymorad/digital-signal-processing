import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt

# ======== Utils ========
def save_signal(first_line, second_line, samples, filename):
    with open(filename, "w") as f:
        f.write(f"{first_line}\n{second_line}\n{len(samples)}\n")
        for x, y in samples:
            f.write(f"{x} {y}\n")
    messagebox.showinfo("Saved", f"Signal saved to {filename}")

def plot_signal_side_by_side(samples, title="Signal"):
    # Display continuous (left) and discrete (right) plots of a signal
    
    x = samples[:,0]
    y = samples[:,1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,4))

    # Continuous plot
    ax1.plot(x, y, color="blue")
    ax1.set_title("Continuous")
    ax1.set_xlabel("Sample Index")
    ax1.set_ylabel("Amplitude")

    # Discrete plot
    ax2.stem(x, y, linefmt='r-', markerfmt='ro', basefmt='k-')
    ax2.set_title("Discrete")
    ax2.set_xlabel("Sample Index")
    ax2.set_ylabel("Amplitude")

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()

def select_files(min_files=1):
    files = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
    if not files:
        return None
    if len(files) < min_files:
        messagebox.showwarning("Not enough files", f"Select at least {min_files} file(s).")
        return None

    return files

def read_samples_from_file(signal_file):
    with open(signal_file, "r") as file:
        first_line = int(file.readline().strip())
        second_line = int(file.readline().strip())
        samples_number = int(file.readline().strip())
        samples = []
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                samples.append([int(parts[0]), int(parts[1])])
        samples = np.array(samples)
    return first_line, second_line, samples_number, samples

def prompt_gui(labels: list):
    gen_window = tk.Toplevel()
    gen_window.title("Prompt")

    output = []
    for i, label in enumerate(labels):
        tk.Label(gen_window, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(gen_window)
        entry.grid(row=i, column=1, padx=5, pady=5)
        output.append(entry)

    return output, gen_window  # return the entries and the window so i can destroy it later

# ======== Main Functions (Lab 1) ========

def read_signal():
    files = select_files()
    if not files: 
        return

    first_line, second_line, samples_number, samples = read_samples_from_file(files[0])
    
    plot_signal_side_by_side(samples)
    
    return first_line, second_line, samples_number, samples

def add_signals():
    files = select_files(min_files=2)
    if not files:
        return

    signals_data = [read_samples_from_file(f)[3] for f in files]
    summed_samples = signals_data[0].copy()
    for sig in signals_data[1:]:
        summed_samples[:,1] += sig[:,1]

    first_line, second_line, _, _ = read_samples_from_file(files[0])
    
    plot_signal_side_by_side(summed_samples, title="Addition Result")
    
    save_signal(first_line, second_line, summed_samples, filename="result_add.txt")

def multiply_signal():
    files = select_files()
    if not files:
        return

    constant = simpledialog.askfloat("Input", "Enter multiplication constant: ")
    if constant is None:
        return

    signal_file = files[0]
    first_line, second_line, _, samples = read_samples_from_file(signal_file)
    samples[:,1] *= constant

    plot_signal_side_by_side(samples, title=f"{signal_file.split('/')[-1]} x {constant}")

    save_signal(first_line, second_line, samples, filename=f"result_multiply_{signal_file.split('/')[-1]}")


# ======== Main Functions (Lab 2) ========

def generate_signal():
    labels = ["signal type", "Amplitude (A)", "Analog Frequency (Hz)", "Sampling Frequency (Hz)", "Phase Shift (radians)"]
    entries, gen_window = prompt_gui(labels)

    def on_generate(entries, gen_window):
        signal_type = str(entries[0].get())
        A = float(entries[1].get())
        f_analog = float(entries[2].get())
        f_s = float(entries[3].get())
        theta = float(entries[4].get())


        # Generate signal
        t_end = 1  # duration 1 second
        t = np.arange(0, t_end, 1/f_s)
        if signal_type.lower() == "sin":
            y = A * np.sin(2 * np.pi * f_analog * t + theta)
        elif signal_type.lower() == "cos":
            y = A * np.cos(2 * np.pi * f_analog * t + theta)

        x = np.arange(len(t))
        samples = np.column_stack((x, y))

        save_signal(0, 0, samples, f"generated_{signal_type}.txt")
        gen_window.destroy()

    tk.Button(gen_window, text="Generate", command=lambda: on_generate(entries, gen_window)).grid(row=len(labels), column=0, columnspan=2, pady=10)

def substract_signals():
    files = select_files(min_files=2)
    if not files:
        return

    signals_data = [read_samples_from_file(f)[3] for f in files]
    result_samples = signals_data[0].copy()
    for sig in signals_data[1:]:
        result_samples[:,1] -= sig[:,1]

    first_line, second_line, _, _ = read_samples_from_file(files[0])

    save_signal(first_line, second_line, result_samples, filename="result_subtract.txt")

def square_signal():
    files = select_files(min_files=1)
    if not files:
        return

    signal_file = files[0]
    first_line, second_line, _, samples = read_samples_from_file(signal_file)
    samples[:,1] = np.square(samples[:,1])

    save_signal(first_line, second_line, samples, filename=f"squared_{signal_file.split('/')[-1]}")

def normalize_signal():
    labels = ["File to normalize", "Normalization type (0-1 or -1 to 1)"]
    entries, gen_window = prompt_gui(labels)

    def on_normalize(entries, gen_window):
        files = select_files()
        if not files:
            return

        norm_type = entries[1].get()
        if norm_type not in ["0-1", "-1 to 1"]:
            messagebox.showerror("Error", "Normalization type must be '0-1' or '-1 to 1'")
            return

        for signal_file in files:
            first_line, second_line, _, samples = read_samples_from_file(signal_file)
            min_val, max_val = samples[:,1].min(), samples[:,1].max()

            if norm_type == "0-1":
                samples[:,1] = (samples[:,1] - min_val) / (max_val - min_val)
            else:  # -1 to 1
                samples[:,1] = 2 * (samples[:,1] - min_val) / (max_val - min_val) - 1

            # plot_signal_side_by_side(samples, title=f"Normalized {signal_file.split('/')[-1]}")
            save_signal(first_line, second_line, samples, filename=f"normalized_{signal_file.split('/')[-1]}")

        gen_window.destroy()

    tk.Button(gen_window, text="Normalize", command=lambda: on_normalize(entries, gen_window)).grid(row=len(labels), column=0, columnspan=2, pady=10)

def accumulation_signal():
    files = select_files(min_files=1)
    if not files:
        return

    signal_file = files[0]
    first_line, second_line, _, samples = read_samples_from_file(signal_file)
    
    accumulated = []
    total = 0
    for y in samples[:,1]:
        total += y
        accumulated.append(total)
    
    samples[:,1] = np.array(accumulated)

    plot_signal_side_by_side(samples, title=f"Accumulated {signal_file.split('/')[-1]}")
    save_signal(first_line, second_line, samples, filename=f"accumulated_{signal_file.split('/')[-1]}")


# ======== RUN ========
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Signal Processing Framework")
    window.geometry("1200x800")

    row = 0

    # === Lab 1 ===
    tk.Label(window, text="Lab 1").grid(row=0, column=0, pady=10)

    buttons = [
        ("Read Signal", read_signal), 
        ("Add Signals", add_signals), 
        ("Multiply Signals", multiply_signal)
    ]
    
    for text, cmd in buttons:
        row += 1
        tk.Button(window, text=text, width=20, command=cmd).grid(row=row, column=0, pady=5)


    # === Lab 2 ===
    tk.Label(window, text="Lab 2").grid(row=4, column=0, pady=10)

    buttons = [
        ("Generate Signal", generate_signal), 
        ("substract Signal", substract_signals), 
        ("square Signal", square_signal), 
        ("normalize Signal", normalize_signal), 
        ("accumulation signal", accumulation_signal)
    ]
    
    for text, cmd in buttons:
        row += 1
        tk.Button(window, text=text, width=20, command=cmd).grid(row=row, column=0, pady=5)


    window.mainloop()
