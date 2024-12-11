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
TEMPLATE_HTML = Path('templates/default.html')
TEMPLATE_SITEMAP = Path('templates/sitemap.xml')
TEMPLATE_SITEMAP_ITEM = Path('templates/sitemap_item.xml')
TEMPLATE_FEED = Path('templates/feed.xml')
TEMPLATE_FEED_ITEM = Path('templates/feed_item.xml')

# sitewide metadata for use in the template
SITE_META = {
    'site_url': 'http://localhost:8000/',
    'site_title': 'Lines in a Landscape',
    'site_author': 'Alan Grant',
    'site_description': 'Trails, trains, maps, Málaga, and more - a personal website'
}

# Empty build directory and copy all contents
rmtree(BUILD_DIR, ignore_errors=True)
copytree(SOURCE_DIR, BUILD_DIR)

# Load the layout templates
layout_html = TEMPLATE_HTML.read_text(encoding='utf-8')
layout_sitemap = TEMPLATE_SITEMAP.read_text(encoding='utf-8')
layout_sitemap_item = TEMPLATE_SITEMAP_ITEM.read_text(encoding='utf-8')
layout_feed = TEMPLATE_FEED.read_text(encoding='utf-8')
layout_feed_item = TEMPLATE_FEED_ITEM.read_text(encoding='utf-8')

# make a list of files with .md extension in the build directory and subfolders
files = list(BUILD_DIR.rglob('*.md'))

sitemap_items = ''
feed_items = ''

print('Writing HTML files converted from Markdown...')

for file in files:

    # set flag for blog post if file is in subfolder of 'blog'
    is_post = ('blog' in str(file.parent)
               and not str(file.parent).endswith('blog'))

    # read the markdown file
    content = file.read_text(encoding='utf-8')

    # Convert markdown to HTML and store metadata
    html = markdown(content, extras=['metadata'])
    page_meta = html.metadata

    # Insert the HTML content into the templates
    output = layout_html.replace('{{ content }}', html)
    sitemap_item = layout_sitemap_item
    if is_post:
        feed_item = layout_feed_item.replace('{{ content }}', html)
    else:
        feed_item = ''

    # various metadata fields not already in the markdown file
    # set the final url for the page
    permalink = (SITE_META.get('site_url')
                 + str(file.relative_to(BUILD_DIR).parent) + '/')
    permalink = permalink.replace('\\', '/')
    permalink = permalink.replace('./', '')  # for root index page
    page_meta['permalink'] = permalink

    # set date for the page in priority order:
    # TODO FIX THIS
    page_meta['date_final'] = '2024-12-01'

    # insert the site metadata into the templates
    for key in SITE_META:
        output = output.replace('{{ ' + key + ' }}', SITE_META.get(key))
        sitemap_item = sitemap_item.replace('{{ ' + key + ' }}',
                                            SITE_META.get(key))
        feed_item = feed_item.replace('{{ ' + key + ' }}', SITE_META.get(key))

    # insert the page metadata into the templates
    # exclude if not a string TODO sort out images in metadata
    keys = [key for key in page_meta if type(page_meta[key]) == str]
    for key in keys:
        output = output.replace('{{ ' + key + ' }}', page_meta.get(key))
        sitemap_item = (sitemap_item.replace('{{ ' + key + ' }}',
                                             page_meta.get(key)))
        feed_item = (feed_item.replace('{{ ' + key + ' }}',
                                       page_meta.get(key)))

    # reformat internal links
    output = output.replace('\index.md', '/')
    feed_item = feed_item.replace('\index.md', '/')

    # set output file name replacing .md with .html
    output_file = Path(file.with_suffix('.html'))

    # Write the output to the build directory
    output_file.write_text(output, encoding='utf-8')

    # Remove the markdown file
    file.unlink()

    print(output_file)

    # Add the page to the sitemap
    sitemap_items += sitemap_item
    feed_items += feed_item

# Generate the sitemap
sitemap_output = layout_sitemap.replace('{{ content }}', sitemap_items)
SITEMAP.write_text(sitemap_output, encoding='utf-8')
print()
print('Sitemap written to', SITEMAP)

# Generate the feed
feed_output = layout_feed.replace('{{ content }}', feed_items)
for key in SITE_META:
    feed_output = feed_output.replace('{{ ' + key + ' }}', SITE_META.get(key))
# TODO date of feed
FEED.write_text(feed_output, encoding='utf-8')
print('Feed written to', FEED)

print()
print('Site generation finished')
