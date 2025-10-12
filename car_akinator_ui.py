#!/usr/bin/env python3
"""
Car Akinator UI - Interactive Streamlit interface
Think of a car and let the AI guess it by asking strategic questions!
"""

try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    print("Streamlit not available. Install with: pip install streamlit")

from car_akinator import CarAkinator

def main():
    """Main Streamlit app for Car Akinator."""
    
    # Page config
    st.set_page_config(
        page_title="Car Akinator - Guess Your Car!",
        page_icon="🔮",
        layout="centered"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .answer-button {
        width: 100%;
        margin: 0.5rem 0;
    }
    .game-stats {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🔮 Car Akinator</h1>
        <h3>I Can Read Your Mind!</h3>
        <p>Think of any Indian car and I'll guess it! 🚗✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'akinator' not in st.session_state:
        st.session_state.akinator = CarAkinator()
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    
    # Sidebar with game info
    with st.sidebar:
        st.header("🎯 Car Akinator")
        
        if st.session_state.game_started and not st.session_state.game_over:
            st.subheader("📊 Live Stats")
            
            # Current game stats
            total_cars = len(st.session_state.akinator.cars)
            remaining = len(st.session_state.akinator.remaining_cars)
            progress = (total_cars - remaining) / total_cars
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Questions", st.session_state.akinator.question_count)
            with col2:
                st.metric("Cars Left", remaining)
            
            st.progress(progress, text=f"{progress*100:.0f}% Complete")
            
            # Show recent questions
            if st.session_state.game_history:
                st.markdown("**Recent Questions:**")
                recent = st.session_state.game_history[-3:]  # Last 3 questions
                for i, (q, a) in enumerate(recent, 1):
                    color = "🟢" if a.lower() == "yes" else "🔴" if a.lower() == "no" else "🟡"
                    st.caption(f"{color} {q[:30]}... → **{a}**")
        
        else:
            st.markdown("""
            **How to Play:**
            1. 🤔 Think of any Indian car
            2. ✅ Answer questions with Yes/No  
            3. 🎯 Watch me narrow it down
            4. 🎉 Be amazed when I guess it!
            
            **Database:** 50+ cars  
            **Average:** 5-7 questions
            """)
        
        st.markdown("---")
        if st.button("🔄 New Game", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.game_over = False
            st.session_state.current_question = None
            st.session_state.game_history = []
            st.rerun()
    
    # Main game area
    if not st.session_state.game_started:
        # Game start screen
        st.markdown("---")
        
        # Make the start screen more prominent
        st.markdown("""
        <div class="question-box">
        <h2 style="text-align: center; color: #667eea;">🎮 Ready to Start?</h2>
        <p style="text-align: center; font-size: 1.2em;">Think of any car and let the magic begin!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Instructions in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📝 Instructions:
            - **Think** of any Indian car
            - **Any brand**: Maruti, Toyota, BMW, etc.
            - **Any type**: Hatchback, Sedan, SUV  
            - **Any price**: Budget to Luxury
            """)
        
        with col2:
            st.markdown("""
            ### 🎯 How it works:
            - I'll ask **strategic questions**
            - Answer with **Yes/No/Don't Know**
            - I'll **narrow down** the possibilities
            - **Guess your car** in 5-7 questions!
            """)
        
        # Prominent start button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 START PLAYING NOW!", type="primary", key="start_game", use_container_width=True):
                st.session_state.akinator.start_game()
                st.session_state.game_started = True
                st.session_state.game_over = False
                st.session_state.current_question = st.session_state.akinator.get_best_question()
                st.rerun()
        
        # Sample cars
        st.markdown("---")
        st.markdown("### 💡 Example cars I can guess:")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info("🚗 **Budget**\n\nMaruti Swift\nHyundai i20\nTata Tiago")
        with col2:
            st.info("🚙 **Family**\n\nToyota Innova\nHonda City\nHyundai Creta") 
        with col3:
            st.info("🏎️ **Premium**\n\nBMW X1\nAudi Q3\nMercedes GLA")
        with col4:
            st.info("⚡ **Electric**\n\nTata Nexon EV\nMG ZS EV\nHyundai Kona")
    
    elif st.session_state.game_over:
        # Game over screen - Make the final guess VERY prominent
        st.markdown("---")
        
        # Show final result
        result = st.session_state.akinator.make_final_guess()
        
        # Make the final result super prominent
        if "I've got it!" in result:
            st.balloons()
            st.markdown("""
            <div style="text-align: center; background: linear-gradient(90deg, #28a745, #20c997); 
                       color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0;">
                <h1>🎉 I'VE GOT IT! 🎉</h1>
                <h2>I successfully guessed your car!</h2>
            </div>
            """, unsafe_allow_html=True)
        elif "down to" in result:
            st.markdown("""
            <div style="text-align: center; background: linear-gradient(90deg, #fd7e14, #ffc107); 
                       color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0;">
                <h1>🤔 SO CLOSE!</h1>
                <h2>I narrowed it down to a few possibilities!</h2>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; background: linear-gradient(90deg, #dc3545, #e74c3c); 
                       color: white; padding: 2rem; border-radius: 15px; margin: 2rem 0;">
                <h1>😅 YOU STUMPED ME!</h1>
                <h2>That was a tough one!</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Display the detailed result in a prominent box
        st.markdown(f"""
        <div class="question-box">
        {result.replace('**', '<strong>').replace('**', '</strong>').replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        # Show game summary
        st.markdown("---")
        st.subheader("📊 Game Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Questions", st.session_state.akinator.question_count)
        with col2:
            st.metric("Final Cars", len(st.session_state.akinator.remaining_cars))
        with col3:
            total_cars = len(st.session_state.akinator.cars)
            remaining = len(st.session_state.akinator.remaining_cars)
            accuracy = ((total_cars - remaining) / total_cars * 100)
            st.metric("Accuracy", f"{accuracy:.1f}%")
        with col4:
            efficiency = "Excellent" if st.session_state.akinator.question_count <= 6 else "Good"
            st.metric("Efficiency", efficiency)
        
        # Show Q&A history
        if st.session_state.game_history:
            st.markdown("### 💭 Question History")
            for i, (question, answer) in enumerate(st.session_state.game_history, 1):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**Q{i}:** {question}")
                with col2:
                    color = "🟢" if answer.lower() == "yes" else "🔴" if answer.lower() == "no" else "🟡"
                    st.write(f"{color} **{answer.title()}**")
    
    else:
        # Active game screen - Make it much more prominent!
        if st.session_state.current_question:
            attribute, question = st.session_state.current_question
            
            # Progress indicator
            total_cars = len(st.session_state.akinator.cars)
            remaining = len(st.session_state.akinator.remaining_cars)
            progress = (total_cars - remaining) / total_cars
            
            st.progress(progress, text=f"🎯 Narrowed down to {remaining} cars from {total_cars}")
            
            # Question display - Make it HUGE and prominent
            question_num = st.session_state.akinator.question_count + 1
            
            st.markdown(f"""
            <div class="question-box">
            <h2 style="color: #667eea; text-align: center;">❓ Question {question_num}</h2>
            <h1 style="color: #333; text-align: center; font-size: 2.5em; margin: 1rem 0;">{question}</h1>
            </div>
            """, unsafe_allow_html=True)
            
            # Large, prominent answer buttons
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("✅ YES", type="primary", key="yes_btn", use_container_width=True, 
                           help="Click if the answer is YES"):
                    st.session_state.game_history.append((question, "Yes"))
                    continue_game = st.session_state.akinator.process_answer("yes", st.session_state.current_question)
                    if not continue_game:
                        st.session_state.game_over = True
                    else:
                        st.session_state.current_question = st.session_state.akinator.get_best_question()
                    st.rerun()
            
            with col2:
                if st.button("❌ NO", type="secondary", key="no_btn", use_container_width=True,
                           help="Click if the answer is NO"):
                    st.session_state.game_history.append((question, "No"))
                    continue_game = st.session_state.akinator.process_answer("no", st.session_state.current_question)
                    if not continue_game:
                        st.session_state.game_over = True
                    else:
                        st.session_state.current_question = st.session_state.akinator.get_best_question()
                    st.rerun()
            
            with col3:
                if st.button("🤷 DON'T KNOW", key="dk_btn", use_container_width=True,
                           help="Click if you're not sure"):
                    st.session_state.game_history.append((question, "Don't Know"))
                    continue_game = st.session_state.akinator.process_answer("don't know", st.session_state.current_question)
                    if not continue_game:
                        st.session_state.game_over = True
                    else:
                        st.session_state.current_question = st.session_state.akinator.get_best_question()
                    st.rerun()
            
            # Game stats in a nice box
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="game-stats">
            <h4>📊 Game Progress</h4>
            <p><strong>Questions Asked:</strong> {st.session_state.akinator.question_count}</p>
            <p><strong>Cars Remaining:</strong> {remaining} out of {total_cars}</p>
            <p><strong>Progress:</strong> {progress*100:.1f}% complete</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show previous questions if any
            if st.session_state.game_history:
                with st.expander("📜 Previous Questions", expanded=False):
                    for i, (prev_q, prev_a) in enumerate(st.session_state.game_history, 1):
                        col1, col2 = st.columns([5, 1])
                        with col1:
                            st.write(f"**Q{i}:** {prev_q}")
                        with col2:
                            color = "🟢" if prev_a.lower() == "yes" else "🔴" if prev_a.lower() == "no" else "🟡"
                            st.write(f"{color} {prev_a}")
        else:
            st.error("No more questions available. Something went wrong!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🔮 <strong>Car Akinator</strong> - Powered by strategic questioning and car database intelligence<br>
        Think of any Indian market car and let the magic begin! ✨
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    if STREAMLIT_AVAILABLE:
        main()
    else:
        print("Please install Streamlit: pip install streamlit")
        print("Then run: streamlit run car_akinator_ui.py")