import requests
from requests.auth import HTTPBasicAuth

# Replace these with your SciHub credentials
username = 'sumedhnagpure123@gmail.com'
password = 'Savitadevang@123'

# Function to search Sentinel data
def search_sentinel_data(platform_name, bbox, start_date, end_date):
    search_url = (
        f"https://apihub.copernicus.eu/apihub/search?"
        f"q=platformname:{platform_name} AND bbox({bbox}) "
        f"AND date:[{start_date}T00:00:00Z TO {end_date}T23:59:59Z]"
    )
    
    try:
        response = requests.get(search_url, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error searching Sentinel data: {e}")
        return None

# Function to download data
def download_data(download_url, file_name='sentinel_image.zip'):
    try:
        response = requests.get(download_url, auth=HTTPBasicAuth(username, password), stream=True)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Data downloaded successfully: {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")

# Example usage
if __name__ == "__main__":
    # Define your search parameters
    bbox = '13.0,50.0,14.0,51.0'  # Format: lon_min,lat_min,lon_max,lat_max
    start_date = '2022-01-01'
    end_date = '2022-01-31'
    
    # Search for Sentinel-2 data
    results = search_sentinel_data('Sentinel-2', bbox, start_date, end_date)
    
    if results and 'feed' in results and 'entry' in results['feed']:
        for entry in results['feed']['entry']:
            # Extract download URL from the result
            download_url = entry.get('link', [{}])[0].get('href')
            if download_url:
                # Download the data (you may want to use different file names based on the result)
                file_name = entry.get('title', 'sentinel_image.zip') + '.zip'
                download_data(download_url, file_name)
    else:
        print("No results found or error retrieving results.")
