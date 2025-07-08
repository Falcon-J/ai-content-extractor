import json
import csv
import io
import pandas as pd
from datetime import datetime
import re

def structure_data(raw_data, data_type="general"):
    """Convert raw extracted data into structured format"""
    structured_data = []
    
    if data_type == "contacts":
        # Extract contact information
        lines = raw_data.split('\n')
        for line in lines:
            if line.strip():
                contact = {}
                # Extract email
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
                if email_match:
                    contact['email'] = email_match.group()
                
                # Extract phone
                phone_match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', line)
                if phone_match:
                    contact['phone'] = phone_match.group()
                
                # Extract name (simple heuristic)
                words = line.split()
                if len(words) >= 2:
                    contact['name'] = ' '.join(words[:2])
                
                if contact:
                    structured_data.append(contact)
    
    elif data_type == "products":
        # Extract product information
        lines = raw_data.split('\n')
        for line in lines:
            if line.strip():
                product = {}
                # Extract price
                price_match = re.search(r'\$[\d,]+\.?\d*', line)
                if price_match:
                    product['price'] = price_match.group()
                
                # Extract product name (everything before price)
                if price_match:
                    product['name'] = line[:price_match.start()].strip()
                else:
                    product['name'] = line.strip()
                
                if product:
                    structured_data.append(product)
    
    elif data_type == "jobs":
        # Extract job information
        lines = raw_data.split('\n')
        for line in lines:
            if line.strip():
                job = {}
                # Simple parsing - can be enhanced
                parts = line.split(' - ')
                if len(parts) >= 2:
                    job['title'] = parts[0].strip()
                    job['company'] = parts[1].strip()
                    if len(parts) >= 3:
                        job['location'] = parts[2].strip()
                
                if job:
                    structured_data.append(job)
    
    else:
        # General structure - split by lines
        lines = raw_data.split('\n')
        for line in lines:
            if line.strip():
                structured_data.append({'data': line.strip()})
    
    return structured_data

def validate_extraction(data, expected_format="general"):
    """Validate extracted data quality"""
    if not data:
        return 0.0, ["No data extracted"]
    
    lines = data.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    
    if len(non_empty_lines) == 0:
        return 0.0, ["No meaningful data found"]
    
    quality_score = 0.0
    suggestions = []
    
    # Basic quality checks
    if len(non_empty_lines) > 0:
        quality_score += 0.3  # Data exists
    
    if len(non_empty_lines) > 5:
        quality_score += 0.2  # Sufficient quantity
    
    # Format-specific validation
    if expected_format == "contacts":
        email_count = len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', data))
        phone_count = len(re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', data))
        
        if email_count > 0:
            quality_score += 0.25
        else:
            suggestions.append("No email addresses found")
        
        if phone_count > 0:
            quality_score += 0.25
        else:
            suggestions.append("No phone numbers found")
    
    elif expected_format == "products":
        price_count = len(re.findall(r'\$[\d,]+\.?\d*', data))
        if price_count > 0:
            quality_score += 0.5
        else:
            suggestions.append("No prices found")
    
    else:
        # General validation
        avg_line_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
        if avg_line_length > 10:
            quality_score += 0.5
        else:
            suggestions.append("Content seems too brief")
    
    quality_score = min(quality_score, 1.0)
    
    if quality_score < 0.5:
        suggestions.append("Try being more specific in your extraction query")
    
    return quality_score, suggestions

def convert_to_csv(data, data_type="general"):
    """Convert structured data to CSV format"""
    structured_data = structure_data(data, data_type)
    
    if not structured_data:
        return "No data to convert"
    
    output = io.StringIO()
    
    if structured_data:
        # Get all unique keys
        all_keys = set()
        for item in structured_data:
            all_keys.update(item.keys())
        
        writer = csv.DictWriter(output, fieldnames=list(all_keys))
        writer.writeheader()
        writer.writerows(structured_data)
    
    return output.getvalue()

def convert_to_json(data, data_type="general"):
    """Convert structured data to JSON format"""
    structured_data = structure_data(data, data_type)
    
    return json.dumps({
        "extraction_date": datetime.now().isoformat(),
        "data_type": data_type,
        "total_items": len(structured_data),
        "data": structured_data
    }, indent=2)

def convert_to_excel(data, data_type="general"):
    """Convert structured data to Excel format"""
    structured_data = structure_data(data, data_type)
    
    if not structured_data:
        return None
    
    df = pd.DataFrame(structured_data)
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Extracted Data', index=False)
    
    return output.getvalue()

# Extraction templates
EXTRACTION_TEMPLATES = {
    "lead_generation": {
        "description": "Extract contact information including names, emails, phone numbers, and company names",
        "fields": ["name", "email", "phone", "company"],
        "data_type": "contacts"
    },
    "product_catalog": {
        "description": "Extract product information including names, prices, descriptions, and URLs",
        "fields": ["name", "price", "description", "url"],
        "data_type": "products"
    },
    "job_listings": {
        "description": "Extract job information including titles, companies, locations, and salary ranges",
        "fields": ["title", "company", "location", "salary"],
        "data_type": "jobs"
    },
    "news_articles": {
        "description": "Extract article headlines, publication dates, authors, and summaries",
        "fields": ["headline", "date", "author", "summary"],
        "data_type": "general"
    },
    "social_media": {
        "description": "Extract social media posts, usernames, timestamps, and engagement metrics",
        "fields": ["username", "post_content", "timestamp", "likes", "shares"],
        "data_type": "general"
    }
}

def get_template_query(template_name):
    """Get extraction query for a specific template"""
    if template_name in EXTRACTION_TEMPLATES:
        template = EXTRACTION_TEMPLATES[template_name]
        return template["description"]
    return ""
