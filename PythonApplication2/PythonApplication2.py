from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
from pytesseract import pytesseract
from instagrapi import Client
import requests
from io import BytesIO
import urllib.request
import requests
import cv2
import os


# Instagram Login

Insta_UserName = "bitganggggggsafasf"
Insta_Password = "asdasfasgasgasgdasd4124124"


# Chrome Options
 
options = Options()
options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


if os.name == 'nt':
    pytesseract.tesseract_c md="C:/Program Files/Tesseract-OCR/tesseract.exe"
else:
    pass


def fetch_data():


    global Insta_TextToSend

    try:

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

        driver.close()

        priceimage = Image.open("pricess")
        descimage = Image.open("descss")


        NFT_Description = pytesseract.image_to_string(descimage)
        NFT_Price = pytesseract.image_to_string(priceimage)


        ## Instagram Setup

        text = NFT_Description + ", Price: " + NFT_Price + " ETH ⧫" 
        img = urllib.request.URLopener()
        img.retrieve(img_src, "nft.jpg")
        new_width = 1080
        im = Image.open("nft.jpg")
        concat = int(new_width/float(im.size[0]))
        size = int((float(im.size[1])*float(concat)))
        resized_im = im.resize((new_width,size), Image.ANTIALIAS).convert('RGB')
        resized_im.save('nft2.jpg')
        Insta_TextToSend = text.replace("\n\x0c","").replace("\n","")

        


    except Exception as err:
        raise SystemExit(err) 



def send_to_insta():

    try:

        # Launch Bot

        cl = Client()
        cl.login(Insta_UserName,Insta_Password)

        print(Insta_TextToSend)

        cl.photo_upload("nft2.jpg", Insta_TextToSend)



    except Exception as e:
        raise SystemExit(e)



if __name__ == "__main__":
    fetch_data()
    send_to_insta()