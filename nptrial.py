import secrets
import string
import requests
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Constants
PASSWORD_LENGTH = 12
PHONE_FORMAT = '{:3}-{:3}-{:4}'
API_BASE_URL = 'https://api.mail.tm'
DOMAINS_URL = f'{API_BASE_URL}/domains'
ACCOUNTS_URL = f'{API_BASE_URL}/accounts'
TOKEN_URL = f'{API_BASE_URL}/token'
MESSAGES_URL = f'{API_BASE_URL}/messages'
NESSUS_TRIAL_URL = "https://www.tenable.com/evaluations/api/v2/trials"
HEADERS = {"Content-Type": "application/json"}

def perform_http_request(method, url, headers=None, json_data=None):
    headers = headers or HEADERS
    try:
        response = requests.request(method, url, headers=headers, json=json_data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Request error for {url}: {e}")
        raise

def gen_random_string(length, chars=string.ascii_lowercase):
    return ''.join(secrets.choice(chars) for _ in range(length))

def gen_pass():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return gen_random_string(PASSWORD_LENGTH, characters)

def gen_phone():
    parts = (
        secrets.randbelow(900) + 100,
        secrets.randbelow(900) + 100,
        secrets.randbelow(9000) + 1000,
    )
    return PHONE_FORMAT.format(*parts)

def register_email_account(name, password):
    domain = perform_http_request('GET', DOMAINS_URL)['hydra:member'][0]['domain']
    account_data = perform_http_request('POST', ACCOUNTS_URL, json_data={"address": f"{name}@{domain}", "password": password})
    return account_data["address"]

def main():
    try:
        random_name = gen_random_string(8)
        random_password = gen_pass()
        random_phone = gen_phone()
        email = register_email_account(random_name, random_password)
        logging.info(f"Your TempMail is: {email}\nYour Password is: {random_password}")

        trial_info = perform_http_request('POST', NESSUS_TRIAL_URL, json_data={
            "first_name": random_name, "last_name": random_name,
            "email": email, "phone": random_phone, "company": random_name,
            "companySize": "1-9", "product": "expert", "apps": ["expert"], "skipContactLookup": "true"
        })
        logging.info(f"Nessus Trial Response: {trial_info}")
        logging.info(f"Use nessuscli.exe fetch --register {trial_info['trial']['code']} to activate your product")
        logging.info("You can also use https://plugins.nessus.org/v2/offline.php for offline activation")
    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
