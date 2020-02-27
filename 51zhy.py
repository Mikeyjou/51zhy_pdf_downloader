import os
import json
import requests
import numpy as np
import base64
import progressbar
import time
import warnings
import random

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)


key = json.load(open('key.json', 'r', encoding='utf-8'))
authorize = json.load(open('authorize.json', 'r', encoding='utf-8'))
file_id = str(authorize['Data']['FileId'])
book_urls = authorize['Data']['SplitFileUrls']

rsa_private = key['privateKey']
rsa_public = key['publicKey']
pdf_key = authorize['Data']['Key']

# RSA解密出AES的Key
data = base64.b64decode(pdf_key)
key = RSA.importKey(rsa_private)
cipher = PKCS1_v1_5.new(key)
decrypted = cipher.decrypt(data,1).decode()
#print(decrypted)
aes_key = ''.join([hex(ord(x))[2:] for x in decrypted])
print('AES Key:' + str(aes_key))
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Origin': 'http://yd.51zhy.cn/',
    'Referer': 'https://yd.51zhy.cn/ebook/reader/index.html',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors'
}

# 保存PDF
p = progressbar.ProgressBar()

if not os.path.isdir(file_id):
    os.makedirs(file_id)

for url in p(book_urls):
    page = book_urls.index(url)+1
    file = f"x-{page}"
    if not os.path.isfile(file_id + '/' + file + '.pdf'):
        r = requests.get(url=url, headers=headers, stream=True, verify=False)
        with open(file_id + '/' + file + '.aes','wb') as f:
            f.write(r.content)
        os.system(f'openssl enc -d -aes-128-ecb -K {aes_key} -in {file_id}/{file}.aes -out {file_id}/{file}.pdf -iv 0')
        #os.remove(file_id + '/' + file + '.aes')
        time.sleep(random.uniform(3,5))

print("正在合成PDF文件.........")
files = os.listdir(file_id)
pdf_files = []
for file in files:
    if '.pdf' in file:
        pdf_files.append(file)
pdf_files.sort(key=lambda x: int(x[x.rfind('-') + 1:][:-4]))

merger = PdfFileMerger(strict=False)
for file_name in pdf_files:
    # print(file_name)
    merger.append(PdfFileReader(open(file_id + '/' + file_name, 'rb')))
merger.write(file_id + '.pdf')
print('PDF合成完成!!')