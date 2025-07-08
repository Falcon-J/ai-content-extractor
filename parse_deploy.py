import streamlit as st
import re
import json
from datetime import datetime

# Mock AI parser for deployment demo
class MockAIParser:
    def __init__(self):
        self.model_name = "gemma3"
    
    def parse_content(self, content, description):
        """Mock AI parsing - extracts basic patterns"""
        results = []
        
        # Simple pattern matching based on description
        if "email" in description.lower():
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
            results.extend(emails)
        
        if "phone" in description.lower():
            phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', content)
            results.extend(phones)
        
        if "price" in description.lower():
            prices = re.findall(r'\$[\d,]+\.?\d*', content)
            results.extend(prices)
        
        if "url" in description.lower() or "link" in description.lower():
            urls = re.findall(r'https?://[^\s]+', content)
            results.extend(urls)
        
        # Generic extraction - return first few lines that might be relevant
        if not results:
            lines = content.split('\n')
            relevant_lines = []
            keywords = description.lower().split()
            
            for line in lines:
                if any(keyword in line.lower() for keyword in keywords):
                    relevant_lines.append(line.strip())
                    if len(relevant_lines) >= 10:
                        break
            
            if relevant_lines:
                results = relevant_lines
            else:
                # Return first 10 non-empty lines as fallback
                results = [line.strip() for line in lines if line.strip()][:10]
        
        return '\n'.join(results) if results else "No matching content found"

# Initialize mock parser
mock_parser = MockAIParser()

def parse_with_ollama(dom_chunks, parse_description, progress_callback=None):
    """Mock version of parse_with_ollama for deployment"""
    
    # Show deployment notice
    st.info("""
    🚀 **Deployment Demo Mode**
    
    This is a demo version using pattern matching instead of AI. 
    For full AI capabilities, run locally with Ollama installed.
    
    **Current capabilities:**
    - Email extraction
    - Phone number extraction  
    - Price extraction
    - URL extraction
    - Basic keyword matching
    """)
    
    parsed_results = []
    total_chunks = len(dom_chunks)

    for i, chunk in enumerate(dom_chunks, start=1):
        if progress_callback:
            progress_callback(i, total_chunks)
        
        # Use mock parser instead of real AI
        result = mock_parser.parse_content(chunk, parse_description)
        parsed_results.append(result)

    return "\n".join(parsed_results)
