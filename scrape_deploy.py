import requests
from bs4 import BeautifulSoup
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

# Fallback scraper for deployment (doesn't require Chrome)
def simple_scrape_website(website):
    """Simple scraper for deployment without Chrome dependencies"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(website, headers=headers, timeout=10)
        response.raise_for_status()
        
        return response.text
    except Exception as e:
        st.error(f"Error scraping {website}: {str(e)}")
        return None

def scrape_website(website):
    """Main scraper function - falls back to simple scraper for deployment"""
    # Check if we're in a deployment environment
    if os.getenv("STREAMLIT_CLOUD") or not os.path.exists("chromedriver.exe"):
        return simple_scrape_website(website)
    
    # Original Chrome-based scraper for local development
    try:
        from selenium.webdriver import Remote, ChromeOptions
        from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
        
        SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")
        
        if not SBR_WEBDRIVER:
            # Fall back to simple scraper if no Chrome service
            return simple_scrape_website(website)
        
        print("Connecting to Scraping Browser...")
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            driver.get(website)
            print("Waiting captcha to solve...")
            solve_res = driver.execute(
                "executeCdpCommand",
                {
                    "cmd": "Captcha.waitForSolve",
                    "params": {"detectTimeout": 10000},
                },
            )
            print("Captcha solve status:", solve_res["value"]["status"])
            print("Navigated! Scraping page content...")
            html = driver.page_source
            return html
    except ImportError:
        # Selenium not available, use simple scraper
        return simple_scrape_website(website)
    except Exception as e:
        print(f"Chrome scraper failed: {e}")
        return simple_scrape_website(website)


def extract_body_content(html_content):
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    if not body_content:
        return ""
    
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
