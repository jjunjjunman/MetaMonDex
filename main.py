import streamlit as st
import requests

st.set_page_config(page_title="포켓몬 도감", page_icon="🔍")
st.title("🔍 포켓몬 도감")
st.write("포켓몬 이름을 선택하면 **이미지, 한글 이름, 타입, 키, 몸무게** 정보를 확인할 수 있어요!")

# 타입 아이콘 이미지 URL 포맷
TYPE_ICON_URL = "https://raw.githubusercontent.com/duiker101/pokemon-type-svg-icons/master/icons/{type}.svg"

@st.cache_data
def get_all_pokemon_names():
    """포켓몬 이름 리스트를 가져옵니다."""
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        names = [pokemon["name"] for pokemon in data["results"]]
        return sorted(names)
    else:
        return []

def get_korean_name(pokemon_name):
    """한글 이름을 가져옵니다."""
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for name_entry in data["names"]:
            if name_entry["language"]["name"] == "ko":
                return name_entry["name"]
    return pokemon_name.capitalize()

pokemon_names = get_all_pokemon_names()

selected_pokemon = st.selectbox("포켓몬을 선택하세요:", pokemon_names)

if selected_pokemon:
    poke_url = f"https://pokeapi.co/api/v2/pokemon/{selected_pokemon}"
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{selected_pokemon}"

    poke_response = requests.get(poke_url)
    species_response = requests.get(species_url)

    if poke_response.status_code == 200 and species_response.status_code == 200:
        data = poke_response.json()
        species_data = species_response.json()

        image_url = data["sprites"]["front_default"]
        height = data["height"] / 10  # m
        weight = data["weight"] / 10  # kg
        types = [t["type"]["name"] for t in data["types"]]
        type_icons = [TYPE_ICON_URL.format(type=type_) for type_ in types]

        korean_name = get_korean_name(selected_pokemon)

        # 표시
        st.subheader(f"📌 {korean_name} ({selected_pokemon.capitalize()})")
        st.image(image_url, caption=korean_name, width=200)

        st.markdown(f"**키:** {height} m")
        st.markdown(f"**몸무게:** {weight} kg")
        st.markdown("**타입:**")

        cols = st.columns(len(types))
        for idx, (type_name, icon_url) in enumerate(zip(types, type_icons)):
            with cols[idx]:
                st.image(icon_url, width=50)
                st.caption(type_name.capitalize())

    else:
        st.error("포켓몬 정보를 불러올 수 없습니다. 이름을 다시 확인해주세요.")
