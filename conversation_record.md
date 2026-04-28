# AIoT 氣象預報系統 - AI 協作對話紀錄

## 專案目標
開發一個完整的 Python 專案，透過中央氣象署 (CWA) API 獲取台灣各區的 7 日農業氣象預報資料，並建置具互動式地圖的 Streamlit 網頁應用程式。

---

## 歷次對話與實作流程 (階段一至階段五)

### 階段一：資料爬蟲與環境變數設定
**使用者請求：**
- 請幫我寫一個 Python 程式，可以去接中央氣象署的農業氣象預報 API (F-A0010-001)。
- 幫我把抓到的資料篩選出「北部地區、中部地區、南部地區、東北部地區、東部地區、東南部地區」的每日最高與最低溫。
- API 金鑰請不要寫死在程式碼裡面，要用環境變數 (`.env`) 的方式安全管理。

**AI 執行動作：**
- **建立腳本**：撰寫 `data_fetcher.py` 並匯入 `requests`, `dotenv`。
- **處理金鑰**：設定透過 `os.getenv("CWA_API_TOKEN")` 讀取 `api.env` 檔案。
- **資料解析**：針對 CWA 回傳的複雜 JSON 結構，深入至 `location` 節點萃取所需的分區與溫度資料，並過濾出目標區域。
- **SSL 設定**：加入 `urllib3.disable_warnings` 以處理暫時的 SSL 驗證問題。

### 階段二：建置本地 SQLite 資料庫
**使用者請求：**
- 我想要把剛剛抓下來的氣象資料存到一個本機的 SQLite 資料庫 (`data.db`)。
- 每次執行腳本時，先清空舊的資料再寫入新的，確保資料是最新的。

**AI 執行動作：**
- **資料庫整合**：在 `data_fetcher.py` 加入 `setup_db()` 函式，並透過 `CREATE TABLE IF NOT EXISTS` 建立資料表架構。
- **覆寫邏輯**：實作 `DELETE FROM TemperatureForecasts`，清除舊有預報紀錄。
- **資料寫入**：利用迴圈與 `cursor.execute` 將過濾好的日期、地區、最低與最高溫結構化寫入資料庫。

### 階段三：建構 Streamlit 前端網頁與視覺化
**使用者請求：**
- 請幫我寫一個 `app.py`，用 Streamlit 做一個網頁介面來顯示剛剛存進 SQLite 的資料。
- 網頁要有下拉選單讓使用者選擇地區。
- 畫面分成左右兩半：左邊顯示該地區一週氣溫的折線圖 (用 Plotly)，右邊顯示詳細數值的表格。

**AI 執行動作：**
- **UI 佈局**：設定 `layout="wide"`，並利用 `st.columns([1, 1])` 切割左右版面。
- **資料整合**：撰寫 `get_db_data()`，將 SQLite 的查詢結果轉換為 Pandas DataFrame。
- **圖表繪製**：引入 `plotly.express`，繪製雙線圖 (MaxT 與 MinT)；右側利用 `st.dataframe` 顯示整齊的數據表，並將欄位名稱中文化。

### 階段四：除錯與警告優化 (Debugging)
**使用者狀況：**
- 直接執行 `python app.py` 失敗，而且網頁圖表一直跳出 `use_container_width=True` 即將被棄用 (deprecated) 的警告。

**AI 執行動作：**
- **啟動方式除錯**：向使用者解釋 Streamlit 的底層運作邏輯，指導其改用 `streamlit run app.py` 指令啟動。
- **程式碼重構**：將 `st.plotly_chart` 和 `st.dataframe` 的參數從舊版的 `use_container_width=True` 全面替換為最新版官方建議的 `width='stretch'`，解決所有相容性警告。

### 階段五：新功能開發 (Folium 地圖與動態過濾)
**使用者請求：**
- 保留原本的 SQLite 與折線圖功能。
- 將獲取的資料額外匯出為 `weather_data.csv`。
- 新增 Folium 台灣氣溫地圖，根據平均溫度 (<20°C藍、20-25°C綠、25-30°C黃、>30°C紅) 標示不同顏色的地圖圓點，點擊需有 Popup 詳細資訊。
- 新增「日期選擇器」，並搭配地圖與表格顯示當天所有地區的氣溫。
- 修復開發過程出現的 `ArrowStringArray` 排序錯誤，最後推送到 GitHub (`weather-report`)。

**AI 執行動作：**
- **擴充 `data_fetcher.py`**：加入 Pandas DataFrame 處理邏輯，將提取之資料儲存至 `weather_data.csv`。
- **更新 `app.py` 與套件**：引入 `folium` 與 `streamlit_folium`，定義各區經緯度，並利用 `selectbox` 連動地圖圓點與表格渲染。
- **修復錯誤**：透過加上 `.tolist()` 強制將 PyArrow 陣列轉型為原生列表，徹底解決排序異常問題。
- **文件與版控**：自動產生 `.gitignore`，補齊 `README.md` 及 `development_log.md` 後，完成 Git 初始化並推送到使用者的 GitHub。

---

### 總結
本專案經歷了五個階段的演進，從單純的 API 爬蟲、本地端資料庫建置，一路升級為具備雙向互動 (單一地區 7 日趨勢 + 單日全台 GIS 氣象地圖) 的完整 Web 系統。在 AI 協同開發的過程中，不僅高效率完成需求，亦妥善處理了非同步型別衝突、環境安全管理及版控紀錄。
