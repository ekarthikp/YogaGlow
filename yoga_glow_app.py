"""
🧘 YogaGlow - Your Gentle Guide to Instagram Growth
A beautiful, beginner-friendly content creation companion for yoga instructors
"""

import streamlit as st
import google.generativeai as genai
from pytrends.request import TrendReq
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
from typing import List, Dict
import random
import sys
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use manual entry

# Import our yoga-specific discovery module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yoga_viral_discovery import YogaViralDiscovery, create_viral_analysis_prompt_yoga

# Page Configuration
st.set_page_config(
    page_title="🧘 YogaGlow - Your Content Companion",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Cormorant+Garamond:wght@300;400;500;600;700&display=swap');
    
    :root {
        --bg-dark: #0F172A;
        --bg-gradient: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #312E81 100%);
        --glass-bg: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --glass-highlight: rgba(255, 255, 255, 0.15);
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --accent-glow: #F59E0B;
        --accent-purple: #8B5CF6;
        --success-green: #10B981;
    }
    
    .stApp {
        background: var(--bg-gradient);
        font-family: 'Outfit', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3, .hero-title, .metric-number, .welcome-title, .idea-title {
        font-family: 'Cormorant Garamond', serif !important;
        color: var(--text-primary) !important;
    }
    
    p, .hero-subtitle, .metric-label, .welcome-text, li, .stMarkdown {
        font-family: 'Outfit', sans-serif !important;
        color: var(--text-secondary) !important;
    }

    /* Hero Section */
    .hero-header { 
        text-align: center; 
        padding: 60px 20px 40px; 
        margin-bottom: 30px;
        background: radial-gradient(circle at center, rgba(139, 92, 246, 0.15) 0%, transparent 70%);
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 300;
        letter-spacing: 0.1em;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        background: linear-gradient(90deg, #F59E0B, #FCD34D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glass Cards */
    .glow-card, .idea-card, .metric-glow, .week-card, .milestone-card, .welcome-box, .schedule-day, .tip-box {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    .glow-card:hover, .idea-card:hover {
        transform: translateY(-5px);
        background: var(--glass-highlight);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 40px 0 rgba(139, 92, 246, 0.2);
    }
    
    /* Metrics */
    .metric-number {
        font-size: 3rem;
        font-weight: 600;
        background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.9rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: var(--text-secondary);
    }

    /* Specific Component Styling */
    .idea-hook {
        background: rgba(245, 158, 11, 0.1);
        border-left: 3px solid var(--accent-glow);
        padding: 16px;
        border-radius: 0 12px 12px 0;
        font-style: italic;
        color: #FCD34D !important;
    }

    .week-number {
        background: linear-gradient(135deg, var(--accent-purple), #6366F1);
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.5rem;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
    }

    /* Streamlit Overrides */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent-purple) 0%, #4F46E5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9);
        border-right: 1px solid var(--glass-border);
    }
    
    section[data-testid="stSidebar"] h3 {
        color: var(--accent-glow) !important;
        font-size: 1.2rem;
        font-weight: 400;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 2rem;
    }

    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 8px;
        border: 1px solid var(--glass-border);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        border-radius: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--accent-glow), var(--accent-purple));
    }

    /* Hashtag Pill */
    .hashtag-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        color: var(--text-secondary);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 4px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .glow-card, .idea-card, .metric-glow { animation: fadeInUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); }
