import os
import json
import collections
import urllib2

hostdir = os.path.abspath(os.path.dirname(__file__))
atlas_info_filename = os.path.join(hostdir, "_atlas_info.json")
atlas_url = 'https://basin-genesis-hub.github.io/Atlas/'
atlas_pages_dirname = 'pages'
atlas_pages_url = os.path.join(atlas_url, atlas_pages_dirname)
atlas_index_filename = os.path.join(hostdir, 'index.html')
page_notebook_dir = True 
# header_path = os.path.join(os.path.abspath(os.path.join(os.path.split(os.getcwd())[0], os.pardir)),'site_resources','header.txt')
target_url = 'https://raw.githubusercontent.com/basin-genesis-hub/Atlas/master/site_resources/header.txt'

def load_atlas_info():
    try:
        with open(atlas_info_filename, 'r') as file:
            atlas_info_items = json.load(file)
        atlas_info = dict(atlas_info_items)
    except:
        atlas_info = {}
    return atlas_info

def save_atlas_info(atlas_info):
    with open(atlas_info_filename, 'w') as file:
        json.dump(atlas_info, file)

def update_frontpage():
    atlas_info = load_atlas_info()
    text = []
    text.append('---')
    text.append('layout: default')
    text.append('---')

    header_data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
    for line in header_data: # files are iterable
        text.append(line)

    text.append('<body>')
    text.append('<p><h1>Basin Genesis Hub Atlas</h1></p>')
    
    cat_list = ['Underworld','Badlands','Badlands Case Study','Underworld Badlands Coupled']#,'PyGplates','Gplates & Citcoms']
    uw_list = ['Extension','Compression','Underworld-Strike-slip']
    blc_list = ['Basin','Rift','Badlands-Strike-slip','Fluvio-deltaic']
    blr_list = ['Case-studies']
    cp_list = ['Extension-coupled','Compression-coupled', 'Strike-slip-coupled']
    # pg_list = ['PyGplates']
    # gc_list = ['Gplates & Citcoms']

    categories = {c:dict() for c in cat_list}
    for url in atlas_info.keys():
        cat = atlas_info[url]['category']
        if cat in uw_list:
            if cat in categories['Underworld'].keys():
                categories['Underworld'][cat].append(url)
            else:
                categories['Underworld'][cat] = [url] 

        elif cat in blc_list:
            if cat in categories['Badlands'].keys():
                categories['Badlands'][cat].append(url)
            else:
                categories['Badlands'][cat] = [url] 

        elif cat in blr_list:
            if cat in categories['Badlands Case Study'].keys():
                categories['Badlands Case Study'][cat].append(url)
            else:
                categories['Badlands Case Study'][cat] = [url] 

        elif cat in cp_list:
            if cat in categories['Underworld Badlands Coupled'].keys():
                categories['Underworld Badlands Coupled'][cat].append(url)
            else:
                categories['Underworld Badlands Coupled'][cat] = [url] 

        # elif cat in pg_list:
        #     if cat in categories['PyGplates'].keys():
        #         categories['PyGplates'][cat].append(url)
        #     else:
        #         categories['PyGplates'][cat] = [url] 
        
        # elif cat in gc_list:
        #     if cat in categories['Gplates & Citcoms'].keys():
        #         categories['Gplates & Citcoms'][cat].append(url)
        #     else:
        #         categories['Gplates & Citcoms'][cat] = [url] 
        # else:
        #     if cat in categories['Uncategorised'].keys():
        #         categories['Uncategorised'][cat].append(url)
        #     else:
        #         categories['Uncategorised'][cat] = [url] 

    # categories = collections.OrderedDict(sorted(categories.items()))
    for k,v in categories.items():
        for k1,v1 in categories[k].items():
            categories[k][k1] = sorted(v1)
    
    # for cat in categories.keys():
    for cat in cat_list:
        text.append('<br>')
        text.append('<p><h2> %s models</h2></p>' %(cat.capitalize()))
        text.append('<p><h2>  </h2></p>')
        for sub_cat in categories[cat]:
            text.append('<h3> %s </h3>' %(sub_cat.capitalize()))
            text.append('<h3>  </h3>')
            text.append('<div style="overflow-x:auto;">')
            text.append('<table>')
            text.append('<thead>')
            text.append('<tr>')
            text.append('<th style="text-align: left">%s</th>'%('  '))
            text.append('<th style="text-align: left">%s</th>'%('Model Name'))
            text.append('<th style="text-align: left">%s</th>'%('Contributor Name '))
            text.append('<tr>')
            text.append('</thead>')
            text.append('<tbody>')
            
            for url in categories[str(cat)][str(sub_cat)]:
                direc = str(os.path.split(atlas_info[url]['url'])[:-1])
                direc = direc.encode('utf8')
                
                if atlas_info[url]['image'] != "":
                    image_url = direc[3:-3] +'/'+ atlas_info[url]['image']
                else:
                    if cat == 'Underworld':
                        image_url = 'https://www.earthbyte.org/wp-content/uploads/2017/09/underworld.png'
                    elif cat == 'Badlands':
                        image_url = 'https://www.earthbyte.org/wp-content/uploads/2015/08/a5a5fb2e-3f32-11e5-9a1c-407c3a6d327a.png'
                    elif cat == 'Coupled':
                        image_url = 'https://www.earthbyte.org/wp-content/uploads/2015/08/bgh_image.jpg'
                    elif cat == 'PyGplates':
                        image_url = 'https://www.earthbyte.org/wp-content/uploads/2019/05/image001.png'
                    elif cat == 'Gplates & Citcoms':
                        image_url = 'https://www.earthbyte.org/wp-content/uploads/2018/10/GPlates_CitcomS_EBA-01.png'
                    else:
                        image_url = 'https://www.earthbyte.org/wp-content/uploads/2015/08/EByteglobe.jpg'
                text.append('<tr>')
                text.append('<td style="text-align: left"><img src="%s" height="75" width="90"></td>'%(image_url))
                text.append('<td style="text-align: left"><a href="%s"> %s </a></td>'%(atlas_info[url]['url'],atlas_info[url]['name']))
                text.append('<td style="text-align: left">%s </td>'%(atlas_info[url]['contributor']))
                
                text.append('</tr>')

            text.append('</tbody>')
            text.append('</table>')
            text.append('</div>')

    # text.append('<p><h3>Contribute to the Atlas</h3></p>')
    # text.append('<p>')
    # text.append('<ol>')
    # text.append('<li><a href="https://github.com/basin-genesis-hub/Atlas">Clone the repository</a></li>')
    # text.append('<li>Go to the "pages" directory and make a copy of the "example" folder</li>')
    # text.append('<li>Open up the Jupyter notebook and follow the instructions (make sure to run the code at the bottom when you are finished!)</li>')
    # text.append('<li>Push your changes back up to the repository</li>')
    # text.append('</ol>')
    # text.append('</p>')
    text.append('</body>')
    with open(atlas_index_filename, 'w') as file:
        file.write('\n'.join(text))

    print "Successfully binded page! "
