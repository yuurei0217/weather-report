# 🌦️ AIoT Weather Map (台灣分區 7 日氣象預報系統)

這是一個以 Python 開發的 Web 應用程式，專門用來自動抓取並顯示台灣特定區域的「7 日農業氣象預報」資料。系統結合了自動化的資料爬蟲、本地端資料庫儲存，以及互動式的資料視覺化網頁介面。

## 🌟 專案特色 (Features)
*   **自動化資料獲取**：串接**中央氣象署 (CWA)** 開放資料 API，自動獲取最新的天氣預報 JSON 數據。
*   **資料庫儲存**：利用 SQLite 建立本地資料庫，確保資料在網頁存取時能快速且穩定地讀取。
*   **互動式視覺化**：透過 Streamlit 與 Plotly，呈現精美的氣溫趨勢折線圖，一眼就能掌握未來一週的最高與最低溫變化。
*   **地圖視覺化**：整合 Folium 於地圖上以顏色標示各地區當日平均氣溫，並支援互動式 Popup 顯示詳細資訊。
*   **資料匯出**：可自動將抓取的氣溫資料匯出成 CSV 檔案 (`weather_data.csv`)。
*   **安全環境管理**：支援 `.env` 環境變數配置，安全隱藏並管理您的 API Token。

## 🛠️ 技術堆疊 (Tech Stack)
*   **後端與資料處理**：Python, Pandas, SQLite3
*   **API 串接**：Requests, urllib3, python-dotenv
*   **前端網頁框架**：Streamlit
*   **圖表與視覺化**：Plotly Express

---

## 🚀 快速開始 (Getting Started)

### 1. 安裝套件
請確保您的系統已安裝 Python，接著安裝專案所需的套件：
```bash
pip install requests python-dotenv pandas streamlit plotly folium streamlit-folium
```

### 2. 設定環境變數 (API Key)
本專案需要使用中央氣象署的 API 金鑰。
1. 請至 [氣象資料開放平臺](https://opendata.cwa.gov.tw/) 註冊並取得您的 API Token。
2. 在專案的根目錄下建立一個名為 `api.env` 的檔案。
3. 將您的 Token 貼入檔案中，格式如下：
```env
CWA_API_TOKEN=替換成您自己的API金鑰字串
```

### 3. 獲取並儲存氣象資料
在啟動網頁之前，請先執行爬蟲程式將最新的預報資料抓取並存入本地端資料庫 (`data.db`)：
```bash
python data_fetcher.py
```
*(程式執行成功後，您會看到「資料已成功存入 SQLite3 資料庫」的提示訊息。)*

### 4. 啟動網頁應用程式
最後，啟動 Streamlit 伺服器來瀏覽您的互動式氣象網頁：
```bash
streamlit run app.py
```
執行後，瀏覽器將會自動開啟並顯示儀表板！

---

## 📂 專案檔案結構 (Project Structure)
*   `app.py`: Streamlit 網頁主程式，負責讀取資料庫並繪製前端介面與圖表。
*   `data_fetcher.py`: API 資料爬取程式，負責解析 CWA JSON 資料並寫入 SQLite。
*   `api.env`: (需自行建立) 放置 API Token 的環境變數設定檔。
*   `development_log.md`: 紀錄專案的開發過程、除錯歷史與實作細節。

## 📝 授權條款 (License)
本專案僅作學術/教學用途。資料來源：交通部中央氣象署。
