#Ask Mostafa if anyhting isn't clear
from sqlite3 import Date
from attr import NOTHING
import pandas as pd
import matplotlib.pyplot as plt
from regex import F
from statsmodels.graphics import tsaplots
import os 
import sys
import seaborn as sns
import numpy as np; np.random.seed(42)
from pandas.plotting import autocorrelation_plot
from scipy.stats import pearsonr, spearmanr
import re
# pipreqs
# Add the Data using pandas
if len(sys.argv) == 1:
    print("No file was dropped\n")
    print("please Drag and Drop the file")
    exit()
nmu = len(sys.argv)
droppedFile = []
Corpus = [] # Create a dictionary
seabornsns = []
name = []
x = []
y = []

for i in range(1,nmu):
    droppedFile.append(sys.argv[i]) 

for i in range(0,len(droppedFile)): # Loop through the files
    Corpus.append(pd.read_csv(droppedFile[i], encoding='latin-1')) # Read the file

for i in range(0,len(droppedFile)):
    name.append(os.path.basename(droppedFile[i]))

path = (r'.\/'+ ' & '.join(name)  + ' Results') # Create a folder with the name of the file


print ("""

   ▄███████▄  ▄█        ▄██████▄      ███         ███        ▄████████    ▄████████ 
  ███    ███ ███       ███    ███ ▀█████████▄ ▀█████████▄   ███    ███   ███    ███ 
  ███    ███ ███       ███    ███    ▀███▀▀██    ▀███▀▀██   ███    █▀    ███    ███ 
  ███    ███ ███       ███    ███     ███   ▀     ███   ▀  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
▀█████████▀  ███       ███    ███     ███         ███     ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
  ███        ███       ███    ███     ███         ███       ███    █▄  ▀███████████ 
  ███        ███▌    ▄ ███    ███     ███         ███       ███    ███   ███    ███ 
 ▄████▀      █████▄▄██  ▀██████▀     ▄████▀      ▄████▀     ██████████   ███    ███ 
             ▀                                                           ███    ███ 


""")

try: 
    os.mkdir(path)  # Create target Directory
except OSError as error: # If the folder already exists
    print(error)  # Print the error


def get_date_format(date):
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return "%Y-%m-%d"
    elif re.match(r"^\d{2}-\d{2}-\d{4}$", date):
        return "%d-%m-%Y"
    elif re.match(r"^\d{2}/\d{2}/\d{4}$", date):
        return "%m/%d/%Y"
    elif re.match(r"^\d{4}/\d{2}/\d{2}$", date):
        return "%Y/%d/%m"
    elif re.match(r"^\d{4}\d{2}\d{2}$", date):
        return "%Y%m%d"
    elif re.match(r"^\d{2}\d{2}\d{4}$", date):
        return "%d%m%Y"
    elif re.match(r"^\d{4}/\d{2}/\d{4}$", date):
        return "%Y/%m/%d"
    elif re.match(r"^\d{2} \w{3} \d{4}$", date):
        return "%d %b %Y"
    elif re.match(r"^\d{2} \w{4,9} \d{4}$", date):
        return "%d %B %Y"
    else:
        return None


try: 
    for i in range(0, len(Corpus)):
        dateform = get_date_format(Corpus[i]['DATE'].iloc[1].astype(str))
        Corpus[i]['DATE'] = pd.to_datetime(Corpus[i]['DATE'], format=dateform)
except:
    for i in range(0, len(Corpus)):
        dateform = get_date_format(Corpus[i]['DATE'].iloc[1])
        Corpus[i]['DATE'] = pd.to_datetime(Corpus[i]['DATE'], format=dateform)
else:
    print("No Date Column Found")


def menu(): # menu
    print("Choose the data you want to use")
    print("1. calculate all the data")
    print("2. Show all columns")
    print("3. Exit")
    return int(input("Enter your choice: "))

def selection(): # Selection of the data
    x =[]
    y =[]
    for i in range(0,len(Corpus)): # Loop through the files
        print(i,name[i]) # Print the name of the file
        for j in range(0,len(Corpus[i].columns)): # Loop through the columns
            print(j,Corpus[i].columns[j]) # Print the name of the columns
        print("") # Print a new line
    try: # Try to get the data
            print("Choose the X axis") # Print the message
            f = (int(input("Choose the Data: "))) # Get the data
            h = (int(input("Choose the Column: "))) # Get the data
            x.append(f) # Get the data
            x.append(Corpus[f].columns[h]) # Get the data
            print("Choose the Y axis")
            f = (int(input("Choose the Data: "))) # Get the data
            h = (int(input("Choose the Column: "))) # Get the data
            y.append(f) # Get the data
            y.append(Corpus[f].columns[h]) # Get the data
    except ValueError:
        print("Please enter a number") 
    return x, y

