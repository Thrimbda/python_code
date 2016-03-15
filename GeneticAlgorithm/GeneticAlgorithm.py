# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-03-12 09:58:53
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-03-14 22:45:07
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

# V = np.arange(10)
# E = np.random.randint(1, 50, size=[10, 10])
sizePop = 10

V = list(zip(np.random.random(sizePop)*100, np.random.random(sizePop)*100))
E = np.zeros([sizePop, sizePop])
for i in range(0, sizePop):
    for j in range(0, sizePop):
        if i == j:
            E[i, j] = None
        else:
            E[i, j] = np.sqrt((V[i][0]-V[j][0])**2+(V[i][1]-V[j][1])**2)


class GAUnit:
    def __init__(self, sizePop, dimention, bound):
        self.dimention = dimention
        self.bound = bound
        self.fitness = 0
        self.geneCode = np.zeros(self.dimention, dtype=int)
        self.length = 0
        self.sizePop = sizePop

    # def initGrapg(self):
    #     V = list(zip(np.random.random(self.imention)*100, np.random.random(self.dimention)*100))
    #     E = np.zeros([self.dimention, self.dimention])
    #     for i in range(0, self.dimention):
    #         for j in range(0, self.dimention):
    #             if i == j:
    #                 E[i, j] = None
    #             else:
    #                 E[i, j] = np.sqrt((V[i][0]-V[j][0])**2+(V[i][1]-V[j][1])**2)

    def generate(self):
        for i in range(0, self.dimention):
            gen = np.random.randint(0, self.dimention - i)
            self.geneCode[i] = gen

    def geneDecode(self):
        self.cityIndex = copy.deepcopy(self.geneCode)
        for i in range(0, self.dimention)[::-1]:
            for j in range(0, i)[::-1]:
                if self.cityIndex[j] <= self.cityIndex[i]:
                    self.cityIndex[i] += 1
        return self.cityIndex

    def evaluateFitness(self):
        self.length = 0
        global E
        self.geneDecode()
        for i in range(0, self.dimention):
            if i == self.dimention - 1:
                pass
            else:
                self.length += E[self.cityIndex[i], self.cityIndex[i+1]]
        self.length += E[1, -1]
        self.fitness = self.sizePop/self.length


