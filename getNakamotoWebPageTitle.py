import urllib.request
import urllib.error
import dataclasses
import sqlite3

from bs4 import BeautifulSoup

# remoteOpen
url = "http://www.moukotanmen-nakamoto.com/n_menu"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html.read(), "html.parser")

# localOpen
# soup = BeautifulSoup(open("/Users/hiraok/projects/python_env/nakamoto.html"), "lxml")

thumbs = soup.find_all('img', class_="attachment-large wp-post-image")
post_contents = soup.find_all('div', class_="post_content")
excerpts = soup.find_all('div', class_="post_excerpt")

products = []


# data class
@dataclasses.dataclass(frozen=True)
class Product:
    title: str
    thumb: str
    excerpt: str


for i in range(len(thumbs)):
    products.append(Product(title=post_contents[i].find('a').string, thumb=thumbs[i]['src'], excerpt=excerpts[i].text))

DB_NAME = 'nakamoto_menu.db'
TABLE_NAME = 'menu_data'

con = sqlite3.connect(DB_NAME)
cursor = con.cursor()
cursor.executescript("""drop table if exists menu_data;
CREATE TABLE %s(title, thumb, excerpt)""" % TABLE_NAME)

for product in products:
    cursor.execute("INSERT INTO %s VALUES(?,?,?);" % TABLE_NAME, (product.title, product.thumb, product.excerpt))

con.commit()
