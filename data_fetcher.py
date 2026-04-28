import os
from dotenv import load_dotenv
import requests
import json
import sqlite3
import urllib3
import pandas as pd

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def setup_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # HW2-3: 創建資料庫 Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TemperatureForecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regionName TEXT,
            dataDate TEXT,
            minT INTEGER,
            maxT INTEGER
        )
    ''')
    conn.commit()
    return conn

def fetch_and_save(api_key):
    # HW2-1: 調用 CWA API (F-A0010-001 農業氣象)
    url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001"
    params = {"Authorization": api_key, "downloadType": "WEB", "format": "JSON"}
    
    try:
        response = requests.get(url, params=params, verify=False)
        data = response.json()
        
        # 檢查 API 請求是否成功
        if 'cwaopendata' not in data:
            print("API 請求失敗或沒有回傳預期的資料！")
            return

        # HW2-1: 觀察獲得的資料 (使用 json.dumps)
        # 將部分原始資料印出觀察
        print("HW2-1 觀察獲得的資料:")
        print(json.dumps(data, indent=4, ensure_ascii=False)[:300], "...(略)\n")

        conn = setup_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TemperatureForecasts") # 清空舊資料
        
        # 載入 rawData 檔案結構中的位置資料
        locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
        target_regions = ["北部地區", "中部地區", "南部地區", "東北部地區", "東部地區", "東南部地區"]
        
        extracted_data = [] # 用來蒐集提取出的結果以利後續觀察
        
        for loc in locations:
            region_name = loc['locationName']
            if region_name in target_regions:
                # HW2-2: 提取最高與最低氣溫
                min_temps = loc['weatherElements']['MinT']['daily']
                max_temps = loc['weatherElements']['MaxT']['daily']
                
                for i in range(len(min_temps)):
                    date = min_temps[i]['dataDate']
                    mint = int(min_temps[i]['temperature'])
                    maxt = int(max_temps[i]['temperature'])
                    
                    extracted_data.append({
                        "regionName": region_name,
                        "dataDate": date,
                        "minT": mint,
                        "maxT": maxt
                    })
                    
                    # HW2-3: 將氣溫資料存到資料庫
                    cursor.execute('''
                        INSERT INTO TemperatureForecasts (regionName, dataDate, minT, maxT)
                        VALUES (?, ?, ?, ?)
                    ''', (region_name, date, mint, maxt))
        
        # HW2-2: 使用 json.dumps 觀察提取的資料
        print("HW2-2 觀察提取的資料:")
        print(json.dumps(extracted_data[:3], indent=4, ensure_ascii=False), "\n...(只顯示前3筆)\n")
        
        conn.commit()
        print("HW2-3: 資料已成功存入 SQLite3 資料庫 (data.db)。\n")
        
        # 儲存為 CSV 檔案
        df = pd.DataFrame(extracted_data)
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather_data.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"資料已成功存入 CSV 檔案 ({csv_path})。\n")
        
        # HW2-3 檢查資料：列出所有地區名稱
        cursor.execute("SELECT DISTINCT regionName FROM TemperatureForecasts")
        print("HW2-3 列出所有地區名稱：", [r[0] for r in cursor.fetchall()])
        
        # HW2-3 檢查資料：列出中部地區的氣溫資料
        cursor.execute("SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區'")
        print("HW2-3 中部地區的氣溫資料：", cursor.fetchall()[:3], "...(略)")
        
        conn.close()
    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    # 取得目前腳本所在的資料夾路徑
    base_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(base_dir, 'api.env')
    
    # 載入絕對路徑下的 api.env
    load_dotenv(env_path)
    
    # 從環境變數獲取 Token
    USER_TOKEN = os.getenv("CWA_API_TOKEN") 
    
    if not USER_TOKEN:
        print("請在 api.env 檔案中設定 CWA_API_TOKEN 變數")
    else:
        fetch_and_save(USER_TOKEN)