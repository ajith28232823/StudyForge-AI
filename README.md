# StudyForge AI — Learn beyond memorization

**ForgeHacks 2026 track:** AI + Education

StudyForge is a student-focused learning assistant. A learner pastes class notes and chooses their level and goal. The app creates:
1. A plain-language explanation
2. Key concepts and suggested connections
3. Practice questions
4. A short active-learning plan

The goal is to help learners understand concepts, make connections, and apply what they learn—not just memorize answers.

## Features
- Streamlit web interface
- Generative AI mode powered by Gemini API (optional API key)
- Local text-analysis fallback mode, so the prototype can be demonstrated without an API key
- Downloadable learning kit
- Clear note-processing/privacy notice

## Run locally
Requires Python 3.10+.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local address printed by Streamlit.

## Enable generative AI
1. Get your own Gemini API key from Google AI Studio.
2. Run the app and paste the key into the optional sidebar field.
3. Paste notes and click **Forge my learning kit**.

Do not commit API keys to GitHub. Notes are sent to Google's Gemini API only when a key is entered. Without a key, the app uses local text analysis; that mode is a demo fallback and is not a generative AI model.

## Technology
- Python
- Streamlit
- Regular-expression-based sentence and keyword extraction for fallback mode
- Google Gemini API for optional generative explanation, concept links, practice questions, and planning

## Architecture
Student notes + learning preferences → Streamlit interface → (Gemini API when configured / local text-analysis fallback) → explanation, concept links, questions, plan → Markdown download.

## Limitations and responsible use
- AI output can be incorrect or incomplete. Compare explanations and answers with course materials.
- The fallback mode extracts text patterns and does not independently understand or verify facts.
- Do not paste private, medical, or confidential information.
- This is a learning aid, not a replacement for teachers or official academic guidance.

## Demo checklist
1. Paste 2–4 paragraphs of class notes.
2. Select **College / undergraduate** and **Apply concepts to a real problem**.
3. Click **Forge my learning kit**.
4. Show the explanation, concept connections, questions, and study plan.
5. Download the Markdown learning kit.

## Hackathon submission checklist
- [ ] Confirm this project matches the current official track prompt.
- [ ] Test the app and capture real screenshots.
- [ ] Push the project code to a public GitHub repository.
- [ ] Record and publish a 2–4 minute demo video.
- [ ] Add the real GitHub, demo video, and optional deployment links to Devpost.
- [ ] List all actual team members.
