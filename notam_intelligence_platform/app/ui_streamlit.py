"""Streamlit UI for the NOTAM Intelligence Platform."""

from __future__ import annotations

import streamlit as st

from app.main import process_notam


st.set_page_config(page_title="NOTAM Intelligence Platform", layout="centered")

st.title("NOTAM Intelligence Platform")
st.caption("Parse, expand abbreviations, and score operational impact.")

col_a, col_b = st.columns(2)
departure = col_a.text_input("Departure ICAO", value="KJFK")
arrival = col_b.text_input("Arrival ICAO", value="KLAX")

sample_notam = "RWY 09/27 CLSD DUE WIP. ILS U/S. TFR ACTIVE."
notam_text = st.text_area("Enter NOTAM text", value=sample_notam, height=160)

if st.button("Analyze NOTAM", type="primary"):
    try:
        result = process_notam(notam_text, departure=departure, arrival=arrival)
    except (TypeError, ValueError) as exc:
        st.error(f"Input error: {exc}")
    else:
        col1, col2 = st.columns(2)
        col1.metric("Impact Score", result.impact_score)
        col2.metric("Severity", result.severity)
        st.write(f"**Route:** {result.departure} → {result.arrival}")
        st.subheader("Category")
        st.write(result.category)

        st.subheader("Operational Insight")
        if result.severity == "CRITICAL":
            st.error("⚠️ Major operational impact")
        elif result.severity == "HIGH":
            st.warning("⚠️ Significant impact")
        else:
            st.info("Minor impact")

        st.subheader("Raw NOTAM")
        st.code(result.raw_text)
        st.subheader("Expanded NOTAM")
        st.code(result.expanded_text)

st.markdown("---")
st.markdown("Run locally with: `streamlit run app/ui_streamlit.py`")
