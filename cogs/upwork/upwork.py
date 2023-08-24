import sqlite3

import discord
from discord.ext import commands, tasks

from utils.search_jobs import search_jobs
from utils.utils import extract_info
from database import (
    create_link,
    delete_link,
    get_links,
    check_table_exists,
    get_jobs_to_notify,
    tables,
)


async def notify_new_jobs(bot, channel_id):
    """Notifies of new jobs"""
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE notified = 0")
    jobs_to_notify = get_jobs_to_notify()

    print(f"Notifying about {len(jobs_to_notify)} jobs")

    for job in jobs_to_notify:
        job_id, title, link, summary, published, _, notified = job

        channel = await bot.fetch_channel(channel_id)

        embed = discord.Embed(
            title="",
            description="",
            color=discord.Color.red(),
        )

        extracted_info = extract_info(summary)

        skills = ", ".join([skill for skill in extracted_info["skills"]])

        compensation = None
        if extracted_info["hourly_rate"]:
            comp_from = extracted_info["hourly_rate"]["min"]
            comp_to = extracted_info["hourly_rate"]["max"]
            compensation = f"From {comp_from} to {comp_to} $/hr"
        elif extracted_info["budget"]:
            comp_from = extracted_info["budget"]
            compensation = f"Budget: {comp_from}"

        # Prepare fields
        embed.add_field(name="Date", value=published, inline=False)
        embed.add_field(name="Compensation", value=compensation, inline=False)
        embed.add_field(name="Skills", value=skills, inline=False)

        # Prepare view
        view = discord.ui.View(timeout=None)
        button = discord.ui.Button(url=link, label="Show")
        view.add_item(item=button)
        message = f"<@{1141553740382482452}> {title}"
        await channel.send(message)
        await channel.send(embed=embed, view=view)

        cursor.execute("UPDATE jobs SET notified = 1 WHERE id = ?", (job_id,))

    conn.commit()
    conn.close()


class UpworkBot(commands.Cog):
    """Upwork bot to send notifications for newly posted jobs"""

    def __init__(self, bot):
        self.bot = bot
        self.channel = None

    @discord.slash_command()
    async def start_bot(self, ctx: commands.Context):
        for key in tables:
            if not check_table_exists(key):
                tables[key]()

        self.channel = ctx.channel.id

        try:
            get_links()
            self.check_for_jobs.start()
            await ctx.response.send_message(content="Bot started", ephemeral=True)
        except Exception as e:
            await ctx.response.send_message(content=e, ephemeral=True)

    @discord.slash_command()
    async def add_link(
        self,
        ctx: commands.Context,
        link: discord.Option(str, "Link to Upwork jobs page"),
    ):
        create_link(link=link)
        await ctx.response.send_message(content="Link added", ephemeral=True)

    @discord.slash_command()
    async def delete_link(
        self, ctx: commands.Context, id: discord.Option(int, "Link id")
    ):
        delete_link(id=id)
        await ctx.response.send_message(content="Link deleted", ephemeral=True)

    @discord.slash_command()
    async def show_links(self, ctx: commands.Context):
        links = get_links()
        for link in links:
            await ctx.send(content=f"id: {link[0]}: {link[1]}")

        await ctx.response.send_message(content="Done", ephemeral=True)

    @tasks.loop(seconds=120)
    async def check_for_jobs(self):
        """Check for jobs on Upwork, saves to database, notifies in Discord"""
        print("Checking for jobs..")
        await search_jobs()
        await notify_new_jobs(self.bot, self.channel)
        print("Finished checking for jobs..")

    @check_for_jobs.before_loop
    async def before_check_for_jobs(self):
        print("Task waiting for bot to start..")
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Upwork bot ready")


def setup(bot):
    bot.add_cog(UpworkBot(bot))
