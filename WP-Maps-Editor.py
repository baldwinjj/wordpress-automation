from urllib import parse
from bs4 import BeautifulSoup
import requests
import json
import csv
import os
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
LOGIN_URL = os.getenv('LOGIN_URL')
MAPS_URL = os.getenv('MAPS_URL')

# Login Data
payload = {
    'log': USERNAME,
    'pwd': PASSWORD,
    'wp-submit': 'Log In',
    'redirect_to': MAPS_URL,
    'testcookie': 1
}

# Utility functions for getting page links
def getPageLinks(soup, baseUrl):
    tags = soup.find_all('a', href=lambda x: ('doaction', 'edit') in parse.parse_qsl(x))
    return [baseUrl + a['href'] for a in tags]

def getNextPage(soup):
    tag = soup.find('a', class_=lambda x: x and 'next-page' in x)
    return '' if 'disabled' in tag['class'] else tag['href']

def getAllLinks(url, session):
    baseUrl = url[:url.find('?')]
    links = []
    while url:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = links + getPageLinks(soup, baseUrl)
        url = getNextPage(soup)
    return links

# Get example template
def getFormData():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data/formData.csv')
    with open(filename, 'r') as formDataFile:
        reader = csv.reader(formDataFile)
        formData = dict(reader)
    return formData

def updateForm(url, formData, session):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Keep nonce
    wpnonce = soup.select('#_wpnonce')[0]['value']
    formData['_wpnonce'] = wpnonce
    # Keep http referrer
    wp_http_referer = soup.select('[name="_wp_http_referer"]')[0]['value']
    formData['_wp_http_referer'] = wp_http_referer
    # Keep exportCode
    exportCode = soup.select('textarea[name="wpgmp_export_code"]')[0].string
    formData['wpgmp_export_code'] = exportCode
    # Keep existing ID
    entityID = soup.select('[name="entityID"]')[0]['value']
    formData['entityID'] = entityID
    # Keep existing title
    mapTitle = soup.select('[name=map_title]')[0]['value']
    formData['map_title'] = mapTitle
    # UpdateForm
    formData = {k: ('', v) for k, v in formData.items()}
    response = session.post(url, files=formData)
    if (response.status_code == 200):
        print(formData['map_title'][1], 'successfully updated!')
    else:
        print(formData['map_title'][1], 'failed to update')

# Open Session
with requests.Session() as session:
    # Log In
    session.post(LOGIN_URL, data=payload)
    # Get all page links
    links = getAllLinks(MAPS_URL, session)
    # Get form template
    formData = getFormData()
    # Update each page
    for link in links:
        updateForm(link, formData, session)
