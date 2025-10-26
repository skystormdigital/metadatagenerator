import streamlit as st
import pandas as pd
from io import BytesIO

# =========================================
# CONFIGURATION
# =========================================
TITLE_MIN, TITLE_MAX = 50, 60
DESC_MIN, DESC_MAX = 150, 160

st.set_page_config(page_title="SEO Meta Generator", page_icon="⚙️", layout="wide")
st.title("⚙️ Professional SEO Meta Generator with Tone Selection")
st.markdown(
    """
Generate professional **meta titles** (50–60 chars) and **meta descriptions** (150–160 chars)  
that are complete sentences and **adapt to your chosen tone**. No API key required.
"""
)

# =========================================
# TONE SELECTION
# =========================================
tone = st.selectbox(
    "Select Tone for Meta Data",
    options=["Professional", "Friendly", "Persuasive", "Educational"]
)

# =========================================
# INTENT DETECTION
# =========================================
def detect_intent(title, desc):
    text = f"{title} {desc}".lower()
    if any(k in text for k in ["buy","shop","price","model","deal","feature","specs"]):
        return "product"
    elif any(k in text for k in ["service","consult","solution","support","agency","expert"]):
        return "service"
    elif any(k in text for k in ["how to","guide","tips","news","insight","learn","blog"]):
        return "blog"
    elif any(k in text for k in ["collection","list","type","best","compare","category"]):
        return "category"
    else:
        return "generic"

# =========================================
# TONE-BASED CONNECTORS
# =========================================
def tone_connectors(tone):
    if tone == "Professional":
        return {"start": "Discover", "join": "|", "suffix": "Learn More"}
    elif tone == "Friendly":
        return {"start": "Check out", "join": "-", "suffix": "Find out more!"}
    elif tone == "Persuasive":
        return {"start": "Get", "join": "|", "suffix": "Act Now!"}
    elif tone == "Educational":
        return {"start": "Learn about", "join": "-", "suffix": "Detailed Insights"}
    else:
        return {"start": "Discover", "join": "|", "suffix": "Learn More"}

# =========================================
# COMPLETE TITLE GENERATION
# =========================================
def generate_title_with_tone(title1, primary_kw, secondary_kw, tone):
    connectors = tone_connectors(tone)
    pieces = [f"{connectors['start']} {title1}", primary_kw, secondary_kw]
    title = ""
    for p in pieces:
        if not p:
            continue
        if len(title + " " + p) <= TITLE_MAX:
            title = (title + " " + p).strip()
        else:
            break
    # Ensure minimum length
    while len(title) < TITLE_MIN:
        suffix = f" {connectors['suffix']}"
        if len(title + suffix) <= TITLE_MAX:
            title += suffix
        else:
            break
    return title

# =========================================
# COMPLETE DESCRIPTION GENERATION
# =========================================
def generate_description_with_tone(title1, primary_kw, secondary_kw, tertiary_kw, tone):
    connectors = tone_connectors(tone)
    base = f"{title1} provides comprehensive information about {primary_kw}"
    extras = ""
    if secondary_kw:
        extras += f", including {secondary_kw}"
    if tertiary_kw:
        extras += f" and {tertiary_kw}"
    extras += f". {connectors['suffix']}."
    desc = f"{connectors['start']} {base}{extras}"
    # Ensure min length
    while len(desc) < DESC_MIN:
        extra_suffix = " More details available."
        if len(desc + extra_suffix) <= DESC_MAX:
            desc += extra_suffix
        else:
            break
    # Final safety cut
    if len(desc) > DESC_MAX:
        desc = desc[:DESC_MAX].rstrip()
    return desc

# =========================================
# FILE UPLOAD
# =========================================
uploaded = st.file_uploader("Upload your SEO CSV/Excel file", type=["csv","xlsx"])

if uploaded:
    try:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.success(f"Loaded {len(df)} rows successfully!")
    st.dataframe(df.head())

    if st.button("Generate Meta Titles & Descriptions"):
        generated_titles, generated_descriptions, intents = [], [], []

        for _, row in df.iterrows():
            title1 = str(row.get("Title 1","")).strip()
            existing_desc = str(row.get("Existing Description","")).strip()
            primary_kw = str(row.get("Primary KW","")).strip()
            secondary_kw = str(row.get("Secondary KW","")).strip()
            tertiary_kw = str(row.get("Tertiary KW","")).strip()

            intent = detect_intent(title1, existing_desc)

            meta_title = generate_title_with_tone(title1, primary_kw, secondary_kw, tone)
            meta_desc = generate_description_with_tone(title1, primary_kw, secondary_kw, tertiary_kw, tone)

            generated_titles.append(meta_title)
            generated_descriptions.append(meta_desc)
            intents.append(intent)

        df["Detected Intent"] = intents
        df["Generated Meta Title"] = generated_titles
        df["Generated Meta Description"] = generated_descriptions
        df["Title Char Count"] = df["Generated Meta Title"].apply(len)
        df["Description Char Count"] = df["Generated Meta Description"].apply(len)

        # Color-coded preview
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
        ]].style.applymap(lambda v: color_len(v, TITLE_MIN, TITLE_MAX) if isinstance(v,int) else "", subset=["Title Char Count"]) \
         .applymap(lambda v: color_len(v, DESC_MIN, DESC_MAX) if isinstance(v,int) else "", subset=["Description Char Count"])

        st.success("✅ Meta data generated successfully!")
        st.markdown("### Preview (color-coded by length)")
        st.dataframe(styled, use_container_width=True)

        # Download button
        towrite = BytesIO()
        df.to_excel(towrite, index=False)
        towrite.seek(0)
        st.download_button(
            label="Download Enhanced Excel File",
            data=towrite,
            file_name="seo_meta_output_with_tone.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Upload your SEO CSV or Excel file to get started.")
