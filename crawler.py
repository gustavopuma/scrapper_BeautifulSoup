from bs4 import BeautifulSoup
from epicerie import Produit, Persistence
import datetime
import requests
from selenium import webdriver
import selenium as se
from time import time, sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Crawler:
   # options = se.webdriver.ChromeOptions()
   # options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install())

    def __init__(self, url):
        self.url = url

    def get_page(self, url):
        req = requests.get(url)

        return BeautifulSoup(req.text, 'html.parser')

    #  return BeautifulSoup(driver.page_source, 'html.parser')

    def get_page_webdrive(self, url):
        self.driver.set_page_load_timeout(30)
        self.driver.get(url)
        myElem = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-tile')))
        self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML").encode('utf-8')

        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def craw_links(self):
        bs = self.get_page(self.url)

        nav = bs.find("li", class_='nav-item has-sub-nav listener-clickoutside')

        links = []
        links_bs = nav.find_all('a', class_='sub-nav-link')
        for link in links_bs:
            if link.find('span', class_='more-indicator') is None:
                links.append([link.text ,link.attrs['href']])
        print("Total de sous-catégories=", len(links))
        return links

    def craw(self):
        produits = []
        links = self.craw_links()
        #links = ["/Alimentation/Boulangerie/Pains-frais/Pains-surgel%C3%A9s/c/MAX001003017009?navid=frozen"]
        init = time()
        index = 0
        for link in links:

            bs = self.get_page_webdrive(self.url + link[1])
            # print("link=", self.url + link)
            # pour eviter être bloqué par le administrateur du site
            #sleep(1)
            products_detail = bs.find_all('div', class_='product-tile')
            # items = bs.find_all('span', class_='product-name__item product-name__item--name')
            print("=" * 100)
            print("lien=", link[1])
            print("Quantité de produit à scraper:", len(products_detail))
            for p in products_detail:
                description = p.find('span', class_='product-name__item product-name__item--name').contents[0]
                b_marque = p.find('span', class_='product-name__item product-name__item--brand')
                if b_marque is not None:
                    marque = b_marque.contents[0]
                else:
                    marque = None
                classes_prix = "price__value selling-price-list__item__price" \
                               " selling-price-list__item__price--now-price__value"
                prix = p.find('span',
                              class_=classes_prix).contents[0]
                prix = str.replace(prix, ',', '.')
                code = p.find('a', class_='product-tile__details__info__name__link').attrs['href'].split('/')[-1:][0]
                prod = Produit(description,link[0].strip(), float(str.replace(prix, ' $', '')), code, marque,
                               datetime.datetime.now().__format__("%Y-%m-%d %H:%M"))
                produits.append(prod)
            end = time()
            index = index + 1
            print("Temps écoulé:" + str(round((end - init), 1)) + " Seconds")
            print("état d\'avancement:{}/{}".format(index, len(links)))

        return produits

        bar.fini


produits = Crawler("https://www.maxi.ca").craw()
print("Total de Produits scrapés:", len(produits))
Persistence().save(produits)
# for produit in produits:
#     print("Description=", produit.description)
#     print("prix=", produit.prix)
#     print("code=", produit.code)
