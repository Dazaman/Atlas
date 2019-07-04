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
    text.append('<p><h1>BGH Atlas</h1></p>')
    
    categories = {}
    
    for url in atlas_info.keys():
        cat = atlas_info[url]['category']
        if cat in categories.keys():
            categories[cat].append(url)
        else:
            categories[cat] = [url] 

    categories = dict(sorted(categories.items()))
    for k,v in categories.items():
        categories[k] = sorted(v)

    for cat in categories.keys():
        text.append('<p><h2> %s Models </h2></p>' %(cat.capitalize()))
        text.append('<p><h2> %s Models </h2></p>' %(cat.capitalize()))
        text.append('<table>')
        text.append('<thead>')
        text.append('<tr>')
        text.append('<th style="text-align: left">%s</th>'%('  '))
        text.append('<th style="text-align: left">%s</th>'%('Model Name'))
        text.append('<th style="text-align: left">%s</th>'%('Contributor Name '))
        text.append('<tr>')
        text.append('</thead>')
        text.append('<tbody>')
        for url in categories[cat]:
            direc = str(os.path.split(atlas_info[url]['url'])[:-1])
            direc = direc.encode('utf8')
            
            if atlas_info[url]['image'] != "":
                image_url = direc[3:-3] +'/'+ atlas_info[url]['image']
            else:
                image_url = 'https://www.earthbyte.org/wp-content/uploads/2015/08/EByteglobe.jpg'
            text.append('<tr>')
            text.append('<td style="text-align: left"><img src="%s" height="75" width="90"></td>'%(image_url))
            text.append('<td style="text-align: left"><a href="%s"> %s </a></td>'%(atlas_info[url]['url'],atlas_info[url]['name']))
            text.append('<td style="text-align: left">%s </td>'%(atlas_info[url]['contributor']))
            
            text.append('</tr>')

        text.append('</tbody>')
        text.append('</table>')

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
            'other': page_info['other']
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
    
    # print 'length before del', len(atlas_info)
    
    for key, value in atlas_info.items():

        # print '\nkey  ', key
        directory = os.path.join(*(key.split('/')[-3:-1]))
        file = os.path.join(*(key.split('/')[-3:]))
        local_dir_path = os.path.join(hostdir,directory)
        local_file_path = os.path.join(hostdir,file)
        
        # print 'Check dir exists ', os.path.isdir(local_dir_path)
        # print 'Check file exists' ,os.path.exists(local_file_path)

        if os.path.exists(local_file_path) and os.path.isdir(local_dir_path):
            pass
        else:
            atlas_info.pop(key, None)

    # print 'length after del',len(atlas_info)
    
    with open(atlas_info_filename, 'w') as file:
        json.dump(atlas_info, file)

    # Create a new front page:
    update_frontpage()