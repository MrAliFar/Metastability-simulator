import matplotlib.pyplot as plt


def plot_list(lst):
    x = list(range(len(lst)))
    plt.plot(x, lst)
    plt.show()