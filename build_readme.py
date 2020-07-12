import feedparser
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()

TOKEN = os.environ.get("SIMONW_TOKEN", "")


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r'<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->'.format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = '\n{}\n'.format(chunk)
    chunk = '<!-- {} starts -->{}<!-- {} ends -->'.format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_writing():
    entries = feedparser.parse('https://eugeneyan.com/feed')['entries'][:5]
    return [
        {
            'title': entry['title'],
            'url': entry['link'].split('#')[0],
            'published': re.findall(r'(.*?)\s00:00', entry['published'])[0]
        }
        for entry in entries
    ]


if __name__ == '__main__':
    readme_path = root / 'README.md'
    readme = readme_path.open().read()
    entries = fetch_writing()[:5]
    entries_md = '\n'.join(
        ['* [{title}]({url}) - {published}'.format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme, 'writing', entries_md)

    readme_path.open('w').write(rewritten)
