
from selenium import webdriver 
import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
from time import sleep
def scrap_link(at) :
# Scrap all the links 
    links = []
    j = 1
    page = "?page="
    try :
        r = requests.get(at+page+str(j))
        soup = BeautifulSoup(r.content, 'html.parser')
        nb_pages = int(re.match('.*?([0-9]+)$',soup.find_all("a", "block br3 brc8 large tdnone lheight24")[-1]["href"]).group(1))
    
    except :
        nb_pages = 1
    
   
    for j in range(1,nb_pages+1) :
        try :
            r = requests.get(at+page+str(j))
            
            soup = BeautifulSoup(r.content, 'html.parser')
            for i in soup.find_all("h3", "lheight22 margintop5") :
                links.append(i.find("a")["href"])
            
            print("Scraped page " + str(j) )
            
            
        except :
            print("Break at :" + str(j))
            break
    
    # Remove duplicates
    links = list(dict.fromkeys(links))
    return links


def open_browser(at) :
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(at)
    driver.implicitly_wait(15)   
    
    element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    
    driver.find_element_by_id('onetrust-accept-btn-handler').click()
        
        
    # Check and click if the phone number is present
    
    return driver

def go_to(driver, at) :
    driver.get(at)
    


def show_number(driver) :
    try :
        element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1af0qjn-BaseStyles")))
        driver.find_element_by_class_name('css-1af0qjn-BaseStyles').click()
        t = True
    except :
        t = False
    
    return t
    
def scrap_data(links) :
    
    # Open a chrome browser
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # Create a DataFrame
    df = pd.DataFrame(columns = {"Link","Tags", "Loc", "Title", "Type", "Desc", "Author", "Tel", "About us", "Images"})
    
    first_run = True
    # Scrap all informations
    for i in links :
        try :
            if first_run :
                 driver = open_browser(i)  
                 first_run = False
              
            else :
                go_to(driver, i)
            
            driver.implicitly_wait(15) 
            
            t = show_number(driver)                            
            
            sleep(1)      
                                   
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            #Tags
            tags = soup.find_all("li", "css-7dfllt")[2].text
    
            # Loc
            tmp = soup.find("div", "css-1nrl4q4")
            loc = tmp.find("p", "css-7xdcwc-Text eu5v0x0").text +" "+ tmp.find("p", "css-xl6fe0-Text eu5v0x0").text 
    
            # Title
            title = soup.find("h1", "css-r9zjja-Text eu5v0x0").text
    
            # Type
            t = soup.find("p", "css-xl6fe0-Text eu5v0x0").text
    
            # Desc
            desc = soup.find("div", "css-g5mtbi-Text").text
    
            # Author
            auth = soup.find("h2", "css-u8mbra-Text eu5v0x0").text
    
            if t :
                # Tel
                tel = soup.find("div", "css-r8u9sk").text
                if tel == "xxx xxx xxxArata" :
                    driver.quit()
                    driver = open_browser(i) 
                    driver.implicitly_wait(15) 
                    
                    t = show_number(driver)                            
                    
                    sleep(1)      
                                           
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                        
                    tel = soup.find("div", "css-r8u9sk").text
                    
            img = ""
            try :
                for j in soup.find("div", "swiper-container swiper-container-initialized swiper-container-horizontal").find_all("img") :
                    try :
                        img += j["src"] + "\n"
                    except :
                        img += j["data-src"] + "\n"
            
                
            except :
                pass 
            
            try :
                ab = soup.find("div", "css-1oj9129-Text").text
            
            except :
                ab = ""
            
            
            
            df = df.append({"Link" : i ,"Tags" : tags, "Loc" : loc, "Title" : title, "Type" : t, "Desc" : desc, "Author" : auth, "Tel" : tel, "About us" : ab, "Images" : img}, ignore_index=True)
                        
            print("Scraped "+ title + " from " + loc+ " by " + auth)
            
        # Show if a problem occured
        except Exception as e:
            print(e)
            print("Problem :"+ str(i)+ "\n")
    
    # Create the promoted column
    df["Promoted"] = df["Link"].str.contains("promoted")
    
    # Erase promoted in Link column
    df["Link"] = df["Link"].str.replace(";promoted", "")
    
    df = df[["Link","Tags", "Loc", "Title", "Type", "Desc", "Author", "Tel", "About us", "Images"]]
    return df

def save_file(df,at) :
    # Save csv      
    df.to_csv(at.split(r"/")[-2]+".csv", index = False) 
    

def main():
    at = "https://www.olx.ro/servicii-afaceri-colaborari/contabilitate-traduceri/iasi_39939/"
    links = scrap_link(at)
    df = scrap_data(links)
    save_file(df, at)
    
if __name__ == "__main__":
    main()
    