import datetime
import pickle
import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

class Tableau :

    def __init__(self,filepath,resolution):

        with open(filepath, 'rb') as fp:
            tableau = pickle.load(fp)

        echeanceRun = tableau[0][0][0:13]
        self.dateRun = datetime.datetime(int(echeanceRun[0:4]),int(echeanceRun[5:7]),int(echeanceRun[8:10]),int(echeanceRun[11:13]),0)
        self.moyenne = Grandeur(resolution)
        self.moyenne.fill(tableau)

    def montrer(self):
        self.moyenne.montrerGrandeur()



class Grandeur :

    def __init__(self, resolution):
        self.resolution = resolution
        self.keyT = []
        self.keyValues = []

        self.t = []
        self.values = []
        self.smoothF = 0


    def fill(self, tableau):
        self.keyT = []
        self.values = [0] * (384 * self.resolution + 1)

        print(len(self.values))
        h = [int(i[1]) for i in tableau]

        for i in range(len(tableau)):
            self.keyT += [float(tableau[i][1])]
            self.keyValues += [sum(tableau[i][2:32]) / 30]

            if i < len(tableau)-1 :
                self.t += [self.keyT[i]+r/self.resolution for r in range(self.resolution*(int(tableau[i+1][1])-int(tableau[i][1])))]

        self.smoothF = interp1d(self.keyT, self.keyValues,kind='cubic')
        self.values = self.smoothF(self.t)

    def montrerGrandeur(self):
        plt.plot(self.t,self.values)
        plt.plot(self.keyT, self.keyValues, linestyle='None', marker='.')
        plt.show()





tableau1 = Tableau("data/2020121518.gefs",4)
tableau1.montrer()
