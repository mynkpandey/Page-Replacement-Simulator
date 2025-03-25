import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from simulation import FIFOHandler, LRUHandler, OptimalHandler, ClockHandler
from visualization import plot_page_faults

class CyberpunkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CYBERPUNK 2077 PAGE REPLACEMENT SIMULATOR")
        self.root.configure(bg='#0a0a0a')
        
        # Cyberpunk color scheme
        self.colors = {
            'background': '#0a0a0a',
            'neon_green': '#00ff9d',
            'neon_pink': '#ff0055',
            'neon_blue': '#08f7fe',
            'text': '#ffffff',
            'terminal': '#00ff9d',
            'warning': '#ff0000'
        }

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('alt')
        
        # Base styles
        self.style.configure('.', 
                           background=self.colors['background'],
                           foreground=self.colors['text'],
                           font=('OCR A Extended', 10))
        
        # Widget styles
        self.style.configure('Cyber.TButton',
                           background=self.colors['neon_green'],
                           foreground='#000000',
                           borderwidth=3,
                           font=('OCR A Extended', 12, 'bold'),
                           padding=10)
        self.style.map('Cyber.TButton',
                     background=[('active', self.colors['neon_pink'])])
        
        self.style.configure('Cyber.TEntry',
                           fieldbackground='#1a1a1a',
                           foreground=self.colors['neon_blue'],
                           insertcolor=self.colors['neon_blue'])
        
        self.style.configure('Cyber.TCheckbutton',
                           indicatorbackground='#1a1a1a',
                           indicatorcolor=self.colors['neon_green'],
                           selectcolor='#1a1a1a')
        
        self.style.configure('Header.TLabel',
                           font=('OCR A Extended', 18, 'bold'),
                           foreground=self.colors['neon_pink'],
                           background=self.colors['background'])
        
        self.style.configure('Cyber.Horizontal.TProgressbar',
                           background=self.colors['neon_green'],
                           troughcolor='#1a1a1a')

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Header
        header = ttk.Label(main_frame, 
                         text="PAGE REPLACEMENT SIMULATOR", 
                         style='Header.TLabel')
        header.pack(pady=10)

        # Input Section
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill='x', pady=10)
        
        ttk.Label(input_frame, text="RAM FRAMES:", style='Header.TLabel').grid(row=0, column=0, padx=5)
        self.frame_entry = ttk.Entry(input_frame, style='Cyber.TEntry', width=10)
        self.frame_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="PAGE STREAM:", style='Header.TLabel').grid(row=0, column=2, padx=5)
        self.sequence_entry = ttk.Entry(input_frame, style='Cyber.TEntry', width=40)
        self.sequence_entry.grid(row=0, column=3, padx=5)
        
        ttk.Button(input_frame, text="UPLOAD DATASET", 
                 command=self.load_sequence, style='Cyber.TButton').grid(row=0, column=4, padx=5)

        # Algorithm Selector
        algo_frame = ttk.LabelFrame(main_frame, text="[ SELECT ALGORITHMS ]")
        algo_frame.pack(fill='x', pady=10)
        
        self.vars = {
            'FIFO': tk.IntVar(),
            'LRU': tk.IntVar(),
            'OPTIMAL': tk.IntVar(),
            'CLOCK': tk.IntVar()
        }
        
        for i, (algo, var) in enumerate(self.vars.items()):
            ttk.Checkbutton(algo_frame, text=algo, variable=var,
                          style='Cyber.TCheckbutton').grid(row=0, column=i, padx=15)

        # Control Panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill='x', pady=10)
        
        ttk.Button(control_frame, text="INITIATE SIMULATION", 
                 command=self.run_simulation, style='Cyber.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="VISUALIZE DATA", 
                 command=self.show_visualization, style='Cyber.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="SAVE RESULTS", 
                 command=self.save_results, style='Cyber.TButton').pack(side='left', padx=5)

        # Progress Matrix
        self.progress = ttk.Progressbar(main_frame, 
                                      style='Cyber.Horizontal.TProgressbar',
                                      length=500,
                                      mode='determinate')
        self.progress.pack(pady=15, fill='x')

        # Results Terminal
        term_frame = ttk.Frame(main_frame)
        term_frame.pack(fill='both', expand=True)
        
        self.result_text = tk.Text(term_frame, 
                                 bg='#1a1a1a', 
                                 fg=self.colors['terminal'],
                                 insertbackground=self.colors['terminal'],
                                 font=('Consolas', 11),
                                 wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(term_frame, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def load_sequence(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    self.sequence_entry.delete(0, tk.END)
                    self.sequence_entry.insert(0, content)
                    self.result_text.insert(tk.END, f"\n> DATASET LOADED FROM: {file_path}\n")
        except Exception as e:
            messagebox.showerror("DATA CORRUPTED", f"LOAD FAILURE:\n{str(e)}")

    def run_simulation(self):
        try:
            # Validation
            frames = int(self.frame_entry.get())
            sequence = [int(x) for x in self.sequence_entry.get().split(',')]
            
            # Initialize handlers
            handlers = []
            if self.vars['FIFO'].get(): handlers.append(('FIFO', FIFOHandler(frames)))
            if self.vars['LRU'].get(): handlers.append(('LRU', LRUHandler(frames)))
            if self.vars['OPTIMAL'].get(): handlers.append(('OPTIMAL', OptimalHandler(frames, sequence)))
            if self.vars['CLOCK'].get(): handlers.append(('CLOCK', ClockHandler(frames)))
            
            if not handlers:
                messagebox.showwarning("SYSTEM ALERT", "NO ALGORITHMS SELECTED")
                return

            # Run simulation
            self.progress['value'] = 0
            total = len(sequence)
            results = {}
            states = {}
            
            for idx, page in enumerate(sequence):
                for name, handler in handlers:
                    faults, mem = handler.step(page)
                    states.setdefault(name, []).append(faults)
                self.progress['value'] = (idx+1)/total*100
                self.root.update_idletasks()
            
            # Display results
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\n> SIMULATION RESULTS:\n")
            for algo, handler in handlers:
                self.result_text.insert(tk.END, f"{algo}: {handler.page_faults} PAGE FAULTS\n")
            
            self.results = {name: handler.page_faults for name, handler in handlers}
            self.memory_states = states

        except ValueError as e:
            messagebox.showerror("INPUT ERROR", f"INVALID DATA FORMAT\n{e}")
        except Exception as e:
            messagebox.showerror("SYSTEM FAILURE", f"SIMULATION CRASHED\n{e}")

    def show_visualization(self):
        if hasattr(self, 'results'):
            plot_page_faults(list(self.results.keys()), 
                           list(self.results.values()), 
                           self.memory_states)
        else:
            messagebox.showwarning("NO DATA", "RUN SIMULATION FIRST!")

    def save_results(self):
        try:
            if not hasattr(self, 'results'):
                messagebox.showwarning("NO DATA", "NOTHING TO SAVE!")
                return
            
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(f"FRAMES: {self.frame_entry.get()}\n")
                    f.write(f"SEQUENCE: {self.sequence_entry.get()}\n\n")
                    for algo, faults in self.results.items():
                        f.write(f"{algo}: {faults}\n")
                self.result_text.insert(tk.END, f"\n> RESULTS SAVED TO: {file_path}\n")
        except Exception as e:
            messagebox.showerror("SAVE ERROR", f"FAILED TO SAVE:\n{str(e)}")
