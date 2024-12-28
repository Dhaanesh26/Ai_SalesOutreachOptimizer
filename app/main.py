import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    
    # Input field to enter URL
    url_input = st.text_input("Enter a URL:", value="https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4109918108")
    
    # Submit button to trigger job extraction and cold mail generation
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load page content from URL
            loader = WebBaseLoader([url_input])
            page_content = loader.load()
            
            # Clean the content from the webpage
            data = clean_text(page_content[0].page_content)

            # Load portfolio data into ChromaDB
            portfolio.load_portfolio()

            # Extract job postings using the LLM
            jobs = llm.extract_jobs(data)
            
            # Iterate over jobs and generate emails
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                
                # Generate cold email using the job and links
                email = llm.write_mail(job, links)
                
                # Display generated email
                st.code(email, language='markdown')
        
        except Exception as e:
            # Display any errors that occur
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    # Initialize the necessary objects for Streamlit app
    chain = Chain()  # Make sure Chain class has methods extract_jobs and write_mail
    portfolio = Portfolio()  # Make sure Portfolio class methods are correct
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    
    # Run the Streamlit app
    create_streamlit_app(chain, portfolio, clean_text)
