
import streamlit as st
import string
import re

st.set_page_config(
    page_title="Password Analyzer",
    page_icon="🔐",
    layout="centered"
)

# Simple CSS design

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --purple: #7c3aed;
    --blue: #4f6cf7;
    --lavender: #f1edff;
    --text: #24213b;
    --muted: #77758f;
    --border: #e8e3f5;
}

.stApp {
    background: linear-gradient(135deg, #f8f7ff 0%, #eef3ff 100%);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 850px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Headings */
h1 {
    color: #5434a5 !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    letter-spacing: -1.2px;
}

h2, h3 {
    color: #30264f !important;
    font-weight: 700 !important;
}

/* Supporting text */
p, label, .stMarkdown {
    color: var(--text);
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.92);
    padding: 24px;
    border-radius: 18px;
    border: 1px solid var(--border);
    margin: 16px 0;
    box-shadow: 0 8px 24px rgba(81, 61, 150, 0.06);
}

/* Password input */
div[data-testid="stTextInput"] input {
    background: #ffffff;
    color: #24213b;
    border: 1px solid #dcd5f1;
    border-radius: 12px;
    min-height: 46px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: var(--purple);
    box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.12);
}

/* Buttons */
div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(100deg, #7c3aed, #4f6cf7);
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 46px;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(100deg, #6d28d9, #4058df);
    color: white;
    box-shadow: 0 5px 16px rgba(99, 74, 220, 0.2);
    transform: translateY(-1px);
}

/* Strength progress bar */
div[data-testid="stProgress"] > div {
    background: #e7e0fa;
    border-radius: 20px;
    height: 10px;
}

div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #a78bfa, #6366f1, #4f6cf7);
    border-radius: 20px;
}

/* Score metrics */
div[data-testid="stMetric"] {
    background: #f8f6ff;
    border: 1px solid #ebe5ff;
    padding: 16px;
    border-radius: 14px;
}

div[data-testid="stMetricLabel"] {
    color: #77708f;
}

div[data-testid="stMetricValue"] {
    color: #6338c7;
    font-weight: 750;
}

/* Separators */
hr {
    border-color: #e8e3f5;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #8985a3;
    font-size: 12px;
    padding-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# Header

st.markdown("""
<div style="text-align:center; padding: 10px 0 25px 0;">
    <div style="
        display:inline-block;
        background:#e8e0ff;
        color:#6d42c2;
        padding:7px 14px;
        border-radius:30px;
        font-size:12px;
        font-weight:600;
        letter-spacing:1px;
        margin-bottom:14px;">
        🔒  PASSWORD SECURITY
    </div>
    <h1 style="
        font-size:42px;
        background:linear-gradient(90deg,#7c3aed,#4f6cf7);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        margin-bottom:8px;">
        Password Analyzer
    </h1>
    <p style="color:#77758f; font-size:16px;">
        Understand your password strength. Stay one step ahead.
    </p>
</div>
""", unsafe_allow_html=True)


# Password input
with st.form("password_form"):
    password = st.text_input(
        "Enter a test password",
        type="password",
        placeholder="Enter your password..."
    )
    submitted = st.form_submit_button(
        "🔍 Analyze Password",
        use_container_width=True
    )

if submitted:
    if not password:
        st.warning("Please enter a password.")
    else:
        score = 0
        tips = []
        checks = []

        # Length check
        if len(password) >= 16:
            score += 40
            checks.append(("Length (16+ characters)", True))
        elif len(password) >= 12:
            score += 30
            checks.append(("Length (12–15 characters)", True))
            tips.append("Consider using at least 16 characters.")
        elif len(password) >= 8:
            score += 20
            checks.append(("Password length", False))
            tips.append("Use a longer password.")
        else:
            score += 5
            checks.append(("Password length", False))
            tips.append("Your password is too short.")

        # Character variety
        categories = {
            "Lowercase letters": any(c.islower() for c in password),
            "Uppercase letters": any(c.isupper() for c in password),
            "Numbers": any(c.isdigit() for c in password),
            "Special characters": any(c in string.punctuation for c in password)
        }

        score += sum(categories.values()) * 10

        for name, present in categories.items():
            checks.append((name, present))

        # Common password check
        common = {
            "password", "password123", "123456",
            "qwerty", "admin", "admin123", "monkey",
            "11111111", "iloveyou", "secret", 
            "mainahibataunga", "welcome", "football",
            "abc123", "sunshine", "motherfather"
        }

        if password.lower() in common:
            score = min(score, 10)
            checks.append(("Common password", False))
            tips.append("Avoid common passwords.")
        else:
            checks.append(("Common password examples", True))

        # Repeated characters
        if re.search(r"(.)\1{2,}", password):
            score -= 10
            checks.append(("Repeated characters", False))
            tips.append("Avoid repeating the same character many times.")
        else:
            checks.append(("Repeated characters", True))

        # Sequential patterns
        patterns = ["1234", "abcd", "qwerty"]

        if any(p in password.lower() for p in patterns):
            score -= 10
            checks.append(("Predictable sequence", False))
            tips.append("Avoid predictable sequences like 1234.")
        else:
            checks.append(("Predictable sequences", True))

        score = max(0, min(score, 100))

        # Strength label
        if score < 25:
            strength = "Very Weak"
            color = "#dc2626"
        elif score < 45:
            strength = "Weak"
            color = "#ea580c"
        elif score < 65:
            strength = "Moderate"
            color = "#ca8a04"
        elif score < 85:
            strength = "Strong"
            color = "#2563eb"
        else:
            strength = "Very Strong"
            color = "#16a34a"

        # Score card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Password Strength")

        col1, col2 = st.columns(2)
        col1.metric("Security Score", f"{score}/100")
        col2.metric("Strength", strength)

        st.progress(score / 100)

        st.markdown(
            f"<p style='color:{color};font-weight:bold'>"
            f"{strength}</p>",
            unsafe_allow_html=True
        )
        st.caption("This is a basic educational score, not a guarantee of security.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Password checks
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Password Checks")

        for name, passed in checks:
            symbol = "✅" if passed else "⚠️"
            st.write(f"{symbol} {name}")

        st.markdown('</div>', unsafe_allow_html=True)

        # Suggestions
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💡 Suggestions")

        if tips:
            for tip in dict.fromkeys(tips):
                st.write(f"• {tip}")
        else:
            st.success("No basic warning patterns detected.")

        st.write("• Use a unique password for every account.")
        st.write("• Enable two-factor authentication.")

        st.markdown('</div>', unsafe_allow_html=True)

st.caption("Educational project | Use fictional passwords for testing.")
st.divider()
st.subheader("✨ Analysis Results")
