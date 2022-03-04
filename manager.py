import xml.etree.ElementTree as ET
import os

tree = ET.parse("MetaData.xml")
root = tree.getroot()
print(root)
def generate_suras_files():
    os.chdir(r"C:\Users\Zain Ali\Documents\GitHub\Al-Quran\Suras")
    for i in range(114):
        i = str(i+1)
        while len(i) != 3:
            i = "0" + i
        with open(i+".txt", 'w') as new_file:
            pass

def generate_surah_html(filename):
    pass