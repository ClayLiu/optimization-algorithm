import numpy as np
import matplotlib.pyplot as plt

def get_fig(fitness_array, fig_name, show = False):
    plt.figure()
    plt.title('Fitness value in x_th interation')
    plt.xlabel('x_th interation')
    plt.ylabel('fitness value')
    
    plt.plot(fitness_array)
    # plt.plot(x, head_fitness, color = 'blue')

    # plt.legend(['F_fitness', 'head_slap_fitness'])
    if show:
        plt.show()
    plt.savefig(fig_name)
    plt.close()