def bind_page(page_info,u=None):
    # Create html:
    command = 'jupyter nbconvert --to html ' + 'page.ipynb'
    os.system(command)

    if u == None:
        page_notebook_dir = True
        page_dirname = os.path.split(os.getcwd())[-1]
        page_url = os.path.join(atlas_pages_url, page_dirname, 'page.html')
        print 'Running from Individual notebook'#, page_url
    else:
        page_notebook_dir = False
        page_url = os.path.join(atlas_pages_url, u, 'page.html')
        print 'Running from Update notebook '#, page_url

    # Save page info:
    page_dict = {
        'tools': {
            'underworld': page_info['underworld'],
            'badlands': page_info['badlands'],
            'gplates': page_info['gplates'],
            'pygplates': page_info['pygplates'],
            'citcoms': page_info['citcoms'],
            'gmt': page_info['gmt'],
            'other': page_info['other'],
            },
        'contributor': page_info['contributor_name'],
        'category': page_info['category'],
        'name': page_info['model_name'],
        'url': page_url,
        'image': page_info['image'],
        }

    # Add page info to atlas info:
    atlas_info = load_atlas_info()
    atlas_info[page_url] = page_dict
    
    for key, value in atlas_info.items():
        directory = os.path.join(*(key.split('/')[-3:-1]))
        file = os.path.join(*(key.split('/')[-3:]))
        local_dir_path = os.path.join(hostdir,directory)
        local_file_path = os.path.join(hostdir,file)
        if os.path.exists(local_file_path) and os.path.isdir(local_dir_path):
            pass
        else:
            atlas_info.pop(key, None)
    
    save_atlas_info(atlas_info)

    # Create a new front page:
    update_frontpage()