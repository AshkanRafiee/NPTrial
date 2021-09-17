import random
import string
import json
import time
import sys
import re
import requests
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)


# Generate Random 8-Char String
def gen_name():
    random_name = ''.join(random.sample(string.ascii_lowercase * 8, 8))
    return random_name

# Generate Random Password
def gen_pass():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    length = 12
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    random.shuffle(password)
    return("".join(password))

# Registers Random Mail on mail.tm
def mail_generator(random_name,random_password):
    response = requests.get('https://api.mail.tm/domains')
    response = response.json()
    domain = list(map(lambda x: x["domain"], response["hydra:member"]))[0]

    url     = "https://api.mail.tm/accounts"
    headers = {"Content-Type": "application/json"}
    body    = {"address": random_name+"@"+domain, "password": random_password}
    r       = requests.post(url, headers=headers, json=body)
    parsed  = r.json()
    email   = parsed["address"]
    return email

# Get Authorization Token from mail provider
def get_token(email,password):
    url     = "https://api.mail.tm/token"
    headers = {"Content-Type": "application/json"}
    body    = {"address": email, "password": password}
    r       = requests.post(url, headers=headers, json=body)
    parsed  = r.json()
    token   = parsed["token"]
    eid     = parsed["id"]
    return (eid,token)

# Get mail Count
def get_mail_count(token):
    url         = "https://api.mail.tm/messages"
    headers     = {"Authorization": "Bearer "+token}
    r           = requests.get(url, headers=headers)
    parsed      = r.json()
    mail_count  = parsed["hydra:totalItems"]
    return mail_count

# Get New Mail ID
def get_mail_id(token):
    url         = "https://api.mail.tm/messages"
    headers     = {"Authorization": "Bearer "+token}
    r           = requests.get(url, headers=headers)
    parsed      = r.json()
    mid         = parsed["hydra:member"][0]["id"]
    return mid

# Get Mail Reffered to Providing ID
def get_mail(mid,token):
    url = "https://api.mail.tm/messages/"+mid
    headers = {"Authorization": "Bearer "+token}
    r       = requests.get(url, headers=headers)
    parsed  = r.json()
    html    = parsed["html"][0]
    return html

# Generate Random Phone Number
def gen_phone():
    first = str(random.randint(100,999))
    second = str(random.randint(1,888)).zfill(3)
    last = (str(random.randint(1,9998)).zfill(4))
    while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
        last = (str(random.randint(1,9998)).zfill(4))

    return '{}-{}-{}'.format(first,second, last)

# Request Nessus Pro Trial
def request_trial(random_name,random_email,random_num):
    url = "https://www.tenable.com/evaluations/api/v1/nessus-pro"
    headers = {"Content-Type": "application/json"}
    body={"_mkto_trk": "", 
    "alert_email": "", 
    "apps": ["nessus"], 
    "code": "", 
    "company": random_name, 
    "companySize": "1-9", 
    "consentOptIn": True, 
    "country": "", 
    "email": random_email, 
    "essentialsOptIn": False, "first_name": random_name, 
    "last_name": random_name, 
    "lookbook": "", 
    "mkt_tok": "", 
    "partnerId": "", 
    "phone": random_num, 
    "pid": "", 
    "preferredSiteId": "", 
    "queryParameters": "utm_promoter=&utm_source=&utm_medium=&utm_campaign=&utm_content=&utm_term=&pid=&lookbook=&product_eval=nessus", 
    "referrer": "https://www.tenable.com/products/nessus/nessus-professional/evaluate?utm_promoter=&utm_source=&utm_medium=&utm_campaign=&utm_content=&utm_term=&pid=&lookbook=&product_eval=nessus", 
    "region": "", 
    "tempProductInterest": "Nessus Professional", 
    "title": random_name, 
    "utm_campaign": "", 
    "utm_content": "", 
    "utm_medium": "", 
    "utm_promoter": "", 
    "utm_source": "", 
    "utm_term": "", 
    "zip": ""}
    r = requests.post(url, headers=headers, json=body)
    parsed = r.json()
    message = parsed["message"]
    return message

# Parse Mail Body
def mail_parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    first_link = soup.find('a').get('href')
    return first_link

# Register at Tenable, Login and Get Trial Token
def nessus_login(activation_url,email,random_password):
    options = Options()
    options.headless = True
    options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

    driver.get(activation_url)
    driver.find_element_by_css_selector("input[name='password'][type='password'][placeholder='New password']").send_keys(random_password)
    driver.find_element_by_css_selector("input[name='password'][type='password'][placeholder='Confirm password']").send_keys(random_password)
    driver.find_element_by_css_selector("button[class='auth0-lock-submit'][type='submit']").click()

    print("I just Signed Up at Nessus with provided email and password!")
    print("Let's Login...")

    time.sleep(10)

    driver.get("https://community.tenable.com/login")
    time.sleep(5)
    driver.find_element_by_css_selector("input[type='email'][placeholder='Email Address']").send_keys(email)
    driver.find_element_by_css_selector("input[name='password'][type='password'][placeholder='Password']").send_keys(random_password)
    driver.find_element_by_css_selector("button[class='auth0-lock-submit'][type='submit']").click()

    print("Logged In! Let's Find the Activation Key...")

    time.sleep(2)

    driver.get("https://community.tenable.com/s/trials")
    time.sleep(5)
    driver.get("https://community.tenable.com/s/trials")
    time.sleep(10)

    active_code = driver.find_element_by_css_selector("span[class='evalCode']").text
    active_code = re.search(r'....-....-....-....',active_code).group()
    driver.close()
    return active_code

def main():
    # Generate Random Details
    random_name = gen_name()
    random_password = gen_pass()
    random_number = gen_phone()
    email = mail_generator(random_name,random_password)
    print("Your TempMail is: ",email)
    print("Your Password is: ",random_password)
    eid,token = get_token(email,random_password)
    print("Logged Into Email!")

    # Request Trial
    nessus_r = request_trial(random_name,email,random_number)
    print("Nessus Trial Response: ",nessus_r)
    print("--Usually it takes 10-15 mins to receive mail--")

    # Wait for mail, Register at Tenable, Login and Extract Activation Code
    if nessus_r == "Success":
        nessus_req_iter = 1
        mail_count = get_mail_count(token)
        wait_iter = 0
        while mail_count == 0:
            if nessus_req_iter >= 3:
                print("What the hell is wrong with Tenable...")
                Print("Try changing yout ip address and Run again!")
            if wait_iter >= 7:
                wait_iter = 0
                print("They Didn't Send it yet...")
                print("Requesting Trial Again...")
                nessus_r = request_trial(random_name,email,random_number)
                print("Nessus Trial Response: ",nessus_r)
                print("--Usually it takes 10-15 mins to receive mail--")
                nessus_req_iter += 1
            print("Still Got No Email, Waiting 2 Minute...")
            wait_iter += 1
            for remaining in range(120, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write("{:2d} seconds remaining.".format(remaining))
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\rChecking Mail...              \n")
            mail_count  = get_mail_count(token)

        mid = get_mail_id(token)
        html = get_mail(mid,token)
        activation_url = mail_parser(html)
        print("-----Got it!-----")
        print(activation_url)
        print("I'm Lazier than this... Let's Get the Activation Code!")
        active_code = nessus_login(activation_url,email,random_password)

        print("Your Active Code is:",active_code)

    else:
        print("Nessus Trial Request Failed!")

if __name__ == '__main__':
    main()