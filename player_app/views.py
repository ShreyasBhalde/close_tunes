import requests
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


@login_required
def home_view(request):
    query = request.GET.get('q')
    if query:
        # Make a request to the external API to search for songs based on the query
        response = requests.get(f'https://saavn.dev/api/search/songs?query={query}&limit=20')
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Debug print to check the structure of the response
            print(data)
            all_artists = set()  
            # Ensure 'data' and 'results' exist in the response
            if 'data' in data and isinstance(data['data'], dict):
                results = data['data'].get('results', [])
                songs = []
                for result in results:
                    name = result.get('name')
                    duration = result.get('duration')  # Duration in seconds
                    album = result.get('album', {}).get('name', 'Unknown Album')
                    download_urls = result.get('downloadUrl', [])
                    artist_info = result.get('artists', {})  # Changed from 'artist' to 'artists'

                    # Extract all primary and featured artists from the 'artists' field
                    if isinstance(artist_info, dict):
                        primary_artists = artist_info.get('primary', [])
                        featured_artists = artist_info.get('featured', [])
                        
                        # Add all primary artists to the set
                        for artist in primary_artists:
                            if isinstance(artist, dict) and 'name' in artist:
                                all_artists.add(artist['name'])
                        
                        # Add all featured artists to the set
                        for artist in featured_artists:
                            if isinstance(artist, dict) and 'name' in artist:
                                all_artists.add(artist['name'])
                    
                    first_5_artists = list(all_artists)[:5]
                    print("ARTISTS:", first_5_artists)  # Debug print to verify artists collected

                    image_url = None
                    if 'image' in result and isinstance(result['image'], list):
                        # Get the highest quality image if available
                        image_url = result['image'][-1].get('url')
                    url_160kbps = next((item['url'] for item in download_urls if item['quality'] == '160kbps'), None)
                    if url_160kbps:
                        print(f"160kbps URL for '{result['name']}': {url_160kbps}")
                        songs.append({
                            'name': name,
                            'duration': f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown Duration",
                            'album': album,
                            'image_url': image_url,
                            'url_160kbps': url_160kbps,
                            'artists': ', '.join(first_5_artists)
                        })
                    else:
                        print(f"160kbps URL not found for '{result['name']}'")
            else:
                songs = []  # No valid results found
        else:
            print(f"API call failed with status code {response.status_code}")
            songs = []  # Handle the case where the API call fails
    else:
        # Initial page with blank song boxes
        songs = []

    return render(request, 'home.html', {'songs': songs})


@login_required
def play_song(request, query):
    # Directly pass the song URL to the template
    return render(request, 'play_song.html', {'song_url': query})

