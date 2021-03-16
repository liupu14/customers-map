import numpy as np
import pandas as pd
import folium
import streamlit as st 
from streamlit_folium import folium_static
import geopandas as gpd

hangzhou_section = gpd.read_file("./hangzhou.shp",encoding="utf8")
hangzhou_ratio = pd.read_excel("./项目渗透率.xlsx")
projects_list = np.unique(hangzhou_ratio["project_name"])
dates_list = np.unique(hangzhou_ratio["date"])

st.title("杭州项目板块渗透率")
st.write("请在左侧面板中输入相应的参数，而后点击执行")

project_name = st.sidebar.selectbox("选择项目名称",projects_list)
date = st.sidebar.selectbox("选择日期",dates_list)
pressed = st.sidebar.button("执行")

show_data = hangzhou_ratio[np.logical_and(hangzhou_ratio["project_name"]==project_name,hangzhou_ratio["date"]==date)]
geo_data = hangzhou_section[hangzhou_section.id.isin(hangzhou_ratio.id)]

if pressed:
    Map = folium.Map(location=[30.40024,120.31582],zoom_start=12,tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',attr="gaode")
    g = folium.Choropleth(
        geo_data=geo_data,
        data=show_data,
        columns=['id','ratio'],
        key_on='feature.properties.id',
        fill_color='OrRd',
        fill_opacity=0.85,
        line_opacity=0.2  
    ).add_to(Map)
    folium_static(Map)

