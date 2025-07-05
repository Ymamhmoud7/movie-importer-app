from notion_client import Client

class NotionClient:
    def __init__(self, token, database_id):
        self.client = Client(auth=token)
        self.database_id = database_id

    def check_exists(self, title):
        result = self.client.databases.query(
            database_id=self.database_id,
            filter={
                "property": "Movie Name",
                "title": {"equals": title}
            }
        )
        return bool(result.get("results"))

    def create_page(self, metadata):
        self.client.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Movie Name": {"title": [{"text": {"content": metadata["title"]}}]},
                "Watched": {"status": {"name": "Not started"}},
                "Release Date": {"number": int(metadata["release_date"]) if metadata["release_date"] else None},
                "Genre": {"multi_select": [{"name": g} for g in metadata["genres"]]},
                "Director": {"multi_select": [{"name": d} for d in metadata["directors"]]},
                "Country": {"multi_select": [{"name": metadata["country"]}]},
                "Language": {"select": {"name": metadata["language"]}}
            },
            cover={"external": {"url": metadata["poster_url"]}} if metadata["poster_url"] else None,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": metadata["overview"] or "No description available."}
                        }]
                    }
                }
            ]
        )
