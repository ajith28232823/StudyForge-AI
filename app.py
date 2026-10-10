import os, json, re
import streamlit as st

st.set_page_config(page_title="StudyForge AI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
.main {background: #f7f9fc;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#182848,#4b6cb7); color:white;}
.small-note {color:#536174;font-size:0.92rem;}
div.stButton > button {border-radius: 10px; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🧠 StudyForge AI</h1><p>Turn study notes into understanding, practice, and a plan.</p><p>Learn the idea • connect concepts • test yourself</p></div>', unsafe_allow_html=True)
st.write("")

with st.sidebar:
    st.header("About this project")
    st.write("StudyForge helps students move beyond memorization by turning their own notes into plain-language explanations, concept connections, practice questions, and a short study plan.")
    st.caption("Track: AI + Education")
    st.divider()
    api_key = st.text_input("Gemini API key (optional)", type="password", help="Add your own key to enable generative AI. The demo still works without a key.")
    st.caption("Privacy: notes are processed in this session. If you use an API key, submitted notes are sent to the AI provider.")

def fallback_generate(notes, level, goal):
    # Lightweight local text analysis for a usable demo without an API key.
    clean = re.sub(r'\s+', ' ', notes).strip()
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', clean) if len(s.strip()) > 20]
    words = re.findall(r'\b[A-Za-z][A-Za-z-]{3,}\b', clean.lower())
    stop = set("""about above after again against all also among an and any are around as at because been before being between both but by can could did does doing during each few for from further had has have having here how into its itself just more most not of off on once only other our out over own same should some such than that the their them then there these they this those through too under until up use very was were what when where which while who will with would you your""".split())
    freq = {}
    for w in words:
        if w not in stop:
            freq[w] = freq.get(w, 0) + 1
    keywords = [w for w, _ in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:6]]
    if not sentences:
        sentences = [clean] if clean else ["Add some notes to get started."]
    summary = "\n".join(f"- {s}" for s in sentences[:4])
    concept_lines = "\n".join(f"- **{w.title()}**: Find where *{w}* appears in your notes and explain how it supports the main idea." for w in keywords[:5]) or "- Add more detailed notes to discover key concepts."
    questions = []
    for i, s in enumerate(sentences[:5], 1):
        words_in = re.findall(r'\b[A-Za-z][A-Za-z-]{4,}\b', s)
        target = next((w for w in words_in if w.lower() in keywords), None)
        if target:
            masked = re.sub(re.escape(target), "________", s, count=1, flags=re.I)
            questions.append(f"{i}. Fill in the blank: {masked}\n   Answer: {target}")
        else:
            questions.append(f"{i}. Explain this idea in your own words: “{s}”")
    plan = f"""1. **Understand (5 minutes):** Read the key ideas and explain them aloud at {level} level.
2. **Connect (5 minutes):** Choose two key concepts ({', '.join(keywords[:2]) if keywords else 'from your notes'}) and describe their relationship.
3. **Apply (10 minutes):** Answer the practice prompts without looking at the notes.
4. **Reflect (2 minutes):** Write one thing you understand and one question you still have.
Goal: {goal}."""
    return {
        "plain_explanation": f"Here is a simple first-pass explanation based on your notes:\n\n{summary}\n\nRewrite each bullet in your own words. This local demo extracts sentences; it does not verify facts.",
        "key_concepts": concept_lines,
        "practice_questions": "\n\n".join(questions) or "Add a few complete sentences to generate practice questions.",
        "study_plan": plan,
        "mode": "Local demo (text analysis)"
    }

def gemini_generate(notes, level, goal, api_key):
    import urllib.request
    prompt = f"""You are StudyForge, a careful educational tutor. Help a student understand rather than memorize.
Student level: {level}
Learning goal: {goal}
Study notes:
{notes}

Return valid JSON only with exactly these string fields:
plain_explanation: explain the ideas in simple language, avoid inventing facts, flag ambiguity.
key_concepts: identify 3-6 key concepts and explain how at least two connect.
practice_questions: give 5 questions with answers hidden after each question using 'Answer:' on the next line; mix recall, why, and application.
study_plan: a realistic 20-30 minute plan that uses active recall and application.
Keep it supportive and concise."""
    payload = {"contents":[{"parts":[{"text":prompt}]}], "generationConfig":{"responseMimeType":"application/json","temperature":0.4}}
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + api_key,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type":"application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=45) as response:
        data = json.loads(response.read().decode("utf-8"))
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    result = json.loads(text)
    result["mode"] = "Gemini generative AI"
    return result

col1, col2 = st.columns([1.25, 0.75])
with col1:
    notes = st.text_area("1. Paste your study notes", height=250, placeholder="Example: Friction is the force that opposes relative motion between surfaces in contact...")
with col2:
    level = st.selectbox("2. Explanation level", ["Beginner", "High-school", "College / undergraduate"])
    goal = st.selectbox("3. Your learning goal", ["Understand the concept", "Prepare for an exam", "Apply concepts to a real problem", "Revise quickly"])
    st.info("Tip: use your own class notes or a short topic summary. Avoid personal or confidential information.")

if st.button("✨ Forge my learning kit", type="primary", use_container_width=True):
    if len(notes.strip()) < 80:
        st.warning("Please paste at least a few complete sentences (about 80 characters) so the results are useful.")
    else:
        with st.spinner("Building your learning kit..."):
            try:
                if api_key.strip():
                    result = gemini_generate(notes, level, goal, api_key.strip())
                else:
                    result = fallback_generate(notes, level, goal)
                st.session_state["studyforge_result"] = result
                st.session_state["studyforge_notes"] = notes
            except Exception as e:
                st.error("The AI request failed. Check your API key or internet connection. Showing local text-analysis results instead.")
                st.session_state["studyforge_result"] = fallback_generate(notes, level, goal)
                st.session_state["studyforge_notes"] = notes

result = st.session_state.get("studyforge_result")
if result:
    st.divider()
    st.success("Your learning kit is ready • " + result.get("mode", ""))
    tabs = st.tabs(["📘 Understand", "🔗 Connect concepts", "📝 Practice", "🗓️ Study plan"])
    with tabs[0]:
        st.markdown("### Explain it simply")
        st.markdown(result.get("plain_explanation", ""))
    with tabs[1]:
        st.markdown("### Concept connections")
        st.markdown(result.get("key_concepts", ""))
    with tabs[2]:
        st.markdown("### Practice questions")
        st.markdown(result.get("practice_questions", ""))
        st.caption("Try answering before revealing each answer or looking back at your notes.")
    with tabs[3]:
        st.markdown("### Your next 20–30 minutes")
        st.markdown(result.get("study_plan", ""))
    export = "# StudyForge AI — Your Learning Kit\n\n" + "\n\n".join([
        "## Understand\n" + result.get("plain_explanation", ""),
        "## Connect concepts\n" + result.get("key_concepts", ""),
        "## Practice\n" + result.get("practice_questions", ""),
        "## Study plan\n" + result.get("study_plan", "")
    ])
    st.download_button("⬇️ Download learning kit (.md)", export, file_name="studyforge_learning_kit.md")
    st.caption("Educational aid only. Review AI-generated content against trusted course material.")

st.divider()
st.markdown("**Built for ForgeHacks 2026 · AI + Education**  \nStudyForge turns notes into explanations, concept links, practice, and an actionable plan.")
