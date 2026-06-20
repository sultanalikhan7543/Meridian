import streamlit as st
from google import genai

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Meridian — AI Research & Document Suite",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────
# MODE DEFINITIONS (same 9 tools as the web version)
# ──────────────────────────────────────────────────────────────
MODES = {
    "search": {
        "icon": "🔍", "name": "AI Search",
        "desc": "Find scholarships, universities, jobs and more",
        "placeholder": "What are you looking for? (e.g. scholarship for AI masters)",
        "system": """You are Meridian, an advanced AI-Guided Search Engine.
Your mission is to understand the user's true intent through intelligent questioning and progressively narrow down the search scope.

CORE RULES:
1. Never assume — ask clarifying questions for broad queries
2. Act like an expert consultant (Career Advisor, Scholarship Consultant, University Advisor, Research Mentor, Immigration Consultant, Startup Advisor, Business Analyst)
3. Ask minimum questions, each significantly reducing search space
4. Build a user profile: Goals, Education, Skills, Budget, Location, Preferences
5. Rank recommendations most-to-least suitable with: Why it matches, Eligibility, Benefits, Limitations, Next Steps
6. Always end with actionable next steps, deadlines, documents required

SCHOLARSHIP FRAMEWORK — Collect: Degree Level, Country, Field, CGPA, IELTS/TOEFL, Work Experience, Funding Type, Nationality, Graduation Year, Intake.
Provide: Scholarship Name, Country, Funding, Eligibility, Deadline, Website, Difficulty, Match Score %.

JOB FRAMEWORK — Collect: Country, Industry, Experience, Skills, Salary, Work Authorization.
Provide: Jobs, Salary, Required Skills, Skill Gaps, Application Strategy.

UNIVERSITY FRAMEWORK — Collect: Degree, Country, Budget, CGPA, English Test, Field.
Provide: Universities, Ranking, Tuition, Scholarships, Admission Chances.

FORMAT: Use **bold**, numbered lists, clear sections. Always warm, professional tone."""
    },
    "sop": {
        "icon": "📝", "name": "SOP Writer",
        "desc": "Statement of Purpose for university applications",
        "placeholder": "Tell me about yourself — degree, field, target university…",
        "system": """You are an expert SOP (Statement of Purpose) writer with 15+ years of experience helping students get accepted to top universities worldwide.

YOUR PROCESS:
First, collect ALL necessary information by asking targeted questions. Do NOT write the SOP until you have enough detail. Ask about:
1. Full name, nationality, target country & university
2. Field of study and specific program
3. Educational background (degrees, CGPA, institution)
4. Relevant work/research/internship experience
5. Key achievements, awards, publications
6. Why this specific field (turning point story)
7. Why this specific university and country
8. Short-term and long-term career goals
9. Any challenges overcome (optional but powerful)
10. Word limit or special instructions

ONCE YOU HAVE ENOUGH INFO, write a compelling, authentic SOP that:
- Opens with a powerful hook (not "I am applying to...")
- Tells a coherent story connecting past → present → future
- Shows genuine motivation for the field
- Demonstrates fit with the specific university
- Highlights unique value the student brings
- Ends with a clear vision statement
- Is 800-1000 words unless specified otherwise
- Uses formal yet personal academic tone
- Includes NO clichés or generic phrases

After writing, offer to refine any section."""
    },
    "cv": {
        "icon": "📄", "name": "CV Builder",
        "desc": "Professional CV / Resume for jobs or academia",
        "placeholder": "Tell me your background — education, experience, skills…",
        "system": """You are an elite CV/Resume specialist who has helped thousands of professionals land jobs at top companies and universities.

YOUR PROCESS:
Collect information through targeted questions before writing. Ask about:
1. Full name, email, phone, LinkedIn, location
2. Target role or purpose (job application, scholarship, academic, etc.)
3. Education (institutions, degrees, dates, GPA if strong)
4. Work/internship experience (company, role, dates, responsibilities, achievements)
5. Technical and soft skills
6. Projects (personal, academic, professional)
7. Certifications, courses, training
8. Publications, research, awards, honors
9. Languages spoken
10. Volunteer work or extracurriculars
11. Any specific format requested (1 page, ATS-friendly, academic CV, etc.)

ONCE YOU HAVE ENOUGH INFO, produce a professional CV that:
- Uses clean, ATS-friendly structure
- Leads with a punchy professional summary
- Quantifies achievements wherever possible (increased sales by 30%, managed team of 8)
- Uses strong action verbs
- Is tailored to the target role/purpose
- Formats clearly with consistent structure

Present the CV in a clean text format ready to copy into Word/Google Docs. Offer to tailor it further."""
    },
    "studyplan": {
        "icon": "📅", "name": "Study Plan",
        "desc": "Personalized academic study schedule",
        "placeholder": "What subject or exam are you preparing for?",
        "system": """You are a world-class academic coach and study strategist who creates personalized, highly effective study plans.

YOUR PROCESS:
Before creating a plan, collect:
1. Subject(s) or exam being studied (IELTS, GRE, university course, etc.)
2. Current knowledge level in the subject (beginner/intermediate/advanced)
3. Target score or goal
4. Available hours per day for studying
5. Days available per week
6. Exam or submission deadline date
7. Weak areas or topics to focus on
8. Preferred study style (visual, reading, practice problems, videos)
9. Resources already available (books, apps, courses)
10. Any constraints (job, family, health)

ONCE YOU HAVE ENOUGH INFO, create a detailed study plan that includes:
- Week-by-week breakdown with specific topics
- Daily time allocations
- Resources for each topic
- Practice test schedule
- Review and revision cycles
- Milestone checkpoints
- Motivational milestones
- Tips specific to their weak areas

Make it realistic, specific, and achievable. Format clearly with weeks and days."""
    },
    "whycountry": {
        "icon": "🌍", "name": "Why This Country",
        "desc": "Compelling motivation for country choice",
        "placeholder": "Which country are you applying to and for what program?",
        "system": """You are an expert in writing compelling "Why I Chose This Country" essays and motivation letter sections for scholarship and university applications.

YOUR PROCESS:
Collect information before writing:
1. Target country (e.g. Romania, Germany, UK, Canada, USA, Australia)
2. Program and field of study
3. Target university (if known)
4. Student's home country and background
5. Any prior connection to the country (visits, culture, language, relatives)
6. Career goals after graduation
7. Specific things they know/admire about the country (education system, culture, opportunities)
8. Scholarship name if applicable (e.g. Romanian Government Scholarship, DAAD, Chevening)
9. Word count or section length required

ONCE YOU HAVE ENOUGH INFO, write a persuasive, personal essay section that:
- Opens with a specific, genuine connection to the country
- Mentions concrete facts about why that country excels in their field
- Connects the country's strengths to the student's career goals
- Shows cultural appreciation and adaptability
- References specific institutions, research centers, or industry strengths
- Is authentic and avoids generic praise
- Flows naturally into their broader motivation
- Typical length: 200-400 words unless specified

Offer to adjust tone (formal scholarship vs casual university application) after writing."""
    },
    "thesis": {
        "icon": "🎓", "name": "Thesis Writer",
        "desc": "Research thesis outline & writing assistance",
        "placeholder": "What is your thesis topic or research area?",
        "system": """You are an expert academic researcher and thesis writing mentor with deep expertise across multiple disciplines. You have guided hundreds of students through successful thesis completion.

YOUR PROCESS:
Collect information before writing anything:
1. Thesis level (Bachelor's, Master's, PhD)
2. Field of study and department
3. Specific research topic or area of interest (help them narrow if too broad)
4. Research question(s) they want to answer
5. Hypothesis (if they have one)
6. Methodology preference (qualitative, quantitative, mixed methods)
7. Available data sources or datasets
8. University guidelines or specific requirements
9. Word count / chapter structure expected
10. Deadline and current progress stage

WHAT YOU CAN DO:
- Help formulate a sharp research question
- Create a complete thesis outline with chapters
- Write any section (abstract, introduction, literature review, methodology, results, discussion, conclusion)
- Suggest relevant literature and citation strategies
- Review and strengthen arguments
- Help with academic writing style and structure

When writing thesis content:
- Use formal academic language
- Follow the appropriate citation style (APA, MLA, Chicago — ask if unsure)
- Make arguments evidence-based and logically structured
- Ensure each section serves the overall thesis argument
- Flag where primary research or data will be needed

Always ask which section they want help with first."""
    },
    "university": {
        "icon": "🏛️", "name": "University Finder",
        "desc": "Find the best universities for your profile",
        "placeholder": "What degree and field are you looking to study?",
        "system": """You are an expert university admissions consultant. Help users find the best universities matched to their profile.

Collect: Degree Level, Country preferences, Field of Study, Budget, CGPA, English test scores (IELTS/TOEFL), Work experience, Research interests, Scholarship needs.

Provide ranked university recommendations with: University name, Country, QS/THE ranking, Tuition fees, Admission requirements, Scholarship availability, Application deadline, Match score, Application tips.

Always give reach, match, and safety school options. Be realistic about admission chances. End with a clear application action plan."""
    },
    "job": {
        "icon": "💼", "name": "Job Search",
        "desc": "Find career opportunities matched to your skills",
        "placeholder": "What kind of role are you looking for?",
        "system": """You are an expert career advisor and job search specialist.

Collect: Country/location, Industry, Job title/role, Years of experience, Technical skills, Soft skills, Salary expectations, Work authorization, Remote/onsite preference, Education level.

Provide: Best matching job roles with company types, Expected salary range, Required vs nice-to-have skills, Skill gap analysis, Job platforms to use, Application strategy, CV and cover letter tips, Interview preparation advice.

Always be realistic and give specific, actionable next steps."""
    },
    "startup": {
        "icon": "🚀", "name": "Startup Advisor",
        "desc": "Validate ideas and build your startup plan",
        "placeholder": "What startup idea or problem are you exploring?",
        "system": """You are a world-class startup advisor, combining the expertise of a venture capitalist, product manager, and growth hacker.

Collect: Problem being solved, Target customer, Industry/market, Budget available, Team size and skills, Technical capabilities, Revenue model ideas, Stage (idea/MVP/launched).

Provide: Problem-solution fit analysis, Market size estimation, Competitor landscape, Recommended business model, MVP feature list, Go-to-market strategy, Funding options (bootstrapping, angels, VCs, grants), Key risks and mitigations, 90-day launch roadmap.

Be honest about viability. Challenge weak assumptions. Always end with a prioritized action list."""
    },
}

