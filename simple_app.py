import streamlit as st
import requests
import os
from bs4 import BeautifulSoup
import time
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple web scraper
def scrape_website(url):
    """Simple web scraper"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Clean HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        st.error(f"Error scraping: {str(e)}")
        return None

# AI extractor using Groq
def extract_with_ai(content, task):
    """Extract information using Groq AI"""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("Please add GROQ_API_KEY to your .env file")
        return None
    
    try:
        import requests
        
        # Limit content size to avoid API limits
        if len(content) > 8000:
            content = content[:8000] + "..."
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
Extract and organize the following information from this web content:

TASK: {task}

CONTENT:
{content}

Please provide a clean, organized list of the extracted information:
"""
        
        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that extracts specific information from web content. Provide clear, organized results."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"AI extraction error: {str(e)}")
        return None

# Streamlit App
st.set_page_config(page_title="AI Data Extractor", page_icon="🤖", layout="wide")

st.title("🤖 AI Data Extractor")
st.markdown("**Scrape website data → Extract with AI → Get organized results**")

# Check if Groq API key is configured
if not os.getenv("GROQ_API_KEY"):
    st.warning("⚠️ **Setup Required**: Add your Groq API key to the .env file")
    st.info("""
    1. Get free API key: https://console.groq.com/keys
    2. Add to .env file: `GROQ_API_KEY=your_key_here`
    3. Restart the app
    """)

# Step 1: Scrape Data
st.subheader("📊 Step 1: Scrape Website Data")

url = st.text_input(
    "Website URL", 
    placeholder="https://example.com",
    help="Enter the website you want to extract data from"
)

if st.button("🌐 Scrape Website", type="primary"):
    if url:
        with st.spinner("Scraping website..."):
            scraped_content = scrape_website(url)
            
            if scraped_content:
                st.session_state.scraped_content = scraped_content
                st.session_state.source_url = url
                st.success(f"✅ Scraped {len(scraped_content):,} characters")
                
                with st.expander("Preview scraped content"):
                    st.text_area("Content Preview", scraped_content[:1000] + "...", height=200, disabled=True)
    else:
        st.error("Please enter a URL")

# Step 2: Extract with AI
if "scraped_content" in st.session_state:
    st.divider()
    st.subheader("🤖 Step 2: Extract Information with AI")
    
    task = st.text_area(
        "What do you want to extract?",
        placeholder="Examples:\n- Extract all contact information (emails, phones, names)\n- Find all product names and prices\n- Get all job titles and companies\n- Extract event dates and locations",
        height=100
    )
    
    if st.button("🚀 Extract with AI", type="primary"):
        if task:
            with st.spinner("AI is extracting information..."):
                extracted_data = extract_with_ai(st.session_state.scraped_content, task)
                
                if extracted_data:
                    st.session_state.extracted_data = extracted_data
                    st.success("✅ Information extracted successfully!")
                    
                    # Display results
                    st.subheader("📋 Extracted Results")
                    st.text_area("Results", extracted_data, height=300)
                    
                    # Download options
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            "📄 Download as TXT",
                            extracted_data,
                            f"extracted_data_{int(time.time())}.txt",
                            "text/plain"
                        )
                    
                    with col2:
                        # Convert to CSV format
                        lines = [line.strip() for line in extracted_data.split('\n') if line.strip()]
                        df = pd.DataFrame(lines, columns=['Extracted_Data'])
                        csv = df.to_csv(index=False)
                        
                        st.download_button(
                            "📊 Download as CSV",
                            csv,
                            f"extracted_data_{int(time.time())}.csv",
                            "text/csv"
                        )
                    
                    with col3:
                        # Save as JSON
                        import json
                        json_data = {
                            "source_url": st.session_state.source_url,
                            "extraction_task": task,
                            "extracted_data": lines,
                            "timestamp": time.time()
                        }
                        
                        st.download_button(
                            "📋 Download as JSON",
                            json.dumps(json_data, indent=2),
                            f"extracted_data_{int(time.time())}.json",
                            "application/json"
                        )

        else:
            st.error("Please describe what you want to extract")

# Footer
st.divider()
st.markdown("*Simple AI-powered data extraction from websites*")
