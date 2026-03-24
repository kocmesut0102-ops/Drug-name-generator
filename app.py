import streamlit as st
import random
import pandas as pd
from Levenshtein import distance

# Hece havuzu
syllables = ["va","vi","vo","ta","to","na","ne","mi","co","zol","tin","ra","lo","fi"]

# İsim üretme fonksiyonu
def generate_name():
    return (
        random.choice(syllables) +
        random.choice(syllables) +
        random.choice(syllables)
    ).upper()

# Basit benzerlik skoru
def similarity_score(name, existing_names):
    if not existing_names:
        return 0
    scores = [distance(name, ex) for ex in existing_names]
    return min(scores)

# Skor hesaplama
def calculate_score(name, existing_names):
    reg = random.randint(70, 95)
    sim = 100 - similarity_score(name, existing_names)*5
    fon = random.randint(70, 95)
    klinik = random.randint(70, 95)
    marka = random.randint(70, 95)

    total = 0.3*reg + 0.3*sim + 0.15*fon + 0.15*klinik + 0.1*marka
    return round(total,1), reg, sim, fon, klinik, marka

# UI
st.title("💊 Drug Name Generator")

etken = st.text_input("Etkin Madde(ler)")
atc = st.text_input("ATC Kodu")
endikasyon = st.text_input("Endikasyon")
form = st.text_input("Form")
doz = st.text_input("Doz")

existing = st.text_area("Mevcut İsimler (virgülle ayır)")

if st.button("İSİM ÜRET 🚀"):

    existing_list = [x.strip().upper() for x in existing.split(",") if x]

    results = []

    for _ in range(50):
        name = generate_name()
        score, reg, sim, fon, klinik, marka = calculate_score(name, existing_list)

        results.append({
            "İsim": name,
            "Skor": score,
            "Regülasyon": reg,
            "Benzerlik": sim,
            "Fonetik": fon,
            "Klinik": klinik,
            "Marka": marka
        })

    df = pd.DataFrame(results)
    df = df.sort_values(by="Skor", ascending=False)

    st.subheader("🎯 En İyi Öneriler")
    st.dataframe(df.head(10))
