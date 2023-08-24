import sqlite3


def create_jobs_table():
    con = sqlite3.connect("jobs.db")
    cur = con.cursor()
    cur.execute(
        """
CREATE TABLE jobs(
                id INTEGER PRIMARY KEY, 
                title TEXT, 
                link TEXT, 
                summary TEXT, 
                published TEXT, 
                upwork_id TEXT,
                notified BOOLEAN)
"""
    )
    con.close()


def create_links_table():
    con = sqlite3.connect("jobs.db")
    cur = con.cursor()
    cur.execute(
        """
CREATE TABLE links(
                id INTEGER PRIMARY KEY, 
                link TEXT, 
                active BOOLEAN)
"""
    )
    con.close()


def check_table_exists(table_name):
    con = sqlite3.connect("jobs.db")
    cur = con.cursor()
    cur.execute(
        f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    )
    count = cur.fetchone()[0]
    con.close()
    if count == 1:
        return True
    else:
        return False


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
    query = f"SELECT COUNT(*) FROM jobs"
    cur = con.cursor()
    cur.execute(query)
    row = cur.fetchall()
    con.close()

    if row:
        print(row)
    else:
        return None


def get_links():
    con = sqlite3.connect("jobs.db")
    query = f"SELECT id, link FROM links WHERE active = 1"
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    con.close()

    if not rows:
        raise Exception("Missing links. Add your first link by using command /add_link")

    return rows


def get_jobs_to_notify():
    con = sqlite3.connect("jobs.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM jobs WHERE notified = 0")
    rows = cursor.fetchall()
    con.close()
    return rows


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


def create_link(
    link,
):
    query = "INSERT INTO links (link, active) VALUES (?, ?)"

    data = (link, True)
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


def delete_link(
    id,
):
    query = "DELETE FROM links WHERE id = ?"

    try:
        con = sqlite3.connect("jobs.db")
        cur = con.cursor()
        cur.execute(query, (id,))
        con.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if con:
            con.close()


tables = {"jobs": create_jobs_table, "links": create_links_table}