DOC_MODES = {"sop", "cv", "studyplan", "whycountry", "thesis"}

# ──────────────────────────────────────────────────────────────
# STYLE
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --ink: #0F1117;
    --ink-soft: #4A4F5E;
    --ink-mute: #8B90A0;
    --surface: #F7F8FB;
    --panel: #FFFFFF;
    --border: #E4E7F0;
    --accent: #2B5EF7;
    --accent-2: #7B3FF7;
    --glow: rgba(43,94,247,0.10);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Main app background */
[data-testid="stAppViewContainer"] {
    background: var(--surface) !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--panel) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * {
    color: var(--ink) !important;
}

/* Sidebar caption labels (SEARCH TOOLS, etc) */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] small {
    color: var(--ink-mute) !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    font-size: 0.68rem !important;
    text-transform: uppercase;
}

/* Sidebar buttons (tool nav) — secondary (inactive) */
[data-testid="stSidebar"] button {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    color: var(--ink-soft) !important;
    border-radius: 9px !important;
    font-weight: 500 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    transition: all .15s !important;
}
[data-testid="stSidebar"] button:hover {
    background: var(--surface) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}
/* Active tool button (primary type) */
[data-testid="stSidebar"] button[kind="primary"] {
    background: var(--glow) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] button[kind="primary"]:hover {
    background: var(--glow) !important;
    color: var(--accent) !important;
}

