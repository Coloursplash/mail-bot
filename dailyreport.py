import asyncio
from datetime import datetime
import pytz
from email.message import EmailMessage
import requests

class DailyReport:    
    def __init__(self, smtp, info):
        self.smtp = smtp
        self.BOT_EMAIL = info[0]
        self.PERSONAL_EMAIL = info[1]
        self.NEWS_API_KEY = info[2]
        self.ACTIVATE_TIME = 390 # in minutes

        self.log("Daily report initialised")

    def log(self, message):
        print(self.now().strftime('%H:%M:%S'), "[Daily report]", message)

    def get_email_text(self, subject, body, priority: int = 3):
        email_message = EmailMessage()
        email_message.add_header('To', self.PERSONAL_EMAIL)
        email_message.add_header('From', self.BOT_EMAIL)
        email_message.add_header('Subject', subject)
        email_message.add_header('X-Priority', str(priority))  # Urgency, 1 highest, 5 lowest
        email_message.set_content(body)
        
        return email_message.as_bytes()

    def send_email(self, subject, body):
        self.smtp.sendmail(self.BOT_EMAIL, [self.PERSONAL_EMAIL], self.get_email_text(subject, body))

    def get_school_timetable(self):
        day = self.now().strftime('%A')
        if day == 'Monday':
            return "\n\nSchool\nA\nBiology\nEconomics\nEnglish - Hartwell\nHistory\nArt\n\nB\nEnglish - Maxwell-Lyte\nComputer Science\nHistory\nEnglish - Hartwell\nArt"
        elif day == "Tuesday":
            return "\n\nSchool\nA\nEnglish - Hartwell\nPhysics\nEnglish - Maxwell-Lyte\nGAMES\nGAMES\n\nB\nEconomics\nPhysics\nEnglish - Hartwell\nGAMES\nGAMES"
        elif day == "Wednesday":
            return "\n\nSchool\nA\nMaths\nEnglish - Maxwell-Lyte\nComputer Science\nHistory\nBiology\n\nB\nMaths\nComputer Science\nEnglish - Maxwell-Lyte\nHistory\nBiology"
        elif day == "Thursday":
            return "\n\nSchool\nA\nArt\nMaths\nEconomics\nChemistry\nComputer Science\n\nB\nHistory\nMaths\nEconomics\nChemistry\nBiology"
        elif day == "Friday":
            return "\n\nSchool\nA\nChemistry\nEconomics\nArt\nPhysics\nMaths\n\nB\nChemistry\nArt\nPhysics\nComputer Science\nMaths"
        return "\n\nEnjoy the weekend!"

    def get_news(self):
        url = ('https://newsapi.org/v2/top-headlines?'
        'country=gb&'
        'apiKey=bf0f2affd1f941cbab43443ea1d3b61f')
        all_articles = requests.get(url).json()
        formatted_articles = []
        for i in range(10):
            formatted_articles.append(str(i + 1) + '. ' + all_articles['articles'][i]['title'] + '  :  ' + all_articles['articles'][i]['url'])
        return "\n\nThe News\n" + '\n'.join(formatted_articles)

    def get_links(self):
        links = ["\n","Useful links"]
        links.append("Wordle: https://www.nytimes.com/games/wordle/index.html")
        return "\n".join(links)

    def now(self):
        return datetime.now(pytz.timezone("Europe/London"))

    def main(self):
        subject = "Daily update - " + self.now().strftime("%d/%m/%Y")
        body = self.now().strftime('%H:%M:%S on %A, %d %D, %Y')
        body += self.get_school_timetable()
        body += self.get_news()
        body += self.get_links()
        self.send_email(subject, body)
    
    async def mainloop(self):
        self.log("Daily report running")
        
        while True:
            dt = self.now()
            time = dt.hour * 60 + dt.minute
            dif = self.ACTIVATE_TIME - time
            if dif == 0:
                self.main()
                await asyncio.sleep(60 * 60)
            elif dif > 65:
                await asyncio.sleep(60 * 60) # hour
            elif dif > 35:
                await asyncio.sleep(60 * 30) # 30 min
            elif dif > 15:
                await asyncio.sleep(60 * 10) # 10 min
            elif dif > 5:
                await asyncio.sleep(60 * 2) # 2 min
            elif dif < 0:
                await asyncio.sleep(60 * 60)
            else:
                await asyncio.sleep(60) # 1 min
        