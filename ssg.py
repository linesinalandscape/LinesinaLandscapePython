from shutil import copytree

import markdown
import os

SOURCE_DIR = 'content/'
BUILD_DIR = 'build/'

# == Copy all contents to the build directory ==
copytree(SOURCE_DIR, BUILD_DIR, dirs_exist_ok=True)

# == Load the template and content ==
template: str
content: str

with open("templates/default.html") as file:
    template = file.read()

# make a list of files with .md extension in the build directory and subfolders with their full path
md_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(
    BUILD_DIR) for f in filenames if f.endswith('.md')]

print('Writing HTML files converted from markdown...')

for f in md_files:
	with open(f, encoding='utf-8') as file:
		content = file.read()

	# == Convert the markdown to HTML and store metadata ==
	md = markdown.Markdown(extensions=["meta"])
	html = md.convert(content)
	
	# == Insert the HTML content into the template ==
	output: str = template.replace('{{ content }}', html)
	output = output.replace('index.md', '\\')
		
	# set output file name replacing .md with .html
	output_file = f.replace('.md', '.html')

	# == Write the output to the build directory ==
	with open(output_file, "w", encoding='utf-8') as file:
		file.write(output)

	# == Remove the markdown file ==
	os.remove(f)

	print(output_file)

print('Site generation finished')
