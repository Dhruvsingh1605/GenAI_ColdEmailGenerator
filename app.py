import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def add_custom_styles():
    st.markdown(
        """
        <style>
        body {
            background-color: #f9f9f9;
            color: #2c3e50;
        }
        .main-title {
            font-size: 2.5em;
            color: #3498db;
            text-align: center;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 1.2em;
            color: #34495e;
            text-align: center;
            margin-bottom: 40px;
        }
        .stButton > button {
            background-color: #3498db;
            color: white;
            font-size: 1.1em;
            border-radius: 8px;
            padding: 8px 16px;
        }
        .stButton > button:hover {
            background-color: #2980b9;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def create_streamlit_app(llm, portfolio, clean_text):
    st.markdown("<div class='main-title'>📧 Cold Mail Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Generate personalized cold emails for job postings effortlessly.</div>", unsafe_allow_html=True)

    # Sidebar for additional details
    with st.sidebar:
        st.title("About 📧 Cold Mail Generator")
        st.markdown(
            """
            **Ataquilc** helps companies find the right candidates for job profiles. 
            Use this tool to:
            - Extract job details from a URL.
            - Generate a tailored cold email.
            - Impress potential clients!
            """
        )
        st.info("Powered by LangChain and Streamlit.")

    url_input = st.text_input("🔗 Enter Job Posting URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Generate Email")

    if submit_button:
        try:
            st.markdown("### 💼 Job Information Extracted:")
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get("skills", [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.markdown("#### 📧 Generated Email:")
                st.code(email, language="markdown")
        except Exception as e:
            st.error(f"⚠️ An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    add_custom_styles()
    create_streamlit_app(chain, portfolio, clean_text)
