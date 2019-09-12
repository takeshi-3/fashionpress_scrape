import requests
import re
import os
from bs4 import BeautifulSoup

class PageInfo:
    def __init__(self, brand, season, gender, id):
        self.brand = brand
        self.season = season
        self.gender = gender
        self.id = id

# 保存先フォルダ
save_path = "./data/fashionpress/%s"

# コレクションページurl
url = "https://www.fashion-press.net/collections/%s"

# 対象ブランド
target_brands = [
    'Alexander McQueen', 'BALENCIAGA', 'Berluti', 'BURBERRY', 'CHANEL', 'CHRISTIAN DADA',
    'COMME des GARÇONS', 'DIOR', 'dunhill', 'FENDI', 'Givenchy', 'GUCCI', 'HERMÈS', 'ISSEY MIYAKE',
    'LACOSTE', 'LOUIS VUITTON', 'Paul Smith', 'PRADA', 'Saint Laurent', 'Y\'s', 'Yohji Yamamoto'
]

# フォルダ名変換
folder_names = {
    'メンズ': 'mens', 'ウィメンズ': 'womens', 'ウィメンズ&メンズ': 'w&m'
}
for age in range(2009, 2021):
    folder_names[str(age) + '年春夏'] = str(age) + 'ss'
    folder_names[str(age) + '-' + str(age+1)[2:4] + '年秋冬'] = str(age) + '-' + str(age+1) + 'aw'


def get_brand_id():
    req = requests.get(url%(''))
    soup = BeautifulSoup(req.text, 'lxml')
    brands = soup.find('ul', class_ = 'tab_content_alphabet').find_all('li')
    id = {}
    for brand in brands:
        atag = brand.find('a')
        for tb in target_brands:
            if atag.text == tb:
                id[tb] = atag['href'].split('/')[-1]
    return id

def get_page_info(brand_id):
    req = requests.get(url%('brand/' + brand_id))
    soup = BeautifulSoup(req.text, 'lxml')
    pages = soup.find_all('div', class_ = 'fp_media_tile')
    brand = soup.find('div', class_ = 'fp_wrapper').find('h1').find('a').text
    page_info = []
    for page in pages:
        tags = page.find('div', class_ = 'collections_media_title').find_all('span')
        season = tags[1].text
        gender = tags[2].text
        id = page.find('a')['href'].split('/')[-1]
        page_info.append(PageInfo(brand, season, gender, id))
    return page_info

def save_images(info):
    req = requests.get(url%(info.id))
    soup = BeautifulSoup(req.text, 'lxml')
    if info.season in folder_names:
        dir = save_path%(info.brand + '/' + folder_names[info.season] + '/' + folder_names[info.gender] + '/')
        os.makedirs(dir, exist_ok=True)
        imgs = soup.find_all('img', class_ = 'object_fit')
        for i, img in enumerate(imgs):
            src = requests.get('https://www.fashion-press.net' + img['src'])
            with open(dir + str(i) + '.jpeg', 'wb') as file:
                file.write(src.content)

def main():
    brand_ids = get_brand_id()
    for key in brand_ids:
        page_infos = get_page_info(brand_ids[key])
        for info in page_infos:
            save_images(info)

main()
