import os
from fastapi import FastAPI
import mysql.connector
from mysql.connector import errorcode

app = FastAPI()

# 環境変数から設定を読み込む
host = os.environ.get("DB_HOST", "default_host")
user = os.environ.get("DB_USER", "default_user")
password = os.environ.get("DB_PASSWORD", "default_password")
database = os.environ.get("DB_DATABASE", "default_database")


# Azure MySQLデータベースへの接続情報
config = {
  'host': host,
  'user': user,
  'password': password,
  'database': database
}

# データベースに接続
def get_db():
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(err)
        return None

@app.get("/search_product/{barcode}")
def search_product(barcode: int):
    # データベースに接続
    conn = get_db()
    if conn is None:
        return {"message": "Database connection failed"}

    cursor = conn.cursor()

    # SQLクエリを実行して商品情報を取得
    cursor.execute(f"SELECT PRD_NAME, PRD_PRICE FROM m_product WHERE PRD_CD = {barcode}") # m_productは商品マスタテーブル名
    result = cursor.fetchone()

    # データベース接続を閉じる
    conn.close()

    # 商品情報が見つかった場合
    if result:
        return {"product_name": result[0], "product_price": result[1]}
    # 商品情報が見つからなかった場合
    else:
        return {"message": "Product not found"}