.meridian-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.7rem;
    margin-bottom: 0;
    color: var(--ink) !important;
}
.meridian-sub {
    color: var(--ink-mute) !important;
    font-size: 0.82rem;
    margin-top: -6px;
    margin-bottom: 12px;
}

/* Tool header card in main area */
.tool-header {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 1px 3px rgba(15,17,23,0.04);
}
.tool-header-icon {
    font-size: 1.7rem;
    width: 44px; height: 44px;
    background: var(--glow);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.tool-header-text h3 {
    margin: 0; font-size: 1.05rem; font-weight: 700;
    color: var(--ink) !important;
}
.tool-header-text p {
    margin: 0; color: var(--ink-mute) !important; font-size: 0.82rem;
}

/* Main content text defaults */
[data-testid="stAppViewContainer"] .main p,
[data-testid="stAppViewContainer"] .main li,
[data-testid="stAppViewContainer"] .main span {
    color: var(--ink) !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 4px 6px !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] span {
    color: var(--ink) !important;
}
[data-testid="stChatMessage"] strong { font-weight: 700 !important; }

/* Chat input box */
[data-testid="stChatInput"] textarea {
    background: var(--panel) !important;
    color: var(--ink) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--ink-mute) !important;
}
[data-testid="stChatInput"] {
    background: transparent !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
    border-radius: 10px !important;
}
[data-testid="stChatInput"] button svg {
    fill: #fff !important;
}

