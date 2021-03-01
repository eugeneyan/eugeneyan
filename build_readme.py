import feedparser
import pathlib
import re

root = pathlib.Path(__file__).parent.resolve()


def replace_writing(content, marker, chunk, inline=False):
    r = re.compile(
        r'<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->'.format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = '\n{}\n'.format(chunk)
    chunk = '<!-- {} starts -->{}<!-- {} ends -->'.format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_writing():
    entries = feedparser.parse('https://eugeneyan.com/feed.xml')['entries']
    top5_entries = entries[:5]
    entry_count = len(entries)
    return [
               {
                   'title': entry['title'],
                   'url': entry['link'].split('#')[0],
                   'published': re.findall(r'(.*?)\s00:00', entry['published'])[0]
               }
               for entry in top5_entries
           ], entry_count


if __name__ == '__main__':
    readme_path = root / 'README.md'
    readme = readme_path.open().read()
    entries, entry_count = fetch_writing()
    print(f'Recent 5: {entries}, Total count: {entry_count}')
    entries_md = '\n'.join(
        ['* [{title}]({url}) - {published}'.format(**entry) for entry in entries]
    )

    # Update entries
    rewritten_entries = replace_writing(readme, 'writing', entries_md)
    readme_path.open('w').write(rewritten_entries)

    # Update count
    readme = readme_path.open().read()  # Need to read again with updated entries
    rewritten_count = replace_writing(readme, 'writing_count', entry_count, inline=True)
    readme_path.open('w').write(rewritten_count)
