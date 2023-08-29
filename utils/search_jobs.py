import feedparser
from database import search_job, create_job, get_links

base_url = "https://www.upwork.com/ab/feed/jobs/rss?q="


async def search_jobs(db_name):
    links = get_links(
        db_name
    )  # E.g. django&sort=recency&client_hires=1-9,10-&proposals=0-4,5-9,10-14,15-19

    for link in links:
        _, link, channel = link

        url = base_url + link

        feed = feedparser.parse(url)

        print(f"Found {len(feed.entries)} entries")

        for object in feed.entries:
            if not search_job(db_name=db_name, upwork_id=object.id):
                print("Creating job")
                create_job(
                    db_name=db_name,
                    title=object.title,
                    link=object.link,
                    summary=object.summary,
                    published=object.published,
                    upwork_id=object.id,
                    notified=False,
                    channel=channel,
                )
