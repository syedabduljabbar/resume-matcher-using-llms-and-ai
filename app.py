import streamlit as st
import PyPDF2
import re

st.set_page_config(page_title="Resume Matcher", page_icon="📄")

st.title("📄 Resume Job Matcher")

# ---------- FUNCTIONS ----------

def extract_text(file):
    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:
        return file.read().decode("utf-8")

# remove useless words
stopwords = {
    "the","is","at","which","on","and","a","an","in","to","for","of",
    "with","by","as","from","that","this","it","are","was"
}

def get_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    filtered = [w for w in words if w not in stopwords and len(w) > 2]
    return set(filtered)

# ---------- INPUT ----------

uploaded_file = st.file_uploader("Upload Resume", type=["txt", "pdf"])
job_desc = st.text_area("Paste Job Description")

# ---------- BUTTON ----------

if st.button("Check Match"):
    if uploaded_file and job_desc:
        

        resume_text = extract_text(uploaded_file)

        resume_words = get_keywords(resume_text)
        job_words = get_keywords(job_desc)

        match = resume_words & job_words
        score = len(match) / len(job_words) * 100

        missing = job_words - resume_words

        # ---------- MATCH RESULT ----------

        if score < 40:
            st.error(f"❌ Low Match: {int(score)}%")
        elif score < 70:
            st.warning(f"⚠️ Moderate Match: {int(score)}%")
        else:
            st.success(f"✅ Good Match: {int(score)}%")

        st.progress(int(score))

        # ---------- SKILLS ----------

        st.subheader("✅ Matching Skills")
        st.write(", ".join(list(match)[:8]))

        st.subheader("❌ Missing Skills")
        st.write(", ".join(list(missing)[:8]))

        # ---------- HUMAN-LIKE SUGGESTIONS ----------

        missing_list = list(missing)[:5]

        st.subheader("💡 Suggestions")

        if score < 40:
            st.write(f"👉 Your resume does not match this role well.")
            st.write(f"👉 If you want to apply, try adding skills like: {', '.join(missing_list)}")
        
        elif score < 70:
            st.write(f"👉 Your resume is somewhat matching.")
            st.write(f"👉 You can improve your chances by adding: {', '.join(missing_list)}")
        
        else:
            st.write("👉 Your resume is a good match for this role.")
            st.write("👉 Just make sure your projects and experience support these skills.")

    else:
        st.warning("Upload resume and add job description")
