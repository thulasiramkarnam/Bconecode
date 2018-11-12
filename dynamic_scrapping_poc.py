from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import requests
import json
#todo iterate over the pages code is pending this is static page code
#todo implementing the loop for page or use Xpath to iterate over last 200 records

generic_elements = ['about us', 'facebook', 'privacy policy', 'newsletter', 'sitemap',
                 'feedback', 'archives', 'epaper', 'terms and conditions',
                 'advertise with us','twitter', 'google+', 'android',
                 'windows', 'windows phone', 'iphone', 'blackberry', 'ipad',
                 'advertise', 'disclaimer', 'investor', 'ombudsman',
                 'careers', 'service terms', 'terms and conditions',
                 'channel distribution', 'complaint redressal',
                    'advertising', 'events', 'subscriptions', 'group subscriptions',
                    'customer service', 'register', 'donate', 'videos', 'maps',
                    'africa', 'asia', 'europe', 'middle east', 'global commons', 'interviews',
                    'economics', 'environment', 'reviews', 'galleries', 'articles',
                    'shared', 'viewed', 'recent', 'site info', 'site news', 'terms & conditions',
                    'more about us', '<img', '<i']
generic_sub_links =['facebook.com', 'twitter.com', 'linkedin.com',
                 'play.google.com', 'itunes,apple.com','plus.google.com',
                    'pinterest.com', 'youtube.com']

content_htmltags = ['<span','<i' '<div', '<class', '<img']
page_elements = ['page', 'next']
page_elements.extend([ str(i) for i in range(100)])

with open('dynamic_scrap.json') as json_data_file:
    json = json.load(json_data_file)

lines_seen = set()        #creating empty set

def scrap_website(websitename, nextpage):
    counter = 0
    while nextpage:
        print (websitename)
        print ('afterwebsitename')
        html_page = requests.get(websitename)
        soup = BeautifulSoup(html_page.text,"lxml")
        
        for link in soup.findAll('a'):
            #finding the valid links to hover around
            
            content = link.contents
           
            if len(content) > 0:
                if len(str(content[0])) > 30 and (all(element not in str(content[0]) for element in generic_elements)):
                    url = link.get('href')
                    
                    if url is not None and (all(sublink not in url for sublink in generic_sub_links)):
                        
                        validate_link= str(url).startswith(base_website)
                        if validate_link is True or ('http' or 'https' in str(url)):
                            if url not in lines_seen:
                                lines_seen.add(url)
                        else:
                            if url not in lines_seen:
                                url = base_website + str(url)
                                lines_seen.add(url)
                elif len(str(content[0])) < 20:
                    
                    url = link.get('href')
                    print (url)
                    print ("after")
                    if url is not None and (all(sublink not in url for sublink in generic_sub_links)) and len(url) < len(websitename)+10:
                        if (any(str(i) in str(url) for i in page_elements)):
                            validate_link= str(url).startswith(base_website)
                            if validate_link is True or ('http' or 'https' in str(url)):
                                print (url)
                                print ("url of the next page website in if")
                                websitename = url
                                counter += 1
                                
                            else:
                                url = base_website + str(url)
                                print (url)
                                print ('url of the next page website in else')
                                websitename = url
                                counter += 1
                            if counter == 4:
                                nextpage = False
                                break
                          

website="https://www.thehindu.com/news/national"
base_website = "https://www.thehindu.com/news/national"
scrap_website(website, True)       
print ("After lines seen")
                    
