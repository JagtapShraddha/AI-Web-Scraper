import streamlit as st
from scraper import scrap_website, clean_content,split_dom_content
from parse import parse_with_ollama

st.title("AI Web Scraper")


url = st.text_input("Enter a Website URL:")


if st.button("Scrape"):
    st.write("Scraping the website...")

    # Scrape the website using the dynamic scraper
    dom_content = scrap_website(url)

    if dom_content:
        # Clean the scraped content
        cleaned_content = clean_content(dom_content)
        
        st.session_state.dom_content = cleaned_content

       
        st.subheader("Scraped Data:")
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
        
        if "dom_content" in st.session_state:    
            parse_description = st.text_area("Describe what you want to parse:")
        
       
            if st.button("Parse Content"):

                if parse_description:
                    st.write("Parsing the content...")

                    # Split the DOM content into chunks if it's too long
                    dom_chunks = split_dom_content(st.session_state.dom_content)

                    parsed_result = parse_with_ollama(dom_chunks,parse_description)
                    if parsed_result:
                        st.write(parsed_result)
                    else:
                        st.error("No Matching Content Found")

            else:
                st.error("Please provide a description of what you want to parse.")

    else:
        st.error("No data was scraped. Please check the URL.")


