from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'YXwu8005',
    'host': 'localhost',
    'database': 'sakila' 
}

# 定義一個路由 /，並允許 GET 和 POST 方法來訪問該路由。
# 當使用者瀏覽器訪問 http://127.0.0.1:5000/ 時，這個 index() 函式會被執行。

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = mysql.connector.connect(**db_config) # 連接到 MySQL 資料庫
    cursor = conn.cursor() # 建立 cursor 物件來執行 SQL 查詢操作

    # 檢查當前的 HTTP 請求方法是否為 POST。POST 方法通常用於處理表單提交或新增資料
    if request.method == 'POST':
         
        # 從表單中提取使用者提交的 actor_id、first_name 和 last_name 值。這些值是來自於 index.html 中 <input> 欄位的 name 屬性
        actor_id = request.form['actor_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # 定義 SQL 插入語句 insert_query，將表單中接收到的資料插入到 actor 資料表中
        insert_query = """
            INSERT INTO actor (actor_id, first_name, last_name, last_update)
            VALUES (%s, %s, %s, NOW())
        """
       
        cursor.execute(insert_query, (actor_id, first_name, last_name))
        conn.commit() # 提交變更，將插入操作儲存至資料庫

    # 查詢 actor 資料表中的所有資料
    select_query = "SELECT actor_id, first_name, last_name FROM actor"
    cursor.execute(select_query)
    actor = cursor.fetchall() # 取得所有查詢結果

    # 執行完操作後，關閉游標 (cursor.close()) 和資料庫連接 (conn.close())，釋放資源
    cursor.close()
    conn.close()

    return render_template('index.html', actor=actor) # 渲染 index.html 模板，並將 actor 資料傳遞給模板，供模板顯示

# 啟動 Flask 應用程式，並開啟除錯模式（debug=True），這樣 Flask 會自動重新載入檔案並顯示錯誤訊息
if __name__ == '__main__':
    app.run(debug=True)
