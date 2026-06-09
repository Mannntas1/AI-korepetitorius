import streamlit as st
from google import genai

st.set_page_config(
    page_title="Python pagalbininkas",
    layout="centered"
)

st.title("Python pagalbininkas")
st.write("Šita programa naudoja Gemini API ir padeda mokytis Python")

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Nerastas GEMINI_API_KEY. Įdėk API raktą į .streamlit/secrets.toml failą.")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.sidebar.header("Nustatymai")

kuo_padeti = st.sidebar.selectbox(
    "Pasirink dalyką",
    ["Paaiškinti", "Padėti", "Parodyti pavyzdį", "Kita"]
)

level = st.sidebar.selectbox(
    "Sudėtingumo lygis",
    ["Pradedantysis", "Vidutinis", "Pažengęs"]
)

tema = st.text_input("Ivesk temą")

extra_info = st.text_area("Papildoma informacija")

def create_prompt(kuo_padeti, level):
    prompt = f"""
        Tu esi draugiškas ir aiškiai kalbantis mokytojas.

        Pagalba: {kuo_padeti}
        Sunkumas: {level}
        tema: {tema}

        Papildoma informacija: {extra_info}

        Tavo atsakymo taisyklės:
        - Atsakyk lietuvių kalba.
        - Naudok aiškią struktūrą.
        - Jei tinka, pateik pavyzdžių.
        - Jei kuri testą, pateik klausimus ir atsakymus.
        - Neatsakinėk pernelyg ilgai, nebent vartotojas to prašo.
        - Neatsakyk į nesusijusius klausimus.
        """
    return prompt



if st.button("Generuoti atsakymą"):
    if not tema:
        st.warning("Pirma įvesk temą.")
    else:
        prompt = create_prompt(create_prompt, level)

        with st.spinner("Gemini generuoja atsakymą..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents = prompt
                )

                st.subheader("AI ATSAKYMAS:")
                st.write(response.text)

                with st.expander("Rodyti sugeneruotą promptą"):
                    st.code(prompt)

            except Exception as e:
                st.error("Įvyko klaida jungiantis prie Gemini API")
                st.exception(Exception)
