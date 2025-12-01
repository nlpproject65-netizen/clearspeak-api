import streamlit as st
import time

try:
    from transformers import pipeline
except ImportError:
    st.error("❌ Failed to load transformers. Refresh the page.")
    st.stop()

st.set_page_config(page_title="ClearSpeak", page_icon="🎯", layout="wide")

@st.cache_resource
def load_model():
    try:
        return pipeline("text2text-generation", model="t5-small")
    except Exception as e:
        st.error(f"❌ Model Error: {str(e)}")
        return None

st.title("🎯 ClearSpeak")
st.markdown("**Convert complex text into simple Indian English**")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Input")
    user_text = st.text_area("Enter complex text:", placeholder="Paste legal or government text...", height=220)
    if user_text:
        st.caption(f"📊 {len(user_text)} characters")

with col2:
    st.subheader("✨ Output")
    output_area = st.empty()

st.markdown("---")

if st.button("🚀 Simplify", use_container_width=True, type="primary"):
    if not user_text.strip():
        st.warning("⚠️ Enter text first!")
    else:
        model = load_model()
        if model is None:
            st.stop()
        
        with st.spinner("Simplifying..."):
            try:
                start = time.time()
                result = model(user_text, max_length=150, do_sample=False)
                simplified = result[0]['generated_text']
                elapsed = time.time() - start
                
                with col2:
                    output_area.success(f"✅ Done ({elapsed:.2f}s)")
                    st.text_area("Result:", value=simplified, height=180, disabled=True)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("ClearSpeak v1.0 | Indian English Simplification")