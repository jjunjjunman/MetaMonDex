import streamlit as st
import requests

# ---------------------- 설정 ----------------------
st.set_page_config(page_title="MetaMonDex", page_icon="🟣", layout="centered")

# 사용자 정의 CSS (메타몽 테마)
st.markdown("""
    <style>
    body {
        background-color: #f3e8fc;
    }
    .stApp {
        background-color: #f3e8fc;
    }
    h1, h2, h3 {
        color: #7b2cbf;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- 언어 설정 ----------------------
language = st.radio("🌐 언어 / Language", ["한국어", "English"], horizontal=True)

lang_ko = language == "한국어"

# ---------------------- 메타몽 GIF ----------------------
st.image("https://media.pokemoncentral.it/wiki/thumb/1/14/Sprnb132.gif/132px-Sprnb132.gif",
         caption="귀여운 메타몽이 당신을 기다려요!" if lang_ko else "Ditto is here to help you!",
         use_column_width=False, width=150)

# ---------------------- 제목 ----------------------
st.title("🟣 MetaMonDex")
st.write("포켓몬을 검색하고 정보를 확인하세요!" if lang_ko else "Search and explore Pokémon data!")

# ---------------------- 포켓몬 이름 가져오기 ----------------------
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

# ---------------------- 타입 한글 매핑 ----------------------
type_translations = {
    "normal": "노말", "fire": "불꽃", "water": "물", "electric": "전기", "grass": "풀", "ice": "얼음",
    "fighting": "격투", "poison": "독", "ground": "땅", "flying": "비행", "psychic": "에스퍼",
    "bug": "벌레", "rock": "바위", "ghost": "고스트", "dragon": "드래곤", "dark": "악",
    "steel": "강철", "fairy": "페어리"
}

def translate_type(type_name):
    return type_translations.get(type_name.lower(), type_name.capitalize())

# ---------------------- 포켓몬 선택 ----------------------
pokemon_names = get_all_pokemon_names()
st.subheader("🔍 포켓몬을 선택하세요!" if lang_ko else "🔍 Choose a Pokémon")
selected_pokemon = st.selectbox("포켓몬 이름 (영어로):", pokemon_names)

# ---------------------- 결과 출력 ----------------------
if selected_pokemon:
    api_url = f"https://pokeapi.co/api/v2/pokemon/{selected_pokemon}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        name = data["name"].capitalize()
        height = data["height"] / 10
        weight = data["weight"] / 10
        types = [t["type"]["name"] for t in data["types"]]
        image_url = data["sprites"]["front_default"]

        type_display = ", ".join(
            [translate_type(t) if lang_ko else t.capitalize() for t in types]
        )

        st.markdown("---")
        st.header(f"✨ {name}")
        st.image(image_url, caption=name, width=200)

        if lang_ko:
            st.markdown(f"**🌈 타입:** {type_display}")
            st.markdown(f"**📏 키:** {height} m")
            st.markdown(f"**⚖️ 몸무게:** {weight} kg")
        else:
            st.markdown(f"**🌈 Type:** {type_display}")
            st.markdown(f"**📏 Height:** {height} m")
            st.markdown(f"**⚖️ Weight:** {weight} kg")
    else:
        st.error("포켓몬 정보를 불러올 수 없습니다." if lang_ko else "Could not fetch Pokémon data.")
