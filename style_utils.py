import streamlit as st

def inject_custom_css():
    """Injects custom CSS for a premium Cyber-Luxe Dark Mode theme."""
    st.markdown("""
        <style>
        /* Import Google Fonts */
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

        /* Base Styles */
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

        /* Glass Card - Enhanced for Dark Mode */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-card:hover {
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 20px 60px rgba(99, 102, 241, 0.1);
        }

        /* Student ID Card / Header Info */
        .student-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            margin-bottom: 2rem;
        }
        .student-info {
            display: flex;
            flex-direction: column;
        }
        .student-name {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text-main);
        }
        .student-meta {
            font-size: 0.7rem;
            color: var(--text-muted);
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .dept-badge {
            background: var(--accent-gradient);
            padding: 4px 12px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 0.8rem;
            color: white;
        }

        /* Input / Output Elements */
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.9) !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
            border-radius: 14px !important;
            padding: 1.25rem !important;
            font-size: 1.05rem !important;
            font-family: 'Space Grotesk', sans-serif !important;
            transition: all 0.3s ease;
        }

        .stTextArea textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.2) !important;
        }
        
        .stTextArea textarea:disabled {
            background: rgba(255, 255, 255, 0.02) !important;
            border-style: solid !important;
            color: var(--text-muted) !important;
            opacity: 1 !important;
        }

        /* Premium Buttons */
        div.stButton > button {
            background: var(--accent-gradient);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 14px;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            width: 100%;
            height: auto;
            min-height: 3.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
        }

        div.stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 15px 30px rgba(99, 102, 241, 0.4);
            border: none;
            color: white;
        }

        /* SWAP BUTTON: High-Visibility White Circle with Black Arrows */
        /* Using multiple selectors to ensure it beats Streamlit's emotion-cache */
        div[data-testid="stColumn"]:nth-child(2) button,
        div[data-testid="stColumn"]:nth-child(2) .stButton > button,
        div[data-testid="stColumn"]:nth-child(2) [data-testid="stBaseButton-secondary"] {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            color: #000000 !important;
            border-radius: 50% !important;
            clip-path: circle(50%) !important;
            width: 60px !important;
            height: 60px !important;
            min-height: 60px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 85px auto 0 auto !important; /* Reduced for tighter layout */
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
            transition: all 0.3s ease !important;
        }

        /* Ensure the arrow icon inside is black and centered - forcing multiple layers */
        div[data-testid="stColumn"]:nth-child(2) button p,
        div[data-testid="stColumn"]:nth-child(2) button div,
        div[data-testid="stColumn"]:nth-child(2) button span,
        div[data-testid="stColumn"]:nth-child(2) button i {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            margin: 0 !important;
            padding: 0 !important;
            font-size: 1.8rem !important;
            font-weight: 900 !important;
            line-height: 1 !important;
            background: transparent !important;
        }

        div[data-testid="stColumn"]:nth-child(2) button:hover {
            transform: scale(1.1) rotate(180deg) !important;
            background-color: #f0f0f0 !important;
            box-shadow: 0 0 20px var(--primary-glow) !important;
        }

        /* Support for dark/light context */
        @media (prefers-color-scheme: dark) {
            /* If the background is black, we use a white button with black arrows */
            /* This is already handled by the rules above */
        }

        /* Audio Input styling */
        .stAudioInput {
            border-radius: 100px !important;
        }

        /* Titles & Containers */
        .main-title {
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
        }
        .sub-title {
            color: var(--text-muted);
            text-align: center;
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }

        /* Hide Streamlit components */
        #MainMenu, footer, header {visibility: hidden;}
        
        /* Mobile adjustment */
        @media (max-width: 768px) {
            .main-title { font-size: 2.2rem; }
            .sub-title { font-size: 0.9rem; }
            .student-header { 
                flex-direction: column; 
                text-align: center; 
                gap: 15px; 
                padding: 1.5rem 1rem;
            }
            .student-info { align-items: center; }
            .student-header > div { text-align: center !important; }
            
            .glass-card { padding: 1.25rem; }
            
            /* Center and adjust swap button for mobile stack */
            div[data-testid="stColumn"]:nth-child(2) button {
                margin: 40px auto !important;
                width: 65px !important;
                height: 65px !important;
            }
            
            .stTextArea textarea {
                height: 180px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def render_header(name, matric, dept):
    """Renders the stylized student header and main title."""
    # Student Profile Header
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
