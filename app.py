# -*- coding: utf-8 -*-
import streamlit as st
import openai
from fpdf import FPDF
import base64

openai.api_key = "DEIN_API_KEY"

st.title("🛠️ SHK.AI Assist – Angebotsgenerator")

kundenanfrage = st.text_area("Kundentext eingeben:", "Badrenovierung 9 m², WC, Dusche, anthrazit")

if st.button("Angebot generieren"):
    prompt = f"Erstelle einen professionellen Angebotstext und eine Materialliste für folgende Anfrage: {kundenanfrage}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    ergebnis = response.choices[0].message["content"]
    st.text_area("Angebot:", ergebnis, height=300)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in ergebnis.split("\\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output("angebot.pdf")

    with open("angebot.pdf", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="angebot.pdf">📄 PDF herunterladen</a>'
        st.markdown(href, unsafe_allow_html=True)
