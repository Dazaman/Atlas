import os
import json

hostdir = os.path.abspath(os.path.dirname(__file__))
atlas_info_filename = os.path.join(hostdir, "_atlas_info.json")
atlas_url = 'https://basin-genesis-hub.github.io/Atlas/'
atlas_pages_dirname = 'pages'
atlas_pages_url = os.path.join(atlas_url, atlas_pages_dirname)
atlas_index_filename = os.path.join(hostdir, 'index.html')

def load_atlas_info():
    try:
        with open(atlas_info_filename, 'r') as file:
            atlas_info_items = json.load(file)
        atlas_info = dict(atlas_info_items)
    except:
        atlas_info = {}
    return atlas_info

def update_frontpage():
    atlas_info = load_atlas_info()
    text = []
    text.append('---')
    text.append('layout: default')
    text.append('---')
    text.append('<body>')
    text.append('<p><h1>BGH Atlas prototype</h1></p>')

    text.append('<p><h2>MODELS</h2></p>')
    for htmlpage, page_info in sorted(atlas_info.items()):
#         modelname, ext = os.path.splitext(os.path.basename(htmlpage))
        text.append('<p>')
        text.append('<a href="')
        text.append(htmlpage)
        text.append('">')
        text.append(page_info['name'])
        text.append('</a>')
        text.append('</p>')
    text.append('<p><h3>Contribute to the Atlas</h3></p>')
    text.append('<p>')
    text.append('<ol>')
    text.append('<li><a href="https://github.com/rsbyrne/demonstration">Clone the repository</a></li>')
    text.append('<li>Go to the "pages" directory and make a copy of the "example" folder</li>')
    text.append('<li>Open up the Jupyter notebook and follow the instructions (make sure to run the code at the bottom when you are finished!)</li>')
    text.append('<li>Push your changes back up to the repository</li>')
    text.append('</ol>')
    text.append('</p>')
    text.append('</body>')
    with open(atlas_index_filename, 'w') as file:
        file.write('\n'.join(text))

def bind_page(page_info):

    # Create html:
    command = 'jupyter nbconvert --to html ' + 'page.ipynb'
    os.system(command)

    # Define page url:
    page_dirname = os.path.split(os.getcwd())[-1]
    page_url = os.path.join(atlas_pages_url, page_dirname, 'page.html')
    
    # Save page info:
    page_dict = {
        'tools': {
            'underworld': page_info['underworld'],
            'badlands': page_info['badlands'],
            'gplate': page_info['gplates'],
            },
        'contributor': page_info['contributor_name'],
        'category': page_info['category'],
        'name': page_info['model_name'],
        'url': page_url,
        'image': page_info['image'],
        }
#     with open('_page_info.json', 'w') as file:
#         json.dump(page_dict, file)

    # Add page info to atlas info:
    atlas_info = load_atlas_info()
    atlas_info[page_url] = page_dict
    with open(atlas_info_filename, 'w') as file:
        json.dump(atlas_info, file)

    # Create a new front page:
    update_frontpage()