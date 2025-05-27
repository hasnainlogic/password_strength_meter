import streamlit as st
import re
import random
import string

# Page configuration
st.set_page_config(
    page_title="Password Strength Coach",
    page_icon="🔐",
    layout="centered"
)

def check_password_criteria(password):
    """
    Analyze password based on security criteria and return detailed results
    """
    criteria = {
        'length': len(password) >= 8,
        'uppercase': bool(re.search(r"[A-Z]", password)),
        'lowercase': bool(re.search(r"[a-z]", password)),
        'digits': bool(re.search(r"\d", password)),
        'special': bool(re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password))
    }
    
    score = sum(criteria.values())
    return criteria, score

def get_strength_level(score):
    """
    Determine password strength level based on score
    """
    if score <= 2:
        return "Weak", "🔴"
    elif score <= 4:
        return "Moderate", "🟡"
    else:
        return "Strong", "🟢"

def get_empathetic_feedback(criteria, score, password_length):
    """
    Provide human-centered, encouraging feedback
    """
    strength, emoji = get_strength_level(score)
    
    feedback = {
        "title": f"{emoji} Your password strength: {strength}",
        "messages": [],
        "encouragement": ""
    }
    
    if score == 5:
        feedback["encouragement"] = "🎉 Excellent work! Your password meets all security standards. You're doing great at protecting your digital life!"
        feedback["messages"].append("✅ Your password is strong and secure!")
        
    elif score >= 3:
        feedback["encouragement"] = "👍 You're on the right track! Your password has good security features, but we can make it even stronger together."
        
        if not criteria['length']:
            feedback["messages"].append("💡 Consider making it at least 8 characters long - think of it as giving your password more armor!")
        if not criteria['uppercase']:
            feedback["messages"].append("💡 Adding an uppercase letter (A-Z) will boost your security significantly.")
        if not criteria['lowercase']:
            feedback["messages"].append("💡 Including lowercase letters (a-z) helps create a more robust password.")
        if not criteria['digits']:
            feedback["messages"].append("💡 A number (0-9) would add an extra layer of protection.")
        if not criteria['special']:
            feedback["messages"].append("💡 A special character (!@#$%^&*) would make hackers' job much harder.")
            
    else:
        feedback["encouragement"] = "🌱 Every strong password starts somewhere! Let's work together to build you a more secure password step by step."
        
        if password_length < 4:
            feedback["messages"].append("🚀 Let's start by making it longer - aim for at least 8 characters. You've got this!")
        elif not criteria['length']:
            feedback["messages"].append("📏 You're close! Just a few more characters to reach the 8-character sweet spot.")
            
        if not criteria['uppercase'] and not criteria['lowercase']:
            feedback["messages"].append("🔤 Try mixing uppercase (A-Z) and lowercase (a-z) letters - it's like adding different colors to your password palette!")
        elif not criteria['uppercase']:
            feedback["messages"].append("⬆️ Adding an uppercase letter will give your password more personality and security!")
        elif not criteria['lowercase']:
            feedback["messages"].append("⬇️ Some lowercase letters would balance out your password nicely!")
            
        if not criteria['digits']:
            feedback["messages"].append("🔢 Numbers are your friends! Adding one (0-9) makes your password much harder to guess.")
            
        if not criteria['special']:
            feedback["messages"].append("✨ Special characters (!@#$%^&*) are like secret ingredients - they make everything stronger!")
    
    return feedback

def generate_strong_password():
    """
    Generate a human-friendly strong password
    """
    # Create a password with a memorable pattern but strong security
    lowercase = random.choices(string.ascii_lowercase, k=3)
    uppercase = random.choices(string.ascii_uppercase, k=2)
    digits = random.choices(string.digits, k=2)
    special = random.choices("!@#$%^&*", k=1)
    
    # Combine and shuffle
    password_chars = lowercase + uppercase + digits + special
    random.shuffle(password_chars)
    
    return ''.join(password_chars)

