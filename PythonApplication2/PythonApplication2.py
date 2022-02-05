from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
from pytesseract import pytesseract
from instabot import Bot
import requests
from io import BytesIO
import urllib.request
import numpy as np  

## Instagram Variables

Insta_UserName = "qjvmhpskpmsee3m"
Insta_Password = "7GCg4U3mVctLk53"

## 
bot = Bot()
options = Options()
options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
tesseract_path = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

## Fetch information from opensea.io

driver.get("https://opensea.io/assets?search[sortAscending]=false&search[sortBy]=LISTING_DATE")
time.sleep(4)
nft = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div/main/div/div/div[3]/div[2]/div[2]/div/div/div[1]")

try:
    price = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div[2]/div[2]/div/div/div[1]/div/article/a/div[2]/div/div[2]/div[1]/div/div[2]').screenshot("pricess")
    desc = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div[2]/div[2]/div/div/div[1]/div/article/a/div[2]/div/div[1]/div[2]').screenshot("descss")
except:
    pass

for i in nft:
    image = i.find_element_by_tag_name("img")
    img_src = str(image.get_attribute("src"))

priceimage = Image.open("pricess")
descimage = Image.open("descss")

pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"
NFT_Description = pytesseract.image_to_string(descimage)
NFT_Price = pytesseract.image_to_string(priceimage)

## Send as Instagram Post

Insta_TextToSend = "Name: " + NFT_Description + "Price: " + NFT_Price
img = urllib.request.URLopener()
img.retrieve(img_src, "nft.png")
Insta_ImageToSend = Image.open("nft.png")
#with client(Insta_UserName, Insta_Password) as cli:
#    cli.upload(file=Insta_ImageToSend, caption=Insta_TextToSend)
bot.login(username = Insta_UserName, password = Insta_Password)
bot.upload_photo("nft.png", caption=Insta_TextToSend)