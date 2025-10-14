import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from automind import CarExpertSystem, RecommendationEngine, SessionLogger
from automind.ui.components import UIComponents

def main():
    """Main application entry point.
    
    Orchestrates the Streamlit UI for the car guessing expert system.
    """
    st.title("AutoMind: AI Car Expert System")
    
    # Mode selection
    mode = st.sidebar.radio(
        "Choose Mode:",
        ("Guessing Game (Akinator)", "Car Recommendation"),
        help="Guessing: Think of a car, I'll guess it. Recommendation: I'll suggest cars for you."
    )
    
    if mode == "Guessing Game (Akinator)":
        run_guessing_mode()
    else:
        run_recommendation_mode()

def run_guessing_mode():
    """Run the Akinator-style guessing game mode."""
    st.markdown("**Think of a car, and I'll try to guess it by asking you questions!**")
    
    # Get AI strategy selection from sidebar
    strategy = st.sidebar.selectbox(
        "AI Strategy:",
        ("entropy", "gini"),
        help="Choose the question selection algorithm"
    )
    
    # Display AI explanation in sidebar
    display_ai_explanation_guessing(strategy)

    # Initialize or retrieve expert system from session state
    expert_system = initialize_expert_system(strategy)

    if not st.session_state.session_started:
        display_start_screen()
    else:
        run_game_session(expert_system)
    
    # Display session log in sidebar
    display_session_log()

def display_ai_explanation_guessing(strategy: str):
    """Display explanation of AI happening in guessing mode."""
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

def run_recommendation_mode():
    """Run the car recommendation mode."""
    st.markdown("**Tell me what you're looking for, and I'll recommend the best cars!**")
    
    st.info("Answer a few questions about your preferences, and I'll suggest the perfect cars for you.")
    
    # Display AI explanation
    display_ai_explanation_recommendation()
    
    # Initialize recommendation state
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
        st.session_state.rec_preferences = {}
    
    # Collect user preferences
    with st.form("preferences_form"):
        st.subheader("What are you looking for?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            brand_pref = st.selectbox(
                "Brand Preference:",
                ["Any", "Toyota", "Honda", "Maruti Suzuki", "Hyundai", "Mahindra", 
                 "Tata", "Mercedes-Benz", "BMW", "Audi", "Other"]
            )
            
            body_pref = st.selectbox(
                "Body Type:",
                ["Any", "Hatchback", "Sedan", "SUV", "MUV"]
            )
            
            fuel_pref = st.selectbox(
                "Fuel Type:",
                ["Any", "Petrol", "Diesel", "Electric", "CNG", "Hybrid"]
            )
            
            era_pref = st.selectbox(
                "Era/Generation:",
                ["Any", "Current (2020+)", "Recent (2015-2019)", 
                 "Older (2010-2014)", "Classic (Pre-2010)"],
                help="Filter by model generation to get latest or older models"
            )
        
        with col2:
            budget_pref = st.selectbox(
                "Budget:",
                ["Any", "Under 5 Lakhs", "5-10 Lakhs", "10-20 Lakhs", 
                 "20-30 Lakhs", "Above 30 Lakhs"]
            )
            
            luxury_pref = st.selectbox(
                "Luxury Preference:",
                ["Any", "Yes, luxury/premium", "No, practical"]
            )
            
            usage_pref = st.selectbox(
                "Primary Usage:",
                ["Any", "City commuting", "Highway cruising", "Off-road/Adventure", 
                 "Family trips", "Business/Executive"]
            )
        
        submitted = st.form_submit_button("Find My Perfect Car", use_container_width=True)
        
        if submitted:
            # Store preferences
            st.session_state.rec_preferences = {
                'brand': brand_pref,
                'body_type': body_pref,
                'fuel_type': fuel_pref,
                'era': era_pref,
                'budget': budget_pref,
                'luxury': luxury_pref,
                'usage': usage_pref
            }
            
            # Log recommendation request
            log_recommendation_request(st.session_state.rec_preferences)
            
            # Get recommendations
            recommendations = get_recommendations(st.session_state.rec_preferences)
            st.session_state.recommendations = recommendations
            
            # Log recommendations result
            log_recommendation_result(recommendations)
    
    # Display recommendations
    if st.session_state.recommendations:
        display_recommendations(st.session_state.recommendations, st.session_state.rec_preferences)

def display_ai_explanation_recommendation():
    """Display explanation of AI happening in recommendation mode."""
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

def log_recommendation_request(preferences: dict):
    """Log recommendation request to file."""
    log_dir = Path("logs/recommendations")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"recommendation_{session_id}.json"
    
    log_entry = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "mode": "recommendation",
        "preferences": preferences
    }
    
    with open(log_file, 'w') as f:
        json.dump(log_entry, f, indent=2)
    
    # Store session_id for later updates
    st.session_state.rec_session_id = session_id
    st.session_state.rec_log_file = str(log_file)

