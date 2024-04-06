import requests
import re

# Function to extract valid hostnames from the given text content
def extract_hostnames(text):
    # Regular expression to match hostnames with at least 3 characters and a period
    hostname_pattern = re.compile(r'(?m)^\s*(?:0\.0\.0\.0\s+)?([a-zA-Z0-9.-]{3,})')
    # Filter hostnames with a period being one of the 3 characters
    return {hostname for hostname in hostname_pattern.findall(text) if '.' in hostname}

# Read the existing blocklist from a file
existing_block_urls = set()
try:
    with open('URL_Blocklist.txt', 'r') as file:
        existing_block_urls = {line.strip() for line in file if line.strip()}
except FileNotFoundError:
    print("URL_Blocklist.txt not found. A new file will be created.")

# Read the list of URLs from a file
with open('URL_list.txt', 'r') as file:
    url_list = [line.strip() for line in file if line.strip()]

# Variable to store all unique hostnames
block_urls = set()

# Process each URL
for url in url_list:
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Extract hostnames and add them to the block_urls set
            extracted_hostnames = extract_hostnames(response.text)
            # Filter out hostnames that are already in the existing blocklist
            new_hostnames = extracted_hostnames - existing_block_urls
            block_urls.update(new_hostnames)
            # Output and log the total number of hostnames per URL
            print(f"URL: {url} - {len(new_hostnames)} new hostnames added.")
        else:
            print(f"Failed to retrieve data from {url}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

# Append new unique hostnames to the blocklist file
with open('URL_Blocklist.txt', 'a') as file:
    for hostname in sorted(block_urls):
        file.write(hostname + '\n')

# Output the total number of unique hostnames
print(f"Total new unique hostnames appended to URL_Blocklist.txt: {len(block_urls)}")
