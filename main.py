import streamlit as st
import requests

# 설정: 앱 제목, 아이콘을 메타몽으로!
st.set_page_config(
    page_title="MetaMonDex",
    page_icon="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png",
    layout="centered"
)

# 메타몽 스타일 CSS
st.markdown("""
    <style>
    body { background-color: #f3e8fc; }
    .stApp { background-color: #f3e8fc; }
    h1, h2, h3 { color: #7b2cbf; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# 상단에 메타몽 이미지 추가
st.image("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png", width=100)
st.title("MetaMonDex")
st.write("간편하게 한글로 검색하는 귀여운 메타몽 포켓몬 도감!")

# 한글-영문 이름 매핑
@st.cache_data
def get_korean_name_mapping():
    species_url = "https://pokeapi.co/api/v2/pokemon-species?limit=1000"
    response = requests.get(species_url)
    name_map = {}
    
    if response.status_code == 200:
        species_list = response.json()["results"]
        for species in species_list:
            species_detail = requests.get(species["url"])
            if species_detail.status_code == 200:
                data = species_detail.json()
                for name_entry in data["names"]:
                    if name_entry["language"]["name"] == "ko":
                        name_map[name_entry["name"]] = data["name"]
                        break
    return dict(sorted(name_map.items()))

name_map = get_korean_name_mapping()
korean_names = list(name_map.keys())

st.subheader("🔍 포켓몬을 한글로 검색해보세요!")
selected_kor_name = st.selectbox("포켓몬 이름 (한글):", korean_names)

if selected_kor_name:
    eng_name = name_map[selected_kor_name]
    api_url = f"https://pokeapi.co/api/v2/pokemon/{eng_name}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        name = selected_kor_name
        height = data["height"] / 10
        weight = data["weight"] / 10
        types = [t["type"]["name"].capitalize() for t in data["types"]]
        image_url = data["sprites"]["front_default"]

        st.markdown("---")
        st.header(f"✨ {name} ✨")
        st.image(image_url, caption=name, width=200)

        st.markdown(f"**🧬 타입:** {', '.join(types)}")
        st.markdown(f"**📏 키:** {height} m")
        st.markdown(f"**⚖️ 몸무게:** {weight} kg")
    else:
        st.error("포켓몬 정보를 불러올 수 없습니다.")
