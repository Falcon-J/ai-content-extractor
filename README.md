# 🤖 AI Content Extractor

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent web content extraction tool that combines advanced browser automation with AI-powered data parsing. Built with Streamlit, Selenium, and Gemma 3 AI model for intelligent content extraction and structuring.

![AI Content Extractor Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=AI+Content+Extractor)

## ✨ Features

### 🧠 **AI-Powered Extraction**

- **Gemma 3 Integration**: Uses Ollama's Gemma 3 model for intelligent content parsing
- **Natural Language Queries**: Describe what you want to extract in plain English
- **Context-Aware Processing**: AI understands the context and structure of web content
- **Chunk Processing**: Handles large content by intelligently splitting into manageable chunks

### 🛡️ **Advanced Web Scraping**

- **Anti-Bot Bypass**: Uses remote browser service to avoid detection
- **Captcha Solving**: Automatic captcha detection and solving capabilities
- **Modern Web Support**: Handles JavaScript-heavy sites and dynamic content
- **Content Cleaning**: Removes scripts, styles, and irrelevant HTML elements

### � **Professional Features**

- **Multiple Export Formats**: Download as TXT, CSV, JSON, or Excel
- **Batch Processing**: Handle multiple URLs simultaneously
- **Data Validation**: Quality metrics and extraction confidence scores
- **Processing History**: Track and revisit previous extractions
- **Smart Templates**: Pre-configured extraction templates for common use cases
- **API Access**: Generate API keys for programmatic access

### 📊 **Smart Analytics**

- **Content Metrics**: Real-time character count, word count, and processing statistics
- **Quality Assessment**: Data completeness and accuracy scoring
- **Processing Time**: Performance monitoring and optimization insights
- **Success Rates**: Extraction success metrics and improvement suggestions

### 🎨 **Modern Interface**

- **Tabbed Navigation**: Organized interface with Single URL, Batch Processing, and Settings
- **Real-time Validation**: URL validation with instant feedback
- **Progress Tracking**: Visual progress bars and status updates
- **Interactive Sidebar**: Quick templates and extraction history
- **Responsive Design**: Works seamlessly on desktop and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Ollama installed locally with LLaMA 3 model
- Chrome browser (for Selenium WebDriver)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ai-content-extractor.git
   cd ai-content-extractor
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   # Create a .env file and add your Bright Data credentials
   echo "SBR_WEBDRIVER=your_bright_data_webdriver_url" > .env
   ```

4. **Install and start Ollama**

   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.ai/install.sh | sh

   # Pull Gemma 3 model
   ollama pull gemma3
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 📖 Usage

### Basic Workflow

1. **Enter URL**: Input the website URL you want to scrape
2. **Scrape Content**: Click "Start Scraping" to extract and clean the content
3. **Describe Extraction**: Tell the AI what specific information you need
4. **Get Results**: AI analyzes and returns the requested data

### Example Queries

```
Extract all email addresses and phone numbers
```

```
Find all product names with their prices
```

```
Get job titles, company names, and locations from job listings
```

```
Extract social media links and contact information
```

```
List all article headlines and publication dates
```

### Use Cases

- **🎯 Lead Generation**: Extract contact information from business directories
- **📊 Market Research**: Gather competitor pricing and product data
- **📰 Content Analysis**: Parse articles, reviews, and social media posts
- **💼 Job Hunting**: Collect job postings and company information
- **🛒 E-commerce**: Monitor product prices and availability

## 🏗️ Architecture

```
ai-content-extractor/
│
├── main.py              # Main Streamlit application with enhanced UI
├── scrape.py           # Web scraping functionality
├── parse.py            # AI-powered content parsing
├── data_processor.py   # Data validation, structuring, and export utilities
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── README.md          # Project documentation
```

### Core Components

- **`main.py`**: Enhanced Streamlit frontend with tabs, batch processing, and settings
- **`scrape.py`**: Selenium-based scraping with anti-bot measures
- **`parse.py`**: LangChain + Ollama integration for AI parsing
- **`data_processor.py`**: Data validation, structuring, and multi-format export
- **`chromedriver.exe`**: Chrome WebDriver for browser automation

## 🛠️ Technical Stack

| Component           | Technology                   | Purpose                                 |
| ------------------- | ---------------------------- | --------------------------------------- |
| **Frontend**        | Streamlit                    | Interactive web interface with tabs     |
| **Web Scraping**    | Selenium + BeautifulSoup     | Browser automation and HTML parsing     |
| **AI Processing**   | LangChain + Ollama (Gemma 3) | Intelligent content extraction          |
| **Data Processing** | Pandas + JSON + CSV          | Data validation and multi-format export |
| **Browser Service** | Bright Data / Remote Chrome  | Anti-bot detection and captcha solving  |

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Bright Data WebDriver URL (for anti-bot scraping)
SBR_WEBDRIVER=wss://your-proxy-url

# Optional: Ollama configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gemma3
```

### Customization Options

- **Chunk Size**: Modify `max_length` in `split_dom_content()` function
- **AI Model**: Change the model in `parse.py` (supports other Ollama models)
- **UI Theme**: Customize CSS styles in `main.py`
- **Scraping Timeout**: Adjust timeout values in `scrape.py`

## 🧪 Testing

Test the application with these sample websites:

- **E-commerce**: `https://example-store.com` (product extraction)
- **News Sites**: `https://news-website.com` (article headlines)
- **Job Boards**: `https://job-site.com` (job listings)
- **Business Directories**: `https://directory.com` (contact info)

## 🚀 Deployment

### Streamlit Cloud Deployment

The application is configured for easy deployment to Streamlit Cloud:

#### 1. **Prepare Your Repository**

```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### 2. **Deploy to Streamlit Cloud**

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file as `main.py`
5. Deploy!

#### 3. **Configuration**

The app automatically detects the deployment environment and uses:

- `scrape_deploy.py` - Simple HTTP scraper (no Chrome dependency)
- `parse_deploy.py` - Pattern matching parser (demo mode)
- Optimized `requirements.txt` for cloud deployment

#### 4. **Environment Variables**

Configure these in Streamlit Cloud secrets:

```toml
# .streamlit/secrets.toml
[general]
# Add any API keys or configuration here
```

#### 5. **Local vs Cloud Features**

| Feature            | Local                  | Cloud            |
| ------------------ | ---------------------- | ---------------- |
| Web Scraping       | Full Chrome automation | HTTP requests    |
| AI Processing      | Ollama + Gemma 3       | Pattern matching |
| Anti-bot Features  | ✅ Advanced            | ⚠️ Basic         |
| All Other Features | ✅ Full                | ✅ Full          |


## 🔮 Roadmap

- [x] **Multiple Export Formats**: TXT, CSV, JSON, Excel export options ✅
- [x] **Batch Processing**: Support multiple URLs simultaneously ✅
- [x] **Data Validation**: Quality scoring and extraction confidence ✅
- [x] **Processing History**: Track and revisit previous extractions ✅
- [x] **Smart Templates**: Pre-configured extraction templates ✅
- [x] **API Integration**: API key generation for programmatic access ✅
- [ ] **Scheduled Scraping**: Add cron-like scheduling functionality
- [ ] **Database Storage**: Store scraped data in databases
- [ ] **Advanced Filtering**: More sophisticated content filtering options
- [ ] **Cloud Deployment**: One-click deployment to cloud platforms
- [ ] **Real-time Monitoring**: Live dashboard for batch operations
- [ ] **Machine Learning**: Custom model training for domain-specific extraction

---

<div align="center">

**⭐ Star this repository if you find it useful!**

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>
"# ai-content-extractor" 
