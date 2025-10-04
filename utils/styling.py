import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling matching the provided image design"""
    
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Root Variables - Matching the dark theme from image */
    :root {
        --primary-purple: #667eea;
        --secondary-purple: #764ba2;
        --accent-teal: #4ecdc4;
        --accent-green: #2ea043;
        --dark-bg: #0d1117;
        --card-bg: #161b22;
        --card-border: #30363d;
        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;
        --text-muted: #656d76;
        --button-bg: #21262d;
        --button-border: #30363d;
        --success: #238636;
        --warning: #d29922;
        --error: #da3633;
        --feature-personalized: #f093fb;
        --feature-ai: #4ecdc4;
        --feature-guided: #667eea;
    }
    
    /* Global App Styling */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hero Section - Matching image header */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 24px 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
        opacity: 0.1;
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: rgba(255,255,255,0.9);
        font-weight: 400;
        margin-bottom: 0;
    }
    
    /* Main Container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* Welcome Section - Exactly matching the image */
    .welcome-section {
        margin: 2rem 0;
    }
    
    .welcome-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 3rem 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .welcome-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(78, 205, 196, 0.05) 100%);
        pointer-events: none;
    }
    
    .welcome-header {
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .rocket-emoji {
        font-size: 3rem;
        display: block;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .welcome-description {
        font-size: 1.125rem;
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Features Grid - Matching the three cards from image */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .feature-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0;
        transition: opacity 0.3s ease;
        border-radius: 12px;
    }
    
    .feature-card.personalized::before {
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%);
    }
    
    .feature-card.ai-powered::before {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.1) 0%, rgba(68, 160, 141, 0.1) 100%);
    }
    
    .feature-card.guided::before {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: var(--primary-purple);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }
    
    .feature-card.personalized .feature-title {
        color: var(--feature-personalized);
    }
    
    .feature-card.ai-powered .feature-title {
        color: var(--feature-ai);
    }
    
    .feature-card.guided .feature-title {
        color: var(--feature-guided);
    }
    
    .feature-desc {
        color: var(--text-secondary);
        line-height: 1.5;
        font-size: 1rem;
    }
    
    /* Action Section */
    .action-section {
        margin: 3rem 0;
    }
    
    /* Stats Section */
    .stats-section {
        margin: 3rem 0 2rem 0;
    }
    
    .stat-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(78, 205, 196, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: var(--primary-purple);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-purple);
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    /* Page Header */
    .page-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .page-subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Form Sections */
    .form-section {
        margin: 2rem 0 1rem 0;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .section-desc {
        color: var(--text-secondary);
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    /* Success Section */
    .success-section {
        background: linear-gradient(135deg, rgba(46, 160, 67, 0.1) 0%, rgba(78, 205, 196, 0.1) 100%);
        border: 1px solid rgba(46, 160, 67, 0.3);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .success-section h3 {
        color: var(--accent-teal);
        margin-bottom: 1rem;
    }
    
    .profile-summary, .top-skills {
        background: rgba(255,255,255,0.02);
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid var(--card-border);
    }
    
    .profile-summary h4, .top-skills h4 {
        color: var(--primary-purple);
        margin-bottom: 1rem;
    }
    
    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-purple) 0%, var(--secondary-purple) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Form Elements */
    .stSelectbox > div > div, .stTextInput > div > div > input {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    .stRadio > div {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .stCheckbox > label {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        margin: 0.25rem !important;
        transition: all 0.3s ease !important;
        color: var(--text-primary) !important;
    }
    
    .stCheckbox > label:hover {
        background: var(--button-bg) !important;
        border-color: var(--primary-purple) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    .streamlit-expanderContent {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--card-bg) 0%, var(--dark-bg) 100%) !important;
    }
    
    /* Alert Styling */
    .stAlert > div {
        background: rgba(46, 160, 67, 0.1) !important;
        border: 1px solid rgba(46, 160, 67, 0.3) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
    }
    
    .stError > div {
        background: rgba(218, 54, 51, 0.1) !important;
        border: 1px solid rgba(218, 54, 51, 0.3) !important;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .welcome-title {
            font-size: 2rem;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .welcome-card {
            padding: 2rem 1rem;
        }
        
        .rocket-emoji {
            font-size: 2rem;
        }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .welcome-card, .feature-card, .stat-card {
        animation: fadeInUp 0.6s ease-out;
        animation-fill-mode: both;
    }
    
    .feature-card:nth-child(1) { animation-delay: 0.1s; }
    .feature-card:nth-child(2) { animation-delay: 0.2s; }
    .feature-card:nth-child(3) { animation-delay: 0.3s; }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

    # Add these styles to your existing CSS in utils/styling.py

additional_css = """
/* About Hacktoberfest Section */
.about-hacktoberfest {
    background: linear-gradient(135deg, rgba(16, 21, 34, 0.8) 0%, rgba(22, 27, 34, 0.9) 100%);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 3rem 2rem;
    margin: 3rem 0;
    position: relative;
    overflow: hidden;
}

