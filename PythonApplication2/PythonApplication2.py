from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
from pytesseract import pytesseract

options = Options()
options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
tesseract_path = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

driver.get("https://opensea.io/assets?search[sortAscending]=false&search[sortBy]=LISTING_DATE")
time.sleep(4)
nft = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div/main/div/div/div[3]/div[2]/div[2]/div/div/div[1]")
price = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div[2]/div[2]/div/div/div[1]/div/article/a/div[2]/div/div[2]/div[1]/div/div[2]')
desc = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div[2]/div[2]/div/div/div[1]/div/article/a/div[2]/div/div[1]/div[2]')
pricess = price.screenshot(price)
descss = desc.screenshot(desc)

for i in nft:
    image = i.find_element_by_tag_name("img")
    img_src = image.get_attribute("src")
    print(img_src)

priceimg = Image.open(pricess)
descimg = Image.open(descss)
pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"
pricetext = pytesseract.image_to_string(priceimg)
desctext = pytesseract.image_to_string(descimg)