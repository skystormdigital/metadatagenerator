# =========================================
# ⚙️ SEO Meta Title & Description Generator
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

st.set_page_config(page_title="SEO Meta Generator", page_icon="⚙️", layout="wide")
st.title("⚙️ SEO Meta Title & Description Generator (Professional, No API)")
st.markdown(
    """
This free tool creates **professional**, **complete** SEO meta titles (50–60 chars)  
and descriptions (150–160 chars) based on your uploaded data — no API key required.
"""
)

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
# ✍️ NATURAL TEMPLATE-BASED GENERATION
# =========================================

def within_range(text, min_len, max_len):
    return min_len <= len(text) <= max_len

def generate_title(intent, title1, primary_kw, secondary_kw):
    templates = {
        "product": [
            f"Buy {title1} | {primary_kw} Details & Pricing",
            f"{primary_kw} – {title1} with Latest Features",
            f"{title1}: Premium {primary_kw} for Every Need",
            f"{title1} – Explore Top {primary_kw} Options"
        ],
        "service": [
            f"{title1} | Professional {primary_kw} Services",
            f"Trusted {primary_kw} Solutions – {title1}",
            f"{title1} – Expert {primary_kw} Support",
            f"Reliable {primary_kw} & {secondary_kw} by {title1}"
        ],
        "blog": [
            f"{title1} – {primary_kw} Insights & Expert Tips",
            f"{primary_kw} Guide: {title1}",
            f"Learn {primary_kw} Strategies with {title1}",
            f"{title1}: Explore {primary_kw} & {secondary_kw}"
        ],
        "category": [
            f"Best {primary_kw} {title1} – Compare Top Choices",
            f"{title1}: Explore Leading {primary_kw} Options",
            f"Top {primary_kw} {title1} for Smart Selection",
            f"{primary_kw} {title1} | Discover What Fits You"
        ],
        "generic": [
            f"{title1} | {primary_kw} Insights & Information",
            f"Discover {primary_kw} at {title1}",
            f"{primary_kw} – Learn More with {title1}",
            f"{title1}: Everything About {primary_kw}"
        ],
    }

    for _ in range(10):  # try multiple templates until one fits range
        title = random.choice(templates.get(intent, templates["generic"]))
        if within_range(title, TITLE_MIN, TITLE_MAX):
            return title
    return random.choice(templates.get(intent, templates["generic"]))[:TITLE_MAX]

def generate_description(intent, title1, primary_kw, secondary_kw, tertiary_kw, existing_desc):
    templates = {
        "product": [
            f"Discover {title1}, a premium {primary_kw} offering the best in performance and value. Compare {secondary_kw} and {tertiary_kw} to find your perfect match today.",
            f"Explore {title1}, designed for those who want the finest {primary_kw}. Compare {secondary_kw} and {tertiary_kw} for a smarter buying choice."
        ],
        "service": [
            f"At {title1}, we provide professional {primary_kw} services that deliver real results. Our experts offer tailored {secondary_kw} and {tertiary_kw} solutions for every client.",
            f"Experience reliable {primary_kw} solutions from {title1}. We help you with {secondary_kw} and {tertiary_kw} support designed for lasting success."
        ],
        "blog": [
            f"Read {title1} to explore expert insights on {primary_kw}. Learn about {secondary_kw} and {tertiary_kw} strategies to stay informed and ahead of the competition.",
            f"{title1} covers essential {primary_kw} knowledge with practical {secondary_kw} and {tertiary_kw} tips for professionals and learners alike."
        ],
        "category": [
            f"Browse the best {primary_kw} in {title1}. Compare {secondary_kw} and {tertiary_kw} options to find products that meet your exact requirements with ease.",
            f"Explore {title1} – a curated range of {primary_kw}. Compare {secondary_kw} and {tertiary_kw} to discover the right fit for your needs."
        ],
        "generic": [
            f"{title1} provides detailed information about {primary_kw}. Explore {secondary_kw} and {tertiary_kw} insights that help you make smarter decisions.",
            f"Learn everything about {primary_kw} with {title1}. Discover {secondary_kw} and {tertiary_kw} to expand your knowledge today."
        ],
    }

    for _ in range(10):
        desc = random.choice(templates.get(intent, templates["generic"]))
        if within_range(desc, DESC_MIN, DESC_MAX):
            return desc
    return random.choice(templates.get(intent, templates["generic"]))[:DESC_MAX]

# =========================================
# 📂 FILE UPLOAD + PROCESSING
# =========================================

uploaded = st.file_uploader("📤 Upload your SEO data file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded:
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

    if st.button("🚀 Generate Professional Meta Data"):
        st.info("Generating professional meta titles and descriptions...")

        generated_titles, generated_descriptions, intents, titles, descs = set(), set(), [], [], []

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
        df["Title Char Count"] = df["Generated Meta Title"].apply(len)
        df["Description Char Count"] = df["Generated Meta Description"].apply(len)

        # Highlight by length compliance
        def color_len(val, min_len, max_len):
            if val < min_len:
                return "background-color: #fff3cd"  # yellow
            elif val > max_len:
                return "background-color: #f8d7da"  # red
            else:
                return "background-color: #d4edda"  # green

        styled = df[[
            "Detected Intent",
            "Generated Meta Title",
            "Title Char Count",
            "Generated Meta Description",
            "Description Char Count"
        ]].style.applymap(lambda v: color_len(v, TITLE_MIN, TITLE_MAX) if isinstance(v, int) else "", subset=["Title Char Count"]) \
         .applymap(lambda v: color_len(v, DESC_MIN, DESC_MAX) if isinstance(v, int) else "", subset=["Description Char Count"])

        st.success("✅ Meta titles and descriptions generated successfully!")
        st.markdown("### 🔍 Preview (Color-coded by Length)")
        st.dataframe(styled, use_container_width=True)

        # Download output
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
