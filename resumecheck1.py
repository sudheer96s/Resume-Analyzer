import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
from docx import Document
import spacy


nlp = spacy.load("en_core_web_sm")

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        st.error("Unsupported file format. Please upload a PDF or DOCX file.")
        return None

def extract_skills(text):
    doc = nlp(text)
    skills = set()
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            skills.add(token.text)
    return list(skills)

def calculate_similarity(resume_text, job_description):
    common = [resume_text, job_description]
    vectorizer = CountVectorizer().fit_transform(common)
    vectors = vectorizer.toarray()
    similarity = cosine_similarity(vectors)
    return similarity[0][1]

def analyze_resume(resume_text, job_description):
    keywords_job = extract_skills(job_description)
    keywords_resume = extract_skills(resume_text)
    missing_keywords = set(keywords_job) - set(keywords_resume)
    similarity_score = calculate_similarity(resume_text, job_description)

    return {
        "keywords": keywords_resume,
        "missing_keywords": list(missing_keywords),
        "similarity_score": similarity_score
    }

def main():
    st.title("Resume Analyzer")
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Paste the job description below")
    if st.button("Check"):
        if uploaded_file and job_description:
            resume_text = extract_text_from_file(uploaded_file)
            if resume_text:
                st.subheader("Resume Text Preview")
                st.text_area("Extracted Resume Text", resume_text, height=300)

                st.subheader("Job Description Preview")
                st.text_area("Job Description", job_description, height=300)

                with st.spinner("Analyzing your resume..."):
                    analysis = analyze_resume(resume_text, job_description)

                st.subheader("Analysis Report")
                st.write(f"Similarity Score: {analysis['similarity_score'] * 100:.2f}%")

                st.write("Extracted Keywords from Resume")
                st.write(", ".join(analysis["keywords"]))

                st.write("Missing Keywords from Job Description")
                st.write(", ".join(analysis["missing_keywords"]))

                if st.button("Download Report"):
                    report = f"""Resume Analysis Report\n\nSimilarity Score: {analysis['similarity_score'] * 100:.2f}%\n\nExtracted Keywords:\n{', '.join(analysis['keywords'])}\n\nMissing Keywords:\n{', '.join(analysis['missing_keywords'])}\n"""
                    st.download_button(
                        "Download Report as Text",
                        report,
                        file_name="resume_analysis_report.txt"
                    )
        else:
            st.error("Please upload a resume and provide a job description.")

    if st.button("Clear"):
        st.session_state.clear() 


if __name__ == "__main__":
    main()