.about-hacktoberfest::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23667eea' fill-opacity='0.03'%3E%3Cpath d='M20 20c0 11.046-8.954 20-20 20v-40c11.046 0 20 8.954 20 20z'/%3E%3C/g%3E%3C/svg%3E") repeat;
    opacity: 0.1;
}

.about-header {
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    z-index: 1;
}

.about-title {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #4ecdc4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}

.about-content {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 3rem;
    position: relative;
    z-index: 1;
}

.about-main .about-description {
    font-size: 1.125rem;
    line-height: 1.7;
    color: var(--text-secondary);
    margin-bottom: 2rem;
}

.about-features {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
    margin-bottom: 3rem;
}

.about-feature {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.5rem;
    background: rgba(102, 126, 234, 0.05);
    border-radius: 12px;
    border: 1px solid rgba(102, 126, 234, 0.1);
}

.feature-number {
    font-size: 2rem;
    min-width: 60px;
    text-align: center;
}

.about-feature h4 {
    color: var(--primary-purple);
    margin-bottom: 0.5rem;
    font-size: 1.25rem;
}

.about-feature p {
    color: var(--text-secondary);
    margin: 0;
}

.about-benefits h3 {
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    font-size: 1.5rem;
}

.benefits-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
}

.benefit-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
    background: rgba(78, 205, 196, 0.05);
    border-radius: 8px;
    border-left: 3px solid var(--accent-teal);
}

.benefit-icon {
    font-size: 1.5rem;
    min-width: 30px;
}

.benefit-text {
    color: var(--text-secondary);
    line-height: 1.5;
}

/* Sidebar Cards */
.about-sidebar {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.timeline-card, .stats-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 1.5rem;
}

.timeline-card h4, .stats-card h4 {
    color: var(--primary-purple);
    margin-bottom: 1rem;
    font-size: 1.125rem;
}

.timeline {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.timeline-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    border-radius: 6px;
    background: rgba(102, 126, 234, 0.05);
}

.timeline-item.active {
    background: rgba(78, 205, 196, 0.1);
    border-left: 3px solid var(--accent-teal);
}

.timeline-date {
    font-weight: 600;
    color: var(--primary-purple);
}

.timeline-desc {
    color: var(--text-secondary);
}

.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--card-border);
}

.stat-row:last-child {
    border-bottom: none;
}

.stat-row .stat-number {
    font-weight: 700;
    color: var(--accent-teal);
}

.stat-row .stat-label {
    color: var(--text-secondary);
}

/* Mentor Help Section */
.mentor-help-section {
    margin: 4rem 0;
    padding: 3rem 0;
}

.mentor-header {
    text-align: center;
    margin-bottom: 3rem;
}

.mentor-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
}

.mentor-subtitle {
    font-size: 1.125rem;
    color: var(--text-secondary);
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
}

.mentor-steps {
    display: grid;
    grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr;
    gap: 1rem;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
}

.step-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 2rem 1.5rem;
    text-align: center;
    position: relative;
    transition: all 0.3s ease;
}

.step-card:hover {
    transform: translateY(-4px);
    border-color: var(--primary-purple);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
}

.step-number {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--primary-purple) 0%, var(--secondary-purple) 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: white;
    margin: 0 auto 1rem auto;
    font-size: 1.25rem;
}

.step-card h3 {
    color: var(--text-primary);
    margin-bottom: 1rem;
    font-size: 1.25rem;
}

.step-card p {
    color: var(--text-secondary);
    line-height: 1.5;
    font-size: 0.9rem;
}

.step-arrow {
    color: var(--primary-purple);
    font-size: 1.5rem;
    font-weight: bold;
}

/* Hero Badge */
.hero-badge {
    margin-top: 1rem;
}

.badge-text {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
}

/* Responsive Design */
@media (max-width: 1024px) {
    .mentor-steps {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    
    .step-arrow {
        transform: rotate(90deg);
        margin: 1rem 0;
    }
    
    .about-content {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
}

@media (max-width: 768px) {
    .about-hacktoberfest {
        padding: 2rem 1rem;
    }
    
    .about-title {
        font-size: 2rem;
    }
    
    .mentor-title {
        font-size: 2rem;
    }
    
    .step-card {
        padding: 1.5rem 1rem;
    }
    
    .hero-title {
        font-size: 2.5rem;
    }
    
    .about-feature {
        flex-direction: column;
        text-align: center;
    }
}
"""
