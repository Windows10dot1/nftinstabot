from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from PIL import Image
from pytesseract import pytesseract
from instagrapi import Client
import requests
import cv2
import os
import sys


# Instagram Login

Insta_UserName = "asdafkjgaskdjkagskdgahsjd"
Insta_Password = "afkjhsaifhwuiqhfiwquhfqw8718297"

try:
    cl = Client()
    cl.login(Insta_UserName,Insta_Password)
except:
    print("Login error, passing")
    pass


# Chrome Options
 
options = Options()
options.headless = False
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


if os.name == 'nt':
    pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"
else:
    pass


def fetch_data():

    global Insta_TextToSend

    try:

        # Generate hashtags

        try:
            driver.get("https://h.bdir.in/hashtags/search")
            driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div/form/div[1]/input").send_keys('nft')
            driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div/form/div[2]/button").click()
            hashtags = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/b").text
        except:
            print("Hashtag generation failed.")
            pass


        # Fetch information from opensea.io

        driver.get("https://opensea.io/assets?search[sortAscending]=false&search[sortBy]=LISTING_DATE")
        sleep(4)
        nft = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div/main/div/div/div[3]/div[2]/div[2]/div/div/div[1]")

        try:
            price = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div[2]/div[2]/div/div/div[1]/div/article/a/div[2]/div/div[2]/div[1]/div/div[2]').screenshot("pricess.png")
            desc = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div[2]/div[2]/div/div/div[1]/div/article/a/div[2]/div/div[1]/div[2]').screenshot("descss.png")
        except:
            pass

        for i in nft:
            image = i.find_element_by_tag_name("img")
            img_src = str(image.get_attribute("src"))

        driver.close()

        priceimage = Image.open("pricess.png")
        descimage = Image.open("descss.png")


        NFT_Description = pytesseract.image_to_string(descimage)
        NFT_Price = pytesseract.image_to_string(priceimage)


        ## Get the image 

        with open('nft.jpg', 'wb') as f:
            f.write(requests.get(img_src).content)

        ## Optimize the image

        new_width = 1080
        im = Image.open("nft.jpg")
        concat = int(new_width/float(im.size[0]))
        size = int((float(im.size[1])*float(concat)))
        resized_im = im.resize((new_width,size), Image.ANTIALIAS).convert('RGB')
        resized_im.save('nft2.jpg')

        text = NFT_Description + " | Price: " + NFT_Price + " ETH ⧫" 
        Insta_TextToSend = text.replace("\n\x0c","").replace("\n","")
        Insta_TextToSend = Insta_TextToSend + "\n\n\n\n\n\n\n  +   -------------------   +\n\n\n\n\n" + hashtags
        

    except Exception as err:
        print("Error caught")
        pass




def send_to_insta():

    try:

        # Launch Bot

        cl.photo_upload("nft2.jpg", Insta_TextToSend)



    except Exception as e:
        pass



if __name__ == "__main__":
    fetch_data()
    send_to_insta()
    sleep(900)
    os.execv(__file__, sys.argv)