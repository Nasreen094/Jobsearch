import os.path
import sys
import yaml
import pprint
from config import *
import pymysql
import pandas as pd
from django.contrib.admin.templatetags.admin_list import results
import requests
import json
import random
import numpy as np
import requests
import itertools
#import urllib.request
from bs4 import BeautifulSoup
import re
import urllib
import time

#urllib.urlopen(url)
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai



global context


def faq(text):
    tex=[]
    new=[]
    ansr=[]
    dic={}
    url = "https://www.jobsireland.ie/en-US/FAQ"
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    exp=r"^\d+\.\s"

    divs=soup.findAll('div', {'class' :'col-lg-12'})

    for div in divs:
        qst=div.find('h4')
        if (qst):
            t=qst.text
            t=t.encode('ascii','ignore')
            tex.append(t)
        ans=div.find('p')
        if (ans):
            for a in ans:
                try:
                    c=a.text
                    c=c.encode('ascii','ignore')
                    new.append(c)
                except Exception, NavigableString: 
                        pass
    del new[17:19]
    questions = [ re.sub(exp, "", line) for line in tex if 
                                            re.search(exp, line) ]
    dic=dict(itertools.izip(questions, new))       
    if text in dic:
        out_dict['messageText'].append(dic[text])
        return out_dict
    else:
        out_dict['messageText'].append('Sorry..I didn\'t get that. Just click to see all our FAQ')
        out_dict["plugin"] = {'name': 'empyer_signin', 'type': 'link to signin', 'data': {'text': "FAQ", 'link': "https://www.jobsireland.ie/en-US/FAQ"}}
        #out_dict["plugin"] = {'name': 'link', 'type': 'faq', 'data': {'text': "FAQ", 'link': "https://www.jobsireland.ie/en-US/FAQ"}}
        return out_dict  
    
    
def job_search(json_data):
    if json_data['location'] == []:
            out_dict["messageText"].append(ask_location)
            #time.sleep(5) 
            out_dict["plugin"] = {'type': 'manufacturers', 'data': locations, 'name': 'popup'}
            return out_dict
    elif json_data['category'] == []:
            out_dict["messageText"].append(ask_category)
            out_dict["plugin"] = {'type': 'manufacturers', 'data': categories, 'name': 'popup'}
            print out_dict
            return out_dict
    elif json_data['Career_level'] == []:
            out_dict['messageText'].append(ask_career_level)
            out_dict["plugin"] = {'name': 'popup', 'type': 'manufacturers', 'data': Career_level}
            return out_dict
    elif json_data['Vacancy_type'] == []:
            out_dict['messageText'].append(random.choice(ask_vacancy_type))
            out_dict["plugin"] = {'name': 'popup', 'type': 'manufacturers', 'data': vacancy_type}
            return out_dict
    else:
            
            #out_dict['messageText'].append(random.choice(utter_results))
            PARAMS=json_data
            print PARAMS
            URL = "http://185.168.192.104/JiraApiv2/api/jv/v1.0/getAllJobDetails"
            headers = {'content-type': 'application/json'}
            r= requests.post(url = URL, data=json.dumps(PARAMS), headers=headers)
            #print r
            data = r.json()
            print data
            out_dict["test"]=data
            #print(len(data))
            #print (l)
            
            global length
            length=str(len(data))
            #print length
            '''
            length=str(np.random.randint(low=1500, high=5000))
            print length
            '''
            #length=str(len(jobs))
            if (length == "0"):
                utter_results=['Sorry, I couldn\'t find any results at the moment. So what\'s next?']
                out_dict['messageText'].append(utter_results)
                out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': failure_buttons}
                
            else:
                #utter_results=['Well, I\'ve found '+length+' jobs for you in '+json_data['location']+'!','Perfect! Here are the relevant vacancies in '+json_data['location']+'!']
                utter_results=['Great! I found '+length+' vacancies for you.']
                out_dict['messageText'].append(utter_results)
                out_dict["plugin"] = {'name': 'link', 'type': 'job lists', 'data': data}
            out_dict["data"]=json_data
            return out_dict

