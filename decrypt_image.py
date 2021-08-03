import requests
import base64
import json
import pprint
import io
from PIL import Image
from urllib.parse import urlparse
import mysql.connector


def select_from_db():
    cnx = None

    try:
        cnx = mysql.connector.connect(
            user='root',  # ユーザー名
            password='niko0115',  # パスワード
            host='localhost',  # ホスト名(IPアドレス）
            database='sampledb'  # データベース名
        )

        print(cnx.is_connected())
    
        cursor=cnx.cursor(buffered=True)

        cnx.commit()

        sql = ('''SELECT img FROM img_to_binary WHERE id = 10''')

        cursor.execute(sql)
    
        cnx.commit()
        result = cursor.fetchone()
        bnr = result[0]
        #thumbnail = Image.open(bnr)
        #thumbnail.save(bnr, "JPEG")

        f = open('load2DBforCameraImage.png', 'wb')
        f.write(bnr)

        cursor.close()
    except Exception as e:
        print(f"Error Occurred: {e}")

    finally:
        if cnx is not None and cnx.is_connected():
            cnx.close()


select_from_db()