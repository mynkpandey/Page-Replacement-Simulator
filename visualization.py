import matplotlib.pyplot as plt

def plot_page_faults(algorithms, faults):
    """Plot a bar chart of page faults for selected algorithms."""
    plt.bar(algorithms, faults)
    plt.xlabel('Algorithms')
    plt.ylabel('Page Faults')
    plt.title('Page Faults Comparison')
    plt.show()