from pyvis.network import Network
import matplotlib as matpb
import matplotlib.cbook as cbook
import pandas
from tkinter import *
import tkinter.ttk as tk

def graphMaker (filename):
    graphObj = Network (height = "720px", width = "1280px", bgcolor= "#222222", font_color= "white")
    graphObj.barnes_hut()

    #Default display options for graph

    data = pandas.read_csv("Data/" + filename + ".csv")  #change extension to CSV if need be

    #RENAME IF NECESSARY
    sourceNodes = data['Source']
    destNodes = data['Target']
    weightNodes = data ['Weight']   #remove from code later. FOR TESTING ONLY

    edges = zip(sourceNodes, destNodes, weightNodes)
    for i in edges:
        fromNode = i[0]
        toNode = i[1]
        weight = i[2]

        graphObj.add_node(fromNode,fromNode, title = fromNode)
        graphObj.add_node(toNode,toNode, title = toNode)
        graphObj.add_edge(fromNode, toNode, value = weight)

    reccomnededVids = graphObj.get_adj_list()
    graphObj.show("Visual Analysis for " + filename + " Videos on YouTube.html")

def StatsAnalysis(filename):
    data = pandas.read_csv("Data/" + filename + ".csv")  # change extension to CSV if need be
    vectorX = []
    vectorY = []

    for line in open ("Data/" + filename + ".csv"):
        values = [line.split(',')]
        vectorX.append(values[0])
        vectorY.append(values[1])
    matpb.plot(vectorX,vectorY)
    matpb.show()

if __name__ == '__main__':
    graphMaker("TestData2")