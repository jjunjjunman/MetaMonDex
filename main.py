import streamlit as st
import requests

st.set_page_config(page_title="MetaMonDex", page_icon="🧬")
st.title("🧬 MetaMonDex")
st.write("한글 또는 영어로 포켓몬 이름을 검색하세요!")

@st.cache_data
def get_korean_pokemon_name_map():
    url = "https://pokeapi.co/api/v2/pokemon-species?limit=1000"
    response = requests.get(url)
    name_map = {}
    
    if response.status_code == 200:
        results = response.json()["results"]
        for species in results:
            species_detail = requests.get(species["url"]).json()
            names = species_detail.get("names", [])
            eng_name = species_detail["name"]
            for name_entry in names:
                if name_entry["language"]["name"] == "ko":
                    kor_name = name_entry["name"]
                    name_map[kor_name] = eng_name
                    break
    return name_map

# 한국어 ↔ 영어 이름 맵
name_map = get_korean_pokemon_name_map()
korean_names = sorted(name_map.keys())

# 셀렉트박스에서 한글 이름 제공
selected_kor_name = st.selectbox("포켓몬을 선택하세요 (한글/영문):", korean_names)

if selected_kor_name:
    eng_name = name_map[selected_kor_name]
    api_url = f"https://pokeapi.co/api/v2/pokemon/{eng_name}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        height = data["height"] / 10  # dm -> m
        weight = data["weight"] / 10  # hg -> kg
        types = [t["type"]["name"].capitalize() for t in data["types"]]
        image_url = data["sprites"]["front_default"]

        st.subheader(f"📌 {selected_kor_name}")
        st.image(image_url, caption=selected_kor_name, width=200)

        st.markdown(f"**타입:** {', '.join(types)}")
        st.markdown(f"**키:** {height} m")
        st.markdown(f"**몸무게:** {weight} kg")
    else:
        st.error("포켓몬 정보를 불러올 수 없습니다.")
