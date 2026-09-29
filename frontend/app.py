"""
Exercise 02 — Streamlit Dashboard

Streamlit frontend consuming the Node Registry API
"""

import os
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://api:8080").rstrip("/")

@st.cache_resource
def get_session():
    return requests.Session()

http = get_session()

st.set_page_config(page_title="Node Registry Dashboard", layout="wide")

st.title("Node Registry Dashboard")

# 1. Health Indicator
st.header("System Health")
try:
    health_res = http.get(f"{API_URL}/health", timeout=3)
    if health_res.status_code == 200:
        health_data = health_res.json()
        col1, col2, col3 = st.columns(3)
        col1.metric("API Status", str(health_data.get("status", "unknown")).upper())
        col2.metric("Database Status", str(health_data.get("db", "unknown")).capitalize())
        col3.metric("Active Nodes", health_data.get("nodes_count", 0))
    else:
        st.error(f"API health returned status code {health_res.status_code}")
except Exception as e:
    st.error(f"Could not connect to API at {API_URL}: {e}")

st.divider()

# Fetch Nodes
nodes = []
try:
    nodes_res = http.get(f"{API_URL}/api/nodes", timeout=3)
    if nodes_res.status_code == 200:
        nodes = nodes_res.json()
    else:
        st.error(f"Failed to fetch nodes: HTTP {nodes_res.status_code}")
except Exception as e:
    st.error(f"Error fetching nodes: {e}")

# 2. Node List
st.header("Registered Nodes")
if nodes:
    st.dataframe(nodes, use_container_width=True)
else:
    st.info("No registered nodes found.")

st.divider()

col_reg, col_del = st.columns(2)

# 3. Register Form
with col_reg:
    st.header("Register Node")
    with st.form("register_node_form", clear_on_submit=True):
        name = st.text_input("Name")
        host = st.text_input("Host")
        port = st.number_input("Port", min_value=1, max_value=65535, value=8000, step=1)
        submit_button = st.form_submit_button("Register Node")

        if submit_button:
            if not name or not host:
                st.warning("Please provide both name and host.")
            else:
                try:
                    payload = {"name": name, "host": host, "port": int(port)}
                    res = http.post(f"{API_URL}/api/nodes", json=payload, timeout=3)
                    if res.status_code == 201:
                        st.success(f"Node '{name}' registered successfully!")
                    elif res.status_code == 409:
                        st.error(f"Node '{name}' already exists.")
                    else:
                        st.error(f"Failed to register node: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Error registering node: {e}")

# 4. Delete Form
with col_del:
    st.header("Delete Node")
    with st.form("delete_node_form", clear_on_submit=True):
        delete_name = st.text_input("Node Name to Delete")
        delete_button = st.form_submit_button("Delete Node")

        if delete_button:
            if not delete_name:
                st.warning("Please specify a node name to delete.")
            else:
                try:
                    res = http.delete(f"{API_URL}/api/nodes/{delete_name}", timeout=3)
                    if res.status_code == 204:
                        st.success(f"Node '{delete_name}' soft-deleted successfully!")
                    elif res.status_code == 404:
                        st.error(f"Node '{delete_name}' not found.")
                    else:
                        st.error(f"Failed to delete node: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Error deleting node: {e}")
