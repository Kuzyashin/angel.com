import re
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import subprocess

def open_csv():
# Open CSV for scraping.
# Must create ./files/ directory before start
    csvFile = open("./files/angel.csv", 'wt', encoding="UTF-8")
    writer = csv.writer(csvFile)
    return writer, csvFile

def open_connect():
# Create drivers for Tor
# Tor must be in C:\Users\yuryy\Desktop\Tor Browser\Browser\firefox.exe directory
    ff_prof=webdriver.FirefoxProfile()
    
    ff_prof.set_preference( "places.history.enabled", False )
    ff_prof.set_preference( "privacy.clearOnShutdown.offlineApps", True )
    ff_prof.set_preference( "privacy.clearOnShutdown.passwords", True )
    ff_prof.set_preference( "privacy.clearOnShutdown.siteSettings", True )
    ff_prof.set_preference( "privacy.sanitize.sanitizeOnShutdown", True )
    ff_prof.set_preference( "signon.rememberSignons", False )
    ff_prof.set_preference( "network.cookie.lifetimePolicy", 2 )
    ff_prof.set_preference( "network.dns.disablePrefetch", True )
    ff_prof.set_preference( "network.http.sendRefererHeader", 0 )
    
    ff_prof.set_preference( "network.proxy.type", 1 )
    ff_prof.set_preference( "network.proxy.socks_version", 5 )
    ff_prof.set_preference( "network.proxy.socks", '127.0.0.1' )
    ff_prof.set_preference( "network.proxy.socks_port", 9150 )
    ff_prof.set_preference( "network.proxy.socks_remote_dns", True )
    
    #DETACHED_PROCESS = 0x00000008
    tor_process = subprocess.Popen(r"C:\Users\yuryy\Desktop\Tor Browser\Browser\firefox.exe")
    driver = webdriver.Firefox(ff_prof)     
    driver1 = webdriver.Firefox(ff_prof)     
    return driver, driver1

def csv_close(csvFile):
    csvFile.close
    
def process_parsing(driver, driver1, writer):
# Scraping, parsing and writing in CSV.
    driver.get("https://angel.co/france")
    time.sleep(5)
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'results_holder'))) # Check for load start page
    except:
        print('Page is not ready')
        driver.quit()    
        driver1.quit()
        return
    
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    
    table = soup.find("div",{"class":"results_holder"})
    elem_all = table.find_all("div",{"class":"base item"})
    while True: 
    #Iteractions on main page by pages
        for elem in elem_all: 
        #Iteractions on main page within one page
            name_s = elem.find("div",{"class":"name"})
            name = re.sub("\n+", "", name_s.get_text()) # First value of goal
            print("--------------")
            print(name)
            link_c = name_s.find("a",{"class":"startup-link"}).attrs["href"]
            driver1.get(link_c)                         # Go to page detail
            time.sleep(5)
            try:
                WebDriverWait(driver1, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'section.tags_and_links')))
            except:
                print('Detail page is not ready')
                driver.quit()    
                driver1.quit()
                return
            sour_c = driver1.page_source
            soup_c = BeautifulSoup(sour_c, 'lxml')
            location = re.sub('\n+','',soup_c.find("span",{"class":"js-location_tags"}).get_text()) # Second value of goal
            site = re.sub('\n+','',soup_c.find("span",{"class":"link s-vgRight0_5"}).get_text()) # Third value of goal
            
            writer.writerow((name, location, site)) # Write CSV

        if driver.find_element_by_css_selector('.more.hidden'):
            driver.find_element_by_css_selector('.more.hidden').click() # Click on More button
            time.sleep(5)
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'more.hidden')))
            except:
                print('Next page is not ready')
                driver.quit()    
                driver1.quit()
                return
        else:
            driver.quit()    
            driver1.quit()
            return

if __name__ == '__main__':
    csv_writer, csvFile = open_csv()
    driver, driver1 = open_connect()
    process_parsing(driver, driver1, csv_writer)
    csv_close(csvFile)
    