import pandas as pd
import requests
import time
from bs4 import BeautifulSoup


def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}
    url = f'https://www.indeed.com/jobs?q=Web+Developer&l=Saint+Paul%2C+MN&radius=100&fromage=1'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')

    for item in divs:
        try:
            post_date = item.find('span', 'date').text.strip().replace('Posted', '')
        except AttributeError:
            post_date = ''
        title = item.find('h2').text.strip().replace('new', '')
        company = item.find('span', class_='companyName').text.strip()
        try:
            estimatedsalary = item.find('span', class_='estimated-salary').text.strip()
        except:
            estimatedsalary = ''
        try:
            salary = item.find('div', class_='metadata salary-snippet-container').text.strip()
        except:
            salary = ''
        summary = item.find('div', class_='job-snippet').text.strip().replace('\n', '')

        job = {
            'post date': post_date,
            'title': title,
            'company': company,
            'estimated salary': estimatedsalary,
            'salary': salary,
            'summary': summary,



        }
        joblist.append(job)
    return


joblist = []

for i in range(1, 5, 1):
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)

print(df.head())

TodaysDate = time.strftime("%Y-%m-%d")
excelfilename = 'jobs-' + TodaysDate +".csv"

df.to_csv(excelfilename)