def candidate_search(json_data):
    if json_data['category'] == []:
            out_dict["messageText"].append(random.choice(ask_category_employer))
            out_dict["plugin"] = {'type': 'manufacturers', 'data': categories, 'name': 'popup'}
            print out_dict
            return out_dict
    elif json_data['Min_qualification'] == '':
            out_dict["messageText"].append(random.choice(ask_min_qualification))
            out_dict["plugin"] = {'type': 'manufacturers', 'data': min_qualification, 'name': 'popup'}
            return out_dict
            #out_dict['Results'] = [data['response']]
    elif json_data['Experience_years'] == '':
            out_dict['messageText'].append(ask_experience_years)
            out_dict["plugin"] = {'name': 'popup', 'type': 'manufacturers', 'data': experience_years}
            return out_dict   
    elif json_data['ability_skills'] == []:
            out_dict["messageText"].append(random.choice(ask_ability_skills))
            out_dict["plugin"] = {'type': 'manufacturers', 'data': ability_skills, 'name': 'popup'}
            return out_dict
    elif json_data['competency_skills'] == []:
            out_dict["messageText"].append(random.choice(ask_competency_skills))
            out_dict["plugin"] = {'type': 'manufacturers', 'data': competency_skills, 'name': 'popup'}
            return out_dict
    else:
            
            length=str(np.random.randint(low=1500, high=5000))
            print length
            if (length == "0"):
                utter_results=['Sorry, I couldn\'t find any results at the moment. So what\'s next?']
                out_dict['messageText'].append(utter_results)
                #out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': failure_buttons}
                
                
                
            else:
                utter_results=['Perfect! '+length+' suitable candidates for you! Can register/login to our site']
                out_dict['messageText'].append(random.choice(utter_results))
                out_dict["plugin"] = {'name': 'register/signin', 'type': 'link to signin', 'data': [{'text': "Register", 'link': "https://www.jobsireland.ie/#/employer-register"},{'text': "Sign in", 'link': "https://employer.jobsireland.ie/Account/WizzkiLogin"}]}
                #out_dict["plugin"] = {'name': 'link', 'type': 'employee lists', 'data': data}
                
            out_dict["data"]=json_data
            return out_dict  

def call_api(dict_input):
    global out_dict
    out_dict = {}
    out_dict['messageText'] = []
    out_dict['messageSource'] = 'messageFromBot'
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'de'
    request.resetContexts = False
    request.session_id = dict_input['user_id']
    request.query = dict_input['messageText']
    print(request.query)
            
    response = yaml.load(request.getresponse())
    pp = pprint.PrettyPrinter(indent=4)
    json_data = response['result']['parameters']
    pp.pprint(response)
    
    
    if response['result']['metadata']=={}:
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        return out_dict
    elif response['result']['metadata']['intentName'] == 'faq':
	from views import flag
	flag=1
        out_dict=faq(request.query)
        
        print out_dict
        return out_dict
    elif response['result']['metadata']['intentName'] == 'need help':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        return out_dict
    elif response['result']['metadata']['intentName'] == 'Default Fallback Intent':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        return out_dict
    elif response['result']['metadata']['intentName'] == 'change_location':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        out_dict["plugin"] = {'type': 'manufacturers', 'data': locations, 'name': 'popup'}
        return out_dict
    elif response['result']['metadata']['intentName'] == 'change_position':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        out_dict["plugin"] = {'name': 'popup', 'type': 'manufacturers', 'data': vacancy_type}
        return out_dict
    elif response['result']['metadata']['intentName'] == 'change category':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        out_dict["plugin"] = {'type': 'manufacturers', 'data': categories, 'name': 'popup'}
        return out_dict
    elif response['result']['metadata']['intentName'] == 'change career level':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        out_dict["plugin"] = {'name': 'popup', 'type': 'manufacturers', 'data': Career_level}
        return out_dict
    elif response['result']['metadata']['intentName'] == 'Default Welcome Intent':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': top_level_buttons}
        return out_dict
    elif response['result']['metadata']['intentName'] == 'login':
        if response['result']['parameters']['account'] == []:
            pp.pprint(response['result']['fulfillment']['messages'][0]['speech'])
            out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
            out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': sign_in}
            return out_dict
        elif response['result']['parameters']['account'] == ["Employer"]:
            out_dict['messageText'].append(employer_signin)
            out_dict["plugin"] = {'name': 'empyer_signin', 'type': 'link to signin', 'data': {'text': "sign in", 'link': "https://employer.jobsireland.ie/Account/WizzkiLogin"}}
            return out_dict
        else:
            out_dict['messageText'].append(jobseeker_signin)
            out_dict["plugin"] = {'name': 'empyee_signin', 'type': 'link to signin', 'data': {'text': "sign in", 'link': "https://jobseeker.jobsireland.ie/Account/UserLogin"}}
            return out_dict
    elif response['result']['metadata']['intentName'] == 'register':
        '''out_dict['data']=response['result']['parameters']['account']
        return out_dict'''
        if response['result']['parameters']['account'] == []:
            pp.pprint(response['result']['fulfillment']['messages'][0]['speech'])
            out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
            out_dict["plugin"] = {'name': 'autofill', 'type': 'items', 'data': sign_in}
            return out_dict
        elif response['result']['parameters']['account'] == ["Employer"]:
            out_dict['messageText'].append(employer_register)
            out_dict["plugin"] = {'name': 'empyer_register', 'type': 'link to signup', 'data': {'text': "Sign Up", 'link': "https://www.jobsireland.ie/#/employer-register"}}
            return out_dict
        else:
            out_dict['messageText'].append(jobseeker_register)
            out_dict["plugin"] = {'name': 'empyee_register', 'type': 'link to signup', 'data': {'text': "Sign Up", 'link': "https://jobseeker.jobsireland.ie/Account/UserLogin"}}
            return out_dict
    elif response['result']['metadata']['intentName'] == 'Job Search':
        out_dict=job_search(json_data)
        print out_dict
        return out_dict
    elif response['result']['metadata']['intentName'] == 'candidate search':
        out_dict=candidate_search(json_data)
        print out_dict
        return out_dict
        
