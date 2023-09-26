import random
import string
import requests


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
    url = "https://www.tenable.com/evaluations/api/v2/trials"
    headers = {"Content-Type": "application/json"}
    body={
    "skipContactLookup":"true",
    "product":"expert",
    "first_name":random_name,
    "last_name":random_name,
    "email":random_email,
    "phone":random_num,
    "title":random_name,
    "company":random_name,
    "companySize":"1-9",
    "apps":["expert"]
    }
    r = requests.post(url, headers=headers, json=body)
    # print(r.status_code)
    # print(r.content)
    parsed = r.json()
    message = parsed["trial"]
    return message

def main():
    try:
        # Generate Random Details
        random_name = gen_name()
        random_password = gen_pass()
        random_number = gen_phone()
        email = mail_generator(random_name,random_password)
        print("Your TempMail is: ",email)
        print("Your Password is: ",random_password)

        # Request Trial
        nessus_r = request_trial(random_name,email,random_number)
        print("Nessus Trial Response: ",nessus_r)
        print(f"Use nessuscli.exe fetch --register {nessus_r['code']} to activate your product")
        print("You can also use https://plugins.nessus.org/v2/offline.php for offline activation")
    except:
        print("Something Wrong Happened!")

if __name__ == '__main__':
    main()
