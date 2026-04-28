# AIoT 氣象預報系統 - AI 協作對話紀錄

## 專案目標
開發一個完整的 Python 專案，透過中央氣象署 (CWA) API 獲取台灣各區的 7 日農業氣象預報資料，並建置具互動式地圖的 Streamlit 網頁應用程式。

## 對話與實作流程

### 1. 需求確認與程式碼更新
**使用者請求：**
- 修改現有專案，保留原有 SQLite 儲存與折線圖功能。
- 將獲取的溫度資料匯出為 `weather_data.csv`。
- 在 Streamlit 應用程式中加入 Folium 台灣氣溫地圖，根據平均溫度標示不同顏色 (<20°C 藍、20-25°C 綠、25-30°C 黃、>30°C 紅)。
- 建立左（地圖）右（數據表）排版，並加入動態日期選擇器。
- 地圖標記需支援 Popup 顯示該區詳細氣溫。
- 自動處理套件安裝 (`requests`, `pandas`, `streamlit`, `folium`, `streamlit-folium`)。

**AI 執行動作：**
- **更新 `data_fetcher.py`**：加入 Pandas DataFrame 的處理邏輯，將 API 獲取的 `extracted_data` 轉換為 DataFrame 並儲存至 `weather_data.csv`。
- **更新 `app.py`**：引入 `folium` 與 `streamlit_folium`。撰寫經緯度對應表，加入 UI 的左右欄位設計 (`st.columns`) 與顏色判斷邏輯。
- **環境設定**：使用自動化指令執行 `pip install folium streamlit-folium` 來滿足環境依賴。
- **測試與驗證**：在背景執行 `data_fetcher.py` 測試資料獲取與 CSV 產生是否成功。

### 2. 錯誤排除 (Debugging)
**使用者狀況：**
- 執行網頁時遇到 `AttributeError: 'ArrowStringArray' object has no attribute 'sort'` 錯誤。

**AI 執行動作：**
- **分析問題**：判斷為 Streamlit 的 `selectbox` 內部排序與 Pandas (基於 PyArrow) 的字串陣列格式產生相容性衝突。
- **修復程式碼**：將 `app.py` 中 `all_data['dataDate'].unique()` 及 `regions` 的回傳值加上 `.tolist()`，強制轉型為 Python 原生列表 (List) 來徹底解決此錯誤。

### 3. 文件更新與 GitHub 推送
**使用者請求：**
- 更新 `README.md` 和開發日誌 (`development_log.md`)。
- 將資料夾內的所有檔案推送到 GitHub (`yuurei0217/weather-report`)。

**AI 執行動作：**
- **文件更新**：
  - 在 `development_log.md` 補上「階段五：新功能開發 (Folium 地圖與動態過濾)」的詳細開發歷程。
  - 在 `README.md` 補上新增的套件安裝指令與新功能介紹。
- **建立安全機制**：為保障資訊安全，主動生成 `.gitignore` 以防止 API 金鑰 (`api.env`) 及虛擬環境 (`venv/`) 等機密/冗餘檔案外洩。
- **版控與推送**：在該目錄初始化 Git 儲存庫，將更新提交 (Commit)，並成功推送到指定的遠端 GitHub 儲存庫。

### 4. 總結
本專案成功透過 AI 協同開發，在短時間內將原本單純的數據爬蟲與折線圖應用，升級為包含地理資訊系統 (GIS) 與動態過濾的完整互動式資料視覺化平台。最後妥善地完成了專案的文件紀錄與版本控制。