</style>
""", unsafe_allow_html=True)

# Session State - Load defaults from environment variables
if 'gemini_api_key' not in st.session_state:
    # Try st.secrets first (Streamlit Cloud), then fall back to env var
    try:
        st.session_state.gemini_api_key = st.secrets.get("GEMINI_API_KEY", os.getenv('GEMINI_API_KEY', ''))
    except:
        st.session_state.gemini_api_key = os.getenv('GEMINI_API_KEY', '')
if 'user_profile' not in st.session_state:
    # Try st.secrets first, then fall back to env var
    try:
        st.session_state.user_profile = {
            'name': st.secrets.get('USER_NAME', os.getenv('USER_NAME', '')),
            'followers': int(st.secrets.get('USER_FOLLOWERS', os.getenv('USER_FOLLOWERS', '260'))),
            'yoga_style': st.secrets.get('USER_YOGA_STYLE', os.getenv('USER_YOGA_STYLE', 'General/Vinyasa')),
            'lifestyle': st.secrets.get('USER_LIFESTYLE', os.getenv('USER_LIFESTYLE', 'full_time_job'))
        }
    except:
        st.session_state.user_profile = {
            'name': os.getenv('USER_NAME', ''),
            'followers': int(os.getenv('USER_FOLLOWERS', '260')),
            'yoga_style': os.getenv('USER_YOGA_STYLE', 'General/Vinyasa'),
            'lifestyle': os.getenv('USER_LIFESTYLE', 'full_time_job')
        }
if 'content_ideas' not in st.session_state:
    st.session_state.content_ideas = []
if 'viral_videos' not in st.session_state:
    st.session_state.viral_videos = None
if 'current_week' not in st.session_state:
    st.session_state.current_week = 1
if 'api_call_count' not in st.session_state:
    st.session_state.api_call_count = 0

# Security Configuration
MAX_API_CALLS_PER_SESSION = 25
MAX_INPUT_LENGTH = 200

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent prompt injection attacks."""
    if not user_input:
        return ""
    
    # Truncate to max length
    sanitized = user_input[:MAX_INPUT_LENGTH]
    
    # Remove dangerous patterns (case-insensitive)
    dangerous_patterns = [
        r'ignore\s+(all\s+)?previous\s+instructions?',
        r'ignore\s+above',
        r'disregard\s+(all\s+)?previous',
        r'system\s*:',
        r'assistant\s*:',
        r'user\s*:',
        r'<\s*script',
        r'</\s*script',
        r'\{\{.*\}\}',
        r'\[\[.*\]\]',
    ]
    
    import re
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    # Remove control characters but keep basic punctuation
    sanitized = ''.join(char for char in sanitized if char.isprintable() or char in '\n\t')
    
    # Escape angle brackets
    sanitized = sanitized.replace('<', '&lt;').replace('>', '&gt;')
    
    return sanitized.strip()

def check_rate_limit() -> bool:
    """Check if user has exceeded rate limit. Returns True if OK, False if blocked."""
    return st.session_state.api_call_count < MAX_API_CALLS_PER_SESSION

def increment_api_count():
    """Increment the API call counter."""
    st.session_state.api_call_count += 1

def get_remaining_calls() -> int:
    """Get remaining API calls for this session."""
    return max(0, MAX_API_CALLS_PER_SESSION - st.session_state.api_call_count)


def create_html_download(content: str, topic: str) -> str:
    """Create a downloadable HTML file from the generated content."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>YogaGlow Ideas for {topic}</title>
        <style>
            body {{
                font-family: system-ui, -apple-system, sans-serif;
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
                line-height: 1.6;
                color: #333;
                background-color: #f8fafc;
            }}
            .header {{
                text-align: center;
                padding-bottom: 30px;
                border-bottom: 2px solid #e2e8f0;
                margin-bottom: 30px;
            }}
            .logo {{
                font-size: 2rem;
                color: #8B5CF6;
                margin-bottom: 10px;
            }}
            .content-card {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }}
            h1, h2, h3 {{ color: #1e293b; }}
            .date {{ color: #64748b; font-size: 0.9rem; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">🧘 YogaGlow</div>
            <h1>Content Ideas: {topic}</h1>
            <div class="date">Generated on {timestamp}</div>
        </div>
        <div class="content-card">
            {content.replace(chr(10), '<br>')}
        </div>
    </body>
    </html>
    """
    return html


