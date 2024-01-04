from typing import Any


class ArtistNotFound(Exception):

    def __init__(self, artist_id: str):
        self.artist_id = artist_id
        self.message = f"Artist with id={artist_id} not found"
        super().__init__(self.message)


class UnknownModel(Exception):

    def __init__(self, value: Any):
        self.value = value
        self.message = f"Unknown model with name {value}"
        super().__init__(self.message)
