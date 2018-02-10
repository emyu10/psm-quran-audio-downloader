'''
This program downloads audio files from http://psm.mv/quran
'''

import requests
import json


def download_file(chap):
    audio_url = chap['urls']['audio']
    local_file_name = str(chap['order']) + '_' + audio_url.split('/')[-1]
    r = requests.get(audio_url, stream=True)
    fx = open('audio/' + local_file_name, 'wb')
    i = 1
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            fx.write(chunk)
        i += 1
    fx.close()


url = "http://psmlive.psm.mv/quran/api/"

response = requests.get(url).text
chapters = json.loads(response)
the_chapters = chapters['chapters']
print("\n**************************************\n")

while True:
    try:
        chap_id = int(input("Please enter where you want to start from (1 ~ 114):\n"))
        if chap_id < 1 or chap_id > 114:
            print("Please choose a valid chapter.")
            continue
        break
    except ValueError:
        print("Please enter a valid number.")

for chaps in the_chapters:
    if int(chaps['order']) >= chap_id:
        print(chaps['order'] + '\t\t' + chaps['title-english'])
        print('\t\t... downloading ...')
        download_file(chaps)
    else:
        print("\t\t ... skipping chapter " + str(chaps['order']) + " ...")
        continue
print("\n**************************************\n")
