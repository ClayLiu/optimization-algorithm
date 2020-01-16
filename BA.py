import numpy as np
import random
import math
import tqdm
 
class Bat():
    def __init__(self, position : np.ndarray, velocity : np.ndarray, f_bound : tuple):
        
        self.position = position
        self.velocity = velocity
        # self.A = random.random()     # 响度   [0, 1]
        self.A = 1.0    # A == 1 also can be used
        self.r = random.random()     # 脉冲率 [0, 1]       
        self.r_zero = self.r

        self.min_f = f_bound[0]
        self.max_f = f_bound[1]
        self.max_min_f = self.max_f - self.min_f

        self.frequency = random.random() * self.max_min_f + self.min_f
        self.position_new = self.position

    def update_global(self, best_position : np.ndarray):
        beta = random.random()
        self.frequency = self.min_f + self.max_min_f * beta

        self.velocity += (self.position - best_position) * self.frequency
        self.position += self.velocity
    
    def search_local(self, ave_A : float) -> np.ndarray:
        eps = (random.random() * 2 - 1)
        self.position_new = self.position + eps * ave_A

    def update_A_and_r(self, alpha : float, gamma : float, t : int):
        self.A *= alpha
        self.r = self.r_zero * (1 - math.exp(- gamma * t))

    def copy(self):
        return Bat(
            self.position.copy(),
            self.velocity.copy(),
            self.f_bound
        )

class BatSwarm():
    def __init__(self, func, subject_func, bat_num, alpha, gamma, x_bound, v_bound, f_bound : tuple):
        '''
        :param func:            目标函数 \n
        :param subject_func:    约束条件判断函数 \n
        :param bat_num:         蝙蝠个数 \n
        :param alpha:           alpha常数 (0, 1) \n
        :param gamma:           gamma常数 (0, +∞) \n
        :param x_bound:         x在各维度的取值范围 \n
        :param v_bound:         v在各维度的取值范围 \n
        :param f_bound:         f在各维度的取值范围 \n
        '''
        self.func = func
        self.suject_func = subject_func
        self.bat_num = bat_num
        self.x_bound = x_bound
        self.v_bound = v_bound
        self.f_bound = f_bound
        self.x_dim = len(x_bound)
        
        self.alpha = alpha
        self.gamma = gamma

        self.bat_swarm = []
        for i in range(bat_num):
            temp_bat = Bat(
                self.randomly_make_up_x(x_bound, self.x_dim),
                self.randomly_make_up_x(v_bound, self.x_dim),
                self.f_bound
            )
            self.bat_swarm.append(temp_bat)

        self.fitness = np.zeros(self.bat_num) + 1e10
        self.subjections()

    def randomly_make_up_x(self, x_bound, x_dim) -> np.ndarray:
        ''' 在所给范围内随机散布 x '''
        x = np.empty(x_dim)

        for i, x_i_bound in enumerate(x_bound):
            l = x_i_bound[0]
            u = x_i_bound[1]
            x[i] = (u - l) * random.random() + l

        return x
 
    def bound_check(self):
        ''' 检查蝙蝠有没有超过边界，有则拉回边界 '''
        for bat in self.bat_swarm:
            for i in range(self.x_dim):
                if bat.position[i] > self.x_bound[i][0]:
                    bat.position[i] = self.x_bound[i][1]
                elif bat.position[i] < self.x_bound[i][0]:
                    bat.position[i] = self.x_bound[i][0]

    def subjections(self):
        ''' 
            检查蝙蝠是否符合约束条件，若不符则随机生成一个新蝙蝠 \n
            随机生成的也要检查是否符合，直到符合条件
        '''
        for i in range(self.bat_num):
            while not self.suject_func(self.bat_swarm[i].position):
                self.bat_swarm[i] = Bat(
                    self.randomly_make_up_x(self.x_bound, self.x_dim),
                    self.randomly_make_up_x(self.v_bound, self.x_dim),
                    self.f_bound
                )

    def get_fitness(self):
        for i, bat in enumerate(self.bat_swarm):
            self.fitness[i] = self.func(bat.position)

    def iteration(self, iter_num : int):
        
        self.get_fitness()
        best_bat_index = np.argmin(self.fitness)
        best_position = self.bat_swarm[best_bat_index].position.copy()
        print(best_position, self.fitness[best_bat_index])

        for t in tqdm.tqdm(range(1, iter_num + 1)):
            _sum = 0
            for single_bat in self.bat_swarm:
                _sum += single_bat.A
            current_ave_A = _sum / self.bat_num

            for i, single_bat in enumerate(self.bat_swarm):
                single_bat.update_global(best_position)

                if random.random() > single_bat.r:
                    single_bat.search_local(current_ave_A)

                if random.random() < single_bat.A:
                    new_fitness = self.func(single_bat.position_new)
                    if new_fitness < self.fitness[i]:
                        self.fitness[i] = new_fitness
                        single_bat.position = single_bat.position_new.copy()
                        single_bat.update_A_and_r(self.alpha, self.gamma, t)
            
            self.bound_check()
            self.subjections()
            self.get_fitness()
            best_bat_index = np.argmin(self.fitness)
            best_position = self.bat_swarm[best_bat_index].position.copy()
        
        return best_position, self.fitness[best_bat_index]

f = lambda x1, x2, x3, x4 : 0.6224 * x1 * x3 * x4 + 1.7781 * x2 * (x3 ** 2) + 3.1661 * (x1 ** 2) * x4 + 19.84 * (x1 ** 2) * x3

a = np.array([0.8125, 0.4375, 42.0984456, 176.6365958])
print(f(*a))

def test_func(x : np.ndarray):
    cal_f = f(*x)
    if cal_f > 0:
        return cal_f
    else:
        return 99999999

def subject_func(x1, x2, x3, x4):
    return x4 <= 240 and -x1 + 0.0193 * x3 <= 0 and -x2 + 0.00954 * x3 <= 0 and - math.pi * x3 ** 2 * x4 - 4/3*math.pi*x3**3 + 1296000 <= 0

def sj_func(x : np.ndarray):
    return subject_func(*x)

if __name__ == '__main__':
    func = test_func
    M = 200
    x_bound = [
        (0.0625, 1), 
        (0, 1), 
        (10, 100), 
        (100, 200)
    ]
    v_bound = [
        (-0.1, 0.1),
        (-0.1, 0.1),
        (-0.1, 0.1),
        (-0.1, 0.1)
    ]
    test = BatSwarm(
        func,
        sj_func,
        25,
        0.9,
        0.9,
        x_bound,
        v_bound,
        (0, 1)
    )
    best = test.iteration(15000)
    print(test.fitness)
    print(best)
