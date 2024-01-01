from clear_sessions import clear_sessions
from generate_timestamp_artist import generate_timestamp_artist
from clear_tracks import clear_tracks
from generate_artists_plays_per_week import generate_artists_plays_per_week

if __name__ == "__main__":
    clear_sessions()
    clear_tracks()
    generate_timestamp_artist()
    generate_artists_plays_per_week()
