import matplotlib.pyplot as plt


def visualize_load_balancers(load_balancers):
    """Visualize ELB instances using Matplotlib."""
    names = [lb['Name'] for lb in load_balancers]
    instances_count = [len(lb['Instances'].split(', ')) for lb in load_balancers]

    fig, ax = plt.subplots()

    ax.bar(names, instances_count, color='blue')

    plt.xlabel('Load Balancer Name')
    plt.ylabel('Number of Instances')
    plt.title('Instances behind each Load Balancer')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
