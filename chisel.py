#!/usr/bin/python

# Chisel
# David Zhou
# 
# Requires:
# jinja2

import sys, re, time, os, codecs
import jinja2, markdown
import shutil

#Settings
SOURCE = "./blog/" #end with slash
DESTINATION = "./live/" #end with slash
HOME_SHOW = 15 #numer of entries to show on homepage
TEMPLATE_PATH = "./templates/"
TEMPLATE_OPTIONS = {}
TEMPLATES = {
    'home': "home.html",
    'detail': "detail.html",
    'static': "static.html",
    'archive': "archive.html",
}
TIME_FORMAT = "%B %d - %Y"
ENTRY_TIME_FORMAT = "%Y-%m-%d"
#FORMAT should be a callable that takes in text
#and returns formatted text
FORMAT = lambda text: markdown.markdown(text, ['footnotes',]) 
#########

STEPS = []

def step(func):
    def wrapper(*args, **kwargs):
        print "Starting " + func.__name__ + "...",
        func(*args, **kwargs)
        print "Done."
    STEPS.append(wrapper)
    return wrapper

def get_tree(source):
    files = []
    for root, ds, fs in os.walk(source):
        for name in fs:
            if name[0] == ".": continue
            path = os.path.join(root, name)
            f = open(path, "rU")
            title = f.readline()
            date = time.strptime(name[:10], ENTRY_TIME_FORMAT)
            year, month, day = date[:3]
            files.append({
                'title': title,
                'epoch': time.mktime(date),
                'content': FORMAT(''.join(f.readlines()).decode('UTF-8')),
                'url': '/'.join([str(year), "-".join(title.split()), "index.html"]),
                'pretty_date': time.strftime(TIME_FORMAT, date),
                'date': date,
                'year': year,
                'month': month,
                'day': day,
                'filename': name,
            })
            f.close()
    return files

def compare_entries(x, y):
    result = cmp(-x['epoch'], -y['epoch'])
    if result == 0:
        return -cmp(x['filename'], y['filename'])
    return result

def write_file(url, data):
    path = DESTINATION + url
    dirs = os.path.dirname(path)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    file = open(path, "w")
    file.write(data.encode('UTF-8'))
    file.close()

def cleanup():
  """ Remove all previously generated pages """
  for root, dirs, files in os.walk(DESTINATION):
    for f in files:
    	os.unlink(os.path.join(root, f))
    for d in dirs:
    	shutil.rmtree(os.path.join(root, d))

@step
def generate_homepage(f, e):
    """Generate homepage"""
    cleanup()
    template = e.get_template(TEMPLATES['home'])
    write_file("index.html", template.render(entries=f[:HOME_SHOW]))

@step
def master_archive(f, e):
    """Generate master archive list of all entries"""
    template = e.get_template(TEMPLATES['archive'])
    write_file("archives.html", template.render(entries=f))

@step
def detail_pages(f, e):
    """Generate detail pages of individual posts"""
    template = e.get_template(TEMPLATES['detail'])
    for file in f:
        write_file(file['url'], template.render(entry=file))

@step
def static_pages(f, e):
    """Generate static pages"""
    template = e.get_template(TEMPLATES['static'])
    for file in f:
        write_file(file['url'], template.render(entry=file))

def main():
    print "Chiseling..."
    print "\tReading files...",
    files = sorted(get_tree(SOURCE), cmp=compare_entries)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), **TEMPLATE_OPTIONS)
    print "Done."
    print "\tRunning steps..."
    for step in STEPS:
        print "\t\t",
        step(files, env)
    print "\tDone."
    print "Done."

if __name__ == "__main__":
    sys.exit(main())
