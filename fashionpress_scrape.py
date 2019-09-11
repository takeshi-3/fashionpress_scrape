import requests
import re
import os
from bs4 import BeautifulSoup

# 保存先フォルダ
save_path = "./picture/fashionpress/%s"

# コレクションページurl
url = "https://www.fashion-press.net/collections/%s"

# 対象ブランド
target_brands = [
    'Alexander McQueen', 'BALENCIAGA', 'Berluti', 'BURBERRY', 'CHANEL', 'CHRISTIAN DADA',
    'COMME des GARÇONS', 'DIOR', 'dunhill', 'FENDI', 'Givenchy', 'GUCCI', 'HERMÈS', 'ISSEY MIYAKE',
    'LACOSTE', 'LOUIS VUITTON', 'Paul Smith', 'PRADA', 'Saint Laurent', 'Y\'s', 'Yohji Yamamoto'
]

# コレクションカテゴリを取得
def get_seasons():
    soup = BeautifulSoup(requests.get(url%('')).text, 'lxml')
    menus = soup.find_all('a', class_ = "dropdown-item")
    pat = re.compile('^\d.*')
    seasons = []
    for menu in menus:
        last_path = menu['href'].split('/')[3]
        result = pat.match(last_path)
        if result:
            seasons.append(result.group())
    return seasons

def get_brands(path):
    req = requests.get(url%('search/' + path))
    soup = BeautifulSoup(req.text, 'lxml')
    brands = soup.find_all('a', class_ = "collection_media_title")
    return brands

def get_images(page_id):
    req = requests.get(url%(page_id))
    soup = BeautifulSoup(req.text, 'lxml')
    imgs = soup.find_all('img', class_ = 'object_fit')
    return imgs

# メインルーチン
seasons = get_seasons()
for season in seasons:
    for i in range(30):
        for gender in ['mens', 'womens']:
            brands = get_brands(season + '/' + gender + '?page=' + str(i))
            for brand in brands:
                try:
                    name = brand.find('p').text
                except Exception as e:
                    print("error: {}".format(e))

                for t_brand in target_brands:
                    if t_brand in name:
                        brand_path = save_path%(t_brand + '/' + season + '/' + gender + '/')
                        os.makedirs(brand_path, exist_ok=True)
                        imgs = get_images(brand['href'].replace('collections/', ''))
                        for i, img in enumerate(imgs):
                            img_req = requests.get('https://www.fashion-press.net' + img['src'])
                            with open(brand_path + str(i) + str('.jpeg'), 'wb') as file:
                                file.write(img_req.content)
