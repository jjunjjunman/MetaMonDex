import streamlit as st
import requests

# 앱 제목 및 스타일 설정
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

# 제목
st.title("🟣 MetaMonDex")
st.write("귀여운 메타몽 스타일의 포켓몬 검색 도감이에요!")

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

# 검색 선택
st.subheader("🔍 포켓몬을 찾아볼까요?")
selected_pokemon = st.selectbox("포켓몬 이름을 선택하세요:", pokemon_names)

# 결과 표시
if selected_pokemon:
    api_url = f"https://pokeapi.co/api/v2/pokemon/{selected_pokemon}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        name = data["name"].capitalize()
        height = data["height"] / 10
        weight = data["weight"] / 10
        types = [t["type"]["name"].capitalize() for t in data["types"]]
        image_url = data["sprites"]["front_default"]

        st.markdown("---")
        st.header(f"✨ {name}")
        st.image(image_url, caption=name, width=200)

        st.markdown(f"**🌈 타입:** {', '.join(types)}")
        st.markdown(f"**📏 키:** {height} m")
        st.markdown(f"**⚖️ 몸무게:** {weight} kg")
    else:
        st.error("포켓몬 정보를 불러올 수 없습니다. 다시 시도해주세요.")
