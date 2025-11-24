import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for orders if not exists
if 'orders' not in st.session_state:
    st.session_state.orders = [
        {'orderid': 'ORD001', 'description': 'Office Supplies', 'item_qty': 10, 'price': 150.00, 'status': 'Placed'},
        {'orderid': 'ORD002', 'description': 'Electronics', 'item_qty': 5, 'price': 500.00, 'status': 'Awaiting'},
        {'orderid': 'ORD003', 'description': 'Furniture', 'item_qty': 3, 'price': 1200.00, 'status': 'Contract placed'},
        {'orderid': 'ORD004', 'description': 'Books', 'item_qty': 20, 'price': 200.00, 'status': 'Processing'},
        {'orderid': 'ORD005', 'description': 'Software License', 'item_qty': 1, 'price': 999.00, 'status': 'Cancelled'},
    ]

if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = False

if 'next_order_id' not in st.session_state:
    st.session_state.next_order_id = 6

# Page config
st.set_page_config(page_title="Order Management Dashboard", layout="wide")

# Title and New Order Button
col_title, col_button = st.columns([3, 1])
with col_title:
    st.title("📦 Order Management Dashboard")
with col_button:
    st.write("")  # Add spacing
    if st.button("➕ New Order", type="primary", use_container_width=True):
        st.session_state.show_dialog = True

# Calculate status counts
def count_by_status(status):
    return len([order for order in st.session_state.orders if order['status'] == status])

# Status boxes
st.write("### Order Status Overview")
col1, col2, col3, col4, col5 = st.columns(5)

statuses = [
    ("Placed", "🟢", col1),
    ("Awaiting", "🟡", col2),
    ("Contract placed", "🔵", col3),
    ("Processing", "🟠", col4),
    ("Cancelled", "🔴", col5)
]

for status, emoji, col in statuses:
    with col:
        count = count_by_status(status)
        st.metric(label=f"{emoji} {status}", value=count)

st.divider()

# New Order Dialog
if st.session_state.show_dialog:
    with st.form("new_order_form", clear_on_submit=True):
        st.subheader("Create New Order")
        
        description = st.text_area("Description", placeholder="Enter order description...")
        
        col_qty, col_price = st.columns(2)
        with col_qty:
            item_qty = st.number_input("Item Quantity", min_value=1, value=1)
        with col_price:
            price = st.number_input("Price ($)", min_value=0.0, value=0.0, format="%.2f")
        
        status = st.selectbox("Status", ["Placed", "Awaiting", "Contract placed", "Processing", "Cancelled"])
        
        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("Submit Order", type="primary", use_container_width=True)
        with col_cancel:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)
        
        if submitted:
            new_order = {
                'orderid': f'ORD{str(st.session_state.next_order_id).zfill(3)}',
                'description': description,
                'item_qty': item_qty,
                'price': price,
                'status': status
            }
            st.session_state.orders.append(new_order)
            st.session_state.next_order_id += 1
            st.session_state.show_dialog = False
            st.success(f"Order {new_order['orderid']} created successfully!")
            st.rerun()
        
        if cancelled:
            st.session_state.show_dialog = False
            st.rerun()

# Orders Table
st.write("### Order Details")

if st.session_state.orders:
    # Convert to DataFrame for better display
    df = pd.DataFrame(st.session_state.orders)
    
    # Format price column
    df['price'] = df['price'].apply(lambda x: f"${x:.2f}")
    
    # Display table with custom styling
    st.dataframe(
        df,
        column_config={
            "orderid": st.column_config.TextColumn("Order ID", width="small"),
            "description": st.column_config.TextColumn("Description", width="medium"),
            "item_qty": st.column_config.NumberColumn("Item Qty", width="small"),
            "price": st.column_config.TextColumn("Price", width="small"),
            "status": st.column_config.TextColumn("Status", width="medium"),
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("No orders yet. Click 'New Order' to create one!")

# Footer
st.divider()
st.caption(f"Total Orders: {len(st.session_state.orders)} | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
