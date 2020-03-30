'''
    using urls to extract full conversation on different pages
    store different parts of conversation respectively
'''

import argparse
from html.parser import HTMLParser
import requests
import urllib.request
from tqdm import tqdm
import time
import random




class MyHTMLParser(HTMLParser):
    '''
        html parser, extract conversations between doctors and patients
    '''
    def __init__(self,output_file):
        HTMLParser.__init__(self)
        self.patient = False
        self.doctor = False
        self.patient_subtitle = False # whether patients are answering description query, compare self.allow_print
        self.doctor_subtitle = False
        self.tag = None
        self.allow_print = False # used to seperate subtitle and patient response
        self.conversing = True
        self.cnt = 0
        self.output_file = output_file
        self.total_page = 1 
        self.is_total_page_number = False
        self.url = None
        self.current_url = None
        self.final_diagnosis = False
        self.doctor_info = False
        self.doctor_faculty = ""
        self.current_page = 1
        self.first_description = True
        

    def handle_starttag(self,tag,attrs):
        '''
            called when facing starttag, 
        '''
        self.tag = tag
        if tag == "p":
            if ("class","doctor-faculty") in attrs:
                self.doctor_info = True
            for att in attrs:
                if att[0] == "class":
                    if att[1] == "f-c-r-w-text": # patient response
                        self.patient = True
                        # subtitle followed by patient response, don't disable subtitle mode
                    elif att[1] == "f-c-r-doctext":
                        self.doctor = True
        elif tag == "h4":
            # this part is the description submitted by patients
            for att in attrs:
                if att[0] == "class" and att[1] == "f-c-r-w-subtitle":
                    self.patient_subtitle = True
                    self.allow_print = True
        elif tag == "a":
            if ("class","page_turn_a") in attrs and ("rel","true") in attrs:
                self.is_total_page_number = True
        elif tag == "div":
            if ("class","f-c-r-tip") in attrs:
                self.patient_subtitle = False


    def handle_endtag(self,tag):
        '''
            return to initial process status
        '''
        self.patient = self.doctor = False
        # if tag != 'h4':
            # self.patient_subtitle = False
        # if self.is_total_page_number == True:
        self.is_total_page_number = False
        if tag == "p":
            # if self.final_diagnosis == True:
            self.final_diagnosis = False
            # if self.doctor_info == True:
            self.doctor_info = False

    

    def handle_data(self,data):
        '''
            handle data respectively
        '''
        data = data.replace("\n","")
        
        if self.tag == 'h4':
            if self.patient_subtitle == True and self.allow_print == True: # and "病情摘要及初步印象" not in data
                # print description title            
                if self.conversing == True:
                    if self.first_description == True:
                        self.first_description = False
                        if "病情摘要及初步印象" not in data and "总结建议" not in data:
                            self.cnt += 1
                            print(f"\n\nid={self.cnt}",file=self.output_file)
                            print(f"{self.url}",file=self.output_file)
                            print(f"\nDoctor faculty\n{self.doctor_faculty}",file=self.output_file)
                            print(f"\nDescription",file=self.output_file)
                            self.conversing = False            
                
                stripped_data = data.strip(' \n')
                if stripped_data[-1] != ':':
                    stripped_data += ':'
                if "病情摘要及初步印象" in data:
                    stripped_data = "\n\nDiagnosis and suggestions\n"+stripped_data
                if "疾病诊断:" in data:
                    stripped_data = "\n\nDiagnosis and suggestions\n"+stripped_data
                if "检查资料(" not in data:
                    print(f"{stripped_data}",end=' ',file=self.output_file)
                self.allow_print = False
                self.conversing = False
  
        if self.tag == 'p':
            if self.patient == True:
                # patient response   
                if self.patient_subtitle == False:
                    # response to doctors
                    if "病历资料仅医生和患者本人可见" not in data:
                        if self.conversing == False:
                            print(f"\nDialogue",end="",file=self.output_file)    
                        print(f"\n病人：\n{data.strip()}",end='',file=self.output_file)
                    self.conversing = True
                    
                else:
                    # response to description query
                    if "病历资料仅医生和患者本人可见" not in data:
                        print(f"\n{data.strip()}",file=self.output_file)
            elif self.doctor == True:
                # doctor response
                if "病情摘要/结论" in data:
                    self.final_diagnosis = True
                    data = data.replace(" ","").replace("病情摘要/结论：","").replace("病情摘要及初步印象：","\n病情摘要及初步印象：\n").replace("总结建议：","\n总结建议：\n")
                    print(f"\n\nDiagnosis and suggestions{data}",file=self.output_file)
                    self.conversing = False
                else:
                    if self.conversing == False:
                        print(f"\nDialogue",end="",file=self.output_file)
                    data = data.strip()
                    print(f"\n医生：\n{data}",end='',file=self.output_file)
                    self.conversing = True


        if self.tag == 'a':
            if self.is_total_page_number == True:
                self.total_page = max(self.total_page,int(data.lstrip("共&nbsp;").rstrip("&nbsp;页")))
            if self.current_page == 1:
                if self.doctor_info == True:
                    self.doctor_faculty += data.strip()+" "


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-year",default="",type=str)
    arg_parser.add_argument("-start_id",default=1,type=int)
    configs = arg_parser.parse_args()

    if configs.year == "":
        print(f"Please enter the year")
        exit(0)
    if configs.start_id == 1:
        print("Please enter start_id")
        exit(0)
    
    url_file = open("all_urls_in_"+configs.year,'r')
    output_file = open("conversation_in_"+configs.year,'w')
    problematic_urls_file = open("problematic_urls_"+configs.year,'w')

    headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    # headers = 

    parser = MyHTMLParser(output_file)
    parser.cnt = configs.start_id - 1


    try_again = False
    conversation_url = None

    while True:
        # outer conversation loop
        if try_again == True:
            pass
        else:
            conversation_url = url_file.readline().strip()
            parser.url = conversation_url
            if conversation_url == "":
                break
        
        try:
            request = urllib.request.Request(conversation_url,headers=headers)
            time.sleep(0.3+0.1*random.random())
            response = urllib.request.urlopen(request).read().decode('GBK')
            try_again = False
            parser.total_page = 1
            parser.current_page = 1
            parser.doctor_info = False
            parser.first_description = True
            parser.doctor_faculty = ""
            parser.conversing = True
            response = response.replace("<br>","").replace("<br />","")
            parser.feed(response)

            if parser.total_page > 1:
                url_stem = conversation_url[:-4]
                # print(f"\nstem:\n{url_stem}")
                inner_page_try_again = False
                current_inner_page_number = 1
                while True:
                    # inner page loop(pages in the same conversation)
                    if not inner_page_try_again:
                        current_inner_page_number += 1
                        parser.current_page = current_inner_page_number
                    if current_inner_page_number == parser.total_page + 1:
                        break
                    page_url = url_stem+"_"+str(current_inner_page_number)+".htm"
                    # print(f"{page_url}")
                    try:
                        request = urllib.request.Request(page_url,headers=headers)
                        time.sleep(0.3+0.1*random.random())
                        response = urllib.request.urlopen(request).read().decode('GBK')
                        response = response.replace("<br>","").replace("<br />","")

                        inner_page_try_again = False
                        parser.feed(response)
                    except urllib.error.HTTPError as e:
                        if e.code == 403:
                            print(f"{page_url} {e.reason}")
                            time.sleep(2+random.random())
                            inner_page_try_again = True
                    except KeyboardInterrupt as e:
                        print(f"\n\nInner KeyboardInterrupt")
                        print(f"current url:\n{page_url}")
                        exit(0)
                    except Exception as e:
                        print(f"\n\nInner Exception!!!!")
                        print(e)
                        print(f"{page_url}\n",file=problematic_urls_file)
                        inner_page_try_again = False
                    
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"{conversation_url} {e.reason}")
                time.sleep(2+random.random())
                try_again = True
        except KeyboardInterrupt as e:
            print(f"\n\nKeyboardInterrupt")
            print(f"current url:\n{conversation_url}")
            exit(0)
        except Exception as e:
            print(f"\n\nException!!!!")
            print(e)
            print(f"{conversation_url}\n",file=problematic_urls_file)
            try_again = False

