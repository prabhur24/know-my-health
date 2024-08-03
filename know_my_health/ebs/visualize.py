import matplotlib.pyplot as plt

def visualize_volumes(volumes):
    """Visualize EBS volumes using Matplotlib."""
    volume_ids = [volume['VolumeId'] for volume in volumes]
    sizes = [volume['Size'] for volume in volumes]
    iops = [volume['Iops'] if volume['Iops'] != 'N/A' else 0 for volume in volumes]
    throughput = [volume['Throughput'] if volume['Throughput'] != 'N/A' else 0 for volume in volumes]

    fig, ax = plt.subplots()

    bar_width = 0.25
    index = range(len(volumes))

    bar1 = plt.bar(index, sizes, bar_width, label='Size (GiB)')
    bar2 = plt.bar([i + bar_width for i in index], iops, bar_width, label='IOPS')
    bar3 = plt.bar([i + 2 * bar_width for i in index], throughput, bar_width, label='Throughput (MB/s)')

    plt.xlabel('Volume ID')
    plt.ylabel('Metrics')
    plt.title('EBS Volume Metrics')
    plt.xticks([i + bar_width for i in index], volume_ids, rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.show()
