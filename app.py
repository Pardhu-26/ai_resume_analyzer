import streamlit as st

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.markdown("""
<h1 style='text-align: center; color: #4169E1;'>
AI Resume Analyzer📄
</h1>
""", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Your Resume Here (PDFs)", type = ["pdf"])

from utils import extract_text
from utils import match_resume_to_jobs
from utils import job_descriptions

if uploaded_file:
    text = extract_text(uploaded_file)
    from utils import is_resume

    if not is_resume(text):
        st.error("⚠️ This doesn't look like a resume. Please upload a valid resume PDF.")
        st.stop()
    scores = match_resume_to_jobs(text, job_descriptions)

    max_score = max(scores.values())

    normalized_scores = {
        role: round((score / max_score) * 100, 2)
        for role, score in scores.items()
    }
    with st.expander("📊 Job Match Scores", expanded=True):
        st.markdown("""
        <h3 style='text-align: center;'>
        Job Match Score
        </h3>
        """, unsafe_allow_html=True)
        sorted_scores = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
    
        for i, (role, score) in enumerate(sorted_scores):
            st.write(f"### {i+1}. {role}")
            st.progress(score / 100)
            st.write(f"{score}% match\n")
        st.info("Scores represent similarity between your resume and job descriptions.")
    
    with st.expander("📈 Visualization"):
        import pandas as pd
        st.markdown("""
        <h3 style='text-align: center;'>
        Job Match Visualization
        </h3>
        """, unsafe_allow_html=True)
        df_scores = pd.DataFrame({
            "Role": list(normalized_scores.keys()),
            "Score": list(normalized_scores.values())
        })
        st.bar_chart(df_scores.set_index("Role"))
    with st.expander("🎯 Best Match"):
        from utils import find_missing_skills
        best_role = max(normalized_scores, key=normalized_scores.get)    
        st.markdown("""
        <h3 style='text-align: center;'>
        Top Recommendation
        </h3>
        """, unsafe_allow_html=True)
        st.success(f"Best Match: **{best_role}** ({normalized_scores[best_role]}%)")
    
    with st.expander("⚠️ Missing Skills"):
        missing = find_missing_skills(text, best_role)
        st.markdown("""
        <h3 style='text-align: center;'>
        Missing Skills
        </h3>
        """, unsafe_allow_html=True)
        for skill in missing:
            st.warning(f"Add '{skill}' to improve your profile")
    
    with st.expander("💡 Suggestions"):
        from utils import generate_suggestions
        suggestions = generate_suggestions(missing)
        st.markdown("""
        <h3 style='text-align: center;'>
        Suggestions
        </h3>
        """, unsafe_allow_html=True)
        for s in suggestions:
            st.write("- " + s)
    
    with st.expander("📊 Resume Score"):
        resume_score = int(sum(normalized_scores.values()) / len(normalized_scores))
        st.markdown("""
        <h3 style='text-align: center;'>
        Resume Score
        </h3>
        """, unsafe_allow_html=True)
        st.metric(label="Overall Score", value=f"{resume_score}/100")

st.markdown("---")
