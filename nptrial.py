import secrets
import string
import requests

# Constants
PASSWORD_LENGTH = 12
PHONE_FORMAT = '{:3}-{:3}-{:4}'
DOMAINS_URL = 'https://api.mail.tm/domains'
ACCOUNTS_URL = 'https://api.mail.tm/accounts'
TOKEN_URL = 'https://api.mail.tm/token'
MESSAGES_URL = 'https://api.mail.tm/messages'
NESSUS_TRIAL_URL = "https://www.tenable.com/evaluations/api/v2/trials"
HEADERS = {"Content-Type": "application/json"}

# Function to handle HTTP GET requests
def make_get_request(url, headers={}):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    return response.json()

# Function to handle HTTP POST requests
def make_post_request(url, headers={}, json_data={}):
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()

# Generate Random 8-Char String
def gen_name():
    return ''.join(secrets.choice(string.ascii_lowercase) for _ in range(8))

# Generate Random Password
def gen_pass():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(characters) for _ in range(PASSWORD_LENGTH))

# Registers Random Mail on mail.tm
def mail_generator(random_name, random_password):
    domain_data = make_get_request(DOMAINS_URL)
    domain = domain_data["hydra:member"][0]["domain"]
    body = {"address": f"{random_name}@{domain}", "password": random_password}
    account_data = make_post_request(ACCOUNTS_URL, headers=HEADERS, json_data=body)
    return account_data["address"]

# Get Authorization Token from mail provider
def get_token(email, password):
    body = {"address": email, "password": password}
    token_data = make_post_request(TOKEN_URL, headers=HEADERS, json_data=body)
    return token_data["id"], token_data["token"]

# Get mail Count
def get_mail_count(token):
    headers = {"Authorization": f"Bearer {token}"}
    message_data = make_get_request(MESSAGES_URL, headers=headers)
    return message_data["hydra:totalItems"]

# Get New Mail ID
def get_mail_id(token):
    headers = {"Authorization": f"Bearer {token}"}
    message_data = make_get_request(MESSAGES_URL, headers=headers)
    return message_data["hydra:member"][0]["id"]

# Get Mail Referred to Providing ID
def get_mail(mid, token):
    headers = {"Authorization": f"Bearer {token}"}
    message_data = make_get_request(f"{MESSAGES_URL}/{mid}", headers=headers)
    return message_data["html"][0]

# Generate Random Phone Number
def gen_phone():
    first = secrets.randbelow(900) + 100
    second = secrets.randbelow(888) + 1
    last = secrets.randbelow(9998) + 1
    while last in {1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888}:
        last = secrets.randbelow(9998) + 1

    return PHONE_FORMAT.format(first, second, last)

# Request Nessus Pro Trial
def request_trial(random_name, random_email, random_num):
    body = {
        "skipContactLookup": "true",
        "product": "expert",
        "first_name": random_name,
        "last_name": random_name,
        "email": random_email,
        "phone": random_num,
        "title": random_name,
        "company": random_name,
        "companySize": "1-9",
        "apps": ["expert"]
    }
    response = make_post_request(NESSUS_TRIAL_URL, headers=HEADERS, json_data=body)
    return response["trial"]

def main():
    try:
        # Generate Random Details
        random_name = gen_name()
        random_password = gen_pass()
        random_number = gen_phone()
        email = mail_generator(random_name, random_password)
        print(f"Your TempMail is: {email}")
        print(f"Your Password is: {random_password}")

        # Request Trial
        nessus_trial_response = request_trial(random_name, email, random_number)
        print(f"Nessus Trial Response: {nessus_trial_response}")
        print(f"Use nessuscli.exe fetch --register {nessus_trial_response['code']} to activate your product")
        print("You can also use https://plugins.nessus.org/v2/offline.php for offline activation")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except Exception as err:
        print(f"An error occurred: {err}")  # Other errors

if __name__ == '__main__':
    main()
