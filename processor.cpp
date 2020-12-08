#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
using namespace std;

// OBJECT CONSTRUCTION
struct Video
{
	int views = 0;
	int likes = 0;
	int dislikes = 0;
	int comments = 0;
	int category = 0;
	string id = "";
	string title = "";
	string channel = "";
	string thumbnail = "";
	string trending = "";	// year.date.month
	string publish = "";	// year-month-dateTtime
	string link = "https://www.youtube.com/watch?v=";
	
};
string categorizer(int n)
{
	map<int, string> ctg = {
		{1, "Film & Animation"},
		{2, "Autos & Vehicles"},
		{10, "Music"},
		{15, "Pets & Animals"},
		{17, "Sports"},
		{19, "Travel & Events"},
		{20, "Gaming"},
		{21, "Videoblogging"},
		{22, "People & Blogs"},
		{23, "Comedy"},
		{24, "Entertainment"},
		{25, "News & Politics"},
		{26, "Howto & Style"},
		{27, "Education"},
		{28, "Science & Technology"},
		{29, "Nonprofits & Activism"},
		{30, "Movies"},
		{43, "Shows"}
	};
	return ctg[n];
}
Video videoConstruct(string s)
{
	Video vid;

	vid.id = s.substr(0, s.find(','));
		s = s.substr(s.find(',') + 1);

	vid.trending = s.substr(0, s.find(','));
		s = s.substr(s.find(',') + 1);
	
	// case handling of title and channels with commas
	if (s[0] == '"')
	{
		s = s.substr(s.find('"') + 1);
		vid.title = s.substr(0, s.find('"'));
		s = s.substr(s.find('"') + 2);
	}
	else
	{
		vid.channel = s.substr(0, s.find(','));
		s = s.substr(s.find(',') + 1);
	}

	if (s[0] == '"')
	{
		s = s.substr(s.find('"') + 1);
		vid.channel = s.substr(0, s.find('"'));
		s = s.substr(s.find('"') + 2);
	}
	else
	{
		vid.title = s.substr(0, s.find(','));
		s = s.substr(s.find(',') + 1);
	}

	vid.category = stoi(s.substr(0, s.find(',')));
		s = s.substr(s.find(',') + 1);

	vid.publish = s.substr(0, s.find(','));
		s = s.substr(s.find(',') + 1);

	vid.views = stoi(s.substr(0, s.find(',')));
		s = s.substr(s.find(',') + 1);

	vid.likes = stoi(s.substr(0, s.find(',')));
		s = s.substr(s.find(',') + 1);

	vid.dislikes = stoi(s.substr(0, s.find(',')));
		s = s.substr(s.find(',') + 1);

	vid.comments = stoi(s.substr(0, s.find(',')));
		s = s.substr(s.find(',') + 1);

	vid.thumbnail = s.substr(0, s.find(','));
		s = s.substr(s.find(',') + 1);

	vid.link = vid.link + vid.id;

	return vid;
}

// GRAPH CONSTRUCTION
class AdjacencyList
{
private:
	map<string, vector<string>> graph;
public:
	// create graph based on a video's views
	void createGraph(vector<Video>& arr, int c)
	{
		int totNeighbors = 0;
		int nodes = 0;
		for (int i = arr.size()-1; i > 0; i--)
		{
			string from = arr[i].id;
			if (from == "#NAME?")
				cout << "i: " << i;
			int fromViews = arr[i].views;
			int fromCategory = arr[i].category;
			if (fromCategory == c)
			{
				// increment nodes
				nodes++;
				int nodeNeighbors = 0;
				for (int j = i - 1; j >= 0; j--)
				{
					string to = arr[j].id;
					int toViews = arr[j].views;
					int toCategory = arr[j].category;
					// only connect to videos that are within one magnitude
					// and in the same category
					if ((toViews >= (fromViews / 10)) && (fromCategory == c))
					{
						graph[from].push_back(to);
						// increment neighbors
						totNeighbors++;
						nodeNeighbors++;
					}
					// cut data and break out of loop
					if (nodeNeighbors >= 100)
						break;
				}
				if (totNeighbors > 5000 || nodes >= 50)
					break;
			}
		}
	}
	// output edge list CSV by genre
	void outputGraph(int n)
	{
		string fileName = "../graphs/category_" + categorizer(n) + ".csv";
		ofstream graphFile(fileName);
		graphFile << "Source,Target\n";
		for (auto itr = graph.begin(); itr != graph.end(); itr++)
		{
			for (int i = 0; i < itr->second.size(); i++)
				graphFile << itr->first << "," << itr->second[i] << endl;
		}
		graphFile.close();
	}
};

