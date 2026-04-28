# AIoT 氣象預報系統 (Weather Map) - 開發日誌

## 專案概述
本專案為一個台灣分區的 7 日農業氣象預報 Web 應用程式。主要功能包含從中央氣象署 (CWA) 自動抓取氣象開放資料、將資料結構化並儲存於本地端資料庫，最後透過 Streamlit 建立具備互動式圖表的網頁介面，供使用者查詢各地區的氣溫趨勢。

## 系統架構與技術堆疊
*   **資料獲取**：Python (`requests`, `json`)
*   **環境變數管理**：`python-dotenv` (`api.env`)
*   **資料儲存**：SQLite3 (`data.db`)
*   **資料處理**：`pandas`
*   **網頁前端框架**：Streamlit
*   **資料視覺化**：Plotly Express (`plotly.express`)

---

## 開發歷程與實作細節

### 階段一：資料抓取與處理 (`data_fetcher.py`)
1.  **API 串接**：
    *   目標設定為中央氣象署的**農業氣象預報**資料集 (代碼：`F-A0010-001`)。
    *   **問題排除**：初期曾遇到 API "Resource not found" 的錯誤，後續將端點修正為正確的 `fileapi/v1/opendataapi` 網址後成功取得 JSON 回傳資料。
    *   實作了環境變數管理，將 API 金鑰安全地儲存於 `api.env` 檔案中，並透過 `os.getenv` 讀取，避免將機密資訊硬編碼在腳本中。
    *   加入 `urllib3.disable_warnings` 來忽略暫時性的 SSL 憑證警告 (`verify=False`)。

2.  **資料解析**：
    *   深層解析複雜的 JSON 結構 `data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']`。
    *   **目標鎖定**：將資料範圍限縮在特定的六大地區（"北部地區", "中部地區", "南部地區", "東北部地區", "東部地區", "東南部地區"）。
    *   針對每日的「最高溫 (MaxT)」與「最低溫 (MinT)」進行資料提取，整理成包含地區、日期、高低溫的結構化字典格式。

### 階段二：資料庫建置
1.  **SQLite 整合**：
    *   在 `setup_db()` 函式中建立本地資料庫檔案 `data.db`。
    *   建立資料表 `TemperatureForecasts`，包含欄位：`id`, `regionName`, `dataDate`, `minT`, `maxT`。
2.  **資料寫入邏輯**：
    *   為確保資料的即時性與正確性，實作了「覆寫邏輯」：在寫入新抓取的資料前，會先執行 `DELETE FROM TemperatureForecasts` 清空舊資料。
    *   透過 `cursor.execute(INSERT INTO...)` 將解析完的預報資料逐筆寫入資料庫。

### 階段三：網頁前端介面 (`app.py`)
1.  **Streamlit 基礎建設**：
    *   設定頁面標題為 "AIoT 氣溫預報 Web App"，並採用寬版佈局 (`layout="wide"`)。
    *   實作 `get_db_data()` 函式，利用 `pandas.read_sql_query` 搭配 sqlite3 連線，將資料庫資料直接轉換為 Pandas DataFrame，方便後續視覺化與表格渲染。

2.  **互動式使用者介面 (UI)**：
    *   透過 `st.selectbox` 實作下拉式選單，動態抓取資料庫內所有不重複的地區名稱 (`unique()`) 作為選項。
    *   使用 `st.columns([1, 1])` 將頁面劃分為左右兩個區塊，達到圖表與數據並排的優美排版。

3.  **資料視覺化**：
    *   **左側圖表**：匯入 `plotly.express` 繪製互動式折線圖 (`px.line`)。將 X 軸設為日期，Y 軸同時呈現最高溫與最低溫的變化趨勢，讓使用者能直觀了解一週氣溫走勢。
    *   **右側表格**：使用 `st.dataframe` 呈現詳細數值，並對 DataFrame 的欄位名稱進行了繁體中文的重新命名，提升閱讀性。

### 階段四：除錯與優化
1.  **Streamlit 執行錯誤排除**：
    *   **問題**：使用者初期嘗試使用一般的 `python app.py` 執行網頁腳本，導致終端機產生大量 `missing ScriptRunContext` 警告且無法顯示網頁。
    *   **解決方案**：釐清了 Streamlit 的底層運作機制，改用專屬的 `streamlit run app.py` 指令啟動本地端伺服器，成功運行應用程式。
2.  **API 棄用警告 (Deprecation Warning) 修正**：
    *   **問題**：執行 Streamlit 時出現 `use_container_width=True` 即將在未來版本被棄用的警告。
    *   **解決方案**：重構 `app.py` 的程式碼，將 `st.plotly_chart` 與 `st.dataframe` 中的舊參數替換為最新的官方建議寫法 `width='stretch'`，確保程式碼具備未來相容性 (Future-proofing)。

---

### 階段五：新功能開發 (Folium 地圖與動態過濾)
1.  **地圖視覺化 (Folium)**：
    *   整合 `folium` 與 `streamlit-folium`，於左側版面顯示台灣地圖。
    *   計算各區平均溫度 `(minT + maxT) / 2`，並依據溫度區間 (<20藍色, 20-25綠色, 25-30黃色, >30紅色) 標示不同顏色的地圖圓點。
    *   點擊圓點可顯示 Popup 包含：地區名稱、日期、最低溫、最高溫及平均溫度。
2.  **動態過濾與 CSV 匯出**：
    *   加入日期選擇器 (`st.selectbox`)，讓使用者能動態切換檢視特定日期的氣溫。
    *   右側增加表格顯示選定日期的詳細數據。
    *   在 `data_fetcher.py` 實作 Pandas `to_csv`，將抓取下來的氣溫資料匯出為 `weather_data.csv`。
3.  **修復 Streamlit 與 Pandas 的型別問題**：
    *   解決 `ArrowStringArray` 導致的 `.sort()` 錯誤，將 `unique()` 取得的資料加上 `.tolist()` 轉型為 Python 原生 List 再進行排序。

---

## 未來展望 (TODOs)
*   [ ] **自動化排程**：可以考慮加入 `schedule` 或系統排程 (Windows Task Scheduler / Linux Cron)，每天定時執行 `data_fetcher.py` 更新資料。
*   [ ] **擴充天氣資訊**：除了氣溫外，進一步從 JSON 中提取並顯示「降雨機率 (PoP)」、「天氣現象 (Wx)」等更多實用的氣象元素。
*   [ ] **視覺化進階**：可以在地圖上 (例如使用 Folium 或 Streamlit 原生的 Map) 直接標示各區氣溫，打造更直觀的「氣象地圖 (Weather Map)」體驗。
