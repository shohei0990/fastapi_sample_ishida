# Azure Database for MySQL のデータベースとFASTAPIの連携    
・バーコード数字を入力し、データベースにあるかどうかをチェックする。     
・バーコードが一致する箇所の商品名と価格を返す。  
            
# 環境変数について  
・ローカルで動かす際には .envファイルに必要な値を入れる。  
・Azure web appで動かす際の手順  
① Azure web app作成  
② デプロイセンターで、git-hubと接続設定  
③ 構成：全般設定 → スタートアップコマンド → この場合はstartup.txt 中身はuvicorn main:app --host 0.0.0.0 --port 8000でFASTAPIのrun指示  
④ 構成:アプリケーション設定→新しいアプリケーション設定にて、各環境変数名と値を登録  
※git-hubに環境変数は入れず、Azureで環境変数の値を設定して動かす方法  
