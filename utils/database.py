import sqlite3

def create_jobs_table():
    con = sqlite3.connect("jobs.db")
    cur = con.cursor()
    cur.execute("""
CREATE TABLE jobs(
                id INTEGER PRIMARY KEY, 
                title TEXT, 
                link TEXT, 
                summary TEXT, 
                published TEXT, 
                upwork_id TEXT,
                notified BOOLEAN)
""")
    con.close()

def search_job(upwork_id: str):
    con = sqlite3.connect("jobs.db")
    query = f"SELECT id from jobs WHERE upwork_id = ?"
    cur = con.cursor()
    cur.execute(query, (upwork_id,))
    row = cur.fetchone()
    con.close()

    if row:
        return row
    else:
        return None
    
def all_jobs():
    con = sqlite3.connect("jobs.db")
    query = f"SELECT COUNT(*) from jobs"
    cur = con.cursor()
    cur.execute(query)
    row = cur.fetchall()
    con.close()

    if row:
        print(row)
    else:
        return None
    
def create_job(
        title, 
        link, 
        summary,  
        published, 
        upwork_id, 
        notified,
        ):
    query = "INSERT INTO jobs (title, link, summary, published, upwork_id, notified) VALUES (?, ?, ?, ?, ?, ?)"

    data = (title, link, summary, published, upwork_id, notified)
    try:
        con = sqlite3.connect("jobs.db")
        cur = con.cursor()
        cur.execute(query, data)
        con.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if con:
            con.close()
    

if __name__ == "__main__":
    #all_jobs()
    #pass
    create_jobs_table()
    #print(search_job("https://www.upwork.com/jobs/Senior-Python-Developers-OpenAI-API-FastAPI_%7E0171a4398635543d19?source=rss"))