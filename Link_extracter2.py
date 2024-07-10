import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode
import json

def get_id_and_title(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the page. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    iframe_tag = soup.find('iframe', src=lambda value: 'streaming.php' in value)
    
    if iframe_tag:
        src = iframe_tag['src']
        
        parsed_url = urlparse(src)
        query_params = parse_qs(parsed_url.query)
        
        video_id = query_params.get('id', [None])[0]
        title = parsed_url.query.split('title=')[1].split('&')[0]
        
        return video_id, title
    else:
        raise Exception("Iframe with streaming.php not found on the page.")

def construct_download_url(video_id, title):
    base_url = "https://embtaku.com/download"
    params = {
        "id": video_id,
        "typesub": "animeflix",
        "title": title
    }
    return f"{base_url}?{urlencode(params)}"

def generate_download_links(base_url, num_episodes):
    download_links = []
    for episode in range(1, num_episodes + 1):
        episode_url = f"{base_url}-episode-{episode}"
        try:
            video_id, title = get_id_and_title(episode_url)
            if video_id and title:
                download_url = construct_download_url(video_id, title)
                download_links.append(download_url)
        except Exception as e:
            print(f"Error processing {episode_url}: {e}")
    
    return download_links

# Base URL and number of episodes
base_url = 'https://embtaku.com/videos/kimetsu-no-yaiba-hashira-geiko-hen'
num_episodes = 8

# Generate download links
download_links = generate_download_links(base_url, num_episodes)

# Save the download links to a JSON file
json_file = 'download_links.json'
with open(json_file, 'w') as file:
    json.dump(download_links, file, indent=4)

print(f"Download links saved to {json_file}")
