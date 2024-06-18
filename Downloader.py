import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os
import re
import json

download_dir = 'downloads'
os.makedirs(download_dir, exist_ok=True)

def download_file(url, episode_number, directory):
    filename = os.path.join(directory, f"{episode_number}.mp4")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"=================================Downloaded: {filename}")

def extract_download_link(html_content, episode_number, directory):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', text=re.compile(r'1080.*mp4', re.IGNORECASE))
    if links:
        for link in links:
            print("Found link:", link['href'])
            download_link = link['href']
            download_file(download_link, episode_number, directory)
    else:
        print("No download link found for 1080P - mp4")


def process_episode(url, episode_number):
    session = requests.Session()

    # Step 1: Initial GET request to get the token
    response = session.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for episode {url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    token = None
    for script in soup.find_all('script'):
        script_content = script.string
        if script_content and 'grecaptcha.execute' in script_content:
            token = script_content.split("'")[1]
            break

    if not token:
        print(f"Token not found on page: {url}")
        return

    # Step 2: Make the POST request to get the download links
    data = {
        'captcha_v3': '03AFcWeA7RciEPBflmfMCWCnjAP8S3Zk8b4Gw8zaQ2vnMr-0Cn6l3O-u-ck84IMiTg1bzDq9Glhr-doZNGhM83PGQ4yE4jiK4x2bWHxWWt392aQTOfEE9UkSRAVtPKD83dSmHpnPV4vzKgHxKKsK2lIRwoXEaOjYjWE3uHDtoRI2dgzeZWVz4rBIYzC3QubujjkqBIxLt4dJL6hf0q_lWiMxGVr6hyrHo0ZqpM2JPQTrgqVJ67aZzQj4QgEyjcqHP9u650VyGYzcTFRB0hB5mIvnw3UyvewbWeqd1M4qagFW9vh2sW4WmnB1tXHOsfpB9Myem2mkaGHhA0ciijJxPFcbEcPYTN2GTX430qcb5hGT-3RaUqnx1UqeTGK6LxBANRooQvmORIbLpkqOF41XN_mGYhXENOLVXWcbzl3dFFbf10wJefZG91jpg7s0MLISI9NLf2hQnm112_z-1a3r5o3Ef24NQmOyg5vCSuL5BzKddBD6vs0EEJuXf8-D3AmMi9FFz1ax-NVM6NbCi4r-3y1_5VPfF6tCKrkIHkhTPOSUnLUUGUGhU6UryQBt4wcDJKU7Gd96rJvhudFoeSKI6kL6laboqGl8Y0rHj18Ejk9hcKmmeWnJGr54io_okQ0lT095l5R1RModIrSkl-xSZLzuJqbK1Cr7-F16IOIAZ2rR7Fz5WdRbevmPFSGEOH1GSyFY3B-2sQwF9m55U2y-Ew-o0zMJ07fY2uEA',
        'id': url.split('id=')[1].split('&')[0]
    }
    post_url = 'https://embtaku.com/download'
    response = session.post(post_url, data=data)
    if response.status_code != 200:
        print(f"Failed to retrieve download links for episode {url}")
        return

    html_content = response.text
    # print(f"HTML Content after POST: {html_content}")  # Print the HTML content received after POST request
    
    extract_download_link(html_content, episode_number,download_dir)


# 
with open('abcd.json', 'r') as file:
    links = json.load(file)
for episode_number, link in enumerate(links, start=1):
    if not link:
        print("Empty link found, skipping...")
        continue
    try:
        parsed_url = urlparse(link)
        query_params = parse_qs(parsed_url.query)
        episode_number = query_params.get('title', [''])[0]
        print(f"Processing link: {link}")
        # change the number with which you want to download 
        process_episode(link, episode_number)
    except Exception as e:
        print(f"An error occurred while processing link {link}: {e}")

print("Script completed.")

