import argparse
import requests
import urllib.request
from html.parser import HTMLParser
import time
import random

class MyHTMLParser(HTMLParser):
    def __init__(self,date_url_file):
        HTMLParser.__init__(self)
        self.tag = None
        self.date_url = False
        self.href = None
        self.date_url_file = date_url_file



    def handle_starttag(self,tag,attrs):
        self.tag = tag
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.href = attr[1]

    
    def handle_endtag(self,tag):
        if tag == "li":
            if self.date_url == True:
                self.date_url = False
    
    def handle_data(self,data):
        '''
            it seems sometimes this function is called twice, anyone knows why?
        '''
        if "按日期查找" in data:
            self.date_url = True
        if self.tag == "a":
            if self.date_url == True and "[" in data:
                print(f"https:{self.href}",file=self.date_url_file)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-year",default="",type=str)
    configs = arg_parser.parse_args()

    if configs.year == "":
        print(f"Please enter the year")
        exit(0)
    
    year_url = "https://www.haodf.com/sitemap-zx/"+str(configs.year)+"/"

    date_url_file = open("date_url_"+str(configs.year),'w')

    html_parser = MyHTMLParser(date_url_file)

#     headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    headers = 


    request = urllib.request.Request(year_url,headers=headers)
    try:
        response = urllib.request.urlopen(request).read().decode('GBK')
        html_parser.feed(response)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(e.reason)
            time.sleep(random.random())

        
