import streamlit as st
import openai
import json
import tempfile
import whisper
import os
import time

# Set your OpenAI API Key
openai.api_key = "xxxxx"  # Replace this with your real key

# For video part - Whisper model
whisper_model = whisper.load_model("base")

# Streamlit page setup
st.set_page_config(page_title="UNICC Media Analysis Tool", layout="wide")
st.title("🧠 UNICC AI Media Analysis Tool")
st.markdown("Upload media content and detect xenophobic language, misinformation, or harmful narratives in text, audio, and video.")

# Sidebar for upload
st.sidebar.title("📁 Upload Your File")
file_type = st.sidebar.radio("Choose Media Type:", ["Text", "Audio", "Video"])
uploaded_file = st.sidebar.file_uploader("Upload File", type=["txt", "mp3", "wav", "mp4"])

# Interaction Panel
st.subheader("💬 Interactive Analysis Panel")
with st.expander("🧪 Try asking:"):
    st.markdown("- *Is there any xenophobic language?*")
    st.markdown("- *What is the sentiment in this content?*")

user_prompt = st.text_input("Ask a question about your uploaded content:")

def analyze_text_content(text_content):
    system_prompt = """You are a multilingual content moderation expert. Detect if the following text includes any of the following: xenophobic speech, hate speech, misinformation, or harmful/dehumanizing narratives.
Respond ONLY in valid JSON format like this:
{
  "is_harmful": true/false,
  "category": "...",
  "confidence": 0.0 - 1.0,
  "reason": "..."
}"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_content}
            ],
            temperature=0
        )
        content = response["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return parsed
    except Exception as e:
        return {"error": str(e)}

def analyze_video_file(video_path):
    segments = whisper_model.transcribe(video_path)["segments"]
    harmful_count = 0
    total_segments = len(segments)
    detailed_results = []

    for seg in segments:
        text = seg['text']
        prompt = f"""
You are a content moderation AI. Given the following text from a video, decide if it contains hate speech, harmful language, or offensive content. Respond with "Harmful" or "Safe", and explain briefly why.

Text: "{text}"
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            result_text = response["choices"][0]["message"]["content"].strip()
            detailed_results.append((seg['start'], seg['end'], text, result_text))

            if "Harmful" in result_text:
                harmful_count += 1
        except Exception as e:
            detailed_results.append((seg['start'], seg['end'], text, f"Error: {e}"))

    toxicity_rate = (harmful_count / total_segments) * 100 if total_segments else 0
    return toxicity_rate, detailed_results

# When the Analyze button is clicked
if st.button("Analyze"):
    if uploaded_file is None:
        st.warning("Please upload a file first.")
    else:
        with st.spinner("Analyzing..."):
            time.sleep(2)

        # Handle Text Files
        if file_type == "Text":
            text_content = uploaded_file.read().decode("utf-8")
            analysis_result = analyze_text_content(text_content)

            if "error" in analysis_result:
                st.error(f"❌ Error analyzing file: {analysis_result['error']}")
            else:
                st.success("✅ Analysis Complete!")
                st.markdown(f"**Detected Harmfulness:** {'⚠️ Harmful' if analysis_result['is_harmful'] else '✅ Not Harmful'}")
                st.markdown(f"**Category:** {analysis_result['category']}")
                st.markdown(f"**Confidence Score:** {analysis_result['confidence']:.2f}")
                st.markdown(f"**Reason:** {analysis_result['reason']}")

        # Handle Video Files
        elif file_type == "Video":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            toxicity_rate, results = analyze_video_file(tmp_path)

            st.success("✅ Video Analysis Complete!")
            st.markdown(f"**Overall Toxicity Rate:** {toxicity_rate:.2f}%")

            for start, end, text, result in results:
                st.markdown(f"**[{start:.2f}s - {end:.2f}s]**")
                st.code(text)
                st.info(result)
                st.markdown("---")

            os.remove(tmp_path)

        # Handle Audio Files Placeholder
        elif file_type == "Audio":
            st.info("Audio analysis integration coming soon! (ASR + Text analysis pipeline in progress.)")

# Footer
st.markdown("---")
st.caption("Developed for UNICC Capstone 2025 • Media Ethics & AI")

