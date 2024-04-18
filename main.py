from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import os 
from PIL import Image
from io import BytesIO
def clean_links(links: list): 
    new = []
    for i in range(len(links)): 
        # check the link validation
        if "m'{sid:,cturl:" in  links[i] or "m{&quot;sid&quot;:&quot;&quot;" in  links[i] or "https://static.ah.nl/" in links[i]:
            # if true skip this step
            pass
        else: 
            # else append image link to new array
            new.append(links[i])
    # remove duplicate 
    return np.unique(new)

def resize(image, width, height):
    # resize the image 
    resized_img = image.resize((width, height))
    # return resized image
    return resized_img

def download_image(image_name :  str, width = 300, height = 300):
    # https://www.bing.com/images/search?q=dog&FORM=HDRSC3
    array_links = []
    for i in range(100):
        try: 
            url = requests.get(f'https://www.bing.com/images/search?q={image_name}&form=HDRSC3&first={i}')
            soup = BeautifulSoup(url.content, 'lxml')
            #  find the image tag 
            get_image = soup.find_all(name = "div", attrs={"class" : "imgpt"})
            # if succed to get the image tag 
            if get_image: 
                # print(get_image)
                for attributes in str(get_image).split("src"):
                    for i in attributes.split(" "): 
                        if "https://tse2.mm.bin" in i: 
                            url = i
                            url = url.replace(" ", "")
                            array_links.append(url.replace("=", "").replace('"', '').replace(" ", ""))
        except Exception as e: 
            print(f'error : {e} or image tag not detected')
    # get the all link 
    array_links = clean_links(array_links)
    # start to download
    for i in range(len(array_links)):
        response = requests.get(array_links[i])
        # check the image path, if the path is not exist, create the path 
        if os.path.exists(f'./{image_name}'):
            print(f'donwloading : {array_links[i]}')
            img = Image.open(BytesIO(response.content))
            # open image from url
            img = resize(img, width= width, height= height )
            # full path for saving the image
            full_path = f'./{image_name}/{image_name}{i}.png'
            # save the image 
            img.save(full_path)
        else:
            #  if the path is exist
            os.mkdir(f"./{image_name}")
            print(f'donwloading : {array_links[i]}')
            # open image from url 
            img = Image.open(BytesIO(response.content))
            img = resize(img, width= width, height= height)
            # full path for saving the image
            full_path = f'./{image_name}/{image_name}{i}.png'
            # save the image 
            img.save(full_path)
    # print this message when succesfully scrap 
    print("succesfully get " + str(len(array_links)) + " images")   
     
