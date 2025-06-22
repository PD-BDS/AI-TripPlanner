# 🌍 AI Trip Planner with CrewAI

A fully modular AI-powered travel planner built using **CrewAI** and **Streamlit**. This app analyzes user profiles and trip preferences to recommend **personalized activities**, and generates an **optimized day-wise itinerary** for unforgettable trips.

---

## ✨ Features

✅ User Profile & Trip Preferences Input via Streamlit

✅ Modular CrewAI Architecture (2 Crews)

✅ Personalized Activity Recommendations
✅ Interactive Activity Selection
✅ Day-wise Optimized Itinerary Generation
✅ Weather, Budget & Travel Tips Included
✅ Integrated with Serper and TripAdvisor APIs
✅ Expandable Agent & Tool System

---

## 🧠 Architecture

### 👥 CrewAI Agents & Crews

**1. Activities Recommender Crew**

* `City Expert Agent`
  Uses: Serper, TripAdvisor Tool
  Goal: Suggest best cities or analyze a given city
* `Activities Recommender Agent`
  Uses: Serper, TripAdvisor Tool
  Goal: Recommend 20+ detailed activities with justification

**2. Trip Planner Crew**

* `Travel Activities Expert Agent`
  Uses: Serper, TripAdvisor Nearby Tool
  Goal: Group nearby activities, analyze weather & logistics
* `Travel Planner Agent`
  Uses: Serper, TripAdvisor Nearby Tool
  Goal: Build full itinerary with day/hour breakdown, tips & costs

---


## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/PD-BDS/AI-TripPlanner.git
cd AI-TripPlanner/src/ai_trip_planner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root:

```env
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
TRIPADVISOR_API_KEY=your_tripadvisor_key
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🖼 Sample Workflow

1. Enter your name, age, travel details, interests, budget, and preferences
2. Receive a list of 20+ tailored activities
3. Select preferred ones via checkboxes
4. Get a detailed, efficient daily itinerary

---

## 📁 Project Structure

```
src/
├── ai_trip_planner/
│   ├── app.py               # Streamlit UI
│   ├── main.py              # Core orchestration
│   ├── crews/
│   │   ├── activities_recommender_crew/
│   │   └── trip_planner_crew/
│   ├── tool/                # TripAdvisor tools
	 ├── location_search_tool.py
│   │   └── nearby_search_tool.py
│   └── type.py              # Pydantic models
```

---

## 📌 To Do

* [ ] Add multi-language support
* [ ] Allow PDF/Email export of itinerary
* [ ] Improve hotel & restaurant selection logic
* [ ] Integrate map-based route planning

---

## 🙏 Acknowledgements

Built using:

* [CrewAI](https://github.com/joaomdmoura/crewAI)
* [TripAdvisor API](https://developer-tripadvisor.com/)
* [Serper](https://serper.dev)
* [LangChain](https://www.langchain.com/)

---

## 📝 License

MIT License — feel free to fork and customize!


# 🌍 AI Trip Planner with CrewAI

A fully modular AI-powered travel planner built using **CrewAI** and **Streamlit**. This app analyzes user profiles and trip preferences to recommend **personalized activities**, and generates an **optimized day-wise itinerary** for unforgettable trips.

---

## ✨ Features

✅ User Profile & Trip Preferences Input via Streamlit
✅ Modular CrewAI Architecture (2 Crews)
✅ Personalized Activity Recommendations
✅ Interactive Activity Selection
✅ Day-wise Optimized Itinerary Generation
✅ Weather, Budget & Travel Tips Included
✅ Integrated with Serper and TripAdvisor APIs
✅ Expandable Agent & Tool System

---

## 🧠 Architecture

### 👥 CrewAI Agents & Crews

**1. Activities Recommender Crew**

* `City Expert Agent`
  Uses: Serper, TripAdvisor Tool
  Goal: Suggest best cities or analyze a given city
* `Activities Recommender Agent`
  Uses: Serper, TripAdvisor Tool
  Goal: Recommend 20+ detailed activities with justification

**2. Trip Planner Crew**

* `Travel Activities Expert Agent`
  Uses: Serper, TripAdvisor Nearby Tool
  Goal: Group nearby activities, analyze weather & logistics
* `Travel Planner Agent`
  Uses: Serper, TripAdvisor Nearby Tool
  Goal: Build full itinerary with day/hour breakdown, tips & costs

---


## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/PD-BDS/AI-TripPlanner.git
cd AI-TripPlanner/src/ai_trip_planner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root:

```env
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
TRIPADVISOR_API_KEY=your_tripadvisor_key
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🖼 Sample Workflow

1. Enter your name, age, travel details, interests, budget, and preferences
2. Receive a list of 20+ tailored activities
3. Select preferred ones via checkboxes
4. Get a detailed, efficient daily itinerary

---

## 📁 Project Structure

```
src/
├── ai_trip_planner/
│   ├── app.py               # Streamlit UI
│   ├── main.py              # Core orchestration
│   ├── crews/
│   │   ├── activities_recommender_crew/
│   │   └── trip_planner_crew/
│   ├── tool/                # TripAdvisor tools
	 ├── location_search_tool.py
│   │   └── nearby_search_tool.py
│   └── type.py              # Pydantic models
```

---

## 📌 To Do

* [ ] Add multi-language support
* [ ] Allow PDF/Email export of itinerary
* [ ] Improve hotel & restaurant selection logic
* [ ] Integrate map-based route planning

---

## 🙏 Acknowledgements

Built using:

* [CrewAI](https://github.com/joaomdmoura/crewAI)
* [TripAdvisor API](https://developer-tripadvisor.com/)
* [Serper](https://serper.dev)
* [LangChain](https://www.langchain.com/)

---

## 📝 License

MIT License — feel free to fork and customize!

