import streamlit as st
import logging
from dotenv import load_dotenv

load_dotenv()

from utils.config.load_config import load_yaml_config
from pipeline import run_pipeline   # import your pipeline function

# ---------------------------
# Streamlit Page Setup
# ---------------------------
st.set_page_config(
    page_title="Reddit Churn Signal Detector",
    layout="centered"
)

st.title("Reddit Customer Churn Signal Detector")
st.caption("Analyze subreddit discussions to identify churn-causing features")

logging.info("Streamlit app loaded")

# ---------------------------
# User Input
# ---------------------------
subreddit = st.text_input(
    "Enter subreddit name",
    placeholder="e.g. spotify"
)

run_button = st.button("Analyze Churn")

# ---------------------------
# Session State
# ---------------------------
if "results" not in st.session_state:
    st.session_state.results = None

# ---------------------------
# Run Pipeline (ONCE)
# ---------------------------
if run_button and subreddit:
    with st.spinner("Fetching Reddit data and analyzing churn..."):
        config = load_yaml_config("utils/config/reddit.yaml")

        results = run_pipeline(
            config=config,
            subreddit_override=subreddit
        )

        st.session_state.results = results

        logging.info(f"Pipeline completed for subreddit: {subreddit}")

# ---------------------------
# Display Results
# ---------------------------
if st.session_state.results:
    st.subheader("Top Churn-Causing Issues")

    for issue in st.session_state.results[:5]:
        st.markdown(f"### 🔴 Feature: `{issue['affected_feature']}`")

        st.write(f"**Problem Type:** {issue['problem_type']}")
        st.write(f"**Churn Score:** {issue['churn_score']}")
        st.write(f"**Posts Affected:** {issue['num_posts']}")

        if issue["example_quotes"]:
            st.markdown("**Example Quote:**")
            st.info(issue["example_quotes"][0])

        st.divider()
