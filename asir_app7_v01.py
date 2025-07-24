import streamlit as st
import pandas as pd
import requests
import time
from io import BytesIO
import folium
from streamlit_folium import st_folium

# 設定頁面
st.set_page_config(page_title="App7 | 好吃好玩探索工具", layout="wide")
st.title("🗺️ App7｜好吃好玩探索工具")

# 建立左右區域：參數區 (3) 與 顯示區 (7)
col_params, col_results = st.columns([3, 7])

# 左側參數區
with col_params:
    st.header("🔍 查詢設定")
    api_key_file = st.file_uploader("📥 上傳您的 Google Maps API 金鑰檔案（api_key.txt）", type=["txt"])
    api_key = None
    if api_key_file:
        api_key = api_key_file.read().decode("utf-8").strip()
        st.success("✅ 已成功載入 API 金鑰")
    else:
        st.warning("⚠️ 請先上傳 api_key.txt")

    keyword = st.text_input("查詢類別關鍵字", value=st.session_state.get('keyword', '加油站'))
    location = st.text_input("查詢中心位置 (經緯度)", value=st.session_state.get('location', '25.0478,121.5319'))
    radius = st.number_input(
        "搜尋半徑 (公尺)", min_value=100, max_value=50000,
        value=st.session_state.get('radius', 3000), step=500
    )

    if st.button("🚀 開始查詢") and api_key:
        # 儲存參數
        st.session_state['keyword'] = keyword
        st.session_state['location'] = location
        st.session_state['radius'] = radius

        def fetch_places(query, location, radius, api_key):
            url = (
                f"https://maps.googleapis.com/maps/api/place/textsearch/json?"
                f"query={query}&location={location}&radius={radius}&language=zh-TW&key={api_key}"
            )
            results = []
            while url:
                resp = requests.get(url)
                data = resp.json()
                for p in data.get('results', []):
                    results.append({
                        '名稱': p.get('name'),
                        '地址': p.get('formatted_address'),
                        '評分': p.get('rating'),
                        '評論數': p.get('user_ratings_total'),
                        '經度': p['geometry']['location']['lng'],
                        '緯度': p['geometry']['location']['lat'],
                        'Google Maps連結': (
                            f"https://www.google.com/maps/place/?q=place_id:{p.get('place_id')}"
                        )
                    })
                token = data.get('next_page_token')
                if token:
                    time.sleep(2)
                    url = (
                        f"https://maps.googleapis.com/maps/api/place/textsearch/json?"
                        f"pagetoken={token}&language=zh-TW&key={api_key}"
                    )
                else:
                    url = None
            return results

        try:
            # 取得資料並存入 state
            df = pd.DataFrame(fetch_places(keyword, location, radius, api_key))
            st.session_state['df'] = df

            # 建立 Folium 地圖物件並存入 state
            lat_c, lon_c = map(float, location.split(','))
            fmap = folium.Map(location=[lat_c, lon_c], zoom_start=14)
            for _, r in df.iterrows():
                folium.Marker(
                    location=[r['緯度'], r['經度']],
                    popup=f"{r['名稱']}<br>{r['地址']}<br>評分：{r['評分']}",
                    tooltip=r['名稱']
                ).add_to(fmap)
            # 存放於 session_state
            st.session_state['map_obj'] = fmap
            st.session_state['html_map'] = fmap.get_root().render()

            st.success(f"✅ 查詢完成，共 {len(df)} 筆資料")
        except Exception as e:
            st.error(f"❌ 查詢失敗：{e}")

    # 下載按鈕區
    if 'df' in st.session_state:
        df = st.session_state['df']
        # Excel 下載
        out = BytesIO()
        with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='查詢結果')
        out.seek(0)
        st.download_button(
            "📥 下載 Excel 結果", out,
            file_name=f"查詢結果_{st.session_state['keyword']}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        # HTML 地圖下載
        html_m = st.session_state.get('html_map')
        if html_m:
            st.download_button(
                "📥 下載地圖 (HTML)", html_m,
                file_name=f"探索地圖_{st.session_state['keyword']}.html",
                mime='text/html'
            )

# 右側顯示區
with col_results:
    if 'df' in st.session_state and 'map_obj' in st.session_state:
        df = st.session_state['df']
        # 資料區
        st.subheader("📋 查詢結果資料")
        sel = st.selectbox("選擇地點", df['名稱'])
        row = df[df['名稱'] == sel].iloc[0]
        st.markdown(f"**地址：** {row['地址']}")
        st.markdown(f"**評分：** {row['評分']}")
        st.markdown(f"[Google Maps]({row['Google Maps連結']})")

        # 地圖區
        st.subheader("🗺️ 互動式地圖")
        st_folium(st.session_state['map_obj'], width='100%', height=500)
    else:
        st.info("請設定參數並點擊「🚀 開始查詢」，結果將持久顯示於此。")
