# Azure Database for MySQL のデータベースと FASTAPI の連携

・バーコード数字を入力し、データベースにあるかどうかをチェックする。  
・バーコードが一致する箇所の商品名と価格を返す。

# 環境変数について

・ローカルで動かす際には .env ファイルに必要な値を入れる。  
・Azure web app で動かす際の手順  
① Azure web app 作成  
② デプロイセンターで、git-hub と接続設定  
③ 構成：全般設定 → スタートアップコマンド → この場合は startup.txt 中身は uvicorn main:app --host 0.0.0.0 --port 8000 で FASTAPI の run 指示  
④ 構成:アプリケーション設定 → 新しいアプリケーション設定にて、各環境変数名と値を登録  
※git-hub に環境変数は入れず、Azure で環境変数の値を設定して動かす方法

※main.py の SQL クエリを実行して商品情報を取得 : p_info はテーブル名に変更要
