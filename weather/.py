import streamlit as st
import pandas as pd
import requests
import os
import folium
from streamlit.components.v1 import html
import time
from datetime import datetime
from weather.config import  API_KEY








st.set_page_config(page_title="Hava Durumu", page_icon="🌤️")
st.title("🌤️ Şehir ve İlçeye Göre Hava Durumu Uygulaması")
st.header("Hoşgeldiniz")





df = pd.read_csv("weather/il_ilce.csv")
sehirler = df["il"].unique()
secilen_sehir = st.selectbox("Şehir Seçin",sorted(sehirler))



ilceler = df[df['il'] == secilen_sehir]['ilce']
secilen_ilce = st.selectbox("İlçe seçin", sorted(ilceler))
st.write(f"Seçilen Şehir: {secilen_sehir}")
st.write(f"Seçilen İlçe: {secilen_ilce}")




if st.button("Hava Durumunu Göster"):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={secilen_ilce},TR&appid={API_KEY}&lang=tr&units=metric"
    #url = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?q={secilen_ilce}&appid={API_KEY}&lang=tr&units=metric"

    try:
        response = requests.get(url)

        # openweather apinin döndürdüğü durum kodu 200-->OK
        if response.status_code==200:
            data = response.json()

            durum = data["weather"][0]["description"].title()
            derece = data["main"]["temp"]
            nem = data["main"]["humidity"]
            ruzgar = data["wind"]["speed"]
            basinc = data["main"]["pressure"]
            max_derece =data["main"]["temp_max"]
            min_derece =data["main"]["temp_min"]
            bulut = data["clouds"]["all"]
            parameter = data["weather"][0]["main"]

            lat = data["coord"]["lat"]  # Enlem
            lon = data["coord"]["lon"]  # Boylam


            m = folium.Map(location=[lat, lon], zoom_start=10)
            folium.Marker([lat, lon], popup=f"{secilen_ilce}, {secilen_sehir}").add_to(m)


            map_html = "map.html"
            m.save(map_html)
            with open(map_html,"r") as f:
                map_html = f.read()

            st.write(f"### {secilen_ilce} Harita")
            html(map_html, width=700, height=500)





            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

            st.subheader(f"{secilen_sehir},{secilen_ilce} Hava Durumu")

            col1, col2, col3, col4 = st.columns(4)


            with col1:
                st.image(icon_url, use_container_width=True)
                st.write(f"Durum: {durum}")

            with col2:
                st.write(f"Sıcaklık: {derece}°C")
                if derece<20:
                    cold_day_image_path = "weather/image/coldday2.jpg"
                    if os.path.exists(cold_day_image_path):
                        st.image(cold_day_image_path, caption="Soğuk", use_container_width=True)
                else:
                    hot_day_image_path = "weather/image/hotday.jpg"
                    if os.path.exists(hot_day_image_path):
                        st.image(hot_day_image_path, caption="Nem", use_container_width=True)
                st.write(f"Max Sıcaklık: {max_derece}°C")
                st.write(f"Min Sıcaklık: {min_derece}°C")
            with col3:
                st.write(f"Nem: {nem}%")
                nem_image_path = "weather/image/humidity.png"
                if os.path.exists(nem_image_path):
                    st.image(nem_image_path, caption="Nem", use_container_width=True)

                st.write(f"Rüzgar: {ruzgar} km/h")
                ruzgar_image_path = "weather/image/winf.jpg"
                if os.path.exists(ruzgar_image_path):
                    st.image(ruzgar_image_path, caption="Rüzgar", use_container_width=True)
                st.write(f"Basınç: {basinc} hPa")
                basinc_image_path = "weather/image/pressure.png"
                if os.path.exists(basinc_image_path):
                    st.image(basinc_image_path, caption="Basınç", use_container_width=True)
            with col4:
                st.write(f"Bulut Durumu: %{bulut}")
                st.write(f"Parametre: {parameter}")



        else:
            st.error("Hava Durumu verisi alınamadı. İlçe veya İl adı uyumsuz")

    except Exception as e:
        st.error(f"Hata{e}")



