import matplotlib.pyplot as plt

def plot_page_faults(algorithms, faults, memory_states):
    """Plot bar chart of total faults and line chart of cumulative faults."""
    plt.figure(figsize=(12, 5))
    
    # Bar chart
    plt.subplot(1, 2, 1)
    plt.bar(algorithms, faults)
    plt.xlabel('Algorithms')
    plt.ylabel('Total Page Faults')
    plt.title('Total Page Faults Comparison')
    
    # Line chart
    plt.subplot(1, 2, 2)
    for algo in algorithms:
        states = memory_states.get(algo, [])
        plt.plot(range(len(states)), states, label=algo)
    plt.xlabel('Page Reference Step')
    plt.ylabel('Cumulative Page Faults')
    plt.title('Page Faults Progression')
    plt.legend()
    
    plt.tight_layout()
    plt.show()