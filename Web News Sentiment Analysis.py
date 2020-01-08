import csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from matplotlib import style
from bs4 import BeautifulSoup
import requests
from newspaper import Article
from tkinter import *



#--------------------------------------------------------------------

def pert2(count,tot):
    p = (count/tot)*100
    return p

def sports(url):
        
    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'html5lib') 
    #print(soup.prettify()) 

    #elements = soup.find('div', attrs = {'class':'top-newslist small'})
    #print(elements.href.text)

    elements = []
    for r in soup.findAll('ul', attrs = {'data-msid':'4719148'}):
        elements.append(r)
    

    #print(elements)

    sp_article_links = []
       
    pattern = 'latest-videos'
    for e in elements:
        for row in e.findAll('li'):
            text = row.a['href'] #for checking if the pattern exists in the link
            if re.search(pattern,text):
                #print("\n News snippet eliminated!\n")
                continue
            elif re.search('http',text):
                pass
            #print(row.a['href'])
            else:
                text = "https://timesofindia.indiatimes.com"+text
            #print(text+"\n\n")
            sp_article_links.append(text)

    #print(sp_article_links)
    #print(len(sp_article_links))        


    sp_article_titles = []

    for a in sp_article_links:
        sp_article = Article(a,language="en")
        sp_article.download()
        sp_article.parse()
        sp_article.nlp()
        sp_article_titles.append(sp_article.title)

    print("\n\n Sports Article Titles: ")
    for i in sp_article_titles:
        print("\n"+i)


    #print("\n\n\n Articles: \n\n\n")
    temp_count=0


    #print("\n Sentiment Analysis: ")

    blob = []

    sp_polarity = []
    sp_subjectivity = []

    polarity = 0
    pcount = 0
    negcount = 0
    neucount = 0
    positive = 0
    negative = 0
    neutral = 0
    total = len(sp_article_titles)
    
    for i in sp_article_titles:
        temp = TextBlob(i)
        #print(temp.sentiment)

        if temp.sentiment.polarity > 0:
            pcount += 1
            #positive += temp.sentiment.polarity

        elif temp.sentiment.polarity == 0:
            neucount += 1
            #neutral += temp.sentiment.polarity

        elif temp.sentiment.polarity < 0:
            negcount += 1
            #negative +=temp.sentiment.polarity

    
        #sp_polarity.append(temp.sentiment.polarity)
        #sp_subjectivity.append(temp.sentiment.subjectivity)
        #blob.append(temp)        

    lofper = []     #list of percentages.

    lofper.append(pert2(pcount,total))
    lofper.append(pert2(neucount,total))
    lofper.append(pert2(negcount,total))

    style.use('ggplot')

    x = [5,8,11]
    y = [lofper[0],lofper[1],lofper[2]]

    plt.bar(x,y,color=['green','black','red'],align='center')

    plt.ylim(0, 100)     # set the ylim to bottom, top

    words = ['Positive','Neutral','Negative']

    plt.xticks(x,words)
    
    plt.title('Sports News Sentiment')
    plt.ylabel('Y-axis (In %)')
    plt.xlabel('X-axis (Sentiment)')

    plt.x_labels=['Positive','Neutral','Negative']
    
    plt.show()
    



