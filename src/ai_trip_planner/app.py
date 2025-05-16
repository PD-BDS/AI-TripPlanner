# app.py
import asyncio
import streamlit as st
from type import UserProfile, TripDetails, ActivitesOutline, UserSelectionOutline
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

    with st.spinner("Generating travel recommendations..."):
            recommendations = generate_recommendations(user, trip)

    st.subheader("🎯 Activity Recommendations")
    st.markdown("Please review and select the activities you want to include in your final itinerary:")

    selected_activities = []
    for activity in recommendations:
        if isinstance(activity, dict):
            title = activity.get("title", "Untitled")
            location = activity.get("location", "Unknown")
            if st.checkbox(f"{title} - {location}", value=True):
                selected_activities.append(ActivitesOutline(**activity))
        elif isinstance(activity, ActivitesOutline):
            if st.checkbox(f"{activity.title} - {activity.location}", value=True):
                selected_activities.append(activity)
        else:
            st.warning("⚠️ Skipping unrecognized activity format.")

    if st.button("Generate Final Trip Plan"):
        outline = UserSelectionOutline(selected=selected_activities)
        with st.spinner("Building your personalized itinerary..."):
            final_plan = generate_plan(user, trip, outline)

        st.subheader("🗓️ Final Itinerary")
        st.markdown(final_plan["day_wise_plan"])
        st.markdown("### 🌤️ Weather Forecast")
        st.markdown(final_plan["weather_condition"])
        st.markdown("### 💰 Expense Breakdown")
        st.markdown(final_plan["expense_breakdown"])
        st.markdown("### 📌 Special Notes")
        st.markdown(final_plan["special_notes"])