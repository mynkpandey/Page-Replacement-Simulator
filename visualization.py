import matplotlib.pyplot as plt

def plot_page_faults(algorithms, faults, states):
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#0a0a0a')
    
    # Bar plot
    colors = ['#00ff9d', '#08f7fe', '#ff0055', '#6c5ce7']
    ax1.bar(algorithms, faults, color=colors[:len(algorithms)])
    ax1.set_title('Total Page Faults', color='white', fontweight='bold')
    ax1.tick_params(colors='white')
    
    # Line plot
    for i, algo in enumerate(algorithms):
        ax2.plot(states[algo], color=colors[i], linewidth=2, label=algo)
    ax2.set_title('Fault Progression', color='white', fontweight='bold')
    ax2.legend()
    ax2.tick_params(colors='white')
    
    plt.tight_layout()
    plt.show()