class TrendAnalyzer:
    def __init__(self):
        try:
            self.pytrends = TrendReq(hl='en-US', tz=360)
        except:
            self.pytrends = None
    
    def get_rising_yoga_topics(self, keyword: str = "yoga poses") -> List[Dict]:
        if not self.pytrends:
            return []
        try:
            self.pytrends.build_payload([keyword], timeframe='today 3-m')
            related = self.pytrends.related_queries()
            rising_topics = []
            
            # Terms to exclude (tech/laptop related)
            excluded_terms = ['lenovo', 'laptop', 'tablet', 'thinkpad', 'battery', 'charger', 'deal', 'specs', 'price', 'windows', 'keyboard']
            
            if keyword in related and related[keyword]['rising'] is not None:
                for _, row in related[keyword]['rising'].head(15).iterrows():
                    topic = row['query'].lower()
                    
                    # Skip if topic contains any excluded terms
                    if any(term in topic for term in excluded_terms):
                        continue
                        
                    growth = row['value']
                    score = 95 if isinstance(growth, str) and 'Breakout' in str(growth) else min(100, int(50 + (int(growth) / 10))) if str(growth).isdigit() else 50
                    rising_topics.append({'topic': row['query'], 'growth': growth, 'viral_potential': score})
                    
                    if len(rising_topics) >= 8:
                        break
                        
            return rising_topics
        except:
            return []


class GeminiContentGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
    
    def generate_yoga_content_ideas(self, sub_niche: str, user_profile: Dict, count: int = 5) -> str:
        lifestyle = user_profile.get('lifestyle', 'full_time_job')
        followers = user_profile.get('followers', 100)
        
        prompt = f"""You are a warm, supportive content coach helping a yoga instructor grow their Instagram.

**About this creator:**
- Current followers: ~{followers}
- Lifestyle: {lifestyle}
- Focus area: {sub_niche}

**Generate {count} content ideas that are:**
1. Achievable with just a smartphone
2. Require minimal editing
3. Can be filmed in 15-30 minutes
4. Authentic and connection-building

**For each idea provide:**

🎬 **Title**: (Catchy but genuine)
🪝 **Hook Script**: (First 3 seconds)
📝 **Full Script/Steps**: (Easy-to-follow)
⏱️ **Duration**: (Optimal length)
📱 **Filming Tips**: (Lighting, angles)
✨ **Why This Works**: (Simple explanation)
#️⃣ **Hashtags**: (5 hashtags)
🌟 **Difficulty**: Easy / Medium

Keep your tone warm, encouraging, and practical!"""
        
        try:
            return self.model.generate_content(prompt).text
        except Exception as e:
            return f"Error: {str(e)}"


