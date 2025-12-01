import streamlit as st
from transformers import pipeline
import time

# Page config
st.set_page_config(
    page_title="ClearSpeak - Text Simplifier",
    page_icon="🎯",
    layout="wide"
)

# Load model once (cache it for speed)
@st.cache_resource
def load_model():
    try:
        return pipeline("text2text-generation", model="t5-small")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Title and description
st.title("🎯 ClearSpeak")
st.markdown("**Convert complex text into simple, easy-to-understand Indian English**")
st.markdown("---")

# Main content
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📝 Input")
    user_text = st.text_area(
        "Enter complex text:",
        placeholder="Paste legal, government, or formal text here...",
        height=200
    )
    
    # Character count
    if user_text:
        st.caption(f"Characters: {len(user_text)}")

with col2:
    st.subheader("✨ Output")
    output_container = st.empty()

# Simplify button
if st.button("🚀 Simplify Text", use_container_width=True):
    if not user_text.strip():
        st.warning("Please enter some text first!")
    else:
        # Load model
        model = load_model()
        if model is None:
            st.stop()
        
        with st.spinner("Simplifying your text..."):
            try:
                start_time = time.time()
                
                # Simplify
                result = model(user_text, max_length=150, do_sample=False)
                simplified_text = result[0]['generated_text']
                
                processing_time = time.time() - start_time
                
                # Display result
                output_container.success(f"✅ Done! ({processing_time:.2f}s)")
                st.text_area(
                    "Simplified Text:",
                    value=simplified_text,
                    height=150,
                    disabled=True
                )
                
                # Copy button
                st.write("")
                st.info(f"**Original:** {len(user_text)} characters → **Simplified:** {len(simplified_text)} characters")
                
            except Exception as e:
                st.error(f"Error during simplification: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 12px;'>"
    "ClearSpeak v1.0 | Built for Indian English Simplification | "
    "<a href='https://github.com/nlpproject65-netizen/clearspeak-api' target='_blank'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)