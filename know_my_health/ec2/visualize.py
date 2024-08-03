import matplotlib.pyplot as plt

def visualize_instance_metrics(instances):
    """Visualize instance metrics using Matplotlib."""
    instance_ids = [instance['InstanceId'] for instance in instances]
    cpu_usages = [instance['CPUUtilization'] if instance['CPUUtilization'] != 'N/A' else 0 for instance in instances]
    ram_usages = [instance['RAMUsage'] if instance['RAMUsage'] != 'N/A' else 0 for instance in instances]

    fig, ax = plt.subplots()

    bar_width = 0.35
    index = range(len(instances))

    bar1 = plt.bar(index, cpu_usages, bar_width, label='CPU Usage (%)')
    bar2 = plt.bar([i + bar_width for i in index], ram_usages, bar_width, label='RAM Usage (%)')

    plt.xlabel('Instance ID')
    plt.ylabel('Usage (%)')
    plt.title('CPU and RAM Usage by Instance')
    plt.xticks([i + bar_width / 2 for i in index], instance_ids, rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.show()
