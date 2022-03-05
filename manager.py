import xml.etree.ElementTree as ET
import bs4, os


def gen_html(filename):
    TEMPLATE = f'''<!DOCTYPE html>
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
    os.mkdir(version)
    os.chdir(version)

    for sura in quran_root.getchildren():
        soup = bs4.BeautifulSoup(TEMPLATE)
        index = sura.attrib['index']
        current_sura_meta = sura_meta[int(index) - 1]

        container = soup.find("div", {"id": "container"})

        sura_div = soup.new_tag('div')
        sura_div['class'] = "sura"

        sura_title = soup.new_tag('h1')
        sura_title.string = sura.attrib['name']

        for sura_attrib in current_sura_meta.keys():
            sura_div[sura_attrib] = current_sura_meta[sura_attrib]

        for aya in sura.getchildren():
            aya_div = soup.new_tag('div')
            aya_div['class'] = 'aya'
            aya_div['id'] = aya.attrib['index']
            aya_text = soup.new_tag('p')
            aya_text.string = aya.attrib['text']
            aya_end = soup.new_tag('div')
            aya_end.string = '۝'
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

if __name__ == "__main__":
    versions_list = [version for version in os.listdir('Versions')]
    for version in versions_list:
        gen_html(version)
    
