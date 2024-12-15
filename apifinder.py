import requests
from bs4 import BeautifulSoup
import re

# Function to find exposed APIs from a website
def find_exposed_apis(website_url):
    print(f"Starting the analysis of the website: {website_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Send a GET request to the website with custom headers
        print("Sending request to the website...")
        response = requests.get(website_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for invalid status codes
        print(f"Successfully fetched the website content. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return
    
    # Parse the HTML content of the page
    print("Parsing the HTML content of the website...")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Initialize a list to store found API endpoints
    api_endpoints = []
    
    # Look for JS files and inline scripts that may contain API URLs
    print("Searching for script tags with potential API references...")
    scripts = soup.find_all('script', src=True)
    for script in scripts:
        js_url = script['src']
        if 'api' in js_url.lower():
            print(f"Found potential API endpoint in JS file: {js_url}")
            api_endpoints.append(js_url)
    
    # Look for inline JavaScript that could contain API references
    print("Searching for inline JavaScript with potential API references...")
    inline_scripts = soup.find_all('script')
    for script in inline_scripts:
        if script.string:
            # Search for any string that looks like an API endpoint (e.g., /api/, /v1/, /data/)
            matches = re.findall(r'\/api\/\S+|\S*\.json|\S*\.php|\S*\.xml', script.string)
            if matches:
                for match in matches:
                    print(f"Found potential API endpoint in inline script: {match}")
                api_endpoints.extend(matches)

    # Output all found potential API endpoints
    if api_endpoints:
        print("\nPotentially exposed API endpoints found:")
        for endpoint in api_endpoints:
            print(f"- {endpoint}")
    else:
        print("\nNo exposed API endpoints found on this page.")

# User input for website URL
website_url = input("Enter the website URL (with http:// or https://): ")

# Call the function to find exposed APIs
find_exposed_apis(website_url)
