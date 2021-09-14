from matplotlib import pyplot


def generate_x_values(scores):
    x_array = []
    for i in range(len(scores)):
        x_array.append(i)
    return x_array


def plot(scores):
    pyplot.xkcd()
    pyplot.plot(generate_x_values(scores), scores)
    pyplot.show()