def log_recommendation_result(recommendations: list):
    """Log recommendation results to the same session file."""
    if 'rec_log_file' not in st.session_state:
        return
    
    log_file = Path(st.session_state.rec_log_file)
    if log_file.exists():
        with open(log_file, 'r') as f:
            log_data = json.load(f)
        
        # Add results
        log_data['results'] = {
            'total_matches': len(recommendations),
            'top_10': [
                {
                    'rank': i+1,
                    'model': car['model'],
                    'score': car['score'],
                    'brand': car['brand'],
                    'body_type': car['body_type'],
                    'fuel_type': car['fuel_type']
                }
                for i, car in enumerate(recommendations[:10])
            ]
        }
        
        # AI explanation
        log_data['ai_processing'] = {
            'algorithm': 'Content-based filtering with multi-criteria matching',
            'steps': [
                '1. Parse user preferences',
                '2. Map preferences to database attributes',
                '3. Apply preferences as high-confidence evidence',
                '4. Update belief state probabilities for all 1050 cars',
                '5. Rank cars by match score',
                '6. Return top 10 matches'
            ],
            'ai_concepts_used': [
                'Expert System reasoning',
                'Content-based recommendation',
                'Multi-criteria decision making',
                'Probability-based ranking',
                'Attribute matching'
            ]
        }
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

def get_recommendations(preferences: dict) -> list:
    """Get car recommendations using the modular RecommendationEngine.
    
    Args:
        preferences: User preference dictionary
        
    Returns:
        List of recommended cars with details
    """
    engine = RecommendationEngine(strategy="entropy")
    recommendations = engine.get_recommendations(preferences)
    
    # Store AI info for logging
    st.session_state.ai_info = engine.get_ai_processing_info()
    
    return recommendations

def display_recommendations(recommendations: list, preferences: dict):
    """Display car recommendations in a nice format."""
    st.success(f"Found {len(recommendations)} cars matching your preferences!")
    
    # Show preferences summary
    with st.expander("Your Preferences", expanded=False):
        for key, value in preferences.items():
            if value != "Any":
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    # Display recommendations
    st.subheader("Recommended Cars")
    
    for i, car in enumerate(recommendations[:10], 1):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"### {i}. {car['model']}")
                st.write(f"**{car['brand']}** | {car['body_type']} | {car['fuel_type']}")
            
            with col2:
                st.metric("Match Score", f"{car['score']:.1%}")
            
            with col3:
                luxury_badge = "Luxury" if car['luxury'] else "Practical"
                st.write(luxury_badge)
                st.write(f"{car['price_range']}")
            
            st.divider()
    
    # Reset button
    if st.button("Try Different Preferences", use_container_width=True):
        st.session_state.recommendations = None
        st.session_state.rec_preferences = {}
        st.rerun()

def initialize_expert_system(strategy: str) -> CarExpertSystem:
    """Initialize the expert system in session state if needed."""
    if 'expert_system' not in st.session_state:
        st.session_state.expert_system = CarExpertSystem(strategy=strategy)
        st.session_state.expert_system.reset()
        st.session_state.session_started = False
        st.session_state.session_logger = SessionLogger(mode="guessing")
    
    return st.session_state.expert_system

def display_start_screen():
    """Display the initial start screen."""
    st.info("Think of any car from our database, and I'll ask you questions to guess which one it is!")
    if st.button("Start Game", type="primary", use_container_width=True):
        st.session_state.session_started = True
        st.rerun()

def run_game_session(expert_system: CarExpertSystem):
    """Run the active game session."""
    if expert_system.ready_to_guess():
        display_conclusion(expert_system)
    else:
        question = expert_system.next_question()
        if question:
            display_question(expert_system, question)
        else:
            display_conclusion(expert_system)

    # Show current top guesses in sidebar
    display_top_hypotheses(expert_system)

def display_top_hypotheses(expert_system: CarExpertSystem):
    """Display the current top hypotheses in the sidebar."""
    st.sidebar.subheader("Current Top Guesses")
    hypotheses = expert_system.hypotheses(5)
    for i, (model, prob) in enumerate(hypotheses, 1):
        st.sidebar.write(f"{i}. **{model}**: {prob:.1%}")

def display_question(expert_system, question):
    st.subheader(f"Question: {question.text}")
    
    # Create buttons for each option
    cols = st.columns(2)
    for idx, option in enumerate(question.options):
        col = cols[idx % 2]
        with col:
            if st.button(option.label, key=f"opt_{option.value}_{idx}", use_container_width=True):
                # Log the interaction using SessionLogger
                if 'session_logger' in st.session_state:
                    st.session_state.session_logger.log_question(
                        question.text,
                        option.label,
                        option.value
                    )
                
                expert_system.submit_answer(question.id, option.value, 1.0)
                st.rerun()

def display_session_log():
    """Display the session log in the sidebar using UIComponents."""
    if 'session_logger' in st.session_state:
        interactions = st.session_state.session_logger.get_interactions()
        UIComponents.display_session_log(interactions)

