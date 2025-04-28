import streamlit as st
from PIL import Image
import time

st.set_page_config(page_title="UNICC Media Analysis Tool", layout="wide")

st.title("🧠 UNICC AI Media Analysis Tool")
st.markdown("Upload media content and detect xenophobic language, misinformation, or harmful narratives in text, audio, and video.")

# Sidebar for upload
st.sidebar.title("📁 Upload Your File")
file_type = st.sidebar.radio("Choose Media Type:", ["Text", "Audio", "Video"])

uploaded_file = st.sidebar.file_uploader("Upload File", type=["txt", "mp3", "wav", "mp4"])

# Chat-style Interaction Placeholder
st.subheader("💬 Interactive Analysis Panel")
with st.expander("🧪 Try asking:"):
    st.markdown("- *Is there any xenophobic language?*")
    st.markdown("- *What is the sentiment in this content?*")

user_prompt = st.text_input("Ask a question about your uploaded content:")

# Simulate response
if st.button("Analyze"):
    if uploaded_file is None:
        st.warning("Please upload a file first.")
    else:
        with st.spinner("Analyzing..."):
            time.sleep(2)
        st.success("✅ Analysis Complete!")

        # Sample output
        st.markdown("**Detected Sentiment:** ⚠️ Negative")
        st.markdown("**Flagged Phrases:**")
        st.code("• 'They are flooding our borders'\n• 'Stealing our jobs'")

        if user_prompt:
            st.markdown(f"**Response to your question:**")
            st.info(f"'{user_prompt}' → Based on the content, the language contains stereotypes and negative framing commonly associated with xenophobic discourse.")

# Footer
st.markdown("---")
st.caption("Developed for UNICC Capstone 2025 • Media Ethics & AI")
