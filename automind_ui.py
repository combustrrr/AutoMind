#!/usr/bin/env python3
"""
AutoMind - Interactive Car Recommendation System
Streamlit-based UI for demo
"""

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print("Streamlit not available. Install with: pip install streamlit")

from nlp_engine import extract_features
from guessing_engine import GuessingEngine


def main():
    """Main Streamlit app."""
    
    # Page config
    st.set_page_config(
        page_title="AutoMind - Car Recommender",
        page_icon="🚗",
        layout="wide"
    )
    
    # Title
    st.title("🚗 AutoMind - Intelligent Car Recommendation System")
    st.markdown("### Describe the car you're looking for, and I'll find the perfect match!")
    
    # Initialize session state
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'engine' not in st.session_state:
        st.session_state.engine = GuessingEngine()
    
    # Sidebar with information
    with st.sidebar:
        st.header("📋 How it works")
        st.markdown("""
        1. **Describe** the car you want
        2. **AutoMind** extracts features using NLP
        3. **Get** personalized recommendations
        
        **Example queries:**
        - "A Toyota SUV under 20 lakhs"
        - "Luxury electric sedan"
        - "Cheap Maruti hatchback"
        - "Premium BMW above 50 lakhs"
        """)
        
        st.header("🎯 Supported Features")
        st.markdown("""
        - **Brand**: Toyota, Hyundai, BMW, etc.
        - **Type**: SUV, Sedan, Hatchback
        - **Fuel**: Petrol, Diesel, Electric
        - **Price**: Under 10L, 20-30L, etc.
        - **Luxury**: Premium or Budget
        """)
        
        if st.button("Clear History"):
            st.session_state.history = []
            st.experimental_rerun()
    
    # Main input area
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input(
            "Describe the car you're thinking of:",
            placeholder="e.g., A luxury sedan above 40 lakhs",
            key="user_input"
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary")
    
    # Process input
    if search_button and user_input:
        with st.spinner("Analyzing your query..."):
            # Extract features
            features = extract_features(user_input)
            
            # Find matches
            matches = st.session_state.engine.find_matches(features, top_n=5)
            
            # Store in history
            st.session_state.history.append({
                'query': user_input,
                'features': features,
                'matches': matches
            })
        
        # Display results
        st.markdown("---")
        st.subheader("🎯 Extracted Features")
        
        # Show extracted features in columns
        feat_cols = st.columns(5)
        feature_labels = {
            'brand': '🏢 Brand',
            'type': '🚙 Type',
            'fuel': '⛽ Fuel',
            'price_range': '💰 Price',
            'luxury': '⭐ Luxury'
        }
        
        for i, (key, label) in enumerate(feature_labels.items()):
            with feat_cols[i]:
                value = features.get(key)
                if value is not None:
                    if key == 'luxury':
                        value = "Yes" if value else "Budget"
                    st.metric(label, value)
                else:
                    st.metric(label, "Not specified", delta="")
        
        st.markdown("---")
        
        # Display matches
        if matches:
            st.subheader(f"🎉 Found {len(matches)} matches!")
            
            # Show top match prominently
            top_car, top_score = matches[0]
            
            st.markdown("### 🏆 Best Match:")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"## {top_car.get('brand', '')} {top_car.get('model', '')}")
                st.markdown(f"**Type:** {top_car.get('body_type', 'N/A')}")
                st.markdown(f"**Fuel:** {top_car.get('fuel_type', 'N/A')}")
                st.markdown(f"**Price Range:** {top_car.get('price_range', 'N/A').replace('_', ' ')}")
                st.markdown(f"**Luxury:** {top_car.get('luxury', 'N/A')}")
            
            with col2:
                st.metric("Match Score", f"{top_score}/100")
                confidence = "High" if top_score >= 50 else "Medium" if top_score >= 30 else "Low"
                st.info(f"Confidence: **{confidence}**")
            
            # Show other matches
            if len(matches) > 1:
                st.markdown("### 📋 Other Recommendations:")
                
                for car, score in matches[1:]:
                    with st.expander(f"{car.get('brand', '')} {car.get('model', '')} - Score: {score}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Type:** {car.get('body_type', 'N/A')}")
                        with col2:
                            st.write(f"**Fuel:** {car.get('fuel_type', 'N/A')}")
                        with col3:
                            st.write(f"**Price:** {car.get('price_range', 'N/A').replace('_', ' ')}")
        else:
            st.warning("😕 No strong matches found. Try providing more details!")
            
            # Suggest follow-up
            followup = st.session_state.engine.suggest_followup_question(features)
            st.info(f"💡 Suggestion: {followup}")
    
    # Show history
    if st.session_state.history:
        st.markdown("---")
        with st.expander("📜 Search History", expanded=False):
            for i, entry in enumerate(reversed(st.session_state.history), 1):
                st.markdown(f"**{i}.** {entry['query']}")
                if entry['matches']:
                    st.write(f"   → Found {len(entry['matches'])} matches")


if __name__ == "__main__":
    if STREAMLIT_AVAILABLE:
        main()
    else:
        print("Please install Streamlit: pip install streamlit")
        print("Then run: streamlit run automind_ui.py")
