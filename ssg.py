'''
TODO
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

import markdown
import os

SOURCE_DIR = 'content/'
BUILD_DIR = 'build/'

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
with open("templates/default.html") as file:
    template = file.read()

# make a list of files with .md extension in the build directory and subfolders
md_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(
    BUILD_DIR) for f in filenames if f.endswith('.md')]

print('Writing HTML files converted from markdown...')

for f in md_files:
    with open(f, encoding='utf-8') as file:
        content = file.read()

    # Convert the markdown to HTML and store metadata
    md = markdown.Markdown(extensions=["meta"])
    html = md.convert(content)

    # Insert the HTML content into the template
    output: str = template.replace('{{ content }}', html)

    # insert the site metadata into the template
    for key in SITE_META:
        output = output.replace('{{ ' + key + ' }}', SITE_META.get(key))

    # insert the page metadata into the template
    for key in md.Meta:
        output = output.replace('{{ ' + key + ' }}', md.Meta.get(key)[0])

    # reformat internal links
    output = output.replace('\index.md', '/')

    # set output file name replacing .md with .html
    output_file = f.replace('.md', '.html')

    # == Write the output to the build directory ==
    with open(output_file, "w", encoding='utf-8') as file:
        file.write(output)

    # == Remove the markdown file ==
    os.remove(f)

    print(output_file)

print('Site generation finished')
