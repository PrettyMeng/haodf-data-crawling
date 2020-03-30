import argparse
import requests
import urllib.request
from html.parser import HTMLParser
import time
import random
from tqdm import tqdm

class MyHTMLParser(HTMLParser):
    def __init__(self,output_file):
        HTMLParser.__init__(self)
        self.tag = None
        self.output_file = output_file
        self.total_page_number = -1
        self.start_collect = False
        self.href = None
        self.id = 0
        self.page_turn_a = False


    def handle_starttag(self,tag,attrs):
        self.tag = tag
        if ("class","hh") in attrs:
            self.start_collect = True
        if ("class","page_turn_a") in attrs:
            self.page_turn_a = True
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    self.href = attr[1]

    def handle_endtag(self,tag):
        if tag == "li":
            if self.start_collect == True:
                self.start_collect = False
        self.page_turn_a = False

    def handle_data(self,data):
        '''
            it seems sometimes this function is called twice, anyone knows why?
        '''
        if self.tag == "a" and self.start_collect == True:
            self.id += 1
            if self.id % 2 == 1:
                # alternatively, print id as well
                # print(f"\nid={int((self.id+1)/2)}\n{data}\nhttps:{self.href}",file=self.output_file)
               
                # alternatively, print only urls
                print(f"https:{self.href}",file=self.output_file)

        if self.page_turn_a == True:
            self.total_page_number = max(int(data),self.total_page_number)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-year",default="",type=str)
    configs = arg_parser.parse_args()

    if configs.year == "":
        print(f"Please enter the year")
        exit(0)

    date_urls = open("date_url_"+str(configs.year),'r').readlines()

    output_file = open("all_urls_in_"+str(configs.year),'w')

    error_date_url_file = open("error_date_url_"+str(configs.year),'w')

    parser = MyHTMLParser(output_file)

    headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    # headers = 



    for date_url_cpy in tqdm(date_urls):
        ###############################
        date_url = date_url_cpy.strip()
        # print(f"date_url:\n{date_url}")
        ##############################
        print(f"Crawl urls from:\n{date_url.strip()}")
        parser.total_page_number = -1
        current_page_number = 0
        try_again = False
        while(True):
            try:
                if not try_again:
                    current_page_number += 1
                    date_url = date_url[:-len(str(current_page_number-1))-1]+str(current_page_number)+"/"
                # print(f"date_url = {date_url}")
                request = urllib.request.Request(date_url,headers=headers)
                time.sleep(0.1+0.1*random.random())
                response = urllib.request.urlopen(request).read().decode('GBK')
                try_again = False
                parser.feed(response)
                if parser.total_page_number == current_page_number:
                    break
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print(f"{date_url} {e.reason}")
                    time.sleep(2+random.random()*2)
                    try_again = True
            except KeyboardInterrupt as e:
                print(f"\n\nKeyboardInterrupt")
                print(e)
                print(f"Interrupt Date URL:\n{date_url_cpy.strip()}, Interrupt Page: {current_page_number}\nInterrupt url:\n{parser.href}")
                exit(0)
            except UnicodeDecodeError as e:
                continue
            except Exception as e:
                print(f"\n\nException!!!!")
                print(e)
                print(f"Error Date URL:\n{date_url_cpy.strip()}, Error Page: {current_page_number}\nError url:\n{parser.href}\n")
                print(f"{date_url_cpy.strip()}\n",file=error_date_url_file)
                if parser.total_page_number == current_page_number:
                    break
                # exit(0)
        print(f"Total pages today: {parser.total_page_number}")
            
            






