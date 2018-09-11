
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib
import requests
import boto3
import re
import itertools
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import nltk
import pandas as pd


# In[2]:


def fetch_results(search_term, number_results, language_code = "en"):
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
    response.raise_for_status()

    return response.text


# In[3]:


def get_only_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html")
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    if ((("raw" in text.lower()) and ("material" in text.lower())) or ("composition" in text.lower()) or ("component" in text.lower())):
        return text
    else:
        pass


# In[12]:


def Start():
    List_of_commodities = []
    pg = requests.get("https://s3-eu-west-1.amazonaws.com/thulasi-ram-dum/scrapping_input/commodities_final.txt")
    sp = BeautifulSoup(pg.text, "html") 
    List_of_commodities.extend(sp.text.split(','))     
    data = pd.read_excel("https://s3-eu-west-1.amazonaws.com/thulasi-ram-dum/input.xlsx",header=None)
    input_list = [j for i in data.values.tolist() for j in i]

    qur = ['what raw materials are used for ** manufacturing','what are the cost drivers in ** manufacturing','** manufacturing process',
          'what are the direct raw materials affecting cost of ** manufacturing','Raw materials required for ** manufacturing'
          '** manufacturing process and raw materials required']


    writer = pd.ExcelWriter('Final_Raw_Materials_Fun.xlsx')
    for keyword in input_list:
        List1 = []
        F_List = []
        for q in qur:
            query = q.replace("**",keyword)
            html_data = fetch_results(query,4)
            List1.append(html_data)
        Link = []
        for i in List1:
            html_mod = BeautifulSoup(str(i),'html.parser')

            Title=[]
            data = html_mod.findAll('div',{'class':'rc'})
            for i in data:
                link = i.find("a",href = True)
                Link.append(link['href'])
            Link1 = []
        for i in Link:
            if "pdf" not in i.split('.')[-1]:
                if "aspx" not in i.split('.')[-1]:
                    Link1.append(i) 
        Final_dict = []
        for ind,text in enumerate(Link1):
            try: 
                text_data = get_only_text(text)
                words = word_tokenize(text_data)
                words = [word.lower() for word in words]
                words = [word for word in words if word.isalpha()]
                tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3),
                         stop_words = 'english')
                tfidf_matrix =  tf.fit_transform(words)
                idf = tf.idf_
                dict_idf = dict(zip(tf.get_feature_names(), idf))
                Final_dict.append(dict_idf)
            except:
                pass
        Dict = {}
        total_count = len(Final_dict)
        flat_list = []
        for ind,list_ in enumerate(Final_dict):
            for j in list(list_.keys()):
                flat_list.append(j)
        for elem in flat_list:
            count = 0
            for list_ in Final_dict:
                if elem in list(list_.keys()):
                    count += 1
                    Dict[elem] = count / total_count
        items = [(v, k) for k, v in Dict.items()]
        items.sort()
        items.reverse()
        items = [(k, v) for v, k in items]
        for item in items:
            if (item[0].lower() in List_of_commodities and item[1] > 0.10):
                F_List.append(item)
        print(F_List)
        pd.DataFrame(F_List).to_excel(writer,'output for '+str(keyword),header=False, index=False)
    writer.save()
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('Final_Raw_Materials_Fun.xlsx', 'output-thulasi', 'output.xlsx')
    object_acl = s3.ObjectAcl('output-thulasi','output.xlsx')
    response = object_acl.put(ACL='public-read')
    #s3.ObjectAcl('bucket_name','object_key')
    print ("given  public access to user successufully")


# In[13]:


if __name__ == "__main__":
    Start()

