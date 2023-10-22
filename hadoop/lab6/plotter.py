import matplotlib.pyplot as plt


def plot_from_file(filename: str, title: str):
    file = open(filename)
    lines = file.readlines()
    lines = [line[:-1] for line in lines]
    points = []
    for line in lines:
        parts = line.split(' : ')
        cluster_id = int(parts[1])
        parts = parts[0].split(", ")
        x = float(parts[0])
        y = float(parts[1])
        points.append([x, y, cluster_id])

    plt.grid()
    colors = ['red', 'blue']
    for point in points:
        plt.scatter(point[0], point[1], c=colors[point[2]])

    plt.title(title)
    plt.show()


plot_from_file('euclidean.txt', 'Euclidean Distance Measure')
plot_from_file('cosine.txt', 'Cosine Measure')
