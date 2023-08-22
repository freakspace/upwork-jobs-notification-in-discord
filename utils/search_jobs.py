from urllib.parse import urljoin
import feedparser
from utils.database import search_job, create_job

base_url = "https://www.upwork.com"
rss_path = "/ab/feed/jobs/rss?q=django&sort=recency&paging=0"

async def search_jobs():
    url = urljoin(base_url, rss_path)

    feed = feedparser.parse(url)

    print(f"Found {len(feed.entries)} entries")

    for object in feed.entries:
        if not search_job(upwork_id=object.id):
            print("Creating job")
            create_job(
                title=object.title, 
                link=object.link, 
                summary=object.summary, 
                published=object.published, 
                upwork_id=object.id, 
                notified=False
            )