def topnews(url):


    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'html5lib') 
    #print(soup.prettify()) 
    #elements = soup.find('div', attrs = {'class':'top-newslist small'})
    #print(elements.href.text)

    elements = []
    for r in soup.findAll('ul', attrs = {'data-vr-zone':'top_stories'}):
        elements.append(r)

    for r in soup.findAll('ul', attrs = {'data-vr-zone':'latest'}):
        elements.append(r)

    #print(elements)

    tn_article_links = []
           
    for e in elements:
        for row in e.findAll('li'):
            text = row.a['href'] #for checking if the pattern exists in the link
            #print(row.a['href'])
            if re.search('http',text):
                pass
            #if(text[0]!='h' and text[1]!='t' and text[2]!='t'):
            else:
                text = "https://timesofindia.indiatimes.com"+text
            #print(text+"\n\n")
            tn_article_links.append(text)
            #print(tn_article_links)
            #print(len(tn_article_links))        

            

    tn_article_titles = []
    for a in tn_article_links:
        tn_article = Article(a,language="en")
        tn_article.download()
        tn_article.parse()
        tn_article.nlp()
        tn_article_titles.append(tn_article.title)
    print("\n\n Top News Titles: ")
    for i in tn_article_titles:
        print("\n"+i)

    #print("\n\n\n Articles: \n\n\n")
    temp_count=0

        
    #print("\n Sentiment Analysis: ")

    blob = []

    tn_polarity = []
    tn_subjectivity = []

    polarity = 0
    pcount = 0
    negcount = 0
    neucount = 0
    positive = 0
    negative = 0
    neutral = 0
    total = len(tn_article_titles)
    

    for i in tn_article_titles:
        temp = TextBlob(i)
        #print(temp.sentiment)
        if temp.sentiment.polarity > 0:
            pcount += 1
            #positive += temp.sentiment.polarity

        elif temp.sentiment.polarity == 0:
            neucount += 1
            #neutral += temp.sentiment.polarity

        elif temp.sentiment.polarity < 0:
            negcount += 1
            #negative +=temp.sentiment.polarity

        #tn_polarity.append(temp.sentiment.polarity)
        #tn_subjectivity.append(temp.sentiment.subjectivity)
        #blob.append(temp)
            
    lofper = []   #list of percentages.

    lofper.append(pert2(pcount,total))
    lofper.append(pert2(neucount,total))
    lofper.append(pert2(negcount,total))

    style.use('ggplot')

    x = [5,8,11]
    y = [lofper[0],lofper[1],lofper[2]]

    plt.bar(x,y,color=['green','black','red'],align='center')

    plt.ylim(0, 100)     # set the ylim to bottom, top

    words = ['Positive','Neutral','Negative']

    plt.xticks(x,words)
    
    plt.title('Web News Sentiment')
    plt.ylabel('Y-axis (In %)')
    plt.xlabel('X-axis (Sentiment)')

    plt.x_labels=['Positive','Neutral','Negative']

    plt.show()
        

#------------------------------------------------------------------------------------------------

def initfornews(user_category):

    #non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    #Categories: city, India, world, business, sports, etimes(entertainment), education 
    #category_names=['city(0)','India(1)','world(2)','business(3)','sports(4)','entertainment(5)','education(6)']
    category_names=['1. Top News','2. Sports']
    #category = ['https://timesofindia.indiatimes.com/city','https://timesofindia.indiatimes.com/india','https://timesofindia.indiatimes.com/world','https://timesofindia.indiatimes.com/business','https://timesofindia.indiatimes.com/sports','https://timesofindia.indiatimes.com/etimes','https://timesofindia.indiatimes.com/education'];
    category = ['https://timesofindia.indiatimes.com/','https://timesofindia.indiatimes.com/sports'];
    #print(len(category))
    
    url=''

    #flask,django,tkinter

    if user_category=='1':
        url=category[0]
        topnews(url)
            
    elif user_category=='2':
        url=category[1]
        sports(url)
        
    
    #print("\n url: "+url)
    print()



#--------------------------------------------------------------------

class App(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		#Setup Menu
		#MainMenu(self)
		#Setup Frame
		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=100)
		container.grid_columnconfigure(0, weight=100)

		self.frames = {}

		for F in (StartPage, PageOne):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")


		self.show_frame(StartPage)
	def show_frame(self, context):
		frame = self.frames[context]
		frame.tkraise()

class StartPage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		label = Label(self, text="Start Page")
		label.pack(padx=10, pady=10)
		page_one = Button(self, text="News Analysis", command=lambda:controller.show_frame(PageOne))
		page_one.pack(pady=10)
		

class PageOne(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		label = Label(self, text="NEWS Analysis")
		label.pack(padx=10, pady=10)
		top_news = Button(self, text="TOP NEWS", command=lambda: initfornews('1'))
		top_news.pack(pady=10)
		sports = Button(self, text="SPORTS NEWS", command=lambda: initfornews('2'))
		sports.pack(pady=10)

		start_page = Button(self, text="Start Page", command=lambda:controller.show_frame(StartPage))
		start_page.pack(pady=20)


app = App()
app.mainloop()

