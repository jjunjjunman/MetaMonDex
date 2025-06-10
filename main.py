import streamlit as st
import requests

st.title("🔎 포켓몬 도감 웹앱")
st.write("포켓몬 이름을 선택하면 이미지와 정보를 확인할 수 있어요!")

@st.cache_data
def get_all_pokemon_names():
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        names = [pokemon["name"] for pokemon in data["results"]]
        return sorted(names)
    else:
        return []

pokemon_names = get_all_pokemon_names()

# 자동완성 셀렉트박스
selected_pokemon = st.selectbox("포켓몬을 선택하세요:", pokemon_names)

if selected_pokemon:
    api_url = f"https://pokeapi.co/api/v2/pokemon/{selected_pokemon}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        name = data["name"].capitalize()
        height = data["height"] / 10  # decimeters -> meters
        weight = data["weight"] / 10  # hectograms -> kilograms
        types = [t["type"]["name"].capitalize() for t in data["types"]]
        image_url = data["sprites"]["front_default"]

        st.subheader(f"📌 {name}")
        st.image(image_url, caption=name, width=200)

        st.markdown(f"**타입:** {', '.join(types)}")
        st.markdown(f"**키:** {height} m")
        st.markdown(f"**몸무게:** {weight} kg")
    else:
        st.error("포켓몬 정보를 불러올 수 없습니다.")