def main():
    # Header
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🧘 YogaGlow</div>
        <div class="hero-subtitle">Your Gentle Guide to Instagram Growth</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🌸 Your Profile")
        
        # API key is loaded from secrets/env - just show status
        api_key = st.session_state.gemini_api_key
        if api_key:
            st.success("✨ AI Connected!")
        else:
            st.warning("⚠️ API key not configured. Add GEMINI_API_KEY to .streamlit/secrets.toml")
        
        st.markdown("### 🎯 About You")
        
        # Load defaults from session state (which pulls from env)
        default_profile = st.session_state.user_profile
        
        name = st.text_input("Your Name", value=default_profile.get('name', ''), placeholder="e.g., Sarah")
        followers = st.number_input("Current Followers", min_value=0, max_value=100000, value=default_profile.get('followers', 260), step=50)
        
        yoga_styles = ["General/Vinyasa", "Beginner-Friendly", "Flexibility", "Stress Relief", "Desk Yoga", "Yoga for Sleep"]
        default_style = default_profile.get('yoga_style', 'General/Vinyasa')
        style_index = yoga_styles.index(default_style) if default_style in yoga_styles else 0
        yoga_style = st.selectbox("Your Yoga Focus", yoga_styles, index=style_index)
        
        lifestyles = ["Working full-time job", "Stay-at-home parent", "Teaching yoga classes", "Full-time creator"]
        lifestyle = st.selectbox("Your Lifestyle", lifestyles)
        
        st.session_state.user_profile = {'name': name, 'followers': followers, 'yoga_style': yoga_style, 'lifestyle': lifestyle}
        
        st.markdown("---")
        st.markdown("### 📊 Your Journey")
        
        discovery = YogaViralDiscovery()
        milestones = discovery.get_growth_milestones(followers)
        next_milestone = next((m for m in milestones['milestones'] if m['target'] > followers), None)
        
        if next_milestone:
            progress = (followers / next_milestone['target']) * 100
            st.markdown(f"**Next Goal:** {next_milestone['target']} followers")
            st.progress(min(progress / 100, 1.0))
        
        st.markdown("---")
        quotes = [
            "Your next follower is looking for exactly what you teach 💫",
            "Every expert was once a beginner 🌱",
            "Your authenticity is your superpower ✨"
        ]
        st.info(random.choice(quotes))
        
        # Usage Counter
        st.markdown("---")
        remaining = get_remaining_calls()
        st.markdown(f"### 🔋 API Usage")
        st.markdown(f"**{remaining}/{MAX_API_CALLS_PER_SESSION}** generations remaining")
        st.progress(remaining / MAX_API_CALLS_PER_SESSION)
    
    # Main Content
    if not api_key:
        st.markdown("""
        <div class="welcome-box">
            <div class="welcome-emoji">🌿</div>
            <div class="welcome-title">Welcome to YogaGlow</div>
            <div class="welcome-text">
                I'm here to help you grow your yoga Instagram with authentic, achievable content ideas.
                <br><br><strong>To get started:</strong> Enter your Gemini API key in the sidebar (free from Google!)
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("🔑 How to get your free API key"):
            st.markdown("1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)\n2. Sign in with Google\n3. Create API Key\n4. Paste in sidebar")
        return
    
    discovery = YogaViralDiscovery()
    content_generator = GeminiContentGenerator(api_key)
    trend_analyzer = TrendAnalyzer()
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏠 Dashboard", "💡 Content Ideas", "📅 Weekly Plan", "📈 Growth Guide", "✍️ Caption Helper", "🔍 Trending"])
    
    # Dashboard Tab
    with tab1:
        name_display = st.session_state.user_profile.get('name', 'Friend')
        st.markdown(f"### Welcome back{', ' + name_display if name_display else ''}! 🌸")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-glow"><div class="metric-number">{followers}</div><div class="metric-label">Followers</div></div>', unsafe_allow_html=True)
        with col2:
            next_target = 250 if followers < 250 else 500 if followers < 500 else 1000
            st.markdown(f'<div class="metric-glow"><div class="metric-number">{next_target}</div><div class="metric-label">Next Goal</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-glow"><div class="metric-number">Week {st.session_state.current_week}</div><div class="metric-label">Content Plan</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-glow"><div class="metric-number">3</div><div class="metric-label">Posts/Week</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### ✨ Today's Focus")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="glow-card"><h4>📱 Content To-Do</h4><ul><li>Post 1 Reel</li><li>Add 2-3 Stories</li><li>Reply to comments within 1 hour</li></ul></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="glow-card"><h4>💬 Engagement (30 min)</h4><ul><li>Comment on 10 yoga accounts</li><li>Engage with 10 potential students</li><li>Connect with 10 similar creators</li></ul></div>', unsafe_allow_html=True)
        
        st.markdown("### 🎬 Quick Ideas")
        week_data = discovery.get_content_ideas_for_beginners(st.session_state.current_week)
        for i, idea in enumerate(week_data['ideas'][:3]):
            with st.expander(f"💡 {idea['title']}", expanded=i==0):
                st.markdown(f"**Hook:** *\"{idea['hook']}\"*")
                st.markdown(f"**Type:** {idea['type']} • **Duration:** {idea['duration']} • **Best Time:** {idea['best_time']}")
    
    # Content Ideas Tab
    with tab2:
        st.markdown("### 💡 Content Ideas Made For You")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            idea_type = st.selectbox("Content Type", ["🌅 Morning Yoga", "😰 Stress Relief", "🖥️ Desk Stretches", "🌙 Bedtime Yoga", "📚 Tips", "🎯 Beginner Flows", "✨ Other (Custom)"])
        with col2:
            num_ideas = st.slider("How many?", 3, 8, 5)
        
        # Show custom input if "Other" is selected
        custom_topic = ""
        if idea_type == "✨ Other (Custom)":
            custom_topic = st.text_input("Enter your focus topic:", placeholder="e.g., Yoga for Runners, Prenatal Yoga, Chair Yoga for Seniors")
        
        if st.button("✨ Generate Ideas", type="primary", use_container_width=True):
            if not check_rate_limit():
                st.error(f"🚫 You've reached the limit of {MAX_API_CALLS_PER_SESSION} generations per session. Please refresh the page to reset.")
            else:
                # Determine the sub-niche to use
                niche_map = {"🌅 Morning Yoga": "morning yoga", "😰 Stress Relief": "stress relief yoga", "🖥️ Desk Stretches": "desk yoga", "🌙 Bedtime Yoga": "sleep yoga", "📚 Tips": "yoga tips", "🎯 Beginner Flows": "beginner yoga"}
                
                if idea_type == "✨ Other (Custom)":
                    sanitized_topic = sanitize_input(custom_topic)
                    if sanitized_topic:
                        sub_niche = sanitized_topic
                    else:
                        st.warning("Please enter a valid topic!")
                        sub_niche = None
                else:
                    sub_niche = niche_map.get(idea_type, "yoga")
                
                if sub_niche:
                    with st.spinner("🧘 Creating personalized ideas..."):
                        ideas = content_generator.generate_yoga_content_ideas(sub_niche, st.session_state.user_profile, num_ideas)
                        st.session_state.content_ideas = ideas
                        increment_api_count()
        
        if st.session_state.content_ideas:
            st.markdown("---")
            
            # Download Button
            if st.session_state.content_ideas:
                topic = custom_topic if idea_type == "✨ Other (Custom)" else idea_type
                html_content = create_html_download(st.session_state.content_ideas, topic)
                st.download_button(
                    label="📥 Download Ideas as HTML",
                    data=html_content,
                    file_name=f"yoga_ideas_{topic.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html",
                    mime="text/html"
                )
            
            st.markdown(st.session_state.content_ideas)
        
        st.markdown("---")
        st.markdown("### 📋 Proven Templates")
        templates = discovery.content_formats
        for t in templates[:5]:
            with st.expander(f"📱 {t['name']} ({t['viral_potential']} potential)"):
                st.markdown(f"**What:** {t['description']}\n\n**Duration:** {t['duration']} • **Difficulty:** {t['difficulty']}")
    
    # Weekly Plan Tab
    with tab3:
        st.markdown("### 📅 Your 4-Week Content Journey")
        st.session_state.current_week = st.selectbox("Week", [1, 2, 3, 4], format_func=lambda x: f"Week {x}")
        week_data = discovery.get_content_ideas_for_beginners(st.session_state.current_week)
        
        st.markdown(f'<div class="week-card"><h3>Theme: {week_data["theme"]}</h3><p>{week_data["focus"]}</p></div>', unsafe_allow_html=True)
        
        for i, idea in enumerate(week_data['ideas']):
            st.markdown(f'<div class="idea-card"><div class="idea-title">{idea["title"]}</div><div class="idea-hook">🪝 "{idea["hook"]}"</div></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Script:** {idea['script']}\n\n**Equipment:** {idea['equipment']} • **Duration:** {idea['duration']} • **Best Time:** {idea['best_time']}")
            with col2:
                for tag in idea['hashtags']:
                    st.markdown(f'<span class="hashtag-pill">{tag}</span>', unsafe_allow_html=True)
            st.markdown("---")
    
    # Growth Guide Tab
    with tab4:
        st.markdown("### 📈 Your Growth Roadmap")
        milestones = discovery.get_growth_milestones(followers)
        
        st.markdown(f'<div class="glow-card" style="text-align:center;"><h3>Currently At</h3><div class="metric-number">{followers} followers</div></div>', unsafe_allow_html=True)
        
        for m in milestones['milestones'][:4]:
            achieved = followers >= m['target']
            color = "#A8E6CF" if achieved else "#E8C872" if m['target'] == next((x['target'] for x in milestones['milestones'] if x['target'] > followers), 0) else "#E0E0E0"
            st.markdown(f'<div class="milestone-card" style="border-left:4px solid {color};"><span class="milestone-target">🏆 {m["target"]:,}</span> followers<br><strong>Timeline:</strong> {m["timeframe"]}<br>{m["celebration"]}<br><em>Unlocks: {m["unlock"]}</em></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 💡 Growth Tactics")
        tactics = discovery.get_engagement_tactics()
        for t in tactics[:4]:
            st.markdown(f'<div class="glow-card"><h4>{t["tactic"]}</h4><p>{t["description"]}</p><small>⏱️ {t["time"]} | Impact: {t["impact"]}</small></div>', unsafe_allow_html=True)
    
    # Caption Helper Tab
    with tab5:
        st.markdown("### ✍️ Caption Generator")
        
        col1, col2 = st.columns(2)
        with col1:
            content_type = st.selectbox("Content type?", ["Tutorial", "Motivational", "Personal Story", "Quick Tip", "Behind the Scenes"])
        with col2:
            topic = st.text_input("What's the post about?", placeholder="e.g., Morning stretch for back pain")
        
        mood = st.select_slider("Vibe", options=["Professional", "Warm & Friendly", "Playful", "Peaceful", "Motivating"], value="Warm & Friendly")
        
        if st.button("✨ Generate Caption", type="primary"):
            if not check_rate_limit():
                st.error(f"🚫 You've reached the limit of {MAX_API_CALLS_PER_SESSION} generations per session. Please refresh to reset.")
            elif topic:
                sanitized_topic = sanitize_input(topic)
                if sanitized_topic:
                    with st.spinner("✍️ Writing..."):
                        prompt = f"Write a {mood.lower()} Instagram caption for a yoga instructor about: {sanitized_topic}. Type: {content_type}. 150-250 words, use 2-3 emojis, end with engagement question."
                        try:
                            response = content_generator.model.generate_content(prompt)
                            st.markdown('<div class="glow-card">', unsafe_allow_html=True)
                            st.write(response.text)
                            st.markdown('</div>', unsafe_allow_html=True)
                            increment_api_count()
                        except Exception as e:
                            st.error(str(e))
                else:
                    st.warning("Please enter a valid topic!")
            else:
                st.warning("Please enter a topic!")
    
    # Trending Tab
    with tab6:
        st.markdown("### 🔍 What's Trending")
        
        if st.button("🔄 Refresh Trends", type="primary"):
            with st.spinner("🔍 Scanning..."):
                st.session_state.viral_videos = discovery.get_trending_yoga_content(limit=5)
        
        if st.session_state.viral_videos:
            for i, v in enumerate(st.session_state.viral_videos):
                with st.expander(f"📱 {v['title']} - {v['viral_score']}/100", expanded=i==0):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Hook:** *\"{v['hook']}\"*\n\n**Format:** {v['content_pattern']} • **Duration:** {v['duration']}s\n\n**Why it worked:** {v['why_viral']}")
                    with col2:
                        st.markdown(f'<div class="metric-glow"><div class="metric-number">{v["views"]:,}</div><div class="metric-label">Views</div></div>', unsafe_allow_html=True)
        else:
            st.info("👆 Click Refresh to see trending yoga content!")
        
        st.markdown("---")
        rising = trend_analyzer.get_rising_yoga_topics("yoga poses")
        if rising:
            st.markdown("#### 📈 Rising Searches")
            cols = st.columns(4)
            for i, t in enumerate(rising[:8]):
                with cols[i % 4]:
                    st.markdown(f'<div class="metric-glow" style="padding:12px;"><p style="margin:0;font-weight:600;">{t["topic"]}</p><p style="color:#6B8A5E;margin:4px 0 0;">{t["viral_potential"]}/100</p></div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align:center;padding:20px;color:#6B8A5E;"><p style="font-family:Cormorant Garamond,serif;font-size:1.3rem;">🧘 YogaGlow</p><p style="font-size:0.85rem;">Built with love for yoga instructors starting their Instagram journey</p></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
