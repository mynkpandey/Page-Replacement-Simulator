import tkinter as tk
from tkinter import messagebox
from simulation import fifo_page_replacement, lru_page_replacement, optimal_page_replacement
from visualization import plot_page_faults

class PageReplacementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Simulator")

        # Input fields
        self.frame_label = tk.Label(root, text="Number of Frames:")
        self.frame_label.grid(row=0, column=0)
        self.frame_entry = tk.Entry(root)
        self.frame_entry.grid(row=0, column=1)

        self.sequence_label = tk.Label(root, text="Page Sequence (comma-separated):")
        self.sequence_label.grid(row=1, column=0)
        self.sequence_entry = tk.Entry(root)
        self.sequence_entry.grid(row=1, column=1)

        # Algorithm selection
        self.algo_label = tk.Label(root, text="Select Algorithms:")
        self.algo_label.grid(row=2, column=0)
        self.fifo_var = tk.IntVar()
        self.lru_var = tk.IntVar()
        self.optimal_var = tk.IntVar()
        self.fifo_check = tk.Checkbutton(root, text="FIFO", variable=self.fifo_var)
        self.fifo_check.grid(row=2, column=1)
        self.lru_check = tk.Checkbutton(root, text="LRU", variable=self.lru_var)
        self.lru_check.grid(row=2, column=2)
        self.optimal_check = tk.Checkbutton(root, text="Optimal", variable=self.optimal_var)
        self.optimal_check.grid(row=2, column=3)

        # Run button
        self.run_button = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=3, column=0, columnspan=4)

        # Results display
        self.result_label = tk.Label(root, text="Results:")
        self.result_label.grid(row=4, column=0)
        self.result_text = tk.Text(root, height=5, width=50)
        self.result_text.grid(row=4, column=1, columnspan=3)

        # Visualization button
        self.viz_button = tk.Button(root, text="Show Visualization", command=self.show_visualization)
        self.viz_button.grid(row=5, column=0, columnspan=4)

    def run_simulation(self):
        """Run the selected page replacement algorithms and display results."""
        # Validate number of frames input
        frames_input = self.frame_entry.get()
        if not frames_input.isdigit() or int(frames_input) <= 0:
            messagebox.showerror("Error", "Number of frames must be a positive integer")
            return

        # Validate page sequence input
        sequence_input = self.sequence_entry.get().strip()
        if not sequence_input:  # Check for empty input
            messagebox.showerror("Error", "Page sequence cannot be empty")
            return
        try:
            sequence = [int(x.strip()) for x in sequence_input.split(',')]
        except ValueError:
            messagebox.showerror("Error", "Page sequence must be integers separated by commas")
            return

        frames = int(frames_input)

        # Run selected algorithms
        results = {}
        if self.fifo_var.get():
            results['FIFO'] = fifo_page_replacement(frames, sequence)
        if self.lru_var.get():
            results['LRU'] = lru_page_replacement(frames, sequence)
        if self.optimal_var.get():
            results['Optimal'] = optimal_page_replacement(frames, sequence)

        # Display results
        self.result_text.delete(1.0, tk.END)
        for algo, faults in results.items():
            self.result_text.insert(tk.END, f"{algo}: {faults} page faults\n")

        self.results = results  # Store results for visualization

    def show_visualization(self):
        """Display a bar chart of page faults if simulation has been run."""
        if hasattr(self, 'results'):
            plot_page_faults(list(self.results.keys()), list(self.results.values()))
        else:
            self.result_text.insert(tk.END, "Run the simulation first.\n")


