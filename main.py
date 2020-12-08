from pyvis.network import Network
from matplotlib import axes
import webbrowser
import numpy as np
from matplotlib import pyplot
import pandas
import tkinter as tk
import tkinter.ttk as ttk

def graphMaker (filename):
    graphObj = Network (height = "720px", width = "1280px", bgcolor= "#222222", font_color= "white")
    graphObj.barnes_hut()

    #Default display options for graph

    data = pandas.read_csv("graphs/" + filename + ".csv")
    extraDataCA = pandas.read_csv("data/CAvideos.csv")
    extraDataUSA = pandas.read_csv("data/USvideos.csv")
    extraDataGB = pandas.read_csv("data/GBvideos.csv")

    vectorLikes = np.concatenate((extraDataGB['likes'],extraDataUSA['likes'],extraDataCA['likes']))
    vectorDislikes = np.concatenate((extraDataGB['dislikes'],extraDataUSA['dislikes'],extraDataCA['dislikes']))
    vectorComments = np.concatenate((extraDataGB['comment_count'],extraDataUSA['comment_count'],extraDataCA['comment_count']))
    vectorViews = np.concatenate((extraDataGB['views'],extraDataUSA['views'],extraDataCA['views']))
    vectorTitles = np.concatenate((extraDataGB['title'],extraDataUSA['title'],extraDataCA['title']))
    vectorID = np.concatenate((extraDataGB['video_id'],extraDataUSA['video_id'],extraDataCA['video_id']))

    TitleMap = {}
    for i in range(0,len(vectorTitles)):
        TitleMap[vectorID[i]] = vectorTitles[i]

    InfoMap = {}
    for i in range(0, len(TitleMap)):
        views = " Views: " + str(vectorViews[i])
        likes = " Likes: " + str(vectorLikes[i])
        dislikes = " Dislikes: " + str(vectorDislikes[i])
        comments = " Number of Comments: " + str(vectorComments[i])
        tempList = [views , likes , dislikes , comments]
        InfoMap[TitleMap[vectorID[i]]] = tempList

    #RENAME IF NECESSARY
    sourceNodes = data['Source']
    destNodes = data['Target']

    edges = zip(sourceNodes, destNodes)
    for i in edges:
        fromNode = TitleMap[i[0]]
        toNode = TitleMap[i[1]]

        graphObj.add_node(fromNode,fromNode, title = fromNode)
        graphObj.add_node(toNode,toNode, title = toNode)
        graphObj.add_edge(fromNode, toNode)
    for node in graphObj.nodes:
        node["title"] += "\n<br>" + "<br>".join(InfoMap[node["id"]])
        node["value"] = 4
    graphObj.show("Visual Analysis for " + filename + " Videos on YouTube.html")

def buildGUI():
    #Creating the user interface with a function
    window = tk.Tk()  # Application Name
    window.title("Video Vis")  # Label
    window.geometry('1280x720')
    lbl = ttk.Label(window, text="Please search for a YouTube video category to display visual analysis: ", font = ("Arial Bold", 25)).pack()  # Click event

    def CategoryClick(event):
        selected = categoryDropDown.current()
        option = categories[selected]
        graphMaker(option)

    file = pandas.read_csv("stats/avgComments.csv")
    categoryDF = file['Category']
    categories = categoryDF.values.tolist()

    clicked = tk.StringVar()
    clicked.set(categories[0])

    categoryDropDown = ttk.Combobox(window, values=categories)
    categoryDropDown.current(0)
    categoryDropDown.bind('<<ComboboxSelected>>', CategoryClick)
    categoryDropDown.pack()

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
        vectorY = data[' Percent Liked']
        vectorZ = data[' Percent Disliked']
        r1 = np.arange(len(vectorX))

        p1 = pyplot.bar(x=vectorX, height=vectorY)
        pl = pyplot.bar(x=vectorX,height=vectorZ)
        pyplot.xticks(rotation=90)
        pyplot.title("Likes and Dislikes per Category")
        pyplot.show()

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

    avgViewsImage = tk.PhotoImage(file='png/004-vision.png')
    avgLikeImage = tk.PhotoImage(file="png/001-like.png")
    avgCommentImage = tk.PhotoImage(file="png/003-list.png")
    numVideosImage = tk.PhotoImage(file="png/006-number.png")
    viewReactionImage = tk.PhotoImage(file="png/002-eye.png")
    comReactionImage = tk.PhotoImage(file="png/005-watching-tv.png")

    avgViewsButton = ttk.Button(window, text = 'Average number of views per category', command = avgViews, image = avgViewsImage).place(x=25, y=150)
    avgLikeButton = ttk.Button(window, text='Average number of likes and dislikes per category', command=avgReaction, image = avgLikeImage ).place(x=615, y=150)
    avgCommentButton = ttk.Button(window, text = 'Average number of comments per category', command = avgComments, image = avgCommentImage).place(x=1127, y=150)
    numVideosButton = ttk.Button(window, text = 'Number of videos per category', command = numVideos, image = numVideosImage).place(x=25, y=450)
    viewReactionButton = ttk.Button(window, text = 'Comparing likes and dislikes to views per category', command = viewReaction, image = viewReactionImage).place(x=615, y=450)
    comReactionButton = ttk.Button(window, text = 'Compating likes and dislikes to comments per category', command = comReaction, image = comReactionImage).place(x=1127, y=450)

    window.mainloop()

if __name__ == '__main__':
    buildGUI()