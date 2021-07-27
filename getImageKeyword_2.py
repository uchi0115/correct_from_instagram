import requests
import base64
import json
import pprint
import io
import datetime
from PIL import Image
from urllib.parse import urlparse
import mysql.connector

dst_path = '/Users/chibaren/NL/Instagram_analyze/image_sample/kari.png'

def request_to_instagram(hashtag):

    try:

        INSTAGRAM_GRAPH_API_URL = f"https://graph.facebook.com/ig_hashtag_search?user_id=17841448441684967&access_token=EAALZBv7JCX7EBANK8WFabF3IxwmRl8eLpMbPvmBj2dDUpacGVWgcR6cyJg5mEdFZBHUupGoICw7WZCBGq8qDCoigdZBYSWVaHdIFv8amooyFHDvDHURrzQKhz5RXuFXndhdiBw8S8pFFr7ZBo6eZAcLl2fRZAc36hpT1Dh9a8tr8bBcNpIrpA6q&q={hashtag}"

        # Vision API にリクエストを行う
        response1 = requests.get(INSTAGRAM_GRAPH_API_URL)

        # データを表示
        pprint.pprint(response1.json())
        hashtag_id = response1.json()['data'][0]['id']

        INSTAGRAM_URL = f'https://graph.facebook.com/{hashtag_id}/top_media?user_id=17841448441684967&access_token=EAALZBv7JCX7EBANK8WFabF3IxwmRl8eLpMbPvmBj2dDUpacGVWgcR6cyJg5mEdFZBHUupGoICw7WZCBGq8qDCoigdZBYSWVaHdIFv8amooyFHDvDHURrzQKhz5RXuFXndhdiBw8S8pFFr7ZBo6eZAcLl2fRZAc36hpT1Dh9a8tr8bBcNpIrpA6q&fields=id,media_type,media_url,caption,permalink&limit=10'
        response2 = requests.get(INSTAGRAM_URL)

        pprint.pprint(response2.json())

        json_object = response2.json()

        return json_object

    except KeyError:
        print("KeyError Exception")




def download_file(url):

    response = requests.get(url)

    f = io.BytesIO(response.content)

    return f


def insert_to_db(img_name, hashtag, binary_data):
    cnx = None

    try:
        cnx = mysql.connector.connect(
            user='root',  # ユーザー名
            password='niko0115',  # パスワード
            host='localhost',  # ホスト名(IPアドレス）
            database='sampledb'  # データベース名
        )

        print(cnx.is_connected())
    
        cursor=cnx.cursor()

        cnx.commit()

        sql = ('''INSERT INTO img_to_binary (name, hashtag, img) VALUES (%s, %s, %s)''')

    
        cursor.execute(sql, (img_name, hashtag, binary_data))
    
        cnx.commit()

        print(f"{cursor.rowcount} records inserted.")

        cursor.close()
    except Exception as e:
        print(f"Error Occurred: {e}")

    finally:
        if cnx is not None and cnx.is_connected():
            cnx.close()


# url = "ダウンロードしたい画像のURL"
# file_name = "保存したいファイル名.png"


f = open('hashtag/hashtag_2.txt', 'r', encoding='utf-8-sig')
datalist_hashtag = f.readlines()
f.close()

print(datalist_hashtag)

dt_now = datetime.datetime.now()

for i, word in enumerate(datalist_hashtag):
    word = word.replace('\n', '')
    json_object = request_to_instagram(word)
    url = []
    try:
        for i in range(9):
            print(i)
            url.append(json_object['data'][i]['media_url'])
    except Exception as e:
        print(f"Error Occurred: {e}")



    for i in range(len(url)):
        f = download_file(url[i]).read()
        print(url[i])
        img_name = dt_now.strftime('%Y_%m_%d_') + word + '_' + str(i)
        insert_to_db(img_name, word, f)
