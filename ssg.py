'''
TODO
- all date related stuff 
- 404
- production permalinks
- remove jekyll from footer
- aria-current?
- paths for feed
- add feed
- add sitemap and path
- blog index page
- OG images
- reorganise images
- validate html
- check performance
- tags?
- image lazy loading, size?
'''

from shutil import copytree, rmtree
from pathlib import Path
import datetime as dt
import markdown

SOURCE_DIR = Path('content')
BUILD_DIR = Path('build')
SITEMAP = Path('build/sitemap.xml')
TEMPLATE_HTML = Path('templates/default.html')
TEMPLATE_SITEMAP = Path('templates/sitemap.xml')
TEMPLATE_SITEMAP_ITEM = Path('templates/sitemap_item.xml')

# sitewide metadata for use in the template
SITE_META = {
    'site_url': 'http://localhost:8000/',
    'site_title': 'Lines in a Landscape',
    'site_author': 'Alan Grant'
}

# Empty build directory and copy all contents
rmtree(BUILD_DIR, ignore_errors=True)
copytree(SOURCE_DIR, BUILD_DIR)

# Load the layout templates
layout_html = TEMPLATE_HTML.read_text(encoding='utf-8')
layout_sitemap = TEMPLATE_SITEMAP.read_text(encoding='utf-8')
layout_sitemap_item = TEMPLATE_SITEMAP_ITEM.read_text(encoding='utf-8')

# make a list of files with .md extension in the build directory and subfolders
md_files = list(BUILD_DIR.rglob('*.md'))
sitemap_items = ''

print('Writing HTML files converted from markdown...')

for md_file in md_files:
    
    # read the markdown file
    content = md_file.read_text(encoding='utf-8')

    # Convert the markdown to HTML and store metadata
    md = markdown.Markdown(extensions=["meta"])
    html = md.convert(content)
    page_meta = md.Meta

    # Insert the HTML content into the template
    output = layout_html.replace('{{ content }}', html)

    # various metadata fields not already in the markdown file 
    # set the final url for the page
    permalink = (SITE_META.get('site_url')
                 + str(md_file.relative_to(BUILD_DIR).parent) + '/')
    permalink = permalink.replace('\\', '/')
    permalink = permalink.replace('./', '')  # for root index page
    page_meta['permalink'] = [permalink]

    # set date for the page in priority order:
    # date updated in metadata, date in metadata, file modified date
    #date_file = dt.datetime.fromtimestamp(md_file.stat().st_mtime)
    # convert to human readable date in format YYYY-MM-DD
    # date_final = dt.datetime.strptime(date_file, '%Y-%m-%d')
    #    date_final = ''
    # if page_meta.get('date_updated'):
    #    date_final = page_meta.get('date_updated')[0]
    # elif page_meta.get('date'):
    #    date_final = page_meta.get('date')[0]
    # page_meta['date_final'] = date_final
    date_final = dt.datetime.now().strftime('%Y-%m-%d') # TODO FIX
    page_meta['date_final'] = [date_final]
    
    # insert the site metadata into the template
    for key in SITE_META:
        output = output.replace('{{ ' + key + ' }}', SITE_META.get(key))

    # insert the page metadata into the templates
    for key in md.Meta:
        output = output.replace('{{ ' + key + ' }}', page_meta.get(key)[0])
        sitemap_item = (layout_sitemap_item.replace('{{ ' + key + ' }}',
                                                      page_meta.get(key)[0]))

    # reformat internal links
    output = output.replace('\index.md', '/')

    # set output file name replacing .md with .html
    output_file = Path(md_file.with_suffix('.html'))

    # Write the output to the build directory
    output_file.write_text(output, encoding='utf-8')

    # Remove the markdown file
    md_file.unlink()

    print(output_file)

    # Add the page to the sitemap
    sitemap_items += sitemap_item

# Generate the sitemap
sitemap_output = layout_sitemap.replace('{{ content }}', sitemap_items)
SITEMAP.write_text(sitemap_output, encoding='utf-8')
print()
print('Sitemap written to', SITEMAP)
print('Site generation finished')
