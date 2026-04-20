import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

        :root {
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.5);
            --secondary: #a855f7;
            --bg-body: #05060b;
            --card-bg: rgba(17, 18, 27, 0.8);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        }

        .stApp {
            background-color: var(--bg-body);
            background-image:
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.15) 0px, transparent 50%);
            color: var(--text-main);
            font-family: 'Space Grotesk', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.04em !important;
            color: var(--text-main) !important;
        }

        /* Glass Card */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
            margin-bottom: 1.5rem;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .glass-card:hover {
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 20px 60px rgba(99, 102, 241, 0.1);
        }

        /* Student Header — compact */
        .student-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 0.45rem 1rem;
            margin-bottom: 1rem;
        }
        .student-info { display: flex; flex-direction: column; }
        .student-name {
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 0.8rem;
            color: var(--text-main);
        }
        .student-meta {
            font-size: 0.65rem;
            color: var(--text-muted);
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .dept-badge {
            background: var(--accent-gradient);
            padding: 2px 10px;
            border-radius: 6px;
            font-weight: 800;
            font-size: 0.7rem;
            color: white;
        }

        /* Text areas */
        .stTextArea textarea {
            background: rgba(0, 0, 0, 0.2) !important;
            color: var(--text-main) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 14px !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            font-family: 'Space Grotesk', sans-serif !important;
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        .stTextArea textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.2) !important;
        }
        .stTextArea textarea:disabled {
            background: rgba(255, 255, 255, 0.02) !important;
            border-style: solid !important;
            color: #f8fafc !important;
            opacity: 1 !important;
        }

        /* Buttons */
        div.stButton > button {
            background: var(--accent-gradient);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 14px;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            transition: all 0.3s ease;
            width: 100%;
            min-height: 3rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
        }
        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 12px 28px rgba(99, 102, 241, 0.4);
            border: none;
            color: white;
        }

        /* Swap column: vertically center the button tightly */
        .swap-col {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            padding-top: 2.2rem;
        }

        /* Audio input */
        .stAudioInput { border-radius: 100px !important; }

        /* Title */
        .main-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }

        #MainMenu, footer, header { visibility: hidden; }

        /* Mobile responsive */
        @media (max-width: 768px) {
            .main-title { font-size: 2rem; }
            .student-header { justify-content: center; text-align: center; }
            .swap-col { padding-top: 0.5rem; padding-bottom: 0.5rem; }
            .stTextArea textarea { font-size: 0.95rem !important; }
        }
        </style>
    """, unsafe_allow_html=True)


def render_header(name, matric, dept):
    st.markdown(f"""
        <div class="student-header">
            <div class="student-info">
                <div class="student-meta">Project Owner</div>
                <div class="student-name">{name}</div>
            </div>
            <div style="text-align: right;">
                <div class="student-meta">Matric No.</div>
                <div class="student-name" style="font-family: monospace;">{matric}</div>
            </div>
            <div class="dept-badge">{dept}</div>
        </div>

        <div>
            <h1 class="main-title">AI VOICE TRANSLATOR</h1>
        </div>
    """, unsafe_allow_html=True)
