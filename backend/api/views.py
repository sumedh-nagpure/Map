from rest_framework.views import APIView
from rest_framework.response import Response
from PIL import Image
import requests
from requests.auth import HTTPBasicAuth
import tempfile
import os
from django.http import FileResponse

# Replace these with your SciHub credentials
USERNAME = 'sumedhnagpure123@gmail.com'
PASSWORD = 'Savitadevang@123'

class DownloadImageView(APIView):
    def post(self, request):
        coords = request.data.get('coords')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        if not coords or len(coords) != 4 or not start_date or not end_date:
            return Response({'error': 'Invalid input parameters'}, status=400)
        
        try:
            # Search for Sentinel-2 data
            search_url = (
                f"https://apihub.copernicus.eu/apihub/search?"
                f"q=platformname:Sentinel-2 AND bbox({coords[0]},{coords[1]},{coords[2]},{coords[3]}) "
                f"AND date:[{start_date}T00:00:00Z TO {end_date}T23:59:59Z]"
            )
            response = requests.get(search_url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
            response.raise_for_status()
            results = response.json()
            
            if not results or 'feed' not in results or 'entry' not in results['feed']:
                return Response({'error': 'No data found'}, status=404)
            
            # Download the first result
            entry = results['feed']['entry'][0]
            download_url = entry.get('link', [{}])[0].get('href')
            
            if not download_url:
                return Response({'error': 'No download URL found'}, status=404)
            
            # Download data
            file_name = entry.get('title', 'sentinel_image.zip') + '.zip'
            data_response = requests.get(download_url, auth=HTTPBasicAuth(USERNAME, PASSWORD), stream=True)
            data_response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                for chunk in data_response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            # Send the file as a response
            response = FileResponse(open(temp_file_path, 'rb'), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            
            # Delete the temporary file after sending
            os.unlink(temp_file_path)
            
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=500)
