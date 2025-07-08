import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("🧪 AI Web Scraper - Status Check")

# Check environment
st.subheader("📋 Environment Status")

# Check API key
api_key = os.getenv("GROQ_API_KEY")
if api_key:
    st.success(f"✅ Groq API key configured: {api_key[:10]}...")
else:
    st.error("❌ Groq API key not found in .env file")

# Check packages
st.subheader("📦 Package Status")

packages = [
    ("streamlit", "Streamlit"),
    ("requests", "Requests"),
    ("bs4", "BeautifulSoup"),
    ("pandas", "Pandas"),
    ("dotenv", "Python-dotenv"),
    ("openpyxl", "OpenPyXL")
]

all_good = True
for module, name in packages:
    try:
        __import__(module)
        st.success(f"✅ {name} installed")
    except ImportError:
        st.error(f"❌ {name} missing")
        all_good = False

if all_good:
    st.success("🎉 All packages are installed correctly!")
    st.info("👍 Your AI Web Scraper is ready to use!")
    st.markdown("### 🚀 Next Steps:")
    st.markdown("1. Run `streamlit run simple_app.py` to start the main app")
    st.markdown("2. Enter a website URL and start extracting data!")
else:
    st.error("⚠️ Some packages are missing. Please install them first.")
