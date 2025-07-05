import requests

SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
DETAILS_URL = "https://api.themoviedb.org/3/movie/{id}"
CREDITS_URL = "https://api.themoviedb.org/3/movie/{id}/credits"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/original"

class TMDbClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_metadata(self, title):
        params = {
            "api_key": self.api_key,
            "query": title,
            "language": "en-US",
            "include_adult": True
        }
        search_result = requests.get(SEARCH_URL, params=params).json()
        results = search_result.get("results", [])
        if not results:
            return None

        movie = results[0]
        movie_id = movie["id"]

        details = requests.get(DETAILS_URL.format(id=movie_id), params={
            "api_key": self.api_key,
            "language": "en-US"
        }).json()

        credits = requests.get(CREDITS_URL.format(id=movie_id), params={
            "api_key": self.api_key
        }).json()

        directors = [c["name"] for c in credits.get("crew", []) if c.get("job") == "Director"]
        countries = details.get("production_countries", [])
        country_name = countries[0]["name"] if countries else "Unknown"

        return {
            "title": details.get("title"),
            "release_date": details.get("release_date", "")[:4],
            "genres": [g["name"] for g in details.get("genres", [])],
            "overview": details.get("overview", ""),
            "poster_url": IMAGE_BASE_URL + details["poster_path"] if details.get("poster_path") else None,
            "language": details.get("original_language", "en"),
            "country": country_name,
            "directors": directors,
            "is_adult": details.get("adult", False)
        }
