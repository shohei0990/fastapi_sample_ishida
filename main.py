import os
from fastapi import FastAPI, Depends ,Request
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
#from sql_app.database import db_session, engine

load_dotenv() 
app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では "*" ではなく、適切なオリジンを設定してください。
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class Product(BaseModel):
    PRD_ID:Optional [int]
    CODE:Optional [str]
    NAME: Optional[str]
    PRICE:Optional [int]

class Transaction(BaseModel):
    EMP_CD:Optional [int]
    STORE_CD:Optional [int]
    POS_NO: Optional[int]
    BUYPRODUCTS: Optional[List[Product]]


# データベースに接続
def get_db():
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(err)
        return None

@app.get("/search_product/{barcode}") # {barcode}はパスパラメータ
def search_product(barcode: int):
    # データベースに接続
    conn = get_db()
    if conn is None:
        return {"message": "Database connection failed"}

    cursor = conn.cursor() # カーソルオブジェクトを作成

    # SQLクエリを実行して商品情報を取得
    cursor.execute("SELECT PRD_NAME, PRD_PRICE FROM m_product WHERE PRD_CD = %s", (barcode,)) # m_productは商品マスタテーブル名
    result = cursor.fetchone()  # 結果を1行取得

    # データベース接続を閉じる
    conn.close()

    # 商品情報が見つかった場合
    if result:
        return {"product_name": result[0], "product_price": result[1]}
    # 商品情報が見つからなかった場合
    else:
        return {"message": "Product not found"}
    
###購入明細の登録
@app.post("/buy_product/")
async def buy_product(data: Transaction,  request: Request ):
    body = await request.json()
    print(f"Raw body: {body}")
    print(f"Model data: {data}")

    conn = get_db()
    if conn is None:
        return {"message": "Database connection failed"}
    cursor = conn.cursor()

    try:
        cursor.execute("START TRANSACTION")
        cursor.execute("INSERT INTO t_txn (EMP_ID, STORE_CD, POS_NO) VALUES (%s, %s, %s)", (12, 30, 90))
        TXN_ID = cursor.lastrowid

        TOTAL_AMT = 0
        TTL_AMT_EX_TAX = 0

        for idx, product in enumerate(data.BUYPRODUCTS):
            TXN_DTL_ID = idx + 1
            TAX_ID = 1
            cursor.execute("INSERT INTO t_txn_dtl (TXN_ID, TXN_DTL_ID, PRD_ID, PRD_CD, PRD_NAME, PRD_PRICE, TAX_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (TXN_ID, TXN_DTL_ID, product.PRD_ID, product.CODE, product.NAME, product.PRICE, TAX_ID))
            if product.PRICE is not None:
                TOTAL_AMT += product.PRICE
                TTL_AMT_EX_TAX += product.PRICE

        cursor.execute("UPDATE t_txn SET TOTAL_AMT = %s, TTL_AMT_EX_TAX = %s WHERE TXN_ID = %s", (TOTAL_AMT, TTL_AMT_EX_TAX, TXN_ID))
        cursor.execute("COMMIT")

    except mysql.connector.Error as err:
        print(err)
        cursor.execute("ROLLBACK")
        return {"message": f"Transaction failed: {err}"}

    finally:
        if conn is not None:
            conn.close()

    return {"success": True, "total_amount": TOTAL_AMT, "total_amount_with_tax": TTL_AMT_EX_TAX}