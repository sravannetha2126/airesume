import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------
# Custom CSS for Animation
# -------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}

.big-title {
    font-size: 50px;
    font-weight: bold;
    text-align: center;
    animation: fadeIn 2s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

.card {
    background-color: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px #00f2fe;
}

.stButton>button {
    background: linear-gradient(to right, #00f2fe, #4facfe);
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.write("### Analyze your resume using AI & get job recommendations")

# -------------------------------
# Load Model
# -------------------------------
@st.cache_resource
def semantic_match(resume_text, job_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(similarity[0][0] * 100, 2)

# -------------------------------
# Job Roles
# -------------------------------
job_roles = {
    "Java Developer": ["java", "spring", "hibernate", "mysql"],
    "Web Developer": ["html", "css", "javascript", "react"],
    "Python Developer": ["python", "django", "flask", "sql"]
}

# -------------------------------
# Skill Extraction
# -------------------------------
def extract_skills(text):
    skills_db = ["python","java","html","css","javascript",
                 "react","django","flask","spring",
                 "hibernate","mysql","sql"]
    text = text.lower()
    return list(set([skill for skill in skills_db if skill in text]))

# -------------------------------
# Semantic Match
# -------------------------------
def semantic_match(resume_text, job_text):
    resume_emb = model.encode([resume_text])
    job_emb = model.encode([job_text])
    score = cosine_similarity(resume_emb, job_emb)[0][0]
    return round(score * 100, 2)

# -------------------------------
# ATS Score
# -------------------------------
def calculate_ats_score(resume_text):
    score = 0
    text = resume_text.lower()

    if 200 <= len(text.split()) <= 800:
        score += 25
    if "skills" in text:
        score += 15
    if "project" in text:
        score += 15
    if "experience" in text:
        score += 20
    if re.search(r"\d+%", text):
        score += 15
    return score

# -------------------------------
# UI
# -------------------------------
resume_text = st.text_area("📄 Paste Resume Text", height=200)

if st.button("✨ Analyze Resume"):
    if not resume_text.strip():
        st.error("Please paste resume text")
        st.stop()

    st.balloons()

    detected_skills = extract_skills(resume_text)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("✅ Detected Skills")
    st.write(", ".join(detected_skills) if detected_skills else "No skills detected")
    st.markdown('</div>', unsafe_allow_html=True)

    ats_score = calculate_ats_score(resume_text)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 ATS Score")
    st.progress(ats_score / 100)
    st.write(f"Score: {ats_score}/100")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📌 Job Match Analysis")

    for role, skills in job_roles.items():
        match = semantic_match(resume_text, " ".join(skills))
        st.write(f"### {role}")
        st.write(f"Match: {match}%")


    st.markdown('</div>', unsafe_allow_html=True)
