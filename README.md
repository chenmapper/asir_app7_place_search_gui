# 📘 asir_app7_好吃好玩探索工具 v0.1

基於 Streamlit + Folium 架構，支援使用者上傳 API 金鑰、查詢任意關鍵字與地點，並即時產製互動地圖與查詢報表。

本應用適合作為地圖資料探索、API 操作、視覺化與下載流程的入門教案與範例工具。

---

## 🚀 主要功能特色

- ✅ 上傳 Google Maps API 金鑰（api_key.txt）
- ✅ 查詢任意地點與關鍵字，支援經緯度座標與搜尋半徑
- ✅ 自動擷取最多 60 筆 Google Maps 地點資料
- ✅ 地點顯示於 Folium 互動式地圖，可點選標記、查看 popup 詳情
- ✅ 結果匯出為 Excel 檔（地點清單）與 HTML 檔（可分享的互動地圖）
- ✅ 支援持久顯示與查詢歷程保留，方便持續探索

---

## 📂 安裝說明

### 安裝必要套件（可透過 requirements.txt）

```bash
pip install -r requirements.txt
# 或手動安裝
pip install streamlit pandas requests folium streamlit-folium
```

---

## ▶️ 執行方式

```bash
streamlit run asir_app7_v01.py
```

1. 上傳您的 `api_key.txt`
2. 輸入地點關鍵字、中心座標與半徑
3. 點擊「🚀 開始查詢」，即時呈現結果與互動地圖
4. 可下載 Excel 結果表與 HTML 地圖檔案

---

## 📁 專案結構

```
case7/
├─ asir_app7_v01.py           # 主程式
├─ requirements.txt           # 套件清單
├─ LICENSE                    # 授權條款
└─ README.md                  # 說明文件（本檔）
```

---

## 🔖 授權

本專案採 MIT License 授權，歡迎學習、教學與延伸應用，請保留原始出處與說明。

---

> 本工具結合地圖資料查詢、API 實務應用與資料視覺化，是學生與學員練習地理資訊視覺探索的最佳起手式。