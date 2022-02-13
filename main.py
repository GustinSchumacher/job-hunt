import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}
    url = f'https://www.indeed.com/jobs?q=web+developer&l=Saint+Paul%2C+MN&start=0'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        title = item.find('h2').text.strip()
        company = item.find('span', class_='companyName').text.strip()
        try:
            estimatedSalary = item.find(
                'span', class_='estimated-salary').text.strip()
        except:
            estimatedSalary = ''
        summary = item.find(
            'div', class_='job-snippet').text.strip().replace('\n', '')

        job = {
            'title': title,
            'company': company,
            'estimatedSalary': estimatedSalary,
            'summary': summary,
        }
        joblist.append(job)
    return


joblist = []

for i in range(0, 50, 10):
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)

print(df.head())

df.to_csv('jobs.csv')
