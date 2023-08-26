import os
import sqlite3

# db_name = "jobs.db"


def create_jobs_table(db_name):
    con = sqlite3.connect(db_name)
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
                notified BOOLEAN,
                channel INTEGER)
"""
    )
    con.close()


def create_links_table(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(
        """
CREATE TABLE links(
                id INTEGER PRIMARY KEY, 
                link TEXT, 
                active BOOLEAN,
                channel INTEGER)
"""
    )
    con.close()


def check_table_exists(db_name, table_name):
    con = sqlite3.connect(db_name)
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


def search_job(db_name, upwork_id):
    con = sqlite3.connect(db_name)
    query = f"SELECT id from jobs WHERE upwork_id = ?"
    cur = con.cursor()
    cur.execute(query, (upwork_id,))
    row = cur.fetchone()
    con.close()

    if row:
        return row
    else:
        return None


def all_jobs(db_name):
    con = sqlite3.connect(db_name)
    query = f"SELECT COUNT(*) FROM jobs"
    cur = con.cursor()
    cur.execute(query)
    row = cur.fetchall()
    con.close()

    if row:
        print(row)
    else:
        return None


def get_links(db_name):
    con = sqlite3.connect(db_name)
    query = f"SELECT id, link, channel FROM links WHERE active = 1"
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    con.close()

    if not rows:
        raise Exception("Missing links. Add your first link by using command /add_link")

    return rows


def create_job(db_name, title, link, summary, published, upwork_id, notified, channel):
    query = "INSERT INTO jobs (title, link, summary, published, upwork_id, notified, channel) VALUES (?, ?, ?, ?, ?, ?, ?)"

    data = (title, link, summary, published, upwork_id, notified, channel)
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(query, data)
        con.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if con:
            con.close()


def create_link(db_name, link, channel):
    query = "INSERT INTO links (link, active, channel) VALUES (?, ?, ?)"

    data = (link, True, channel)
    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(query, data)
        con.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if con:
            con.close()


def delete_link(
    db_name,
    id,
):
    query = "DELETE FROM links WHERE id = ?"

    try:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(query, (id,))
        con.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        if con:
            con.close()


def dump_db(db_name):
    conn = sqlite3.connect(db_name)

    # Close the connection
    conn.close()

    # Delete the database file
    if os.path.exists(db_name):
        os.remove(db_name)
        return True
    else:
        return False


tables = {"jobs": create_jobs_table, "links": create_links_table}
