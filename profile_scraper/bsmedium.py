import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np
from time import sleep

stories_data = []

for month in range(1, 13):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        n_days = 31
    elif month in [4, 6, 9, 11]:
        n_days = 30
    else:
        n_days = 28

    sleep(np.random.randint(1, 15))

    for day in range(1, n_days + 1):
        month_str, day_str = str(month).zfill(2), str(day).zfill(2)  # Ensure two digits

        date = f'{month_str}/{day_str}/2023'
        url = f'https://medium.com/swlh/archive/2023/{month_str}/{day_str}'

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        stories = soup.find_all('div', class_='streamItem streamItem--postPreview js-streamItem')

        for story in stories:
            each_story = []

            author_box = story.find('div', class_='postMetaInline u-floatLeft u-sm-maxWidthFullWidth')
            author_url = author_box.find('a')['href']

            try:
                reading_time = author_box.find('span', class_='readingTime')['title']
            except:
                continue

            sleep(np.random.randint(1, 15))

            title = story.find('h3').text if story.find('h3') else '-'
            subtitle = story.find('h4').text if story.find('h4') else '-'

            if story.find('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents'):
                claps = story.find('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents').text
            else:
                claps = 0

            if story.find('a', class_='button button--chromeless u-baseColor--buttonNormal'):
                responses = story.find('a', class_='button button--chromeless u-baseColor--buttonNormal').text
            else:
                responses = '0 responses'

            story_url = story.find('a', class_='button button--smaller button--chromeless u-baseColor--buttonNormal')['href']

            reading_time = reading_time.split()[0]
            responses = responses.split()[0]

            story_page = requests.get(story_url)
            story_soup = BeautifulSoup(story_page.text, 'html.parser')

            sections = story_soup.find_all('section')
            story_paragraphs = []
            section_titles = []

            sleep(np.random.randint(1, 15))

            for section in sections:
                paragraphs = section.find_all('p')
                for paragraph in paragraphs:
                    story_paragraphs.append(paragraph.text)

                subs = section.find_all('h1')
                for sub in subs:
                    section_titles.append(sub.text)

            number_sections = len(section_titles)
            number_paragraphs = len(story_paragraphs)

            each_story.extend([date, title, subtitle, claps, responses, author_url, story_url, reading_time,
                               number_sections, section_titles, number_paragraphs, story_paragraphs])

            stories_data.append(each_story)

# Create DataFrame and save to CSV outside the loop
columns = ['date', 'title', 'subtitle', 'claps', 'responses',
           'author_url', 'story_url', 'reading_time (mins)',
           'number_sections', 'section_titles',
           'number_paragraphs', 'paragraphs']

df = pd.DataFrame(stories_data, columns=columns)
df.to_csv('1.csv', sep='\t', index=False)
