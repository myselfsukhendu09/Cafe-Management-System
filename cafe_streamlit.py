
import streamlit as st
import pandas as pd
import plotly.express as px
import cafe_backend as db
from datetime import datetime

# Page config
st.set_page_config(page_title="BrewMaster | Admin Dashboard", page_icon="☕", layout="wide")

# Init DB
db.init_db()

st.title("☕ BrewMaster Admin Dashboard")
st.markdown("---")

# Sidebar
menu = ["Sales Analytics", "Menu Management", "New Order"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Sales Analytics":
    st.header("📊 Business Insights")
    df = db.get_orders()
    
    if df.empty:
        st.warning("No orders placed yet.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", f"₹ {df['total'].sum():,.2f}")
        with col2:
            st.metric("Total Orders", len(df))
        with col3:
            st.metric("Avg Order Value", f"₹ {df['total'].mean():,.2f}")
            
        st.markdown("---")
        
        # Plot
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        fig = px.area(df, x='timestamp', y='total', title="Revenue Timeline")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Transaction History")
        st.dataframe(df.sort_values('timestamp', ascending=False), use_container_width=True)

elif choice == "Menu Management":
    st.header("📋 Menu Management")
    menu_df = db.get_menu()
    st.dataframe(menu_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Add New Item")
    with st.form("add_item"):
        name = st.text_input("Item Name")
        cat = st.selectbox("Category", ["Coffee", "Tea", "Snacks", "Bakery", "Beverages"])
        price = st.number_input("Price (₹)", min_value=0.0, step=5.0)
        submit = st.form_submit_button("Add to Menu")
        
        if submit:
            import sqlite3
            conn = sqlite3.connect('cafe.db')
            c = conn.cursor()
            c.execute("INSERT INTO menu (name, category, price) VALUES (?, ?, ?)", (name, cat, price))
            conn.commit()
            conn.close()
            st.success(f"Added {name} to the menu!")
            st.rerun()

elif choice == "New Order":
    st.header("🛒 Quick POS")
    menu_df = db.get_menu()
    
    cart = []
    total = 0
    
    st.subheader("Select Items")
    col1, col2 = st.columns(2)
    
    for index, row in menu_df.iterrows():
        with col1 if index % 2 == 0 else col2:
            if st.button(f"{row['name']} - ₹{row['price']}", key=f"item_{row['id']}"):
                # In a real app we'd use session state for persistent cart
                # But for a simple demo, we'll just record a single item order
                db.place_order(row['name'], row['price'])
                st.toast(f"Order placed for {row['name']}!")
    
    st.info("Desktop POS simulation: Clicking an item places an immediate order in this demo version.")
