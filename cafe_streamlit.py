import streamlit as st
import pandas as pd
from cafe_backend import CafeBackend
import plotly.express as px

st.set_page_config(page_title="BrewMaster Dash", page_icon="☕", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #fdfaf6; }
    .cafe-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

cafe = CafeBackend()

st.title("☕ BrewMaster Dashboard")
st.sidebar.title("Operations")
page = st.sidebar.radio("Navigate to", ["POS System", "Inventory & Menu", "Sales Analytics"])

if page == "POS System":
    st.header("🛒 Point of Sale")
    menu = cafe.get_menu()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Menu")
        cart = {}
        for item in menu:
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.write(f"**{item[1]}**")
            c2.write(f"${item[2]:.2f}")
            qty = c3.number_input("Qty", min_value=0, max_value=20, key=f"item_{item[0]}")
            if qty > 0:
                cart[item[0]] = qty
                
    with col2:
        st.subheader("Your Order")
        if cart:
            total = 0
            for mid, q in cart.items():
                name = [i[1] for i in menu if i[0] == mid][0]
                price = [i[2] for i in menu if i[0] == mid][0]
                sub = price * q
                total += sub
                st.write(f"{name} x{q} - ${sub:.2f}")
            
            st.divider()
            st.subheader(f"Total: ${total:.2f}")
            if st.button("Complete Order", type="primary"):
                oid, t = cafe.create_order(list(cart.items()))
                st.success(f"Order #{oid} confirmed!")
        else:
            st.info("Cart is empty")

elif page == "Inventory & Menu":
    st.header("📋 Menu Management")
    
    with st.expander("Add New Item"):
        n = st.text_input("Item Name")
        p = st.number_input("Price", min_value=0.0, format="%.2f")
        c = st.text_input("Category")
        if st.button("Add to Menu"):
            cafe.add_menu_item(n, p, c)
            st.success("Item added!")
            
    st.subheader("Current Menu")
    menu = cafe.get_menu()
    df = pd.DataFrame(menu, columns=["ID", "Name", "Price", "Category"])
    st.dataframe(df, use_container_width=True)

elif page == "Sales Analytics":
    st.header("📊 Sales Insights")
    orders = cafe.get_orders()
    
    if orders:
        df_ord = pd.DataFrame(orders, columns=["ID", "Total", "Timestamp", "Status"])
        m1, m2 = st.columns(2)
        m1.metric("Total Revenue", f"${df_ord['Total'].sum():,.2f}")
        m2.metric("Orders Processed", len(df_ord))
        
        st.divider()
        st.subheader("Sales by Category")
        analytics = cafe.get_analytics()
        if analytics:
            df_an = pd.DataFrame(analytics, columns=["Category", "Revenue"])
            fig = px.pie(df_an, values="Revenue", names="Category", hole=0.4)
            st.plotly_chart(fig)
            
        st.subheader("Recent Order History")
        st.table(df_ord.head(10))
    else:
        st.info("No sales data available yet.")
