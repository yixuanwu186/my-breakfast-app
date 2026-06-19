import streamlit as st
import random
import urllib.parse
import json
import extra_streamlit_components as stx

st.set_page_config(page_title="🍔 終極早餐店 5.1", layout="wide")

import os
os.environ["STREAMLIT_CLIENT_SHOW_ERROR_DETAILS"] = "False"

def get_cookie_manager():
    return stx.CookieManager()

cookie_manager = get_cookie_manager()

st.title("🍔 終極早餐救星 5.1 (具備長期記憶版)")
st.write("設定一次，記憶一生！明天打開網頁，勾選依然在 !")


default_data = {
    "麥當勞": ["大麥克", "滿福堡", "薯餅", "雞塊", "蛋堡"],
    "永和豆漿": ["蛋餅", "燒餅油條", "小籠包", "飯糰", "饅頭夾蛋"],
    "美而美": ["漢堡", "卡啦雞腿堡", "鐵板麵", "湯種吐司", "蛋餅"],
    "拉亞漢堡": ["貝果", "帕尼尼", "蛋餅", "芝加哥漢堡", "美式咖啡"]
}

if "restaurant_data" not in st.session_state:
    st.session_state.restaurant_data = default_data

saved_data = cookie_manager.get(cookie="breakfast_data")
if saved_data:
    try:
        st.session_state.restaurant_data = json.loads(saved_data)
    except:
        st.session_state.restaurant_data = default_data
else:
    if "restaurant_data" not in st.session_state:
        st.session_state.restaurant_data = default_data


saved_selected = cookie_manager.get(cookie="selected_shops")
if saved_selected:
    try:
        init_selected = json.loads(saved_selected)
    except:
        init_selected = list(st.session_state.restaurant_data.keys())
else:
    init_selected = list(st.session_state.restaurant_data.keys())


if "current_restaurant" not in st.session_state:
    st.session_state.current_restaurant = ""
if "current_food" not in st.session_state:
    st.session_state.current_food = "今天想吃什麼呢? 先在左邊功能版面設定吧!"

with st.sidebar:
    st.header("🌐 1.黑客雷達:尋找附近的早餐店")

    search_query = "早餐店"
    encoded_query = urllib.parse.quote(search_query)
    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"

    st.write("點擊下方按鈕，直接利用手機/電腦 GPS 彈出附近所有早餐店 :")
    st.sidebar.markdown(f'[@img](https://img.shields.io/badge/🗺_開啟_Google_地圖雷達-EA4335?style=for-the-badge&logo=googlemaps&logoColor=white) [{gmaps_url}]({gmaps_url})')

    st.divider()

    st.header("🏪 2. 勾選今日候選店家")
    st.write("你想讓哪幾家店餐與抽獎？(勾選會自動儲存)")

    available_shops = list(st.session_state.restaurant_data.keys())
    selected_shops = []

    for shop in available_shops:
        is_checked = shop in init_selected
        if st.checkbox(shop, value=is_checked):
            selected_shops.append(shop)

    if selected_shops != init_selected:
        cookie_manager.set("selected_shops", json.dumps(selected_shops), max_age=2592000) # 記憶30天
        st.rerun()
        
    st.divider()

    st.header("➕ 3. 手動新增店家")
    new_shop = st.text_input("輸入新店家名稱:")
    new_menu_raw = st.text_input("輸入這家店的菜單（用逗號隔開）:")

    if st.button("✨ 將新店家加入資料庫", use_container_width=True):
        if new_shop and new_menu_raw:
            menu_list = [item.strip() for item in new_menu_raw.split(",")]
            st.session_state.restaurant_data[new_shop] = menu_list
            cookie_manager.set("breakfast_data", json.dumps(st.session_state.restaurant_data), max_age=2592000)
            st.success(f"成功加入【{new_shop}】！")
            st.rerun()

st.subheader("🎯 候選名單池狀態")
if len(selected_shops) == 0:
    st.error("🚨 左邊至少要勾選一家店喔！")
else:
    st.caption(f"目前鎖定的候選名單：{', '.join(selected_shops)}")

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 幫我選一家店 + 一個餐點！", use_container_width=True, type="primary"):
        if len(selected_shops) > 0:
            picked_shop = random.choice(selected_shops)
            picked_food = random.choice(st.session_state.restaurant_data[picked_shop])
            st.session_state.current_restaurant = picked_shop
            st.session_state.current_food = picked_food

with col2:
    if st.button("🔄 店家沒開/不滿意，純重抽", use_container_width=True):
        if len(selected_shops) > 0:
            picked_shop = random.choice(selected_shops)
            picked_food = random.choice(st.session_state.restaurant_data[picked_shop])
            st.session_state.current_restaurant = picked_shop
            st.session_state.current_food = picked_food

st.divider()

if st.session_state.current_restaurant:
    st.markdown(f"""
    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 8px solid #ff4b4b;">
        <h3 style="margin:0; color:#31333F;">👑 今天的黃金組合：</h3>
        <h1 style="margin:10px 0; color:#ff4b4b;">【{st.session_state.current_restaurant}】 的 ─── ✨ {st.session_state.current_food} ✨</h1>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info(st.session_state.current_food)
    
    
             






























    
    
