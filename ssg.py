'''
TODO
- post titles
- all date related stuff
- feed id
- markdown2 in github
- production permalinks
- aria-current?
- paths for feed
- add feed
- blog index page
- OG images
- reorganise images
- validate html
- check performance
- tags?
- image lazy loading, size?
- 404 check
- blogroll redirect check
'''

from shutil import copytree, rmtree
from pathlib import Path
from markdown2 import markdown

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
    'feed': Path('templates/feed.xml'),
    'feed_item': Path('templates/feed_item.xml'),
    'file_404': Path('templates/404.html')
}

SITE_META = {
    'site_url': 'http://localhost:8000/',
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

        # various metadata fields not already in the markdown file
        # set the final url for the page
        permalink = (SITE_META.get('site_url')
                     + str(file.relative_to(BUILD_DIR).parent) + '/')
        permalink = permalink.replace('\\', '/')
        permalink = permalink.replace('./', '')  # for root index page
        file_data['permalink'] = permalink

        # set date for the page in priority order:
        # TODO FIX THIS
        file_data['date_final'] = '2024-12-01'

        md_data.append(file_data)

        # Remove the markdown file
        file.unlink()

    return md_data


def process_md_data(md_files):
    ''' Process the markdown data '''

    sitemap_items = ''
    feed_items = ''

    layouts = load_layouts()

    for md_data in md_files:
        output = layouts['html']
        sitemap_item = layouts['sitemap_item']
        if md_data['is_post']:
            feed_item = layouts['feed_item']
        else:
            feed_item = ''

        # insert the page metadata into the templates
        # exclude if not a string for now
        keys = [key for key in md_data if type(md_data[key]) == str]
        for key in keys:
            output = output.replace('{{ ' + key + ' }}', md_data.get(key))
            sitemap_item = (sitemap_item.replace('{{ ' + key + ' }}',
                                                 md_data.get(key)))
            if md_data['is_post']:
                feed_item = (feed_item.replace('{{ ' + key + ' }}',
                                               md_data.get(key)))

        # reformat internal links
        output = output.replace('\index.md', '/')
        feed_item = feed_item.replace('\index.md', '/')

        # set output file name replacing .md with .html
        output_file = Path(md_data['path'].with_suffix('.html'))

        # Write the output to the build directory
        write_file(output_file, output)

        # Add the page to the sitemap
        sitemap_items += sitemap_item
        feed_items += feed_item

    # generate the blog index page
    # post_index_text = 'placeholder for post index'
    # content = POST_INDEX.read_text(encoding='utf-8')
    # content = content.replace('{{ post_index }}', post_index_text)
    # POST_INDEX.write_text(content, encoding='utf-8')

    # Generate the sitemap
    sitemap_output = layouts['sitemap'].replace('{{ content }}', sitemap_items)
    write_file(SITEMAP, sitemap_output)

    # Generate the feed
    feed_output = layouts['feed'].replace('{{ content }}', feed_items)
    for key in SITE_META:
        feed_output = feed_output.replace(
            '{{ ' + key + ' }}', SITE_META.get(key))
    # TODO date of feed
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
