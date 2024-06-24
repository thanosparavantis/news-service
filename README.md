![image](https://github.com/thanosparavantis/news-service/assets/26002449/ad528592-badf-4eb0-a0b1-fbd1cb3de647)
# News Service
This sample application performs news article scraping with advanced classification and summarization capabilities.
The application fetches article URLs from RSS feeds by polling various news outlets and maintains a cache of discovered URLs.
It leverages OpenAI's ChatGPT-4o to categorize each article according to a specific Greek municipality.
After categorization, the application generates a concise summary of the article.

The summaries are stored in Firebase for each municipality.
The application uses Python for the scraper and NextJS for the frontend map.
Additionally, it uses a Leaflet map to display emoji previews that capture the mood of the news, depending on the municipality area.
These emojis provide a quick visual representation of the news sentiment within each region.

## General notes
You can view a live demo at https://news.paravantis.org/.
- To run this app, set up a Firebase project with Firestore
- Use Docker to spin up a containerized version with `docker compose up -d`

## Scraper setup
To run the Python scraper backend:
- Create a virtual environment and install the dependencies with `pip install -r requirements.txt`
- Install the scraper package locally for development with `pip install -e .`
- Setup the required `.env` and `firebase.json` project files
- Launch the scraper with `python run_instant.py`

## Client setup
To run the NextJS frontend client:
- Install the dependencies with `npm install`
- Setup the required `.env` project files
- Launch the development server with `npm run start`
