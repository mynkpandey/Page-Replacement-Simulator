import tkinter as tk
from tkinter import messagebox, filedialog
from simulation import fifo_page_replacement, lru_page_replacement, optimal_page_replacement
from visualization import plot_page_faults

class PageReplacementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Simulator")
        
        # Configure grid weights for responsive layout
        for i in range(4):
            self.root.columnconfigure(i, weight=1)
            self.root.rowconfigure(i, weight=1)

        # Input fields with improved layout
        self.frame_label = tk.Label(root, text="Number of Frames:")
        self.frame_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.frame_entry = tk.Entry(root)
        self.frame_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.sequence_label = tk.Label(root, text="Page Sequence:")
        self.sequence_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.sequence_entry = tk.Entry(root)
        self.sequence_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Load file button with proper styling
        self.load_button = tk.Button(root, text="📂 Load File", 
                                   command=self.load_sequence,
                                   bg='#4CAF50', fg='white')
        self.load_button.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

        # Algorithm selection with frame
        algo_frame = tk.LabelFrame(root, text="Algorithms", padx=10, pady=10)
        algo_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        
        self.fifo_var = tk.IntVar()
        self.lru_var = tk.IntVar()
        self.optimal_var = tk.IntVar()
        
        self.fifo_check = tk.Checkbutton(algo_frame, text="FIFO", variable=self.fifo_var)
        self.fifo_check.pack(side='left', padx=20)
        self.lru_check = tk.Checkbutton(algo_frame, text="LRU", variable=self.lru_var)
        self.lru_check.pack(side='left', padx=20)
        self.optimal_check = tk.Checkbutton(algo_frame, text="Optimal", variable=self.optimal_var)
        self.optimal_check.pack(side='left', padx=20)

        # Styled buttons
        button_frame = tk.Frame(root)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        self.run_button = tk.Button(button_frame, text="🚀 Run Simulation", 
                                  command=self.run_simulation,
                                  bg='#2196F3', fg='white')
        self.run_button.pack(side='left', padx=10)
        
        self.viz_button = tk.Button(button_frame, text="📊 Show Visualization", 
                                  command=self.show_visualization,
                                  bg='#FF9800', fg='white')
        self.viz_button.pack(side='left', padx=10)
        
        # Add save button
        self.save_button = tk.Button(button_frame, text="💾 Save Results", 
                                   command=self.save_results,
                                   bg='#4CAF50', fg='white')
        self.save_button.pack(side='left', padx=10)


        # Results display with scrollbar
        result_frame = tk.LabelFrame(root, text="Results", padx=10, pady=10)
        result_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        
        self.result_text = tk.Text(result_frame, height=8, width=60)
        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def save_results(self):
        """Save simulation results to a text file"""
        if not hasattr(self, 'results') or not self.results:
            messagebox.showerror("Error", "No results to save. Run simulation first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("Page Replacement Simulation Results\n")
                    f.write("="*40 + "\n")
                    f.write(f"Number of Frames: {self.frame_entry.get()}\n")
                    f.write(f"Page Sequence: {self.sequence_entry.get()}\n\n")
                    f.write("Page Faults:\n")
                    for algo, faults in self.results.items():
                        f.write(f"{algo}: {faults}\n")
                messagebox.showinfo("Success", f"Results saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")

    def load_sequence(self):
        """Load page sequence from a text file"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    # Validate file content before inserting
                    if all(x.strip().isdigit() for x in content.split(',')):
                        self.sequence_entry.delete(0, tk.END)
                        self.sequence_entry.insert(0, content)
                    else:
                        messagebox.showerror("Error", "File contains invalid characters")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")

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
        memory_states = {}
        if self.fifo_var.get():
            total_faults, states = fifo_page_replacement(frames, sequence)
            results['FIFO'] = total_faults
            memory_states['FIFO'] = states
        if self.lru_var.get():
            total_faults, states = lru_page_replacement(frames, sequence)
            results['LRU'] = total_faults
            memory_states['LRU'] = states
        if self.optimal_var.get():
            total_faults, states = optimal_page_replacement(frames, sequence)
            results['Optimal'] = total_faults
            memory_states['Optimal'] = states

        # Display results
        self.result_text.delete(1.0, tk.END)
        for algo, faults in results.items():
            self.result_text.insert(tk.END, f"{algo}: {faults} page faults\n")

        self.results = results  
        self.memory_states = memory_states # Store for visualization

    def show_visualization(self):
        if hasattr(self, 'results') and hasattr(self, 'memory_states'):
            plot_page_faults(
                list(self.results.keys()),
                list(self.results.values()),
                self.memory_states
            )
        else:
            self.result_text.insert(tk.END, "Run the simulation first.\n")
