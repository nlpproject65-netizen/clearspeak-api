import streamlit as st
import time

try:
    from transformers import pipeline
except ImportError:
    st.error("❌ Failed to load transformers library. Please check requirements.txt")
    st.stop()

# Page config
st.set_page_config(
    page_title="ClearSpeak - Text Simplifier",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextArea textarea { font-size: 14px; }
    .success-box { background-color: #d4edda; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# Load model with error handling
@st.cache_resource
def load_model():
    try:
        st.info("⏳ Loading model... (first time only)")
        return pipeline("text2text-generation", model="t5-small")
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

# Header
st.title("🎯 ClearSpeak")
st.markdown("### Convert Complex Text into Simple Indian English")
st.markdown("---")

# Layout
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📝 Input Complex Text")
    user_text = st.text_area(
        "Paste legal, government, or formal text:",
        placeholder="Example: The lessee shall remit the rental consideration...",
        height=220,
        key="input_text"
    )
    
    if user_text:
        st.caption(f"📊 Characters: {len(user_text)} | Words: {len(user_text.split())}")

with col2:
    st.subheader("✨ Simplified Output")
    result_placeholder = st.empty()

# Button to simplify
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])

with col_btn1:
    simplify_button = st.button("🚀 Simplify Now", use_container_width=True, type="primary")

if simplify_button:
    if not user_text.strip():
        st.warning("⚠️ Please enter some text first!")
    else:
        # Load model
        model = load_model()
        if model is None:
            st.stop()
        
        with st.spinner("🔄 Simplifying your text..."):
            try:
                start_time = time.time()
                
                # Generate simplified text
                input_text = f"simplify: {user_text}"
                result = model(input_text, max_length=150, do_sample=False)
                simplified_text = result[0]['generated_text']
                
                processing_time = time.time() - start_time
                
                # Display result in the right column
                with col2:
                    st.success(f"✅ Done in {processing_time:.2f}s")
                    st.text_area(
                        "Simplified Text:",
                        value=simplified_text,
                        height=200,
                        disabled=True,
                        key="output_text"
                    )
                    
                    # Stats
                    st.info(
                        f"📊 **Original:** {len(user_text)} chars | "
                        f"**Simplified:** {len(simplified_text)} chars | "
                        f"**Reduction:** {round((1 - len(simplified_text)/len(user_text))*100)}%"
                    )
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 12px;'>"
    "ClearSpeak v1.0 | Indian English Text Simplification | "
    "<a href='https://github.com' target='_blank'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)