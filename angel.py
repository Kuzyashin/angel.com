import re
import time
import csv
from bs4 import BeautifulSoup
import sys 
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import subprocess

csvFile = open("./files/angel.csv", 'wt', encoding="UTF-8")
writer = csv.writer(csvFile)

#driver = webdriver.PhantomJS(executable_path='D:\\Python\\phantomjs\\bin\\phantomjs.exe') 
#driver.get("https://angel.co/france") 

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

DETACHED_PROCESS = 0x00000008
tor_process = subprocess.Popen(r"C:\Users\yuryy\Desktop\Tor Browser\Browser\firefox.exe")
driver = webdriver.Firefox(ff_prof)     
driver1 = webdriver.Firefox(ff_prof)     

driver.get("https://angel.co/france")
time.sleep(30)

driver.find_element_by_css_selector('.more.hidden').click()
time.sleep(30)
driver.find_element_by_css_selector('.more.hidden').click()
time.sleep(30)
driver.find_element_by_css_selector('.more.hidden').click()
time.sleep(30)

source = driver.page_source

soup = BeautifulSoup(source)

table = soup.find("div",{"class":"results_holder"})
elem_all = table.find_all("div",{"class":"base item"})
#print(len(elem_all))
for elem in elem_all:

    name_s = elem.find("div",{"class":"name"})
    name = re.sub("\n+", "", name_s.get_text())
    print("--------------")
    print(name)
    link_c = name_s.find("a",{"class":"startup-link"}).attrs["href"]
    driver1.get(link_c)
    time.sleep(5)
    sour_c = driver1.page_source
    soup_c = BeautifulSoup(sour_c)
    location = re.sub('\n+','',soup_c.find("span",{"class":"js-location_tags"}).get_text())
    site = re.sub('\n+','',soup_c.find("span",{"class":"link s-vgRight0_5"}).get_text())
    
    writer.writerow((name, location, site))
    csvFile.close
    time.sleep(3)
    
    csvFile = open("./files/angel.csv", 'at')
    writer = csv.writer(csvFile)

