from webapp import keep_alive

# Clients
import imapclient
import smtplib

# Async
import asyncio

# Modules
from dailyreport import DailyReport

# Secrets
from os import getenv

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
BOT_EMAIL = getenv('bot_email')
BOT_PASSWORD = getenv('bot_password')
NEWS_API_KEY = getenv('news_api_key')
PERSONAL_EMAIL = getenv('personal_email')


async def main():
    # SMTP
    s = smtplib.SMTP(SMTP_SERVER, 587)
    s.starttls()
    s.ehlo()
    s.login(BOT_EMAIL, BOT_PASSWORD)

    # IMAP
    i = imapclient.IMAPClient(IMAP_SERVER)
    i.login(BOT_EMAIL, BOT_PASSWORD)

    # objects
    report = DailyReport(s, [BOT_EMAIL, PERSONAL_EMAIL, NEWS_API_KEY])

    coroutines = [
        report.mainloop()
    ]
    await asyncio.gather(*coroutines)

    # Close connections
    s.close()


keep_alive()

asyncio.run(main())