def display_strength_meter(score):
    """
    Display visual strength meter
    """
    progress = score / 5.0
    
    if score <= 2:
        color = "🔴"
        bar_color = "#ff4444"
    elif score <= 4:
        color = "🟡"
        bar_color = "#ffaa00"
    else:
        color = "🟢"
        bar_color = "#44ff44"
    
    st.progress(progress)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<div style='text-align: center; font-size: 1.2em;'>{color} {score}/5 Security Points</div>", 
                   unsafe_allow_html=True)

def main():
    """
    Main application function
    """
    # Header
    st.title("🔐 Password Strength Coach")
    st.markdown("### Your friendly guide to creating secure passwords!")
    
    st.markdown("""
    <div style='background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
    👋 Hi there! I'm here to help you create a strong, secure password. 
    Think of me as your personal cybersecurity coach - I'm here to support you, not judge you!
    </div>
    """, unsafe_allow_html=True)
    
    # Password input
    password = st.text_input(
        "Enter your password:",
        type="password",
        placeholder="Type your password here...",
        help="Don't worry, your password stays private and secure!"
    )
    
    if password:
        # Analyze password
        criteria, score = check_password_criteria(password)
        
        # Display strength meter
        st.markdown("---")
        st.subheader("📊 Password Strength Analysis")
        display_strength_meter(score)
        
        # Get and display feedback
        feedback = get_empathetic_feedback(criteria, score, len(password))
        
        st.markdown("---")
        st.subheader(feedback["title"])
        
        # Encouragement message
        if feedback["encouragement"]:
            st.markdown(f"""
            <div style='background-color: #e8f5e8; padding: 15px; border-radius: 10px; margin: 10px 0;'>
            {feedback["encouragement"]}
            </div>
            """, unsafe_allow_html=True)
        
        # Specific feedback messages
        if feedback["messages"]:
            st.markdown("#### 💬 Here's how we can improve:")
            for message in feedback["messages"]:
                st.markdown(f"• {message}")
        
        # Detailed criteria breakdown
        st.markdown("---")
        st.subheader("🔍 Security Checklist")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Length & Characters:**")
            st.markdown(f"{'✅' if criteria['length'] else '❌'} At least 8 characters ({len(password)} current)")
            st.markdown(f"{'✅' if criteria['uppercase'] else '❌'} Uppercase letters (A-Z)")
            st.markdown(f"{'✅' if criteria['lowercase'] else '❌'} Lowercase letters (a-z)")
        
        with col2:
            st.markdown("**Numbers & Symbols:**")
            st.markdown(f"{'✅' if criteria['digits'] else '❌'} Numbers (0-9)")
            st.markdown(f"{'✅' if criteria['special'] else '❌'} Special characters (!@#$%^&*)")
        
        # Password generator for weak passwords
        if score < 4:
            st.markdown("---")
            st.subheader("🎯 Need a helping hand?")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("If you're feeling stuck, I can suggest a strong password for you!")
            
            with col2:
                if st.button("Generate Strong Password 🎲", type="primary"):
                    suggested_password = generate_strong_password()
                    st.success(f"Here's a strong password suggestion: **{suggested_password}**")
                    st.info("💡 Feel free to modify this suggestion to make it more memorable for you!")
    
    else:
        # Welcome message when no password is entered
        st.markdown("""
        <div style='text-align: center; padding: 40px; background-color: #f9f9f9; border-radius: 15px; margin: 20px 0;'>
        <h3>🌟 Ready to create a strong password?</h3>
        <p>Enter your password above and I'll help you make it as secure as possible!</p>
        <p><em>Remember: A strong password is your first line of defense in the digital world.</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tips section
        st.markdown("---")
        st.subheader("💡 Quick Security Tips")
        
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.markdown("""
            **What makes a password strong:**
            - 🔢 At least 8 characters long
            - 🔤 Mix of upper & lowercase
            - 🔢 Include numbers
            - ✨ Add special characters
            """)
        
        with tips_col2:
            st.markdown("""
            **Pro tips for better security:**
            - 🚫 Avoid personal information
            - 🔄 Use unique passwords for each account
            - 📱 Consider a password manager
            - 🔐 Enable two-factor authentication
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em; padding: 20px;'>
    🔒 Your password is processed locally and never stored or shared. Stay safe online! 💙
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