# Plot the Data
def scaterplot(x, y):
    sns.set()
    plt.scatter(x , y, s=100, color='red') # s is the size of the dots
    plt.title('Scatter plot of X='+x.name+" and Y="+y.name) # Title
    plt.xlabel(x.name) # X label
    plt.ylabel(y.name) # Y label
    fig = plt.gcf() # get current figure
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + "\/X=" + x.name + " Y=" + y.name + ".png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area

# Autocorrelation Plot
def autocorrelation(theData): 
    sns.set()
    autocorrelation_plot(theData)
    fig = plt.gcf() # get current figure
    plt.ylabel(theData.name)
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + "\/Autocorrelation Plot of " + theData.name + ".png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area


# Autocorrelation Plot
def autocorr2(theData):
    sns.set() 
    fig = tsaplots.plot_acf(theData, lags=10, color='g', title='Autocorrelation of '+ theData.name)
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.ylabel(theData.name)
    plt.draw() # draw the plot
    fig.savefig(path + "\/Autocorrelation2 of " + theData.name + ".png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area

# Descriptive Statistics
def Descriptive_Statistics(theData):
    with open(path + '\Descriptive Statistics.txt', 'a') as f: # Open the file
        f.write("Descriptive Statistics\n") # Write the title
        f.write(theData.name + "\n") # Write the name of the data
        f.write("Mean: "+ str(theData.mean()) +"\n") # Write the mean
        f.write("Median: "+ str(theData.median())+"\n") # Write the median
        f.write("Standard Deviation: "+ str(theData.std())+"\n") # Write the standard deviation
        f.write("Variance: "+ str(theData.var())+"\n") # Write the variance
        f.write("Skewness: "+ str(theData.skew())+"\n") # Write the skewness
        f.write("Kurtosis: "+ str(theData.kurt())+"\n") # Write the kurtosis
        f.write("Range: "+ str(theData.max() - theData.min())+"\n") # Write the range
        f.write("Interquartile Range: "+ str(theData.quantile(0.75) - theData.quantile(0.25))+"\n\n") # Write the interquartile range
        f.write("")
        f.write("")
        f.close()

#correlation
def correlation(x, y):
    with open(path + '\Correlation.txt', 'a') as f: # Open the file
        f.write("Correlation of X="+x.name+" and Y="+y.name+"\n") # Write the title
        f.write(str(pearsonr(x,y))+"\n") # Write the spearmanr
        f.write(str(spearmanr(x,y))+"\n")
        f.write("Correlation: "+ str(x.corr(y))+"\n") # Write the correlation
        f.write("Covariance: "+ str(x.cov(y))+"\n\n") # Write the covariance
        f.write("")
        f.write("")
        f.close()

def seaborn_sns(x, y):
    sns.countplot(x= x, y=y)
    fig = plt.gcf() # get current figure
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + "\/Seaborn.png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area
#histogram
def histogram(x):
    plt.hist(x, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
    plt.title('Histogram of X='+x.name) # Title
    plt.xlabel(x.name) # X label
    fig = plt.gcf() # get current figure
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + "\/Histogram of X=" + x.name + ".png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf()

# Boxplot
def boxplot(m,x=[]):
    sns.set()
    df = pd.DataFrame(data = np.random.random(size=(5, m)), columns = x) # Create a dataframe with m columns
    sns.boxplot(x="variable", y="value", data=pd.melt(df)) # Create the boxplot
    fig = plt.gcf() # get current figure
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + "\/Boxplot.png", dpi=200, bbox_inches='tight') # save the plot to file

def displacement(x,y):
    plt.plot(x,y)
    plt.title('Displacement of X='+x.name+" and Y="+y.name) # Title
    plt.xlabel(x.name) # X label
    plt.ylabel(y.name) # Y label
    fig = plt.gcf() # get current figure
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + "\/Displacement of X=" + x.name + " and Y=" + y.name + ".png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area

def heatmap(x,g):
    heatmap = sns.heatmap(x)
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':12}, pad=12);
    plt.title('Heatmap of X='+x.name+" and Y="+y.name) # Title
    plt.xlabel(x.name) # X label
    fig = plt.gcf() # get current figure
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + f"\/Heatmap {g} .png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area


def distplot(x,g):
    sns.distplot(x, hist=True, kde=True, bins=int(180/5), color = 'darkblue', hist_kws={'edgecolor':'black'}, kde_kws={'linewidth': 4})
    fig = plt.gcf() # get current figure
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + f"\/Distplot {g} of X=" + x.name + ".png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area

def distplot2(x,y):
    sns.distplot(x, hist=True, kde=True, bins=int(180/5), color = 'blue', hist_kws={'edgecolor':'black'}, kde_kws={'linewidth': 4})
    sns.distplot(y, hist=True, kde=True, bins=int(180/5), color = 'red', hist_kws={'edgecolor':'grey'}, kde_kws={'linewidth': 4})
    fig = plt.gcf() # get current figure
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + "\/Distplot of X=" + x.name + " and Y=" + y.name + ".png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area


def kdeplot(x,g):
    sns.kdeplot(x, shade=True, shade_lowest=False)
    fig = plt.gcf() # get current figure
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + f"\/KDEplot {g} .png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area

def jointplot(inpu,g):
    h = ['kde', 'scatter']
    for i in h:
        sns.jointplot(data=inpu, kind=i)
        fig = plt.gcf() # get current figure
        fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
        plt.draw() # draw the plot
        fig.savefig(path + f"\/Jointplot {g} " + i+ ".png", dpi=200, bbox_inches='tight') # save the plot to file
        plt.clf() # clear the plot area

def pairplot(x,g):
    h = ['scatter', 'reg', 'resid', 'kde', 'hex']
    for i in h:
        sns.pairplot(x, kind=i)
        fig = plt.gcf()
        fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
        plt.draw() # draw the plot
        fig.savefig(path + f"\/Pair {g} "+ i  + ".png", dpi=200, bbox_inches='tight') # save the plot to file
        plt.clf() # clear the plot area

def FacetGrid(x,y):
    sns.FacetGrid(x, y, height=5)
    fig = plt.gcf()
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + "\/FacetGrid.png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area

def lmplot(x,g):
    sns.lmplot(x, height=7)
    fig = plt.gcf()
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + f"\/lmplot {g}.png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area

def Factorplots(x,g):
    sns.scatterplot(x)
    fig = plt.gcf()
    fig.set_size_inches(32, 18) # set figure's size manually to your full screen (32x18)
    plt.draw() # draw the plot
    fig.savefig(path + f"\/Factorplots {g}.png", dpi=200, bbox_inches='tight') # save the plot to file
    plt.clf() # clear the plot area

def PairGrid(x,h):
    g = sns.PairGrid(x)
    g.map(plt.scatter, alpha=0.8)
    g.add_legend()
    g.savefig(path + f"\/PairGrid {h} .png", dpi=200, bbox_inches='tight') # save the plot to file

iner = menu()
if iner == 1:
    for i in range(0, len(Corpus)):
        g = name[i]
        pairplot(Corpus[i],g)
        PairGrid(Corpus[i],g)
        #lmplot(Corpus[i],g)
        Factorplots(Corpus[i],g)
        jointplot(Corpus[i],g)
        for x in list(Corpus[i].columns): # for each column in the dataframe
            for y in list(Corpus[i].columns): # for each column in the dataframe
                if x != y: # if the column is not the same as the row
                    #heatmap(Corpus[i])
                    if y != "DATE": # if the Y is not the date
                            scaterplot(Corpus[i][x], Corpus[i][y])
                            #distplot2(Corpus[i][x], Corpus[i][y])
                            #displacement(Corpus[i][x], Corpus[i][y])
                            if x != "DATE": # if the X is not the date
                                #correlation(Corpus[i][x], Corpus[i][y])
                                pass

        for x in list(Corpus[i].columns): # for each column in the dataframe
            if x != "DATE": # if the X is not the date
                Descriptive_Statistics(Corpus[i][x])
                autocorrelation(Corpus[i][x])
                autocorr2(Corpus[i][x])
                distplot(Corpus[i][x],g)
                kdeplot(Corpus[i][x],g)
                #histogram(Corpus[i][x])
elif iner == 2:
    x, y = selection()
    xdata = Corpus[x[0]][x[1]] # X data
    ydata =Corpus[y[0]][y[1]] # y data
    g = name[x[0]]
    if xdata.name != "DATE":
        Descriptive_Statistics(xdata) # Descriptive Statistics
        autocorrelation(xdata)
        autocorr2(xdata)
        correlation(xdata, ydata)
        distplot(xdata,g)
        kdeplot(xdata,g)
    histogram(xdata)
    scaterplot(xdata, ydata)
    distplot2(xdata, ydata)
    displacement(xdata, ydata)

elif iner == 3:
    exit()


#frbox = list(Corpus.columns) # get the column names
#frbox.remove("DATE") # remove the date column
#boxplot(len(frbox), frbox) # plot the boxplot

