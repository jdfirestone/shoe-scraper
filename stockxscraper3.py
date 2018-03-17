import time
import requests
from selenium import webdriver
from random import randint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv


# define variables that will be used in more than one function
SESSION = requests.Session()
HDR = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'gzip, deflate, br',
       'Accept-Language': 'en-US,en;q=0.9',
       'Connection': 'keep-alive' }

csvfile = open("stockx.csv", 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
c.writerow(['name', 'number sold', 'highest bid', 'lowest ask'])


# csv code will be in the last function - moved

#FUNCTION 1 - OPEN SELINIUM TO LOAD SCREEN MORE FOR urls
def get_page_contents():
    driver = webdriver.Chrome('/Users/joshfirestone/documents/python/scraping/chromedriver')

    driver.get('https://stockx.com/sneakers');

    # click the button exactly 2 times
    for n in range(13):
        driver.find_element_by_css_selector('.browse-load-more').click()
        # make a random wait time between 1 and 5 seconds to look less bot-like
        s = randint(1, 5)
        time.sleep(s)

    source = driver.page_source
    driver.quit()
    # get the contents of the page out of this function - with return
    return source



#FUNCTION 2 - SCRAPE URLS FROM SNEAKER PAGE AND CREATE LIST OF urls


# pass in the contents of the page that was scraped
def get_urls(source):
    bsObj = BeautifulSoup(source, "html5lib")

    #Sets up empty list
    shoe_list_half = []
    shoe_list_full = []

    #makes list with tags
    for a in bsObj.findAll("a", {"class":"browse-tile"}):
        shoe_list_half.append(a.get('href')) #Fills list

    #makes full urls
    for shoe in shoe_list_half:
        new_url = "https://stockx.com" + shoe
        shoe_list_full.append(new_url) #Fills list

    # print just for testing how many we got - can be deleted
    print("Number of URLs:")
    print(len(shoe_list_full))

    # get the contents of the page out of this function - with return
    return shoe_list_full



def get_shoe_info(shoe_list_full):
    for shoe in shoe_list_full:
        session = requests.Session()
        hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9',
               'Connection': 'keep-alive'}
        url = shoe
        req = session.get(url, headers=hdr)
        bsObj = BeautifulSoup(req.text, "html5lib")
        shoe_details = []
        name = bsObj.find("h1", {"class":"name"})
        sold = bsObj.find("div", {"class":"gauge-value"})
        ask = bsObj.find("div", {"class":"ask"}).find("div", {"class":"stat-small"})
        bid = bsObj.find("div", {"class":"bid"}).find("div", {"class":"stat-small"})

        shoe_details = [name, sold, ask, bid]
        row = []
        for detail in shoe_details:
            try:
                row.append( detail.get_text() )
            except AttributeError:
                row.append( "None" )

        c.writerow( row )

        # delay program for 1 second
        time.sleep(1)


# call the functions - run them
page_contents = get_page_contents()
shoe_urls_list = get_urls(page_contents)
shoe_info = get_shoe_info(shoe_urls_list)
csvfile.close()
