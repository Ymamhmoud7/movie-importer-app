# 🎬 Notion Movie Importer

A professional Python desktop app to **automate adding movies to your Notion watchlist**, saving you hours of manual entry.

Built with **PyQt5**, **TMDb API**, and the **official Notion API**, this tool gives you a beautiful, fast, and interactive way to build your movie library.

---

## ✨ Features

✅ **Search Movies** by title  
✅ **Preview and select the correct result** from a grid with thumbnails and titles  
✅ **Fetch metadata automatically**, including:
- Title
- Release year
- Genres
- Language
- Country
- Directors
- Description
- Poster image

✅ **Create a Notion page** with:
- Cover image
- Pre-filled properties
- Watched status set to *Not Started*

✅ **Modern dark UI** with:

---

## 🛠️ Technologies

- **Python 3**
- **PyQt5** – modern desktop interface
- **Requests** – API calls
- **Notion SDK**
- **TMDb API**

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/notion-movie-importer.git
cd notion-movie-importer
````

---

### 2️⃣ Install dependencies

Make sure you have Python 3 installed.

```bash
pip install -r requirements.txt
```

> Or manually:
>
> ```
> pip install PyQt5 requests python-dotenv notion-client
> ```

---

### 3️⃣ Create `.env` file

Create a `.env` file in the project root with:

```
TMDB_API_KEY=your_tmdb_api_key
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_database_id
```

✅ **TMDb API Key:** [Get one here](https://www.themoviedb.org/settings/api)
✅ **Notion Token & Database ID:** [Official Notion docs](https://developers.notion.com/docs/getting-started)

---

### 4️⃣ Run the app

```bash
python main.py
```

---

## 🖥️ Screenshots

Coming soon!

---

## 🧩 Customization

* Change colors and animations in `ui.py`.
* Modify Notion property mapping in `notion_utils.py`.
* Extend or adjust metadata fields in `tmdb.py`.

---

## 🙏 Credits

* [The Movie Database (TMDb)](https://www.themoviedb.org/)
* [Notion](https://www.notion.so/)

---

## 💡 Author

Made with ❤️ by **YMA**

````
