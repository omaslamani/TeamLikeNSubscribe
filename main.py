from pyvis.network import Network
from matplotlib import axes
import numpy as np
from matplotlib import pyplot
import pandas
import tkinter as tk
import tkinter.ttk as ttk

def graphMaker (filename):
    graphObj = Network (height = "720px", width = "1280px", bgcolor= "#222222", font_color= "white")
    graphObj.barnes_hut()

    #Default display options for graph

    data = pandas.read_csv("graphs/" + filename + ".csv")  #change extension to CSV if need be

    #RENAME IF NECESSARY
    sourceNodes = data['Source']
    destNodes = data['Target']

    edges = zip(sourceNodes, destNodes)
    for i in edges:
        fromNode = i[0]
        toNode = i[1]

        graphObj.add_node(fromNode,fromNode, title = fromNode)
        graphObj.add_node(toNode,toNode, title = toNode)
        graphObj.add_edge(fromNode, toNode)

    reccomnededVids = graphObj.get_adj_list()
    graphObj.show("Visual Analysis for " + filename + " Videos on YouTube.html")

def buildGUI():
    #Creating the user interface with a function
    window = tk.Tk()  # Application Name
    window.title("Video Vis")  # Label
    window.geometry('1280x720')
    lbl = ttk.Label(window, text="Please search for a YouTube video category to display visual analysis: ", font = ("Arial Bold", 25)).pack()  # Click event

    def clickGraph():
        print("Generating " + name.get() + "genre graph")# Textbox widget
        graphMaker(name.get())

    name = tk.StringVar()
    nameEntered = ttk.Entry(window, width=150, textvariable=name).pack()  # Button widget
    button = ttk.Button(window, text="Search", command=clickGraph).pack()

    #Creating dropdown menu for stats analysis

    options = ('Average number of comments per category', 'Average number of views per category',
                  'Average number of likes and dislikes per category', 'Measuring audience reaction per category',
                  'Number of videos per category', 'Measuring reaction by views and comments per category')
    def comReaction():
        data = pandas.read_csv("stats/comReaction.csv")
        vectorX = data['Video Reaction']
        vectorY = data['Video Comments']
        pyplot.scatter(vectorX,vectorY, alpha=0.5)
        pyplot.title("Like and Dislike to Comments ratio")
        pyplot.show()
    def avgViews():
        data = pandas.read_csv("stats/avgViews.csv")
        vectorX = data['Category']
        vectorY = data['Average Views']
        pyplot.bar(x=vectorX, height=vectorY)
        pyplot.xticks(rotation=90)
        pyplot.title("Average Views per Category")
        pyplot.show()
    def avgComments():
        data = pandas.read_csv("stats/avgComments.csv")
        vectorX = data['Category']
        vectorY = data['Average Comments']
        pyplot.bar(x=vectorX, height=vectorY)
        pyplot.xticks(rotation=90)
        pyplot.title("Average Comments per Category")
        pyplot.show()
    def avgReaction():
        data = pandas.read_csv("stats/avgReaction.csv")
        vectorX = data['Category']
        vectorY = data['Percent Liked']
        vectorZ = data['Percent Disliked']
        """
        vectorX = data['Category']
        vectorY = data['Percent Liked']
        vectorZ= data['Percent Disliked']
        barWidth = 0.2
        r1 = np.arange(len(vectorY))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]

        index = np.arrange(17)
        p1 = pyplot.bar(index, vectorY,width = 0.2, x=vectorX)
        pl = pyplot.bar(r2, vectorZ)
        pyplot.show()
        
        """
    def numVideos():
        data = pandas.read_csv("stats/numVideos.csv")
        vectorX = data['Category']
        vectorY = data['Number of Videos']
        vectorZ = data['Percent of Total']
        vectorZ *= 100
        pyplot.bar(x=vectorX, height=vectorY)
        pyplot.xticks(rotation=90)
        pyplot.title("Number of Views per Category")
        pyplot.show()
        pyplot.pie(vectorZ, labels=vectorX)
        pyplot.axis('equal')
        pyplot.title("Percentage of total videos")
        pyplot.show()
    def viewReaction():
        data = pandas.read_csv("stats/viewReaction.csv")
        vectorX = data['Category']
        vectorY = data['Percent Viewers Who Like']
        vectorY *= 100
        pyplot.bar(x=vectorX, height=vectorY)
        pyplot.xticks(rotation=90)
        pyplot.title("Likes per View per Category")
        pyplot.show()
    def method_unknown():
        print ("IDK")

    def DropDownSelect(event):
        selected = dropDown.current()
        option = options[selected]
        functionMap ={
            'Average number of comments per category' : avgComments,
            'Average number of views per category': avgViews,
            'Average number of likes and dislikes per category': avgReaction,
            'Measuring audience reaction per category': viewReaction,
            'Number of videos per category': numVideos,
            'Measuring reaction by views and comments per category': comReaction
        }
        func = functionMap.get(option,method_unknown)
        func()

    dropDown = ttk.Combobox(window, values = options)
    dropDown.current(0)
    dropDown.bind('<<ComboboxSelected>>', DropDownSelect)
    dropDown.pack()
    window.mainloop()

if __name__ == '__main__':
    buildGUI()