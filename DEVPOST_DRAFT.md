# StudyForge AI

## Short description
StudyForge AI turns a student's own study notes into a simple explanation, connected concepts, practice questions, and a short active-learning plan.

## Track
AI + Education

## Problem
Students often reread notes or memorize definitions without checking whether they understand how concepts connect or how to apply them. Many learners need a simple, low-friction way to turn their existing notes into active practice.

## Solution
StudyForge takes pasted notes and the learner's level and goal. With Gemini API configured, it uses generative AI to create a tailored explanation, concept relationships, practice questions, and a realistic study plan. A local text-analysis fallback allows a basic demo without an API key.

## Target users
High-school and college students, especially learners revising technical subjects.

## Technical approach
Python and Streamlit power the interface. The optional Gemini API provides generative tutoring. A lightweight local sentence/keyword extraction path provides fallback output. The app also exports the learning kit as Markdown.

## Impact
The prototype encourages active recall, concept linking, and application rather than passive rereading. It is designed to be inexpensive to test and easy to extend.

## Limitations
Generated content may be wrong and should be checked against trusted course material. The local fallback is text analysis, not a generative model. The prototype is not a replacement for a teacher.

## Links to add before submitting
- GitHub repository: [ADD YOUR PUBLIC REPOSITORY]
- Demo video (2–4 minutes): [ADD YOUR PUBLIC VIDEO]
- Live demo (optional): [ADD DEPLOYMENT LINK]
