# =========================================
# 🧠 SEO Meta Title & Description Generator
# Streamlit App (Free, No API Keys)
# =========================================

import streamlit as st
import pandas as pd
import random
import re
from io import BytesIO

# =========================================
# ⚙️ CONFIGURATION
# =========================================

TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 150, 160

st.set_page_config(page_title="Free SEO Meta Generator", page_icon="⚙️", layout="wide")
st.title("⚙️ SEO Meta Title & Description Generator (Free, No API)")
st.markdown("Generate meta titles (50–60 chars) and descriptions (150–160 chars) automatically — no API key required!")

# =========================================
# 🔍 INTENT DETECTION
# =========================================

def detect_intent(title, desc):
    text = f"{title} {desc}".lower()
    if re.search(r"\b(buy|shop|price|model|deal|feature|specs?)\b", text):
        return "product"
    elif re.search(r"\b(service|consult|solution|support|agency|expert)\b", text):
        return "service"
    elif re.search(r"\b(how to|guide|tips|news|insight|learn|blog)\b", text):
        return "blog"
    elif re.search(r"\b(collection|list|types?|best|compare|category)\b", text):
        return "category"
    else:
        return "generic"

# =========================================
# 🧠 META GENERATION
# =========================================

def truncate_to_range(text, min_len, max_len):
    text = text.strip()
    if len(text) > max_len:
        text = text[:max_len].rstrip(".!,;:- ") + "..."
    elif len(text) < min_len:
        text = (text + " " + text[:min_len])[:min_len]
    return text

def generate_title(intent, title1, primary_kw, secondary_kw):
    t = {
        "product": [
            f"Buy {title1} – {primary_kw} at Best Price",
            f"{title1} | {primary_kw} Features & Specs",
            f"{primary_kw}: {title1} for You"
        ],
        "service": [
            f"{title1} – Expert {primary_kw} Services",
            f"{primary_kw} Solutions | {title1}",
            f"Professional {primary_kw} by {title1}"
        ],
        "blog": [
            f"{title1} – {primary_kw} Guide & Tips",
            f"{primary_kw} Insights: {title1}",
            f"{title1} | Learn About {primary_kw}"
        ],
        "category": [
            f"Best {primary_kw} {title1} | Compare & Choose",
            f"{title1} – Top {primary_kw} Options",
            f"{primary_kw} {title1} Collection"
        ],
        "generic": [
            f"{title1} | {primary_kw}",
            f"Discover {title1} – {primary_kw}",
            f"{primary_kw} – {title1}"
        ]
    }
    title = random.choice(t.get(intent, t["generic"]))
    return truncate_to_range(title, TITLE_MIN, TITLE_MAX)

def generate_description(intent, title1, primary_kw, secondary_kw, tertiary_kw, existing_desc):
    d = {
        "product": [
            f"Buy {title1} with {primary_kw} features. Compare {secondary_kw} and {tertiary_kw} options to find the best deal today.",
            f"Explore {title1} – premium {primary_kw} with latest specs. Check {secondary_kw} & {tertiary_kw} for more details.",
        ],
        "service": [
            f"Get professional {primary_kw} with {title1}. We deliver {secondary_kw} and {tertiary_kw} solutions tailored to your needs.",
            f"{title1} offers reliable {primary_kw} services. Our team ensures quality {secondary_kw} & {tertiary_kw} support.",
        ],
        "blog": [
            f"Read {title1} to learn about {primary_kw}. Discover {secondary_kw} and {tertiary_kw} insights to boost your knowledge.",
            f"{title1} – a complete {primary_kw} guide covering {secondary_kw} and {tertiary_kw} tips you can use today.",
        ],
        "category": [
            f"Explore top {primary_kw} {title1}. Compare {secondary_kw} and {tertiary_kw} to choose the best fit for your needs.",
            f"Discover the latest {primary_kw} {title1}. Browse {secondary_kw} and {tertiary_kw} to make the right choice.",
        ],
        "generic": [
            f"{title1} – your trusted source for {primary_kw}. Explore {secondary_kw} and {tertiary_kw} today.",
            f"Find {primary_kw} information at {title1}. Learn about {secondary_kw} and {tertiary_kw}.",
        ]
    }
    desc = random.choice(d.get(intent, d["generic"]))
    return truncate_to_range(desc, DESC_MIN, DESC_MAX)

# =========================================
# 📂 FILE UPLOAD
# =========================================

uploaded = st.file_uploader("Upload your SEO data file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded:
    # Load file
    try:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    st.success(f"✅ File uploaded successfully! {len(df)} rows loaded.")
    st.dataframe(df.head())

    # Process button
    if st.button("🚀 Generate Meta Titles & Descriptions"):
        st.info("Generating meta titles and descriptions...")
        generated_titles, generated_descriptions, intents = set(), set(), [], []
        titles, descs = [], []

        for _, row in df.iterrows():
            title1 = str(row.get("Title 1", "")).strip()
            existing_desc = str(row.get("Existing Description", "")).strip()
            primary_kw = str(row.get("Primary KW", "")).strip()
            secondary_kw = str(row.get("Secondary KW", "")).strip()
            tertiary_kw = str(row.get("Tertiary KW", "")).strip()

            intent = detect_intent(title1, existing_desc)
            meta_title = generate_title(intent, title1, primary_kw, secondary_kw)
            while meta_title in generated_titles:
                meta_title = generate_title(intent, title1, primary_kw, secondary_kw)
            generated_titles.add(meta_title)

            meta_desc = generate_description(intent, title1, primary_kw, secondary_kw, tertiary_kw, existing_desc)
            while meta_desc in generated_descriptions:
                meta_desc = generate_description(intent, title1, primary_kw, secondary_kw, tertiary_kw, existing_desc)
            generated_descriptions.add(meta_desc)

            titles.append(meta_title)
            descs.append(meta_desc)
            intents.append(intent)

        df["Detected Intent"] = intents
        df["Generated Meta Title"] = titles
        df["Generated Meta Description"] = descs

        st.success("✅ Meta titles and descriptions generated successfully!")
        st.dataframe(df.head())

        # Download button
        towrite = BytesIO()
        df.to_excel(towrite, index=False)
        towrite.seek(0)

        st.download_button(
            label="📥 Download Enhanced Excel File",
            data=towrite,
            file_name="output_with_meta.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("👆 Upload your SEO CSV/Excel file to get started.")
