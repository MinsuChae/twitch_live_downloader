import requests
import re
import subprocess
import datetime
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import sys
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

if len(sys.argv) != 2:
    print("usage :",sys.argv[0],"id")
    exit(0)
else:
    channel_name = sys.argv[1]

service = Service('/chromedriver')
options = Options()
options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("disable-gpu")

while True:
    url = "https://www.twitch.tv/{channel_name}".format(channel_name=channel_name)
    driver = webdriver.Chrome(service=service, options=options, seleniumwire_options={'ignore_certificate_errors': True})
    driver.get(url)
    try:
        time.sleep(5)
        element_with_live_time_class = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, 'live-time')))
        live_match = True
    except:
        live_match = False
    driver.quit()

    if not live_match:
        time.sleep(60)
        continue
    
    print('{channel_name} online at {now}'.format(channel_name=channel_name, now=datetime.datetime.now()))

    try:
        driver = webdriver.Chrome(service=service, options=options, seleniumwire_options={'ignore_certificate_errors': True})
        if os.path.exists("./account.json"):
            driver.get('https://www.twitch.tv/directory')
            account = json.load(open("./account.json"))
            for key in account.keys():
                driver.add_cookie({"name":key, "value":account[key],'sameSite':'Lax'})
            time.sleep(1)
                
        driver.get('https://www.twitch.tv/{channel_name}'.format(channel_name=channel_name))
                
        time.sleep(5)
        url = ''
        for request in driver.requests:
            if request.response:
                if request.url.find('.m3u8')>0 and not request.url.endswith('.m3u8'):
                    url = request.url
                    break

        driver.quit()

        response2 = requests.get(url)
        arr = response2.text.strip().split('\n')
                

        for i in range(len(arr)):
            if arr[i].startswith('#EXT-X-MEDIA'):
                find_index = arr[i].find('1080p60')
                find_index2 = arr[i].find('720p60')
                if find_index==-1 and find_index2==-1:
                    continue
                elif find_index!=-1:
                    tmp_url = arr[i+1]
                    if not tmp_url.startswith('http'):
                        tmp_url = arr[i+2]
                    break
                else :
                    tmp_url = arr[i+1]
                    if not tmp_url.startswith('http'):
                        tmp_url = arr[i+2]
                    break
                    

        stream_url = tmp_url
        print(stream_url)


        # Twitch 스트림을 녹화하여 저장할 파일명
        now = datetime.datetime.now()
        if os.path.exists("./info.json"):
            info = json.load(open("./info.json"))
        else:
            info = {}
            info['output']='.'

        if not os.path.exists('{path}/{channel_name}'.format(path=info['output'],channel_name=channel_name)):
            os.mkdir('{path}/{channel_name}'.format(path=info['output'],channel_name=channel_name))

        start = time.time()
        output_file = '{path}/{channel_name}/{now}_output.ts'.format(path=info['output'],channel_name=channel_name,now=now.strftime("%Y-%m-%d %H_%M_%S"))
        ffmpeg_cmd = 'ffmpeg -i "{stream_url}" -loglevel quiet -c copy "{output_file}"'.format(stream_url=stream_url,output_file=output_file)
        process = subprocess.Popen(ffmpeg_cmd, shell=True)
        process.wait()
        end = time.time()
        if end - start <= 60:
            os.remove(output_file)
    except:
        pass
