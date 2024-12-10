from django.contrib import admin
from .models import Playlist,Song

# Register your models here.

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['id','name','user','created_at']

class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_id', 'title', 'artist', 'album', 'duration', 'get_playlists']

    def get_playlists(self, obj):
        # Return a comma-separated list of playlist names
        return ", ".join([playlist.name for playlist in obj.playlists.all()])

    get_playlists.short_description = 'Playlists'  # Column name in admin



admin.site.register(Playlist,PlaylistAdmin)
admin.site.register(Song,SongAdmin)