def display_ai_explanation_guessing(strategy: str):
    """Display AI explanation using UIComponents."""
    UIComponents.display_ai_explanation_guessing(strategy)

def display_ai_explanation_recommendation():
    """Display AI explanation using UIComponents."""
    UIComponents.display_ai_explanation_recommendation()

def log_recommendation_request(preferences: dict):
    """Log recommendation request using SessionLogger."""
    logger = SessionLogger(mode="recommendation")
    logger.log_preferences(preferences)
    st.session_state.rec_logger = logger

def log_recommendation_result(recommendations: list):
    """Log recommendation results using SessionLogger."""
    if 'rec_logger' in st.session_state and 'ai_info' in st.session_state:
        st.session_state.rec_logger.log_recommendations(
            recommendations,
            st.session_state.ai_info
        )

def save_session_log():
    """Save the current session log to a file."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"session_{st.session_state.session_id}.json"
    with open(log_file, 'w') as f:
        json.dump({
            "session_id": st.session_state.session_id,
            "interactions": st.session_state.interaction_log
        }, f, indent=2)

def display_session_log():
    """Display the session log in the sidebar."""
    if 'interaction_log' in st.session_state and st.session_state.interaction_log:
        with st.sidebar.expander("Session Log", expanded=False):
            q_num = 1
            for entry in st.session_state.interaction_log:
                # Skip non-question entries (like feedback results)
                if 'question' not in entry:
                    continue
                    
                st.write(f"**Q{q_num}:** {entry['question']}")
                st.write(f"→ {entry['answer']}")
                st.write("---")
                q_num += 1

def display_conclusion(expert_system):
    """Display the final conclusion or low-confidence state."""
    best_guess = expert_system.best_guess()
    
    # Always make a guess after questions are done
    if best_guess:
        display_guess_with_alternatives(expert_system, best_guess)
    else:
        display_uncertain_state(expert_system)

    display_restart_buttons()

def display_guess_with_alternatives(expert_system: CarExpertSystem, best_guess: dict):
    """Display best guess along with alternatives (Akinator style)."""
    confidence = best_guess['probability']
    
    if confidence > 0.5:
        st.success("I'm quite confident!")
    elif confidence > 0.15:
        st.info("I think it might be...")
    else:
        st.warning("I'm not very sure, but my best guess is...")
    
    st.markdown(f"## **{best_guess['model']}**")
    st.progress(min(confidence, 1.0))
    st.write(f"**Confidence:** {confidence:.1%}")
    
    # Show top alternatives
    hypotheses = expert_system.hypotheses(5)
    if len(hypotheses) > 1:
        with st.expander("Or could it be one of these?", expanded=confidence < 0.3):
            for i, (model, prob) in enumerate(hypotheses[1:], 2):
                st.write(f"{i}. **{model}**: {prob:.1%}")
    
    display_car_details(expert_system, best_guess['model'])
    display_performance_metrics(expert_system)
    
    # Ask for feedback
    st.markdown("---")
    st.subheader("Was I correct?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, correct!", use_container_width=True):
            st.balloons()
            st.success("Awesome! I guessed it right!")
            # Log success using SessionLogger
            if 'session_logger' in st.session_state:
                st.session_state.session_logger.log_result("correct", best_guess['model'])
    with col2:
        if st.button("No, wrong", use_container_width=True):
            st.session_state.show_feedback_form = True
            st.rerun()
    
    # Show feedback form if needed
    if st.session_state.get('show_feedback_form', False):
        st.markdown("### What car were you actually thinking of?")
        actual_car = st.text_input("Car name:", placeholder="e.g., Toyota Fortuner")
        if st.button("Submit"):
            if actual_car:
                # Log the miss using SessionLogger
                if 'session_logger' in st.session_state:
                    st.session_state.session_logger.log_result(
                        "incorrect",
                        best_guess['model'],
                        actual_car
                    )
                st.success(f"Thanks! I'll learn from this. You were thinking of: {actual_car}")
                st.session_state.show_feedback_form = False

def display_car_details(expert_system, model: str):
    """Display car details using UIComponents."""
    details = expert_system.describe_model(model)
    UIComponents.display_car_details(details)

def display_performance_metrics(expert_system):
    """Display performance metrics using UIComponents."""
    performance = expert_system.get_session_performance()
    UIComponents.display_performance_metrics(performance)

def display_restart_buttons():
    """Display restart and strategy change buttons."""
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again", type="primary", use_container_width=True):
            # Reset session
            st.session_state.expert_system.reset()
            st.session_state.session_started = False
            st.session_state.session_logger = SessionLogger(mode="guessing")
            st.session_state.show_feedback_form = False
            st.rerun()
    with col2:
        if st.button("Change Strategy", use_container_width=True):
            del st.session_state.expert_system
            st.session_state.session_started = False
            st.session_state.session_logger = SessionLogger(mode="guessing")
            st.session_state.show_feedback_form = False
            st.rerun()

if __name__ == "__main__":
    main()
