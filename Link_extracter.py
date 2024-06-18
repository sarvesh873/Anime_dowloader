import requests
import json
import time

base_url = "https://animeflix.ci/getsource/naruto-shippuuden-episode-{}?dub=false"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
links = []

def fetch_url(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Will raise an HTTPError for bad responses
            return response.json()
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    return None

for i in range(18, 501):
    url = base_url.format(i)
    data = fetch_url(url)
    if data and "source" in data:
        links.append(data["source"])
        print(f"Successfully retrieved data for episode {i}")
    else:
        print(f"Failed to retrieve data for episode {i}")

# Save the links to a JSON file
with open("naruto_shippuden_links.json", "w") as file:
    json.dump(links, file, indent=4)

print("Links have been successfully saved to naruto_shippuden_links.json")
