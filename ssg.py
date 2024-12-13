'''
TODO
- date in blog articles
- feed id
- production permalinks
- OG images
- reorganise images
- tags?
- image lazy loading, size?
- 404 check
- blogroll redirect check
'''

from shutil import copytree, rmtree
from pathlib import Path
from markdown2 import markdown
import datetime as dt

SOURCE_DIR = Path('content')
BUILD_DIR = Path('build')
SITEMAP = Path('build/sitemap.xml')
FEED = Path('build/feed.xml')
POST_INDEX = Path('build/blog/index.html')
FILE_404 = Path('build/404.html')

TEMPLATES = {
    'html': Path('templates/default.html'),
    'sitemap': Path('templates/sitemap.xml'),
    'sitemap_item': Path('templates/sitemap_item.xml'),
    'index_item': Path('templates/index_item.html'),
    'feed': Path('templates/feed.xml'),
    'feed_item': Path('templates/feed_item.xml'),
    'file_404': Path('templates/404.html')
}

SITE_META = {
    'site_url': 'test.linesinalandscape.com',
    'site_title': 'Lines in a Landscape',
    'site_author': 'Alan Grant',
    'site_description': 'Trails, trains, maps, Málaga, and more - a personal website'
}


def write_file(path, content):
    ''' Write content to a file '''
    path.write_text(content, encoding='utf-8')
    print('File created:', path)


def prepare_dirs():
    ''' Empty build directory and copy all contents '''
    rmtree(BUILD_DIR, ignore_errors=True)
    copytree(SOURCE_DIR, BUILD_DIR)


def load_layouts():
    ''' Load the layout templates into a dictionary '''
    layouts = {}
    for key in TEMPLATES:
        layouts[key] = TEMPLATES[key].read_text(encoding='utf-8')
    return layouts


def get_md_data():
    ''' read markdown content and metadata into a list of dictionaries '''
    md_data = []

    # make a list of files with .md extension
    files = list(BUILD_DIR.rglob('*.md'))

    for file in files:
        # collect all required data for each markdown file
        file_data = {}
        file_data.update(SITE_META)
        file_data['path'] = file

        # set flag for blog post if file is in subfolder of 'blog'
        file_data['is_post'] = ('blog' in str(file.parent)
                                and not str(file.parent).endswith('blog'))

        # read the markdown file
        md = file.read_text(encoding='utf-8')

        # Convert markdown to HTML and store metadata
        md_converted = markdown(md, extras=['metadata'])
        file_data['content'] = str(md_converted)
        file_data.update(md_converted.metadata)

        # extract the title from the first # line of the markdown file
        if 'title' not in file_data:
            lines = md.split('\n')
            for line in lines:
                if line.startswith('# '):
                    file_data['title'] = line[2:]
                    break
        
        # check for draft status (any value excep False treated as draft)
        if 'draft' in file_data and file_data['draft'] != 'False':
            file_data['is_public'] = False
        else:
            file_data['is_public'] = True

        # various metadata fields not already in the markdown file
        # set the final url for the page
        permalink = (SITE_META.get('site_url')
                     + str(file.relative_to(BUILD_DIR).parent) + '/')
        permalink = permalink.replace('\\', '/')
        permalink = permalink.replace('./', '')  # for root index page
        file_data['permalink'] = permalink

        # reformat internal links
        file_data['content'] = file_data['content'].replace('\index.md', '/')

        # set dates for sorting and feed
        if 'date' not in file_data:
            if file_data['is_post']:
                # extract date from containing directory name
                file_data['date'] = file_data['path'].parts[-2].split('_')[0]
            else:
                # use file modified timestamp
                timestamp = dt.datetime.fromtimestamp(file.stat().st_mtime)
                file_data['date'] = f'{timestamp:%Y-%m-%d}'

        if 'date_modified' in file_data:
            file_data['date_sort'] = file_data['date_modified']
            file_data['date_feed'] = file_data['date'] + 'T00:00:00Z'
            file_data['date_feed_updated'] = (file_data['date_modified']
                                              + 'T00:00:00Z')
            file_data['date_text'] = (f"Published {file_data['date']}"
                                      + f"; updated {file_data['date_modified']}")
        else:
            file_data['date_sort'] = file_data['date']
            file_data['date_feed'] = file_data['date'] + 'T00:00:00Z'
            file_data['date_feed_updated'] = file_data['date_feed']
            file_data['date_text'] = f"Published {file_data['date']}"

        md_data.append(file_data)

        # Remove the markdown file
        file.unlink()

    # Sort in reverse date order
    md_data.sort(key=lambda x: x.get('date_sort'), reverse=True)

    return md_data


def process_md_data(md_files):
    ''' Process the markdown data '''

    sitemap_items = ''
    index_items = ''
    feed_items = ''

    layouts = load_layouts()

    for md_data in md_files:
        sitemap_item = ''
        index_item = ''
        feed_item = ''
       
        html = layouts['html']
        if md_data['is_public']:
            sitemap_item = layouts['sitemap_item']
        if md_data['is_post'] and md_data['is_public']:
            index_item = layouts['index_item']
            feed_item = layouts['feed_item']
        
        # insert the page metadata into the templates
        # exclude if not a string for now
        keys = [key for key in md_data if type(md_data[key]) == str]
        for key in keys:
            html = html.replace('{{ ' + key + ' }}', md_data.get(key))
            if md_data['is_public']:
                sitemap_item = (sitemap_item.replace('{{ ' + key + ' }}',
                                                     md_data.get(key)))
            if md_data['is_post'] and md_data['is_public']:
                index_item = (index_item.replace('{{ ' + key + ' }}',
                                                 md_data.get(key)))
                feed_item = (feed_item.replace('{{ ' + key + ' }}',
                                               md_data.get(key)))

        # set aria-current on navigation link
        nav_link = md_data.get('permalink').removeprefix(
            SITE_META.get('site_url'))
        nav_link = '/' + nav_link.split('/', 1)[0]
        if nav_link != '/':
            nav_link += '/'
        nav_link_html = f'<a href="{nav_link}">'
        nav_link_html_new = f'<a href="{nav_link}" aria-current="page">'
        html = html.replace(nav_link_html, nav_link_html_new)

        # set output file name replacing .md with .html
        output_file = Path(md_data['path'].with_suffix('.html'))

        # Write the output to the build directory
        write_file(output_file, html)

        # Add the page to the sitemap
        sitemap_items += sitemap_item
        index_items += index_item
        feed_items += feed_item

    # Generate the sitemap
    sitemap_output = layouts['sitemap'].replace('{{ content }}', sitemap_items)
    write_file(SITEMAP, sitemap_output)

    # generate the blog index page
    content = POST_INDEX.read_text(encoding='utf-8')
    content = content.replace('{{ post_index }}', index_items)
    write_file(POST_INDEX, content)

    # Generate the feed
    feed_output = layouts['feed'].replace('{{ content }}', feed_items)
    for key in SITE_META:
        feed_output = feed_output.replace(
            '{{ ' + key + ' }}', SITE_META.get(key))
    feed_output = feed_output.replace('{{ date_feed }}',
                                      md_files[0].get('date_feed_updated'))
    write_file(FEED, feed_output)

    # generate simple 404 page
    file_404 = layouts['file_404']
    for key in SITE_META:
        file_404 = file_404.replace('{{ ' + key + ' }}', SITE_META.get(key))
    write_file(FILE_404, file_404)


### main section ###
print('Site generation starting...')
print()

prepare_dirs()

md_files = get_md_data()

process_md_data(md_files)

print()
print('Site generation finished')
