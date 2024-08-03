import matplotlib.pyplot as plt

def visualize_buckets(buckets):
    """Visualize S3 buckets using Matplotlib."""
    names = [bucket['Name'] for bucket in buckets]
    sizes = [bucket['TotalSize'] for bucket in buckets]
    object_counts = [bucket['ObjectCount'] for bucket in buckets]

    fig, ax = plt.subplots()

    bar_width = 0.35
    index = range(len(buckets))

    bar1 = plt.bar(index, sizes, bar_width, label='Total Size (Bytes)')
    bar2 = plt.bar([i + bar_width for i in index], object_counts, bar_width, label='Object Count')

    plt.xlabel('Bucket Name')
    plt.ylabel('Metrics')
    plt.title('S3 Bucket Metrics')
    plt.xticks([i + bar_width / 2 for i in index], names, rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.show()
