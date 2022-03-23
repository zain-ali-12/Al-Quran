from pprint import pformat
import xml.etree.ElementTree as ET
import bs4, os

arabic_numbers = {
    '0': '٠',
    '1': '١',
    '2': '٢',
    '3': '٣',
    '4': '٤',
    '5': '٥',
    '6': '٦',
    '7': '٧',
    '8': '٨',
    '9': '٩'
}


def gen_html(filename):
    TEMPLATE = r'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title></title>
        <link rel="stylesheet" href="../../css/style.css">
    </head>
    <body>
        <div id="container"></div>
    </body>
    </html>'''

    meta_tree = ET.parse("MetaData.xml")
    meta_root = meta_tree.getroot()
    quran_tree = ET.parse(f"Versions/{filename}")
    quran_root = quran_tree.getroot()
    sura_meta = []

    for sura in meta_root.getchildren()[0]:
        sura_meta.append(sura.attrib)

    os.chdir(r'suras\html')
    version = filename[6:-4]
    try:
        os.mkdir(version)
    except Exception as e:
        pass
    os.chdir(version)


    for sura in quran_root.getchildren():
        # print(sura_meta)
        soup = bs4.BeautifulSoup(TEMPLATE)
        index = sura.attrib['index']
        current_sura_meta = sura_meta[int(index) - 1]

        container = soup.find("div", {"id": "container"})

        sura_div = soup.new_tag('div')
        sura_div['class'] = "sura"

        sura_title = soup.new_tag('h1')
        sura_title.string = f"{sura.attrib['name']}"

        for sura_attrib in current_sura_meta.keys():
            sura_div[sura_attrib] = current_sura_meta[sura_attrib]

        for aya in sura.getchildren():
            aya_div = soup.new_tag('div')
            aya_div['class'] = 'aya'
            aya_div['id'] = aya.attrib['index']
            aya_text = soup.new_tag('div')
            aya_text['class'] = "aya-text"
            aya_text.string = aya.attrib['text']
            aya_end = soup.new_tag('div')
            aya_end.string = '۝'
            aya_end['class'] = 'aya-end'
            aya_end_index = ''
            for number in aya.attrib["index"]:
                aya_end_index += arabic_numbers[number]

            aya_end['index'] = aya_end_index
            aya_text.append(aya_end)
            aya_div.append(aya_text)

            for aya_attrib in aya.attrib:
                aya_div[aya_attrib] = aya.attrib[aya_attrib]
        
            sura_div.append(aya_div)

        container.append(sura_title)
        container.append(sura_div)

        while len(index) < 3:
            index = '0' + index

        with open(f"{index}.html", 'w', encoding='utf-8') as html_file:
            html_file.write(soup.prettify())
    os.chdir('../../..')


def gen_home_html():
    TEMPLATE = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title></title>
        <link rel="stylesheet" href="/suras/css/style.css">
    </head>
    <body>
        
    </body>
    </html>'''
    meta_tree = ET.parse("MetaData.xml")
    meta_root = meta_tree.getroot()
    sura_list = []
    for sura in meta_root.getchildren()[0]:
        sura_list.append(sura.attrib['tname'])

    soup = bs4.BeautifulSoup(TEMPLATE)
    body = soup.find('body')
    container = soup.new_tag('div')
    container['id'] = 'home-container'
    os.chdir('suras/html/uthmani')
    itercount = 0
    for sura in os.listdir(os.getcwd()):
        new_link = soup.new_tag('a')
        new_link['href'] = f'suras/html/uthmani/{sura}'
        new_link['class'] = 'sura-link'
        new_link.string = sura_list[itercount]
        itercount += 1
        container.append(new_link)
    body.append(container)
    os.chdir('../../..')
    with open('index.html', 'w') as f:
        f.write(soup.prettify())

if __name__ == "__main__":
    versions_list = [version for version in os.listdir('Versions')]
    #gen_home_html()

    for version in versions_list:
        gen_html(version)
    
