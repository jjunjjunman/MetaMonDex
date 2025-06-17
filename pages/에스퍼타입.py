import streamlit as st
import requests

st.title("🔮 에스퍼타입 포켓몬 목록")

# 에스퍼타입의 ID는 14번
type_url = "https://pokeapi.co/api/v2/type/psychic"
response = requests.get(type_url)

if response.status_code == 200:
    data = response.json()
    psychic_pokemons = data['pokemon']

    for p in psychic_pokemons:
        name = p['pokemon']['name']
        pokemon_url = p['pokemon']['url']

        # 포켓몬 상세 정보 가져오기
        poke_response = requests.get(pokemon_url)
        if poke_response.status_code == 200:
            poke_data = poke_response.json()
            sprite_url = poke_data['sprites']['front_default']

            # 포켓몬 이름 및 이미지 표시
            st.subheader(name.capitalize())
            if sprite_url:
                st.image(sprite_url, width=120)
            else:
                st.write("이미지를 찾을 수 없음")
        else:
            st.write(f"{name} 정보를 불러오지 못했습니다.")
else:
    st.error("포켓몬 타입 정보를 불러오지 못했습니다.")
