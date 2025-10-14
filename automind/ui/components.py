"""Common UI components shared across modes."""

import streamlit as st
from typing import Dict, Any


class UIComponents:
    """Reusable UI components."""
    
    @staticmethod
    def display_ai_explanation_guessing(strategy: str):
        """Display AI explanation for guessing mode.
        
        Args:
            strategy: AI strategy being used ('entropy' or 'gini')
        """
        with st.sidebar.expander("AI Concepts in Action", expanded=False):
            st.markdown("### Current AI Processing:")
            st.write(f"**Strategy:** {strategy.title()}")
            
            if strategy == "entropy":
                st.write("**Algorithm:** Information Gain (Entropy Reduction)")
                st.write("- Selects questions that maximize information gain")
                st.write("- Minimizes uncertainty in belief state")
            else:
                st.write("**Algorithm:** Gini Impurity Reduction")
                st.write("- Selects questions that minimize classification error")
                st.write("- Reduces impurity in candidate set")
            
            st.markdown("### AI Components:")
            st.write("1. **Knowledge Base:** 1,050 cars with attributes")
            st.write("2. **Inference Engine:** Forward & backward chaining")
            st.write("3. **Belief State:** Bayesian probability distribution")
            st.write("4. **Question Selection:** Information theory")
            st.write("5. **Constraint Satisfaction:** Logical consistency")
            st.write("6. **Rule-based Reasoning:** If-then rules")
            
            st.markdown("### Each Answer Updates:")
            st.write("- Probability distribution over 1,050 cars")
            st.write("- Derived facts via forward chaining")
            st.write("- Next question via information maximization")
    
    @staticmethod
    def display_ai_explanation_recommendation():
        """Display AI explanation for recommendation mode."""
        with st.sidebar.expander("AI Concepts in Action", expanded=False):
            st.markdown("### Recommendation AI Processing:")
            
            st.write("**Algorithm:** Content-Based Filtering")
            st.write("- Multi-criteria decision making")
            st.write("- Attribute-based matching")
            st.write("- Probability scoring")
            
            st.markdown("### AI Components:")
            st.write("1. **Preference Parser:** Maps user inputs")
            st.write("2. **Expert System:** Applies preferences as evidence")
            st.write("3. **Belief State:** Scores all 1,050 cars")
            st.write("4. **Ranking Algorithm:** Sorts by match score")
            st.write("5. **Filter:** Returns top N matches")
            
            st.markdown("### Processing Steps:")
            st.write("1. Parse user preferences")
            st.write("2. Map to database attributes")
            st.write("3. Apply as high-confidence evidence")
            st.write("4. Update probabilities for all cars")
            st.write("5. Rank by score")
            st.write("6. Return top 10")
    
    @staticmethod
    def display_session_log(interactions: list):
        """Display session interaction log.
        
        Args:
            interactions: List of interaction dictionaries
        """
        if interactions:
            with st.sidebar.expander("Session Log", expanded=False):
                q_num = 1
                for entry in interactions:
                    # Skip non-question entries (like feedback results)
                    if 'question' not in entry:
                        continue
                    
                    st.write(f"**Q{q_num}:** {entry['question']}")
                    st.write(f"→ {entry['answer']}")
                    st.write("---")
                    q_num += 1
    
    @staticmethod
    def display_car_details(details: Dict[str, Any]):
        """Display car details in a formatted view.
        
        Args:
            details: Dictionary of car attributes
        """
        with st.expander("Car Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Brand:** {details.get('brand', 'N/A')}")
                st.write(f"**Body Type:** {details.get('body_type', 'N/A').upper()}")
                st.write(f"**Fuel Type:** {details.get('fuel_type', 'N/A').title()}")
            with col2:
                st.write(f"**Price Range:** {details.get('price_range', 'N/A')}")
                st.write(f"**Luxury:** {'Yes' if details.get('luxury') else 'No'}")
                st.write(f"**Engine:** {details.get('engine_cc', 'N/A')} cc")
    
    @staticmethod
    def display_performance_metrics(performance: Dict[str, Any]):
        """Display session performance metrics.
        
        Args:
            performance: Dictionary of performance metrics
        """
        st.sidebar.subheader("Performance Metrics")
        st.sidebar.metric("Questions Asked", performance['questions_asked'])
        st.sidebar.metric("Time Taken", f"{performance['session_duration_seconds']:.1f}s")
        st.sidebar.metric("Final Confidence", f"{performance['final_confidence']:.1%}")


__all__ = ['UIComponents']