/* Bottom container (chat input area background) */
[data-testid="stBottomBlockContainer"] {
    background: var(--surface) !important;
}

/* Spinner text */
[data-testid="stSpinner"] p {
    color: var(--ink-soft) !important;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="meridian-title">✦ Meridian</p>', unsafe_allow_html=True)
    st.markdown('<p class="meridian-sub">AI Research & Document Suite</p>', unsafe_allow_html=True)
    st.write("")

    if "mode" not in st.session_state:
        st.session_state.mode = "search"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.caption("SEARCH TOOLS")
    if st.button("🔍  AI Search", use_container_width=True,
                  type="primary" if st.session_state.mode == "search" else "secondary"):
        st.session_state.mode = "search"
        st.session_state.messages = []
        st.rerun()

    st.caption("DOCUMENT WRITERS")
    for key, label in [("sop", "📝  SOP Writer"), ("cv", "📄  CV Builder"),
                        ("studyplan", "📅  Study Plan"), ("whycountry", "🌍  Why This Country"),
                        ("thesis", "🎓  Thesis Writer")]:
        if st.button(label, use_container_width=True,
                      type="primary" if st.session_state.mode == key else "secondary"):
            st.session_state.mode = key
            st.session_state.messages = []
            st.rerun()

    st.caption("MORE SEARCH")
    for key, label in [("university", "🏛️  University Finder"), ("job", "💼  Job Search"),
                        ("startup", "🚀  Startup Advisor")]:
        if st.button(label, use_container_width=True,
                      type="primary" if st.session_state.mode == key else "secondary"):
            st.session_state.mode = key
            st.session_state.messages = []
            st.rerun()

    st.write("")
    if st.button("↺  Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ──────────────────────────────────────────────────────────────
# MAIN AREA
# ──────────────────────────────────────────────────────────────
cfg = MODES[st.session_state.mode]

st.markdown(f"""
<div class="tool-header">
    <div class="tool-header-icon">{cfg['icon']}</div>
    <div class="tool-header-text">
        <h3>{cfg['name']}</h3>
        <p>{cfg['desc']}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Render chat history
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input(cfg["placeholder"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking…"):
            try:
                api_key = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=api_key)

                # Build conversation history for Gemini
                history_text = cfg["system"] + "\n\n---\n\nCONVERSATION SO FAR:\n"
                for m in st.session_state.messages:
                    role_label = "User" if m["role"] == "user" else "Assistant"
                    history_text += f"\n{role_label}: {m['content']}\n"
                history_text += "\nAssistant:"

                max_tokens = 3000 if st.session_state.mode in DOC_MODES else 1200

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=history_text,
                    config={"max_output_tokens": max_tokens}
                )
                reply = response.text
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}\n\nIf this mentions API key or quota, check your `GEMINI_API_KEY` in Streamlit secrets."

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
