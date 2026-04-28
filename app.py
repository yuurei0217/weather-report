import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="AIoT 氣溫預報 Web App", layout="wide")

st.title("🌦️ 台灣分區 7 日氣象預報系統")

# HW2-4: 從 SQLite 資料庫查詢資料
def get_db_data(region=None):
    # 為了避免路徑錯誤，使用腳本所在目錄為基礎路徑
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.db')
    if not os.path.exists(db_path):
        return pd.DataFrame()
        
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM TemperatureForecasts"
    if region:
        query += f" WHERE regionName = '{region}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

all_data = get_db_data()

if not all_data.empty:
    st.markdown("---")
    st.header("🗺️ 台灣氣溫地圖與每日數據 (Folium Map)")
    
    # 建立日期選單
    available_dates = sorted(all_data['dataDate'].unique().tolist())
    selected_date = st.selectbox("請選擇日期查看各地區氣溫：", available_dates)
    
    # 篩選特定日期的資料
    date_df = all_data[all_data['dataDate'] == selected_date].copy()
    
    # 計算平均溫度
    date_df['avgT'] = (date_df['minT'] + date_df['maxT']) / 2
    
    # 定義經緯度字典
    region_coords = {
        "北部地區": [25.0, 121.5],
        "中部地區": [24.0, 120.8],
        "南部地區": [23.0, 120.3],
        "東北部地區": [24.7, 121.7],
        "東部地區": [23.8, 121.5],
        "東南部地區": [22.7, 121.1]
    }
    
    col_map, col_table = st.columns([1, 1])
    
    with col_map:
        st.subheader("📍 氣溫分布地圖")
        # 建立 Folium 地圖，中心設定在台灣
        m = folium.Map(location=[23.7, 121.0], zoom_start=7)
        
        for _, row in date_df.iterrows():
            reg = row['regionName']
            if reg in region_coords:
                avg_t = row['avgT']
                
                # 決定顏色
                if avg_t < 20:
                    color = "blue"
                elif 20 <= avg_t <= 25:
                    color = "green"
                elif 25 < avg_t <= 30:
                    color = "yellow"
                else:
                    color = "red"
                    
                popup_html = f"<b>{reg}</b><br>日期: {row['dataDate']}<br>最低溫: {row['minT']}°C<br>最高溫: {row['maxT']}°C<br>平均溫: {avg_t:.1f}°C"
                
                folium.CircleMarker(
                    location=region_coords[reg],
                    radius=15,
                    popup=folium.Popup(popup_html, max_width=200),
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7
                ).add_to(m)
                
        st_folium(m, width=700, height=500)
        
    with col_table:
        st.subheader(f"📅 {selected_date} 詳細氣溫數據")
        display_date_df = date_df[['regionName', 'minT', 'maxT', 'avgT']].rename(
            columns={'regionName': '地區', 'minT': '最低氣溫 (°C)', 'maxT': '最高氣溫 (°C)', 'avgT': '平均氣溫 (°C)'}
        )
        st.dataframe(display_date_df.set_index('地區'), width='stretch')

    st.markdown("---")
    st.header("📈 單一地區 7 日趨勢")

    # HW2-4: 下拉選單功能，讓使用者選擇地區並查看該地區的氣溫預報
    regions = all_data['regionName'].unique().tolist()
    selected_region = st.selectbox("請選擇預報地區：", regions)
    
    # 從 SQLite3 資料庫查詢單一地區的資料
    region_df = get_db_data(selected_region)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # HW2-4: 使用折線圖來顯示一週的氣溫資料
        st.subheader(f"📈 {selected_region} 氣溫趨勢折線圖")
        fig = px.line(region_df, x='dataDate', y=['minT', 'maxT'], 
                      labels={'value': '溫度 (°C)', 'dataDate': '日期', 'variable': '氣溫類型'},
                      markers=True)
        st.plotly_chart(fig, width='stretch')

    with col2:
        # HW2-4: 使用表格來顯示一週的氣溫資料
        st.subheader(f"📊 {selected_region} 詳細氣溫數據表")
        display_df = region_df[['dataDate', 'minT', 'maxT']].rename(
            columns={'dataDate': '日期', 'minT': '最低氣溫 (minT)', 'maxT': '最高氣溫 (maxT)'}
        )
        st.dataframe(display_df.set_index('日期'), width='stretch')

else:
    st.warning("資料庫中無資料，請先執行 data_fetcher.py 建立 data.db 檔案！")