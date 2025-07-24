import streamlit as st
from vector_setup import query_notes

st.set_page_config(page_title="Medical Notes Assistant", layout="centered")

st.title("🩺 Medical Notes Retrieval")
st.write("Search similar medical cases based on patient symptoms.")

query = st.text_area("Enter symptoms here:")

if st.button("Search"):
    if query.strip():
        results = query_notes(query)
        if results:
            st.success(f"Top {len(results)} matching cases:")
            for i, res in enumerate(results):
                st.subheader(f"Result {i+1}")
                st.write(f"**Symptoms:** {res['Symptoms']}")
                st.write(f"**Diagnosis:** {res['Diagnosis']}")
                st.write(f"**Treatment:** {res['Treatment']}")
                st.write(f"**Doctor Notes:** {res['Doctor Notes']}")
                st.markdown("---")
        else:
            st.warning("No matching records found.")
    else:
        st.error("Please enter some symptoms to search.")
