from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import warnings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
import time
import pyperclip
import requests
import datetime
import pymssql
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
import chromedriver_autoinstaller
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import chromedriver_autoinstaller
import subprocess
import shutil 
import xlrd
import openpyxl 
import pygsheets
import csv
import re
import webbrowser
import sys
import urllib.request
import json
from pandas import json_normalize  # Updated import
import hashlib
import hmac
import base64
import numpy as np
import autoit  # autoit는 반드시 autoit 프로그램이 깔려있어야됨
import pyautogui
from PIL import ImageGrab
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import numpy as np
import glob
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io

from time import gmtime, strftime

import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi

import pdfkit
from PyPDF2 import PdfFileReader, PdfFileWriter
from tika import parser
import pdfkit

import pytumblr  # 텀블러
from requests_oauthlib import OAuth1Session

import tweepy  # 트위터용
import pytumblr  # 텀블러
from requests_oauthlib import OAuth1Session
import config

keywords = ['칼륨 영양제']  # 키워드 입력

for keyword in keywords:

    ################################# 사이트 호출 #################################

    target_url = 'https://www.coupang.com/np/search?component=&q=' + str(keyword) + '&channel=user'  # URL

    headers = {
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'Accept-Encoding': 'gzip'
    }

    res = requests.get(url=target_url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    # 상품명
    product_name = soup.select('div > div.name')

    # 상품가격
    product_price = soup.select('div.price-wrap > div.price > em > strong')

    # 상품리뷰 수
    product_review = soup.select('div.other-info > div > span.rating-total-count')

    # 상품 구매 링크
    product_link = soup.select('a.search-product-link')

    # 상품 이미지
    product_image = soup.select('dt > img')
    # product_images2 = product_images.find('img').get('src')
    # print(product_images2)
    # print(product_images)

    ################################# Top 10만 리스트에 담기 #################################

    product_names = []  # 상품명
    product_prices = []  # 가격
    product_reviews = []  # 리뷰
    product_links = []  # 구매링크
    product_images = []  # 상품이미지

    for name in product_name[:10]:  # 상품명 리스트 집어넣기
        p_name = name.text
        p_name = p_name.replace('\n', '')  # 상품명 필터링1
        p_name = p_name.replace('  ', '')  # 상품명 필터링2
        p_name = p_name.replace(',', '')  # 상품명 필터링3
        # p_price = price.text
        # p_review_cnt = re.sub("[()]","", review.text)
        # p_link = "https://coupang.com" + link['href']
        # p_image = image.get('data-img-src')
        product_names.append(p_name)

    for price in product_price[:10]:  # 상품가격 리스트 집어넣기
        p_price = price.text
        p_price = p_price.replace(",", "")
        # p_price = price.text
        # p_review_cnt = re.sub("[()]","", review.text)
        # p_link = "https://coupang.com" + link['href']
        # p_image = image.get('data-img-src')
        product_prices.append(p_price)

    for review in product_review[:10]:  # 상품리뷰 갯수 리스트 집어넣기
        try:
            p_review_cnt = re.sub("[()]", "", review.text)
        except:
            p_review_cnt = '0'
        product_reviews.append(p_review_cnt)

    for link in product_link[:10]:  # 상품구매링크 리스트 집어넣기
        p_link = "https://www.coupang.com" + link['href']
        product_links.append(p_link)

    for image in product_image[:10]:  # 상품이미지 리스트 집어넣기
        p_image = image.get('data-img-src')
        if p_image is None:
            p_image = image.get('src')
            # print(p_image)
            p_image = p_image.replace("//", "")
            product_images.append(p_image)
        else:
            p_image = p_image.replace("//", "")
            product_images.append(p_image)

    coupang_short_urls = []  # 쿠팡 숏츠 링크 리스트 담을거

    REQUEST_METHOD = "POST"
    DOMAIN = "https://api-gateway.coupang.com"
    URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"

    # Replace with your own ACCESS_KEY and SECRET_KEY
    ACCESS_KEY = ""  # 키를 입력하세요!
    SECRET_KEY = ""  # 키를 입력하세요!

    for i in product_links[:10]:
        coupang_link = i  # 쿠팡링크
        REQUEST = {"coupangUrls": [coupang_link]}  # 해당 쿠팡링크 받기

        def generateHmac(method, url, api_secret_key, api_access_key):
            path, *query = url.split('?')
            os.environ['TZ'] = 'GMT+0'
            dt_datetime = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'  # GMT+0
            msg = dt_datetime + method + path + (query[0] if query else '')
            signature = hmac.new(bytes(api_secret_key, 'utf-8'), msg.encode('utf-8'), hashlib.sha256).hexdigest()

            return 'CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}'.format(api_access_key, dt_datetime, signature)

        authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
        url = "{}{}".format(DOMAIN, URL)
        resposne = requests.request(method=REQUEST_METHOD, url=url,
                                    headers={
                                        "Authorization": authorization,
                                        "Content-Type": "application/json"
                                    },
                                    data=json.dumps(REQUEST)
                                    )

        # print(resposne.json())  #확인

        time.sleep(2)  # 10초마다 한번씩 (총 5분걸림)

        text = resposne.json()
        try:
            text_2 = text['data']
        except:
            text_2 = ['https://www.coupang.com/np/coupangglobal']  # 없을시 가짜 리스트 생성
        for i in text_2:
            try:
                coupang_short_url = i['shortenUrl']
            except:
                coupang_short_url = 'https://link.coupang.com/a/mEezS'  # 가짜 링크 집어넣기
            print(coupang_short_url)  # 확인
            coupang_short_urls.append(coupang_short_url)

    print("최종 숏츠링크가 생성 완료되었습니다.")  # 최종확인

# 엑셀 파일 저장 경로
output_dir = 'C:/Users/samsung/Desktop/s/capstone/capstone-design-2024/crawling'
output_file = os.path.join(output_dir, 'search_results.csv')

# 디렉토리가 존재하지 않으면 생성
os.makedirs(output_dir, exist_ok=True)

# 파일 저장
with open(output_file, 'w', encoding='utf-8-sig') as f:
    f.write("검색어,상품명,상품가격,상품 리뷰수,상품 이미지,판매 링크" + '\n')  # 컬럼명 입력

    for i in range(0, 10):
        name = product_names[i]
        name = name.replace('\n', '')
        name = name.replace("  ", "")
        name = name.replace(",", "")
        price = product_prices[i]
        price = price.replace(",", "")
        review = product_reviews[i]
        image = product_images[i]
        short = coupang_short_urls[i]
        f.write(str(keyword) + ',' + str(name) + ',' + str(price) + ',' + str(review) + ',' + str(image) + ',' + str(short) + '\n')
    f.close()

# github: DBhyeong / digital-marketing / [Python] 쿠팡 상품 키워드 Top 10 리스트 크롤링, 숏츠 링크 생성 엑셀 파일 저장하기