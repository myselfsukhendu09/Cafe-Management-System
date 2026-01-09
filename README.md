# ☕ BrewMaster | Professional Cafe Management System

An end-to-end cafe management solution featuring a professional Flask ordering system and a powerful Streamlit analytics dashboard.

## ✨ Key Features
- **Dynamic POS Interface**: Modern Flask UI with a real-time cart system for quick order placement.
- **Order Tracking**: Comprehensive history of all transactions with timestamped records.
- **Menu Administration**: Easily add new items, adjust prices, and manage categories.
- **Analytics Dashboard**: 
  - Revenue tracking and sales summaries.
  - Category-wise distribution via interactive charts.
  - Real-time inventory monitoring.
- **SQLite Database**: Robust local storage to maintain menu and order integrity.

## 🛠️ Tech Stack
- **Languages**: Python 3
- **Web App**: Flask, Bootstrap 5, JavaScript (ES6)
- **Analytics**: Streamlit, Pandas, Plotly
- **Database**: SQLite

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install flask streamlit pandas plotly
```

### 2. Launch Flask Application (Front-of-House)
```bash
python cafe_flask.py
```
Open `http://127.0.0.1:5002` to start taking orders.

### 3. Launch Streamlit Dashboard (Back-of-House)
```bash
streamlit run cafe_streamlit.py
```

## 📁 Repository Structure
- `cafe_flask.py`: Main Flask application.
- `cafe_streamlit.py`: Streamlit dashboard.
- `cafe_backend.py`: Core logic for orders and menu management.
- `templates/`: HTML structures for the Flask app.
- `cafe.db`: SQLite database file.
