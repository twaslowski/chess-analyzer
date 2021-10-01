from matplotlib import pyplot


def generate_x_values(scores):
    x_array = []
    for i in range(len(scores)):
        x_array.append(i / 2)
    return x_array


def plot(scores):
    # aesthetic stuff
    pyplot.ylim(-100, 100)

    fig, ax = pyplot.subplots()
    ax.margins(0)
    ax.plot(generate_x_values(scores), scores, color='black')

    pyplot.axhline(0, color='red')
    ax.axhspan(-100, 0, facecolor='black', alpha=0.5)
    ax.axhspan(0, 100, facecolor='white', alpha=0.5)

    return pyplot.savefig('test.png', bbox_inches='tight')