// STATISTIC FUNCTIONS
void numberOfVideos(vector<Video>& arr)
{
	// [category] = numVideos
	map<int, int> chart;
	int totalVid = 0;
	for (int i = 0; i < arr.size(); i++)
	{
		chart[arr[i].category]++;
		totalVid++;
	}

	ofstream statsFile("../stats/numVideos.csv");
	statsFile << "Category,Number of Videos,Percent of Total\n";
	for (auto itr = chart.begin(); itr != chart.end(); itr++)
		statsFile << categorizer(itr->first) << "," << itr->second << "," << (double) itr->second / totalVid << endl;
	statsFile.close();
};
void averageViews(vector<Video>& arr)
{
	// [category] = <numViews, numVideos>
	map<int, pair<double, int>> chart;
	for (int i = 0; i < arr.size(); i++)
	{
		chart[arr[i].category].first += arr[i].views;
		chart[arr[i].category].second++;
	}
	ofstream statsFile("../stats/avgViews.csv");
	statsFile << "Category,Average Views\n";
	for (auto itr = chart.begin(); itr != chart.end(); itr++)
		statsFile << categorizer(itr->first) << "," <<(double)itr->second.first / (double)itr->second.second << endl;
	statsFile.close();
};
void averageComments(vector<Video>& arr)
{
	// [category] = <totalComments, numVideos>
	map<int, pair<int, int>> chart;
	for (int i = 0; i < arr.size(); i++)
	{
		chart[arr[i].category].first += arr[i].comments;
		chart[arr[i].category].second++;
	}
	ofstream statsFile("../stats/avgComments.csv");
	statsFile << "Category,Average Comments\n";
	for (auto itr = chart.begin(); itr != chart.end(); itr++)
		statsFile << categorizer(itr->first) << "," << (double)(itr->second.first / itr->second.second) << endl;
	statsFile.close();
};
void averageReaction(vector<Video>& arr)
{
	// [category] = <percentLikes, numVideos>
	map<int, pair<double, int>> chart;
	for (int i = 0; i < arr.size(); i++)
	{
		if (arr[i].dislikes != 0)
		{
			chart[arr[i].category].first += ((double)arr[i].likes / ((double)arr[i].likes + (double)arr[i].dislikes));
			chart[arr[i].category].second++;
		}
	}
	ofstream statsFile("../stats/avgReaction.csv");
	statsFile << "Category, Percent Liked, Percent Disliked\n";
	for (auto itr = chart.begin(); itr != chart.end(); itr++)
	{
		double avgLikes = itr->second.first / itr->second.second;
		double avgDislikes = 1 - avgLikes;
		statsFile << categorizer(itr->first) << "," << avgLikes << "," << avgDislikes << endl;
	}
	statsFile.close();
};
void averageViewReaction(vector<Video>& arr)
{
	// [category] = <reactionToViews, numVideos>
	map<int, pair<double, int>> chart;
	for (int i = 0; i < arr.size(); i++)
	{
		chart[arr[i].category].first += ((double)arr[i].likes / arr[i].views);
		chart[arr[i].category].second++;
	}
	ofstream statsFile("../stats/viewReaction.csv");
	statsFile << "Category,Percent Viewers Who Like\n";
	for (auto itr = chart.begin(); itr != chart.end(); itr++)
		statsFile << categorizer(itr->first) << "," << (double)(itr->second.first / itr->second.second) << endl;
	statsFile.close();
};
void commentReaction(vector<Video>& arr)
{
	ofstream statsFile("../stats/comReaction.csv");
	statsFile << "Video Reaction,Video Comments\n";
	for (int i = 0; i < arr.size(); i++)
	{
		if (arr[i].dislikes != 0)
		{
			double reactionRatio = ((double)arr[i].likes / ((double)arr[i].likes + (double)arr[i].dislikes));
			double percentComment = ((double)arr[i].comments / arr[i].views);
			statsFile << reactionRatio << "," << percentComment << endl;
		}
	}	
	statsFile.close();
};

// SORTING FUNCTIONS
void vidSwap(Video* a, Video* b)
{
	Video t = *a;
	*a = *b;
	*b = t;
}
int partition(vector<Video>& arr, int low, int high)
{
	int pivot = arr[high].views;
	int i = (low - 1);
	for (int j = low; j <= high - 1; j++)
	{
		if (arr[j].views <= pivot)
		{
			i++;
			vidSwap(&arr[i], &arr[j]);
		}
	}
	vidSwap(&arr[i + 1], &arr[high]);
	return (i + 1);
}
void quickSort(vector<Video>& arr, int low, int high)
{
	if (low < high)
	{
		int pivot = partition(arr, low, high);
		quickSort(arr, low, pivot - 1);
		quickSort(arr, pivot + 1, high);
	}
}
void insertionSort(vector<Video>& arr, int size)
{
	for (int i = 1; i < size; i++)
	{
		Video key = arr[i];
		int j = i - 1;

		while (j >= 0 && arr[j].views > key.views)
		{
			arr[j + 1] = arr[j];
			j--;
		}
		arr[j + 1] = key;
	}
}


// MAIN CODE
int main()
{
	vector<Video> vidArray;
	vector<Video> copy;

	// load Video objects from csv files
	string files[3] = { "USvideos.csv", "CAvideos.csv", "GBvideos.csv" };
	for (int i = 0; i < 3; i++)
	{
		string line;
		ifstream dataFile("../data/" + files[i]);
		getline(dataFile, line);
		while (getline(dataFile, line))
			vidArray.push_back(videoConstruct(line));
		dataFile.close();
	}
	// sort vector by views
	//insertionSort(vidArray, vidArray.size());
	//copy = vidArray;
	quickSort(vidArray, 0, vidArray.size()-1);

	// create a graph by genre and output edge list CSV
	int category[17] = { 1,2,10,15,17,19,20,22,23,
						24,25,26,27,28,29,30,43 };
	for (int i = 0; i < 17; i++)
	{
		AdjacencyList g;
		g.createGraph(vidArray, category[i]);
		g.outputGraph(category[i]);
	}

	// output csv files with calculated statistics
	numberOfVideos(vidArray);
	averageViews(vidArray);
	averageComments(vidArray);
	averageReaction(vidArray);
	averageViewReaction(vidArray);
	commentReaction(vidArray);
	
	return 0;
}
