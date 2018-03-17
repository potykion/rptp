"""
Set of methods for parsing PTG.
"""
from typing import Dict, Iterable

from requests_html import HTMLSession


def parse_debut_page() -> Iterable[Dict]:
    url = 'http://www.pornteengirl.com/debutyear/debut.html'
    session = HTMLSession()
    response = session.get(url)

    actress_table = response.html.find('table#debut', first=True)
    actress_rows = actress_table.find('tr')
    for row in actress_rows:
        debut_year = int(row.find('th', first=True).text)
        actress_tags = row.find('a')
        yield from (
            {
                'debut_year': debut_year,
                'name': actress_tag.text.strip(','),
                'link': list(actress_tag.absolute_links)[0]
            }
            for actress_tag in actress_tags
        )
