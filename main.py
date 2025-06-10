import streamlit as st
import requests

st.title("MetaMonDex")

# 사용자로부터 포켓몬 이름 입력 받기
pokemon_name = st.text_input("포켓몬 이름을 입력하세요 (예: pikachu, ditto 등):").strip().lower()

if pokemon_name:
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        image_url = data["sprites"]["front_default"]
        
        st.success(f"{pokemon_name.capitalize()}의 이미지입니다:")
        st.image(image_url, caption=pokemon_name.capitalize())
    else:
        st.error("포켓몬을 찾을 수 없습니다. 이름을 다시 확인해주세요.")
