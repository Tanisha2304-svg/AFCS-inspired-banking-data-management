import streamlit as st
import pandas as pd
import plotly.express as px
from src.pipeline import load_transactions, validate_transactions, standardise, generate_journals, reconcile

st.set_page_config(page_title="Banking Data Management Prototype", layout="wide")
st.title("Banking Financial Data Management & Reconciliation")
st.caption("AFCS-inspired independent simulation | Synthetic data only")

raw = load_transactions()
validated = validate_transactions(raw)
standard = standardise(validated)
valid = standard[standard["dq_status"] == "VALID"].copy()
journals = generate_journals(valid)
recon = reconcile()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Transactions loaded", len(raw))
c2.metric("Valid records", int((validated["dq_status"] == "VALID").sum()))
c3.metric("DQ exceptions", int((validated["dq_status"] == "ERROR").sum()))
c4.metric("Reconciliation breaks", int((recon["status"] == "BREAK").sum()))

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Data Quality", "Journal Simulation", "Reconciliation"])
with tab1:
    st.subheader("Source transaction volumes")
    counts = raw.groupby("source_system").size().reset_index(name="records")
    st.plotly_chart(px.bar(counts, x="source_system", y="records", title="Records by source system"), use_container_width=True)
    st.dataframe(raw, use_container_width=True)
with tab2:
    st.subheader("Data quality results")
    st.dataframe(validated[["source_system","transaction_id","account_id","dq_status","dq_errors"]], use_container_width=True)
    st.download_button("Download DQ results", validated.to_csv(index=False), "data_quality_results.csv", "text/csv")
with tab3:
    st.subheader("Illustrative journal lines")
    st.caption("These are simulated mappings for learning, not approved accounting rules.")
    st.dataframe(journals, use_container_width=True)
    st.download_button("Download journal simulation", journals.to_csv(index=False), "journal_simulation.csv", "text/csv")
with tab4:
    st.subheader("Source vs GL reconciliation")
    st.dataframe(recon, use_container_width=True)
    st.download_button("Download reconciliation", recon.to_csv(index=False), "reconciliation_results.csv", "text/csv")
