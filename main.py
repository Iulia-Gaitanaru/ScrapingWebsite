""" A project where we can scraping a website and filter some information
I scrap Hacker News to filter the articles based on most popular articles
Eliminate the articles that have less than 100 points for focus on the best articles

Author Gaitanaru Iulia
13.09.2022
"""

import requests
import pprint
from bs4 import BeautifulSoup


def read_pages(num_page):
    if num_page == 1:
        res = requests.get('https://news.ycombinator.com/news')
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.titlelink')
        subtext = soup.select('.subtext')
        return links, subtext
    else:
        list_links = []
        list_subtext = []
        for idx in range(num_page+1):
            if idx + 1 == 1:
                res = requests.get('https://news.ycombinator.com/news')
                soup = BeautifulSoup(res.text, 'html.parser')
                links = soup.select('.titlelink')
                subtext = soup.select('.subtext')
                list_links.append(links)
                list_subtext.append(subtext)
            else:
                res = requests.get(f'https://news.ycombinator.com/news?p={idx+1}')
                soup = BeautifulSoup(res.text, 'html.parser')
                links = soup.select('.titlelink')
                subtext = soup.select('.subtext')
                list_links.append(links)
                list_subtext.append(subtext)
        if len(list_links) > 1:
            list_links_flat = [item for sublist in list_links for item in sublist]
            list_subtext_flat = [item for sublist in list_subtext for item in sublist]
            return list_links_flat, list_subtext_flat
        else:
            return list_links, list_subtext


# Sort stories by votes
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hm(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        # take only the links that has points
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
            else:
                continue
    return sort_stories_by_votes(hn)


if __name__ == '__main__':
    links, subtext = read_pages(2)
    custo_hn = create_custom_hm(links, subtext)
    pprint.pprint(custo_hn)