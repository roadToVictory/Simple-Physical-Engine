import numpy as np
import os
import matplotlib.pyplot as plt
from math import sin
from math import cos
from configparser import ConfigParser
cfg=ConfigParser()
cfg.read('app_config.ini')
cfg.sections()

# To produce a data:
# put phone into the ball (it produce noice in the data)
# leave the ball in one place for some time (about 5 sec) so i can recognize when the move starts (break)
# push the ball (move starts)
# make another move but keep in mind that there must be a break between moves 
# at the end also make a break because the last data will be noice produced by pulling out the phone from the ball

#class Parser contains static methods to parse data from files and data array to store loded data
class Parser():
    data=[]
    gendata=[]
    @staticmethod
    def readFile(fname):
        # all in one 2D array 
        # Time (s), X (m/s2), Y (m/s2), Z (m/s2), R (m/s2), Theta (deg), Phi (deg)
        dataFromFile = np.genfromtxt(fname, delimiter=',', skip_header=4)
        return dataFromFile

     # function to draw chart from arr in time and save to filename
    @staticmethod
    def savePlot(time,X,arr,filename):
        # plt.figure()
        plt.plot(time,X, label="X")
        plt.plot(time,arr, label="R")
        plt.xlabel("time")
        plt.ylabel("X")
        plt.legend()
        plt.savefig(filename)
        plt.cla()

    @staticmethod
    def savePlot2(time,X,filename):
        # plt.figure()
        plt.plot(time,X, label="X")
        plt.xlabel("time")
        plt.ylabel("X")
        plt.legend()
        plt.savefig(filename)
        plt.cla()

    def recalculatedata():
        # print(Parser.data[0][0])
        for i in range(len(Parser.data)):
            for v in range(len(Parser.data[i])):
                Parser.data[i][v][1]=Parser.data[i][v][4]*sin(Parser.data[i][v][5])*cos(Parser.data[i][v][6])
                Parser.data[i][v][2]=-Parser.data[i][v][4]*sin(Parser.data[i][v][5])*sin(Parser.data[i][v][6])
                Parser.data[i][v][3]=Parser.data[i][v][4]*cos(Parser.data[i][v][5])

    #iterate over data in dataPath, parse data and draw plots, plots are named after data files
    @staticmethod
    def readAllData():
        files = os.listdir(cfg.get('parser','dataPath'))
        for file in files:
            fname=os.path.join(cfg.get('parser','dataPath'), file)
            print(fname)
            if os.path.isfile(fname):
                dataFromFile=Parser.readFile(fname)
                # separate arrays
                Time = dataFromFile[:,0]
                # X = dataFromFile[:,1]
                # Y = dataFromFile[:,2]
                # Z = dataFromFile[:,3]
                R = dataFromFile[:,4]
                # Theta = dataFromFile[:,5]
                # Phi = dataFromFile[:,6]

                def condition(arr):
                    if np.min(arr) < 10.3 and np.min(arr) > 9.7 and np.max(arr) < 10.3 and np.max(arr) >9.7:
                        return True
                    return False

                # searching for short breaks 
                # 0 - break, 1 - throw
                divide = [1 for _ in range(len(R))]

                i = 0
                while(i<len(R)-10):
                    if condition(R[i:i+10]):
                        for j in range(10):
                            divide[i+j] = 0
                        i+=10
                    else:
                        i+=1

                tmp = 1
                prev1 = divide.index(1)
                prev0 = divide.index(0)
                while tmp:
                    try:
                        next1 = divide.index(1,prev0)
                        next0 = divide.index(0,prev1)
                        # deleting small breaks in moves
                        if next1 - prev0 < 30:
                            for j in range(next1 - prev0):
                                divide[prev1+j] = 1

                        # deleting small moves in breaks
                        if next0 - prev1 < 70:
                            for j in range(next0 - prev1):
                                divide[prev1+j] = 0
                        prev1 = next1
                        prev0 = next0

                    except ValueError:
                        tmp = 0
                
                # marking first and last 20 as move 
                for i in range(20):
                    divide[i] = 1
                    divide[-i-1] = 1

                # list of indexes where throws starts and ends
                indexes = [divide.index(1,divide.index(0))]
        
                tmp = 1
                while tmp:
                    try:
                        indexes.append(divide.index(0,indexes[-1]))
                        indexes.append(divide.index(1,indexes[-1]))
                    except ValueError:
                        tmp = 0

                indexes.pop()
                
                for i in range(0,len(indexes),2):
                    Parser.data.append(dataFromFile[indexes[i]:indexes[i+1]])
                    
    @staticmethod
    def readGenData():
        files = os.listdir(cfg.get('parser','genPath'))
        for file in files:
            fname=os.path.join(cfg.get('parser','genPath'), file)
            print(fname)
            if os.path.isfile(fname):
                dataFromFile=Parser.readFile(fname)
                Parser.gendata.append(dataFromFile)