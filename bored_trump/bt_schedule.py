import urllib.request
from bs4 import BeautifulSoup
import re
from datetime import datetime, date
from time import sleep
import csv

last_post_text = ""

while True:
    page = urllib.request.urlopen("http://www.politico.com/blogs/donald-trump-administration")

    soup = BeautifulSoup(page, 'lxml')

    first_post = soup.find("h3", {"class" : "heading-extra"})

    if ("Today in Trumpworld" in first_post.text) and (first_post.text != last_post_text):
        file = open('trump_schedule.csv', 'w')
        schedule = csv.DictWriter(file, delimiter = ",", fieldnames=["time", "activity"])

        url = first_post.find('a', href = True)
        blog = urllib.request.urlopen(url['href'])
        blog_soup = BeautifulSoup(blog, 'lxml')
        bolds = blog_soup.findAll('b')
        today = datetime.strftime(date.today(), '%b %d %Y')
        for bold in bolds:
            block = {}
            match = re.search('(\d{1,2}:\d\d\s[ap].m.)(: )(.+)', bold.parent.text)
            if match:
                time = match.groups(0)[0].replace(".", "")
                if len(time) == 7:
                    time = "0" + time
                block['time']  = datetime.strptime(today + " " + time, '%b %d %Y %I:%M %p')
                block['activity'] = match.groups(0)[2]
                schedule.writerow(block)
        print(schedule)
        file.close()
        last_post_text = first_post.text
        print("Did a thing!")
    sleep(1800)