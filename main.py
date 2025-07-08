import streamlit as st
import time
import validators
import os

from datetime import datetime

# Environment detection for deployment
IS_DEPLOYMENT = os.getenv("STREAMLIT_CLOUD") or not os.path.exists("chromedriver.exe")

# Import appropriate modules based on environment
if IS_DEPLOYMENT:
    from scrape_deploy import (
        scrape_website,
        extract_body_content,
        clean_body_content,
        split_dom_content,
    )
    from parse_deploy import parse_with_ollama
else:
    from scrape import (
        scrape_website,
        extract_body_content,
        clean_body_content,
        split_dom_content,
    )
    from parse import parse_with_ollama

from data_processor import (
    structure_data,
    validate_extraction,
    convert_to_csv,
    convert_to_json,
    convert_to_excel,
    EXTRACTION_TEMPLATES,
    get_template_query
)

# Page configuration
st.set_page_config(
    page_title="AI Content Extractor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for templates only
if "extraction_history" not in st.session_state:
    st.session_state.extraction_history = []

# Header
st.title("AI Content Extractor")
st.markdown("Intelligent web content extraction and structuring powered by AI")

# Deployment notification
if IS_DEPLOYMENT:
    st.info("🚀 **Demo Mode**: This is a deployment-friendly version. AI parsing uses pattern matching for demonstration purposes. For full AI capabilities, run locally with Ollama.")

# Sidebar
with st.sidebar:
    st.subheader("🎯 Extraction Templates")
    
    # Template selector
    template_names = list(EXTRACTION_TEMPLATES.keys())
    selected_template = st.selectbox(
        "Choose a template",
        ["Custom"] + [name.replace("_", " ").title() for name in template_names],
        help="Pre-configured extraction templates for common use cases"
    )
    
    if selected_template != "Custom":
        template_key = selected_template.lower().replace(" ", "_")
        if template_key in EXTRACTION_TEMPLATES:
            template = EXTRACTION_TEMPLATES[template_key]
            st.info(f"**Purpose**: {template['description']}")
    
    st.divider()
    
    # Usage tips
    st.subheader("� Usage Tips")
    st.markdown("""
    **For best results:**
    - Be specific about what you want to extract
    - Use templates for common tasks
    - Check content preview before extraction
    - Try batch processing for multiple URLs
    """)
    
    st.divider()
    
    # About section
    st.subheader("ℹ️ About")
    st.markdown("""
    **AI Content Extractor** uses advanced AI to intelligently extract structured data from websites.
    
    **Features:**
    - Gemma 3 AI processing
    - Multiple export formats
    - Batch processing
    - Data validation
    """)

# Main content - tabs for different modes
tab1, tab2, tab3 = st.tabs(["🔍 Single URL", "📊 Batch Processing", "⚙️ Settings"])

with tab1:
    # Single URL processing
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Website URL")
        url = st.text_input(
            "Enter the website URL",
            placeholder="https://example.com",
            help="Enter a valid URL starting with http:// or https://"
        )
        
        # URL validation
        url_valid = False
        if url:
            if validators.url(url):
                st.success("✓ Valid URL")
                url_valid = True
            else:
                st.error("Please enter a valid URL")
    
    with col2:
        st.subheader("Content Stats")
        if "dom_content" in st.session_state:
            content_length = len(st.session_state.dom_content)
            word_count = len(st.session_state.dom_content.split())
            
            st.metric("Characters", f"{content_length:,}")
            st.metric("Words", f"{word_count:,}")
            st.metric("Status", "Ready")
        else:
            st.metric("Characters", "0")
            st.metric("Words", "0")
            st.metric("Status", "Waiting")
    
    # Content preview toggle
    if "dom_content" in st.session_state:
        if st.checkbox("Preview content before extraction"):
            st.text_area("Content Preview", st.session_state.dom_content[:2000], height=200, disabled=True)
    
    # Step 1: Scraping
    st.divider()
    st.subheader("Step 1: Scrape Website")
    
    if st.button("Start Scraping", disabled=not url_valid, type="primary"):
        start_time = time.time()
        
        with st.spinner("Scraping website..."):
            progress_bar = st.progress(0)
            
            try:
                # Scrape the website
                progress_bar.progress(25)
                dom_content = scrape_website(url)
                
                progress_bar.progress(50)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)
                
                progress_bar.progress(75)
                
                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content
                st.session_state.source_url = url
                st.session_state.scraping_time = time.time() - start_time
                
                progress_bar.progress(100)
                
                st.success(f"Successfully scraped {len(cleaned_content):,} characters in {st.session_state.scraping_time:.2f}s")
                
                # Display content preview
                with st.expander("Preview scraped content"):
                    preview = cleaned_content[:500] + "..." if len(cleaned_content) > 500 else cleaned_content
                    st.text_area("Content Preview", preview, height=150, disabled=True)
                        
            except Exception as e:
                st.error(f"Error during scraping: {str(e)}")
                st.info("Try checking if the URL is accessible or if you have internet connection.")
    
    # Step 2: Extraction
    if "dom_content" in st.session_state:
        st.divider()
        st.subheader("Step 2: Extract Information")
        
        # Two-column layout for input and examples
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Use form for Ctrl+Enter functionality
            with st.form("extraction_form"):
                # Template or custom query
                if selected_template != "Custom":
                    template_key = selected_template.lower().replace(" ", "_")
                    default_query = get_template_query(template_key)
                    data_type = EXTRACTION_TEMPLATES[template_key]["data_type"]
                else:
                    default_query = ""
                    data_type = "general"
                
                parse_description = st.text_area(
                    "What information do you want to extract?",
                    value=default_query,
                    placeholder="Example: Extract all email addresses and phone numbers",
                    height=100,
                    help="Be specific about what you want to extract. Press Ctrl+Enter to extract.",
                    key="extraction_query"
                )
                
                # Form submit button (automatically works with Ctrl+Enter)
                extract_triggered = st.form_submit_button("Extract Information", disabled=not parse_description, type="primary")
        
        with col2:
            st.markdown("**💡 Extraction Tips:**")
            st.info("""
            • Be specific about data types
            • Mention expected formats
            • Include context clues
            • Use action verbs like "extract", "find", "list"
            • Press **Ctrl+Enter** to extract
            """)
        
        # Add keyboard shortcut info
        st.markdown("💡 **Tip**: Press `Ctrl+Enter` in the text area to extract quickly!")
        
        if extract_triggered:
            extraction_start_time = time.time()
            
            # Estimate processing time based on content length
            content_length = len(st.session_state.dom_content)
            estimated_time = max(10, min(60, content_length // 1000))  # 10-60 seconds based on content
            
            # Create placeholder for time display
            time_placeholder = st.empty()
            
            with st.spinner("Processing content with AI..."):
                progress_bar = st.progress(0)
                
                try:
                    # Show initial time estimate
                    time_placeholder.info(f"⏱️ Estimated time: {estimated_time} seconds")
                    
                    progress_bar.progress(25)
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    
                    elapsed = time.time() - extraction_start_time
                    remaining = max(0, estimated_time - elapsed)
                    time_placeholder.info(f"⏱️ Processing chunks... ~{remaining:.0f} seconds remaining")
                    
                    progress_bar.progress(50)
                    
                    # Define progress callback for AI processing
                    def update_progress(current_chunk, total_chunks):
                        elapsed = time.time() - extraction_start_time
                        avg_time_per_chunk = elapsed / current_chunk if current_chunk > 0 else 5
                        remaining_chunks = total_chunks - current_chunk
                        estimated_remaining = remaining_chunks * avg_time_per_chunk
                        
                        progress_percentage = 50 + (current_chunk / total_chunks) * 25  # 50% to 75%
                        progress_bar.progress(int(progress_percentage))
                        
                        time_placeholder.info(f"⏱️ Processing chunk {current_chunk}/{total_chunks}... ~{estimated_remaining:.0f} seconds remaining")
                    
                    # Parse the content with Ollama
                    parsed_result = parse_with_ollama(dom_chunks, parse_description, update_progress)
                    
                    elapsed = time.time() - extraction_start_time
                    remaining = max(0, estimated_time - elapsed)
                    time_placeholder.info(f"⏱️ Validating results... ~{remaining:.0f} seconds remaining")
                    
                    progress_bar.progress(75)
                    
                    # Validate extraction
                    quality_score, suggestions = validate_extraction(parsed_result, data_type)
                    
                    progress_bar.progress(100)
                    extraction_time = time.time() - extraction_start_time
                    
                    # Clear time placeholder
                    time_placeholder.empty()
                    
                    st.success("Information extracted successfully!")
                    
                    # Processing statistics
                    st.subheader("📊 Extraction Statistics")
                    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                    
                    items_found = len([line for line in parsed_result.split('\n') if line.strip()])
                    
                    with stat_col1:
                        st.metric("Items Found", items_found)
                    with stat_col2:
                        st.metric("Processing Time", f"{extraction_time:.2f}s")
                    with stat_col3:
                        st.metric("Quality Score", f"{quality_score:.1%}")
                    with stat_col4:
                        st.metric("Data Type", data_type.title())
                    
                    # Display quality suggestions
                    if suggestions:
                        st.warning("Quality Suggestions:")
                        for suggestion in suggestions:
                            st.write(f"• {suggestion}")
                    
                    # Display results
                    st.subheader("📋 Extracted Information")
                    
                    if parsed_result.strip():
                        st.text_area("Results", parsed_result, height=250)
                        
                        # Export options
                        st.subheader("📥 Export Options")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.download_button(
                                label="📄 Download TXT",
                                data=parsed_result,
                                file_name=f"extracted_data_{int(time.time())}.txt",
                                mime="text/plain"
                            )
                        
                        with col2:
                            csv_data = convert_to_csv(parsed_result, data_type)
                            st.download_button(
                                label="📊 Download CSV",
                                data=csv_data,
                                file_name=f"extracted_data_{int(time.time())}.csv",
                                mime="text/csv"
                            )
                        
                        with col3:
                            json_data = convert_to_json(parsed_result, data_type)
                            st.download_button(
                                label="📋 Download JSON",
                                data=json_data,
                                file_name=f"extracted_data_{int(time.time())}.json",
                                mime="application/json"
                            )
                        
                        with col4:
                            excel_data = convert_to_excel(parsed_result, data_type)
                            if excel_data:
                                st.download_button(
                                    label="📈 Download Excel",
                                    data=excel_data,
                                    file_name=f"extracted_data_{int(time.time())}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                    
                    else:
                        st.warning("No information matching your description was found.")
                        st.info("Try being more specific or check if the information exists on the page.")
                        
                except Exception as e:
                    st.error(f"Error during parsing: {str(e)}")

with tab2:
    st.subheader("📊 Batch URL Processing")
    st.info("Process multiple URLs simultaneously for efficient data extraction.")
    
    # URL input methods
    input_method = st.radio(
        "Choose input method:",
        ["Manual Entry", "Upload CSV"],
        horizontal=True
    )
    
    urls_to_process = []
    
    if input_method == "Manual Entry":
        url_text = st.text_area(
            "Enter URLs (one per line):",
            placeholder="https://example1.com\nhttps://example2.com\nhttps://example3.com",
            height=150
        )
        
        if url_text:
            urls_to_process = [url.strip() for url in url_text.split('\n') if url.strip()]
    
    else:
        uploaded_file = st.file_uploader(
            "Upload CSV file with URLs",
            type=['csv'],
            help="CSV should have a column named 'url' or 'URL'"
        )
        
        if uploaded_file is not None:
            try:
                import pandas as pd
                df = pd.read_csv(uploaded_file)
                
                # Try to find URL column
                url_column = None
                for col in df.columns:
                    if col.lower() in ['url', 'urls', 'link', 'links']:
                        url_column = col
                        break
                
                if url_column:
                    urls_to_process = df[url_column].tolist()
                    st.success(f"Found {len(urls_to_process)} URLs in the file")
                else:
                    st.error("Could not find URL column. Please ensure your CSV has a column named 'url' or 'URL'")
                    
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
    
    # Show URLs to process
    if urls_to_process:
        st.write(f"**URLs to process ({len(urls_to_process)}):**")
        for i, url in enumerate(urls_to_process[:5]):  # Show first 5
            st.write(f"{i+1}. {url}")
        
        if len(urls_to_process) > 5:
            st.write(f"... and {len(urls_to_process) - 5} more")
        
        # Batch extraction query
        batch_query = st.text_area(
            "What information do you want to extract from all URLs?",
            placeholder="Example: Extract all email addresses and phone numbers",
            height=100
        )
        
        if st.button("🚀 Start Batch Processing", disabled=not batch_query, type="primary"):
            batch_results = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, url in enumerate(urls_to_process):
                try:
                    status_text.text(f"Processing {i+1}/{len(urls_to_process)}: {url[:50]}...")
                    
                    # Scrape
                    dom_content = scrape_website(url)
                    body_content = extract_body_content(dom_content)
                    cleaned_content = clean_body_content(body_content)
                    
                    # Parse
                    dom_chunks = split_dom_content(cleaned_content)
                    parsed_result = parse_with_ollama(dom_chunks, batch_query)
                    
                    # Validate
                    quality_score, _ = validate_extraction(parsed_result)
                    
                    batch_results.append({
                        "url": url,
                        "status": "success",
                        "data": parsed_result,
                        "quality_score": quality_score,
                        "character_count": len(cleaned_content)
                    })
                    
                except Exception as e:
                    batch_results.append({
                        "url": url,
                        "status": "error",
                        "error": str(e),
                        "data": "",
                        "quality_score": 0,
                        "character_count": 0
                    })
                
                progress_bar.progress((i + 1) / len(urls_to_process))
            
            status_text.text("✅ Batch processing completed!")
            
            # Display results
            st.subheader("📊 Batch Results")
            
            successful_extractions = [r for r in batch_results if r["status"] == "success"]
            failed_extractions = [r for r in batch_results if r["status"] == "error"]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total URLs", len(urls_to_process))
            with col2:
                st.metric("Successful", len(successful_extractions))
            with col3:
                st.metric("Failed", len(failed_extractions))
            
            # Show individual results
            for result in batch_results:
                with st.expander(f"🔗 {result['url']} - {result['status'].title()}"):
                    if result['status'] == 'success':
                        st.write(f"**Quality Score**: {result['quality_score']:.1%}")
                        st.write(f"**Characters**: {result['character_count']:,}")
                        st.text_area("Extracted Data", result['data'], height=150, key=f"result_{result['url']}")
                    else:
                        st.error(f"Error: {result['error']}")
            
            # Batch export
            if successful_extractions:
                st.subheader("📥 Batch Export")
                
                # Combine all successful results
                combined_data = "\n".join([r["data"] for r in successful_extractions if r["data"]])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📄 Download Combined TXT",
                        data=combined_data,
                        file_name=f"batch_extraction_{int(time.time())}.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    # Create summary CSV
                    import pandas as pd
                    summary_df = pd.DataFrame(batch_results)
                    summary_csv = summary_df.to_csv(index=False)
                    
                    st.download_button(
                        label="📊 Download Summary CSV",
                        data=summary_csv,
                        file_name=f"batch_summary_{int(time.time())}.csv",
                        mime="text/csv"
                    )

with tab3:
    st.subheader("⚙️ Settings & Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Processing Settings")
        
        chunk_size = st.slider(
            "Content Chunk Size",
            min_value=1000,
            max_value=10000,
            value=6000,
            step=500,
            help="Size of text chunks sent to AI model"
        )
        
        extraction_timeout = st.slider(
            "Extraction Timeout (seconds)",
            min_value=30,
            max_value=300,
            value=120,
            step=10,
            help="Maximum time to wait for AI extraction"
        )
        
        st.markdown("#### Data Quality Settings")
        
        min_quality_score = st.slider(
            "Minimum Quality Score",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Minimum quality score to accept extraction results"
        )
    
    with col2:
        st.markdown("#### Export Settings")
        
        include_metadata = st.checkbox(
            "Include Metadata in Exports",
            value=True,
            help="Add timestamp, URL, and quality metrics to exports"
        )
        
        structured_output = st.checkbox(
            "Enable Structured Output",
            value=True,
            help="Attempt to structure data based on content type"
        )
        
        st.markdown("#### History Settings")
        
        max_history_items = st.slider(
            "Maximum History Items",
            min_value=5,
            max_value=50,
            value=10,
            step=5,
            help="Number of extraction history items to keep"
        )
        
        if st.button("Clear History"):
            st.session_state.extraction_history = []
            st.success("History cleared!")
    
    # Save settings
    if st.button("Save Settings", type="primary"):
        st.session_state.settings = {
            "chunk_size": chunk_size,
            "extraction_timeout": extraction_timeout,
            "min_quality_score": min_quality_score,
            "include_metadata": include_metadata,
            "structured_output": structured_output,
            "max_history_items": max_history_items
        }
        st.success("Settings saved!")

# Footer
st.divider()
if IS_DEPLOYMENT:
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 1rem;'>"
        "🤖 AI Content Extractor - Demo Mode (Pattern Matching)"
        "</div>", 
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 1rem;'>"
        "🤖 AI Content Extractor - Powered by Gemma 3 & LangChain"
        "</div>", 
        unsafe_allow_html=True
    )