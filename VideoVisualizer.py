from pyvis.network import Network
import subprocess
from ttkthemes import ThemedTk
import numpy as np
from matplotlib import pyplot
import pandas
import tkinter as tk
import tkinter.ttk as ttk

def graphMaker (filename):
    graphObj = Network (height = "100%", width = "100%", bgcolor= "#222222", font_color= "white", heading="")
    graphObj.barnes_hut()
    graphObj.options = {
  "nodes": {
    "borderWidth": 2,
    "borderWidthSelected": 3,
    "color": {
      "border": "rgba(186,182,181,1)",
      "background": "rgba(247,27,0,1)",
      "highlight": {
        "border": "rgba(196,194,189,1)",
        "background": "rgba(255,29,0,1)"
      },
      "hover": {
        "border": "rgba(184,187,188,1)",
        "background": "rgba(255,55,0,1)"
      }
    }
  },
  "edges": {
    "arrowStrikethrough": False,
    "color": {
      "inherit": True,
      "opacity": 0.35
    },
    "font": {
      "strokeWidth": 28
    },
    "smooth": False
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -80000,
      "springLength": 250,
      "springConstant": 0.001
    },
    "minVelocity": 0.75
  }
}

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
    # Application Name
    window = ThemedTk(theme='equilux')
    bgColor = '#333231'
    window.configure(bg=bgColor)
    window.title("Video Vis")  # Label
    window.geometry('800x850')
    lbl = ttk.Label(window, text="Please search for a YouTube video category to display visual analysis: ", font=("Lato Bold", 15)).pack()  # Click event

    def CategoryClick(event):
        selected = categoryDropDown.current()
        option = categories[selected]
        graphMaker(option)

    file = pandas.read_csv("stats/avgComments.csv")
    categoryDF = file['Category']
    categories = categoryDF.values.tolist()

    clicked = tk.StringVar()
    clicked.set(categories[0])

    categoryDropDown = ttk.Combobox(window, values=categories, width=53, font = ("Lato 15"))
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
        pyplot.title("Like/Dislike Ratio to Comment Ratio")
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
        pyplot.title("Number of Videos per Category")
        pyplot.show()
        pyplot.pie(vectorZ, labels=vectorX)
        pyplot.axis('equal')
        pyplot.title("Percentage of Total Videos")
        pyplot.show()
    def viewReaction():
        data = pandas.read_csv("stats/viewReaction.csv")
        vectorX = data['Category']
        vectorY = data['Percent Viewers Who Like']
        vectorY *= 100
        pyplot.bar(x=vectorX, height=vectorY)
        pyplot.xticks(rotation=90)
        pyplot.title("Likes per View by Category")
        pyplot.show()

    lbl2 = ttk.Label(window, text="Select an icon to display graphical analysis: ",font=("Lato Bold", 15)).place(x=200,y=100)
    avgViewsImage = tk.PhotoImage(file='png/004-vision.png')
    avgLikeImage = tk.PhotoImage(file="png/001-like.png")
    avgCommentImage = tk.PhotoImage(file="png/003-list.png")
    numVideosImage = tk.PhotoImage(file="png/006-number.png")
    viewReactionImage = tk.PhotoImage(file="png/002-eye.png")
    comReactionImage = tk.PhotoImage(file="png/005-watching-tv.png")

    avgViewsButton = ttk.Button(window, text = 'Average number of views per category', command = avgViews, image = avgViewsImage).place(x=25, y=200)
    avgLikeButton = ttk.Button(window, text='Average number of likes and dislikes per category', command=avgReaction, image = avgLikeImage).place(x=331, y=200)
    avgCommentButton = ttk.Button(window, text = 'Average number of comments per category', command = avgComments, image = avgCommentImage).place(x=617, y=200)
    numVideosButton = ttk.Button(window, text = 'Number of videos per category', command = numVideos, image = numVideosImage).place(x=25, y=400)
    viewReactionButton = ttk.Button(window, text = 'Comparing likes and dislikes to views per category', command = viewReaction, image = viewReactionImage).place(x=331, y=400)
    comReactionButton = ttk.Button(window, text = 'Compating likes and dislikes to comments per category', command = comReaction, image = comReactionImage).place(x=617, y=400)

    avgViewLabel = ttk.Label(window, text = "Average Views", font = ("Lato Bold", 15)).place(x=33,y=350)
    avgLikeLabel = ttk.Label(window, text="Average Likes", font=("Lato Bold", 15)).place(x=345, y=350)
    avgCommentLabel = ttk.Label(window, text="Average Comments", font=("Lato Bold", 15)).place(x=607, y=350)
    numViewLabel = ttk.Label(window, text="Number of Videos", font=("Lato Bold", 15)).place(x=23, y=550)
    viewReactionLabel2 = ttk.Label(window, text="vs Views", font=("Lato Bold", 15)).place(x=365, y=570)
    viewReactionLabel = ttk.Label(window, text="Likes and Dislikes", font=("Lato Bold", 15)).place(x=327, y=550)
    comReactionLabel2 = ttk.Label(window, text="vs Comments", font=("Lato Bold", 15)).place(x=637, y=570)
    comReactionLabel = ttk.Label(window, text="Likes and Dislikes", font=("Lato Bold", 15)).place(x=615, y=550)

    speedFile = pandas.read_csv("stats/performance.txt")
    quickTime = "Quick Sort Time: " + str(speedFile["Time"][0]) + " milliseconds"
    mergeTime = "Shell Sort Time: " + str(speedFile["Time"][1]) + " milliseconds"
    quickLabel = ttk.Label(window, text=quickTime, font = ("Lato Bold", 15)).place(x=33, y=630)
    mergeLabel = ttk.Label(window, text = mergeTime, font = ("Lato Bold", 15)).place(x=33, y=670)


    window.mainloop()

if __name__ == '__main__':
    subprocess.call("processor.exe")
    buildGUI()