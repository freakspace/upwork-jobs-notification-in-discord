from urllib.parse import urljoin
import feedparser
from database import search_job, create_job, get_links

base_url = "https://www.upwork.com"
rss_path = "/ab/feed/jobs/rss?q=django&sort=recency&paging=0"

async def search_jobs():
    links = get_links() # E.g. /ab/feed/jobs/rss?q=django&sort=recency&paging=0

    for link in links:
        print(link)
        url = urljoin(base_url, link[1])

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