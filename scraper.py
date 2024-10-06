from bs4 import BeautifulSoup
from requests import get
from datetime import datetime
import csv
import math
import sys
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

def buildURL(domain, entryTitle, entryID):
    s = re.sub('[^0-9a-zA-Z]+', '-', entryTitle+"-"+entryID)
    if s[-1] == '-':
        s = s[:-1]
    url = f"https://{domain}/product/{s}"
    return url

def scrape_product_page(url):
    response = get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    
    title = soup.select_one('#product-4594 > div:nth-child(1) > div > div > div:nth-child(2) > div > div > h1')
    if not title:
        title = soup.select_one('h1.product_title')
    
    price = soup.select_one('p.price > span.woocommerce-Price-amount')
    
    image = soup.select_one('div.woocommerce-product-gallery__image > a > img')
    image_url = image['data-src'] if image and 'data-src' in image.attrs else None
    if not image_url:
        image_url = image['src'] if image else None
    
    return title.text.strip() if title else None, price.text.strip() if price else None, image_url

def create_xml_feed(catalog, domain):
    root = ET.Element("rss", version="2.0")
    root.set("xmlns:wc", "https://schemas.woocommerce.com/wp/v2/product")
    channel = ET.SubElement(root, "channel")
    
    for product in catalog:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = product[0]
        ET.SubElement(item, "wc:product_id").text = product[1]
        ET.SubElement(item, "wc:price").text = product[2]
        ET.SubElement(item, "link").text = product[3]
        if product[4]:
            ET.SubElement(item, "wc:image_url").text = product[4]
    
    xml_str = ET.tostring(root, encoding="unicode")
    
  
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    
 
    pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
    
    with open(f"{domain}_{datetime.now().date()}.xml", "w", encoding="UTF-8") as f:
        f.write(pretty_xml)

if __name__ == '__main__':
    catalog = []
    page_number = 1
    products_scraped = 0
    max_products = 200
    if len(sys.argv) == 2:
        domain = sys.argv[1]
    else:
        print("Použití: 'python scraper.py [example.com]'")
        exit()
    

    while products_scraped < max_products:
        url = f"https://{domain}/page/{page_number}/?s=&post_type=product"
        response = get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        
        products = soup.find_all('h2', class_='woocommerce-loop-product__title')
        if not products:
            products = soup.find_all('p', class_='product-title')
        
        print(f"Scraping products from page {page_number}")
        for item in products:
            if products_scraped >= max_products:
                break
            
            item_title = item.text.strip()
            product_url = buildURL(domain, item_title, '')
            

            full_title, price, image_url = scrape_product_page(product_url)
            
            catalog.append((full_title or item_title, '', price or "N/A", product_url, image_url))
            
            products_scraped += 1
            print(f"  Progress: {products_scraped}/{max_products} products scraped")
        
        page_number += 1
        if not products:
            break


    print("Vytvářím XML Feed...")
    create_xml_feed(catalog, domain)
    print(f"XML feed vytvořen: {domain}_{datetime.now().date()}.xml")