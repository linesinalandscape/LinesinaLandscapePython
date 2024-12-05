'''
TODO
- 404
- remove jekyll from footer
- navigation
- aria-current?
- paths for canonical and feed
- add feed
- add sitemap
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
import markdown

SOURCE_DIR = Path('content')
BUILD_DIR = Path('build')
TEMPLATE_FILE = Path('templates/default.html')

# sitewide metadata for use in the template
SITE_META = {
    'site_url': '',
    'site_title': 'Lines in a Landscape',
    'site_author': 'Alan Grant'
}

# Empty build directory and copy all contents
rmtree(BUILD_DIR, ignore_errors=True)
copytree(SOURCE_DIR, BUILD_DIR)

# Load the template
template = TEMPLATE_FILE.read_text(encoding='utf-8')

# make a list of files with .md extension in the build directory and subfolders
md_files = list(BUILD_DIR.rglob('*.md'))

print('Writing HTML files converted from markdown...')

for md_file in md_files:

    # read the markdown file
    content = md_file.read_text(encoding='utf-8')

    # Convert the markdown to HTML and store metadata
    md = markdown.Markdown(extensions=["meta"])
    html = md.convert(content)

    # Insert the HTML content into the template
    output = template.replace('{{ content }}', html)

    # insert the site metadata into the template
    for key in SITE_META:
        output = output.replace('{{ ' + key + ' }}', SITE_META.get(key))

    # insert the page metadata into the template
    for key in md.Meta:
        output = output.replace('{{ ' + key + ' }}', md.Meta.get(key)[0])

    # reformat internal links
    output = output.replace('\index.md', '/')

    # set output file name replacing .md with .html
    output_file = Path(md_file.with_suffix('.html'))

    # Write the output to the build directory
    output_file.write_text(output, encoding='utf-8')

    # Remove the markdown file
    md_file.unlink()

    print(output_file)

print('Site generation finished')
