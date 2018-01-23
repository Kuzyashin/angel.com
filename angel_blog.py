import time
import csv
import requests
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import sys 
import re
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import subprocess

csvFile = open("./files/angel.csv", 'wt', encoding="UTF-8")
writer = csv.writer(csvFile)

driver = webdriver.PhantomJS(executable_path='D:\\Python\\phantomjs\\bin\\phantomjs.exe') 
#driver.get("https://angel.co/france") 


#ff_prof=webdriver.FirefoxProfile()

#ff_prof.set_preference( "places.history.enabled", False )
#ff_prof.set_preference( "privacy.clearOnShutdown.offlineApps", True )
#ff_prof.set_preference( "privacy.clearOnShutdown.passwords", True )
#ff_prof.set_preference( "privacy.clearOnShutdown.siteSettings", True )
#ff_prof.set_preference( "privacy.sanitize.sanitizeOnShutdown", True )
#ff_prof.set_preference( "signon.rememberSignons", False )
#ff_prof.set_preference( "network.cookie.lifetimePolicy", 2 )
#ff_prof.set_preference( "network.dns.disablePrefetch", True )
#ff_prof.set_preference( "network.http.sendRefererHeader", 0 )

#ff_prof.set_preference( "network.proxy.type", 1 )
#ff_prof.set_preference( "network.proxy.socks_version", 5 )
#ff_prof.set_preference( "network.proxy.socks", '127.0.0.1' )
#ff_prof.set_preference( "network.proxy.socks_port", 9150 )
#ff_prof.set_preference( "network.proxy.socks_remote_dns", True )

#DETACHED_PROCESS = 0x00000008
#tor_process = subprocess.Popen(r"C:\Users\yuraz_000\Desktop\Tor Browser\Browser\firefox.exe")
#driver = webdriver.Firefox(ff_prof)          


driver.get("https://angel.co/blogging-platforms")
time.sleep(30)

driver.find_element_by_css_selector('.more.hidden').click()
time.sleep(30)
driver.find_element_by_css_selector('.more.hidden').click()
time.sleep(30)
driver.find_element_by_css_selector('.more.hidden').click()
time.sleep(30)

source = driver.page_source

soup = BeautifulSoup(source)
#print(soup)

table = soup.find("div",{"class":"results_holder"})
#print("________________")
#print(table)

elem_all = table.find_all("div",{"class":"base item"})
print(len(elem_all))
for elem in elem_all:
    print("+++++++++++++++")
    print(elem)

    name = elem.find("div",{"class":"name"}).get_text()
    print("--------------")
    print(name)

i = 1