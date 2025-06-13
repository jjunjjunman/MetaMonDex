import streamlit as st
import requests

# ----- 타입 한글 번역 -----
TYPE_TRANSLATIONS = {
    "Normal": "노말", "Fire": "불꽃", "Water": "물", "Electric": "전기",
    "Grass": "풀", "Ice": "얼음", "Fighting": "격투", "Poison": "독",
    "Ground": "땅", "Flying": "비행", "Psychic": "에스퍼", "Bug": "벌레",
    "Rock": "바위", "Ghost": "고스트", "Dragon": "드래곤", "Dark": "악",
    "Steel": "강철", "Fairy": "페어리"
}

# ----- 앱 설정 -----
st.set_page_config(page_title="MetaMonDex", page_icon="🟣", layout="centered")

# ----- 페이지 상태 초기화 -----
if "page" not in st.session_state:
    st.session_state.page = "search"
if "selected_pokemon_kor" not in st.session_state:
    st.session_state.selected_pokemon_kor = None

# ----- 포켓몬 이름 매핑 (한글 → 영어) -----
@st.cache_data
def get_korean_name_mapping():
    url = "https://pokeapi.co/api/v2/pokemon-species?limit=1000"
    response = requests.get(url)
    name_map = {}
    if response.status_code == 200:
        for species in response.json()["results"]:
            detail = requests.get(species["url"])
            if detail.status_code == 200:
                data = detail.json()
                for name_entry in data["names"]:
                    if name_entry["language"]["name"] == "ko":
                        name_map[name_entry["name"]] = data["name"]
                        break
    return dict(sorted(name_map.items()))

name_map = get_korean_name_mapping()

# ----- 검색 화면 -----
if st.session_state.page == "search":
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='https://assets.pokemon.com/assets/cms2/img/pokedex/full/132.png' width='300'/>
            <h1 style='color:#7b2cbf; font-family:sans-serif;'>MetaMonDex</h1>
            <p style='font-size:18px;'>한글로 포켓몬을 검색해보세요!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_kor_name = st.selectbox("🔍 포켓몬 이름 선택:", list(name_map.keys()))

    if st.button("검색"):
        st.session_state.selected_pokemon_kor = selected_kor_name
        st.session_state.page = "result"
        st.rerun()

# ----- 결과 화면 -----
elif st.session_state.page == "result":
    selected_kor_name = st.session_state.selected_pokemon_kor
    eng_name = name_map[selected_kor_name]
    api_url = f"https://pokeapi.co/api/v2/pokemon/{eng_name}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        image_url = data["sprites"]["front_default"]
        height = data["height"] / 10
        weight = data["weight"] / 10
        types_eng = [t["type"]["name"].capitalize() for t in data["types"]]
        types_kor = [TYPE_TRANSLATIONS.get(t, t) for t in types_eng]

        st.title(f"✨ {selected_kor_name}")
        st.image(image_url, caption=selected_kor_name, width=200)
        st.markdown(f"**🧬 타입:** {', '.join(types_kor)}")
        st.markdown(f"**📏 키:** {height} m")
        st.markdown(f"**⚖️ 몸무게:** {weight} kg")

        if st.button("🔙 돌아가기"):
            st.session_state.page = "search"
            st.rerun()
    else:
        st.error("포켓몬 정보를 불러오지 못했습니다.")
