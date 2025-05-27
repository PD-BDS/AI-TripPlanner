# app.py
import asyncio
import streamlit as st
from type import UserProfile, TripDetails, ActivitesOutline, ActivitiesList, UserSelectionOutline, PlanOutline, TripPlan
from main import generate_recommendations, generate_plan
#from main import TripPlanFlow, TripPlanState

st.set_page_config(page_title="AI Trip Planner")

st.title("🌍 AI Trip Planner")

with st.form("user_form"):
    st.subheader("User Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1)
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Other"])
    occupation = st.text_input("Occupation")
    email = st.text_input("Email")
    nationality = st.text_input("Nationality")
    interests = st.multiselect("Interests", ["Nature", "Adventure", "Culture", "Shopping", "Relaxation", "Food"])

    st.subheader("Trip Details")
    from_location = st.text_input("From Location")
    to_location = st.text_input("To Location")
    from_date = st.date_input("From Date").isoformat()
    to_date = st.date_input("To Date").isoformat()
    purpose = st.selectbox("Purpose of the trip", ["Business Trip", "Family Trip", "Friendly Trip", "Solo Trip"])
    companions = st.multiselect("Accompanies", ["Friends", "Spouse", "Kids", "Parents", "Colleagues", "None"])
    budget_type = st.selectbox("Budget Type", ["Low", "Medium", "Premium", "Luxury"])
    budget = st.number_input("Estimated Budget (€)", min_value=100)
    travelers = st.number_input("Number of Travelers", min_value=1)
    preferences = st.multiselect("Preferences", ["Local experience", "Nightlife", "Historic places", "Nature", "Shopping", "Sightseeing", "Food", "Sports", "Music", "Exhibitions", "Beach", "Mountains", "Street Walk"])
    special_requirements = st.text_area("Special Requirements", placeholder="Any dietary, medical, or access needs")

    submitted = st.form_submit_button("Generate Recommendations")

if 'user' not in st.session_state:
    st.session_state.user = None

if 'trip' not in st.session_state:
    st.session_state.trip = None

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

if submitted:
    user = UserProfile(
        name=name,
        age=age,
        marital_status=marital_status,
        occupation=occupation,
        email=email,
        nationality=nationality,
        interests=interests
    )

    trip = TripDetails(
        from_location=from_location,
        to_location=to_location,
        from_date=from_date,
        to_date=to_date,
        purpose=purpose,
        companions=companions,
        budget_type=budget_type,
        budget=budget,
        travelers=travelers,
        preferences=preferences,
        special_requirements=special_requirements or None
    )
    
    st.session_state.user = user
    st.session_state.trip = trip

    with st.spinner("Generating travel recommendations..."):
        recommendations = generate_recommendations(user, trip)
        st.session_state.recommendations = recommendations

# ✅ Display activity checkboxes with cards
if st.session_state.recommendations:
    st.subheader("🎯 Activity Recommendations")
    st.markdown("Please review and select the activities you want to include in your final itinerary:")

    selected_activities = []

    for i, activity in enumerate(st.session_state.recommendations):
        if isinstance(activity, ActivitesOutline):
            cols = st.columns([0.1, 0.9])
            with cols[0]:
                checked = st.checkbox("Select", key=f"activity_{i}", label_visibility="collapsed")
            with cols[1]:
                st.markdown(
                    f"""
                    <div style='padding: 10px; background-color: #f9f9f9; border-radius: 10px;
                                border: 1px solid #ddd; margin-bottom: 10px;'>
                        <b>{activity.title}</b><br>
                        {activity.short_description}<br>
                        <b>📍 Location:</b> {activity.location}<br>
                        <b>💸 Cost:</b> {activity.approximate_expense}<br>
                        <b>⭐ Rating:</b> {activity.recommendation_rating}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            if checked:
                selected_activities.append(activity)

    # Final trip plan generation
    if st.button("Generate Final Trip Plan"):
        if not selected_activities:
            st.warning("Please select at least one activity before generating the plan.")
        else:
            outline = [a.model_dump() for a in selected_activities]

            user = st.session_state.get("user")
            trip = st.session_state.get("trip")

            if not user or not trip:
                st.error("User or Trip information is missing. Please fill out the form again.")
            else:
                with st.spinner("Building your personalized itinerary..."):
                    trip_plan = generate_plan(user, trip, outline)

                st.subheader("🗓️ Detailed Plan")
                for i, plan in enumerate(trip_plan):
                    st.markdown(f"\n\n{plan.day_wise_plan}")
                    st.markdown(f"**🌦️ Weather:**\n\n{plan.weather_condition}")
                    st.markdown(f"**🎒 Packing Tips:**\n\n{plan.packing_and_clothing_tips}")
                    st.markdown(f"**💰 Expenses:**\n\n{plan.expense_breakdown}")
                    st.markdown(f"**📝 Notes:**\n\n{plan.special_notes}")
                    st.markdown("---")