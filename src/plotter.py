from matplotlib import pyplot

scores = [0.33, 0.46, 0.36, 0.33, 0.2, 0.35, 0.11, 0.12, 0.06, 0.11, -0.15, 0.01, 0.08, 0.41, -0.73, -0.33, -0.37,
          -0.35, -1.99, 2.57, 2.71, 2.48, 2.28, 8.67, 8.59, 10.7, 8.48, 8.94, 7.7, 8.05, 7.63, 7.45, 7.51, 7.86, 7.34,
          8.23, 8.53, 8.54, 7.51, 8.0, 8.03, 8.0, 3.65, 7.69, -100, 0.0, 0.23, 0.11, -1.35, -1.02, -9.68, 0.81, 1.06,
          2.94, 2.69, 2.62, 2.52, 4.21, 4.32, 4.67, 2.55, 2.46, 0.71, 2.58, -100, -100]


def generate_x_values(scores):
    x_array = []
    for i in range(len(scores)):
        x_array.append(i / 2)
    return x_array


def plot():
    # aesthetic stuff
    pyplot.ylim(-100, 100)

    fig, ax = pyplot.subplots()
    ax.margins(0)
    ax.plot(generate_x_values(scores), scores, color='black')

    pyplot.axhline(0, color='red')
    ax.axhspan(-100, 0, facecolor='black', alpha=0.5)
    ax.axhspan(0, 100, facecolor='white', alpha=0.5)

    pyplot.show()


plot()