class GA:
    def __init__(self, sizePop, dimention, bound, maxGen, params):
        self.sizePop = sizePop
        self.maxGen = maxGen
        self.dimention = dimention
        self.bound = bound
        self.params = params  #Mutation, crossRate
        self.population = []
        self.fitness = np.zeros((self.sizePop, 1))
        self.trace = np.zeros((self.maxGen, 2))
        self.genTh = 0
        self.best = None
        self.t = 0
        self.done = False

    def initUnit(self):
        for i in range(0, self.sizePop):
            unit = GAUnit(self.sizePop, self.dimention, self.bound)
            unit.generate()
            self.population.append(unit)

    def evaluate(self):
        for i in range(0, self.sizePop):
            self.population[i].evaluateFitness()
            self.fitness[i] = self.population[i].fitness

    def selection(self):
        newPop = []
        fitnessTotal = np.sum(self.fitness)
        fitnessSection = np.zeros((self.sizePop, 1))
        temp = 0
        for i in range(0, self.sizePop):
            fitnessSection[i] = temp + self.fitness[i]/fitnessTotal
            temp = fitnessSection[i]

        for i in range(0, self.sizePop):
            seed = np.random.random()
            index = 0
            for j in range(0, self.sizePop - 1):
                if j == 0 and seed < fitnessSection[j]:
                    index = 0
                    break
                elif seed >= fitnessSection[j] and seed < fitnessSection[j+1]:
                    index = j + 1
                    break
            newPop.append(self.population[index])
        self.population = newPop

    def recombination(self):
        newPop = []
        for i in range(0, self.sizePop, 2):
            index1 = np.random.randint(0, self.sizePop-1)
            index2 = np.random.randint(0, self.sizePop-1)
            while index1 == index2:
                index2 = np.random.randint(0, self.sizePop-1)
            newPop.append(copy.deepcopy(self.population[index1]))
            newPop.append(copy.deepcopy(self.population[index2]))
            seed = np.random.random()
            if seed < self.params[1]:
                swapIndex = np.random.randint(1, self.dimention - 2)
                for j in range(swapIndex, self.dimention - 1):
                    newPop[i].geneCode[j] = int(newPop[i].geneCode[j]+(newPop[i+1].geneCode[j]-newPop[i].geneCode[j])*self.params[2])
                    newPop[i+1].geneCode[j] = int(newPop[i+1].geneCode[j]+(newPop[i].geneCode[j]-newPop[i+1].geneCode[j])*self.params[2])
                    # swap
        self.population = newPop

    def mutation(self):
        newPop = []
        for i in range(0, self.sizePop):
            newPop.append(copy.deepcopy(self.population[i]))
            seed = np.random.random()
            if seed < self.params[0]:
                mutateIndex = np.random.randint(0, self.dimention - 1)
                # alpha = np.random.random()
                # if alpha < 0.5:
                newPop[i].geneCode[mutateIndex] = int((self.bound[1, mutateIndex]-mutateIndex) ** (1 - self.t / self.maxGen))
                # else:
                #     newPop[i].geneCode[mutateIndex] = int((self.dimention-mutateIndex)**(1-self.t/self.maxGen))
        self.population = newPop

    def bigBang(self):
        self.initUnit()
        self.evaluate()
        self.best = np.max(self.fitness), np.argmax(self.fitness), copy.deepcopy(self.population[np.argmax(self.fitness)])
        self.aveFitness = np.mean(self.fitness)
        self.trace[self.t, 0] = (1 - self.best[0])/self.best[0]
        self.trace[self.t, 1] = (1 - self.aveFitness)/self.aveFitness
        while(self.t < self.maxGen - 1):
            self.t += 1
            self.selection()
            # self.recombination()
            self.mutation()
            self.evaluate()
            self.best = np.max(self.fitness), np.argmax(self.fitness), copy.deepcopy(self.population[np.argmax(self.fitness)])
            self.aveFitness = np.mean(self.fitness)
            self.trace[self.t, 0] = (1 - self.best[0])/self.best[0]
            self.trace[self.t, 1] = (1 - self.aveFitness)/self.aveFitness

        self.done = True
        print('done')
        for i in range(0, self.sizePop):
            print(self.population[i].cityIndex)


class PlotGraph(GA):
    def __init__(self, sizePop, dimention, bound, maxGen, params):
        super.__init__(sizePop, dimention, bound, maxGen, params)
        global V
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.set_title("TSP")
        self.x_data, self.y_data = [], []
        self.length_text = self.ax.text(2, 95, '')
        self.line, = self.ax.plot([], [], 'g-', lw=2)

    def init(self):
        self.length_text.set_text('')
        self.line.set_data([], [])
        return self.line

    def generate(self):
        while not self.done:
            self.x_data, self.y_data = [], []
            for i in self.best[2].cityIndex:
                self.x_data.append(V[i][0])
                self.y_data.append(V[i][1])
            self.x_data.append(V[self.best[2].cityIndex[0]][0])
            self.y_data.append(V[self.best[2].cityIndex[0]][1])
            yield V[i][0], V[i][1], self.best[2].length

    def func(self, generate):
        self.length_text.set_text('length = %.2f' % self.best[2].length)
        self.line.set_data(self.x_data, self.y_data)
        return self.line

    def animationInit(self):
        self.draw = animation.FuncAnimation(self.fig, self.func, self.bigBang, init_func=self.init, blit=False, interval=50, repeat=False)


if __name__ == '__main__':
    bound = np.tile([[0], [sizePop-1]], sizePop)
    ga = GA(100, sizePop, bound, 2000, [0.1, 0.9, 0.25])
    ga.animationInit()
    plt.show()
