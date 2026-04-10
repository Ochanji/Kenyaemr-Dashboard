"""
app.py
------
KenyaEMR Dashboard - main Streamlit application.

Four pages navigable via a radio selector:
    1. Overview         - Programme-wide KPI scorecards
    2. HIV Testing      - HTS_TST / HTS_TST_POS trends and breakdowns
    3. Prevention       - KP_PREV, GBV, and PrEP uptake
    4. Care & Treatment - TX_CURR, TX_NEW, TX_PVLS, TB indicators

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from dataset import (
    df_overview,
    df_hts,
    df_ct,
    df_prevention,
    df_prep,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    layout="wide",
    page_title="KenyaEMR Dashboard",
    page_icon=":bar_chart:",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Shared month order (Oct FY start)
# ---------------------------------------------------------------------------
MONTH_ORDER = [
    "October", "November", "December",
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
]

# ---------------------------------------------------------------------------
# KPI Targets  (update each financial year)
# ---------------------------------------------------------------------------
TARGETS = {
    "HTS_TST": 5582,
    "HTS_TST_POS": 76,
    "HTS_SELF_KP": 5442,
    "KP_PREV_FSW": 4152,
    "KP_PREV_MSM": 1028,
    "KP_PREV_PWID": 1107,
    "TX_CURR_KP": 1157,
    "TX_NEW_KP": 124,
    "TX_PVLS_N_KP": 0,
    "TX_PVLS_D_KP": 757,
    "TB_PREV_N_KP": 0,
    "TB_PREV_D_KP": 89,
    "TB_STAT_KP": 33,
}

# Apply ordered month categories to shared DataFrames once at startup
for _df in [df_hts, df_prevention, df_ct, df_prep]:
    if "Month" in _df.columns:
        _df["Month"] = pd.Categorical(
            _df["Month"], categories=MONTH_ORDER, ordered=True
        )


# ===========================================================================
# HELPER
# ===========================================================================
def _pct(numerator: int, denominator: int) -> str:
    """Return a percentage string, guarding against zero division."""
    if not denominator:
        return "0%"
    return f"{round(numerator / denominator * 100, 1)}%"


def _chart_layout(fig):
    """Apply a consistent transparent background to a Plotly figure."""
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="#e5e5e5"),
    )
    return fig


# ===========================================================================
# PAGE 1 - OVERVIEW
# ===========================================================================
def page_overview() -> None:
    st.markdown("## Programme Overview")
    st.caption("High-level KPI scorecards across all programme areas.")
    st.divider()

    with st.sidebar:
        st.header("Filters")
        fy = st.multiselect(
            "Financial Year",
            options=df_hts["Financial_Year"].unique(),
            default=[df_hts["Financial_Year"].iloc[-1]],
        )

    df_h = df_hts[df_hts["Financial_Year"].isin(fy)]

    # HTS scorecard
    st.subheader("HIV Testing Services")
    tst = len(df_h)
    pos = len(df_h[df_h["HTSResult"] == "Positive"]) if "HTSResult" in df_h.columns else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tested (HTS_TST)", tst, _pct(tst, TARGETS["HTS_TST"]) + " of target")
    c2.metric("Positive (HTS_TST_POS)", pos, _pct(pos, tst) + " positivity")
    c3.metric("HTS_TST Target", TARGETS["HTS_TST"])
    c4.metric("Positivity Target", TARGETS["HTS_TST_POS"])

    st.divider()

    # Treatment scorecard
    st.subheader("HIV Care and Treatment")
    tx_curr = len(df_ct[df_ct["Status"] == "On ART"]) if "Status" in df_ct.columns else 0
    tx_new = len(df_ct[df_ct["Status"] == "New on ART"]) if "Status" in df_ct.columns else 0
    c5, c6, c7, c8 = st.columns(4)
    c5.metric("TX_CURR", tx_curr, _pct(tx_curr, TARGETS["TX_CURR_KP"]) + " of target")
    c6.metric("TX_NEW", tx_new, _pct(tx_new, TARGETS["TX_NEW_KP"]) + " of target")
    c7.metric("TX_CURR Target", TARGETS["TX_CURR_KP"])
    c8.metric("TX_NEW Target", TARGETS["TX_NEW_KP"])

    st.divider()

    # Prevention scorecard
    st.subheader("Prevention Services")
    p1, p2, p3 = st.columns(3)
    p1.metric("KP_PREV FSW Target", TARGETS["KP_PREV_FSW"])
    p2.metric("KP_PREV MSM Target", TARGETS["KP_PREV_MSM"])
    p3.metric("KP_PREV PWID Target", TARGETS["KP_PREV_PWID"])

    # Overview summary chart
    if not df_overview.empty:
        st.divider()
        st.subheader("Summary Chart")
        cols = df_overview.columns.tolist()
        if len(cols) >= 2:
            fig = px.bar(
                df_overview, x=cols[0], y=cols[1],
                title="Programme KPI Overview",
                color_discrete_sequence=["#0083B8"],
                text_auto=True,
            )
            st.plotly_chart(_chart_layout(fig), use_container_width=True)


# ===========================================================================
# PAGE 2 - HIV TESTING SERVICES
# ===========================================================================
def page_hts() -> None:
    st.markdown("## HIV Testing Services")
    st.caption("Testing volumes, positivity trends, and disaggregated breakdowns.")
    st.divider()

    cf1, cf2 = st.columns(2)
    fy = cf1.multiselect(
        "Financial Year",
        options=df_hts["Financial_Year"].unique(),
        default=[df_hts["Financial_Year"].iloc[-1]],
    )
    result_filter = cf2.multiselect(
        "HTS Result",
        options=["Positive", "Negative"],
        default=["Positive", "Negative"],
    )

    df_sel = df_hts[df_hts["Financial_Year"].isin(fy)]
    if result_filter and "HTSResult" in df_sel.columns:
        df_sel = df_sel[df_sel["HTSResult"].isin(result_filter)]

    # KPI metrics
    tst = len(df_sel)
    pos = len(df_sel[df_sel["HTSResult"] == "Positive"]) if "HTSResult" in df_sel.columns else 0
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("HTS_TST", tst, f"Target: {TARGETS['HTS_TST']}")
    k2.metric("HTS_TST_POS", pos, f"Target: {TARGETS['HTS_TST_POS']}")
    k3.metric("Achievement", _pct(tst, TARGETS["HTS_TST"]))
    k4.metric("Positivity Rate", _pct(pos, tst))

    st.divider()

    # Monthly trend
    if "Month" in df_sel.columns and "HTSResult" in df_sel.columns:
        monthly = df_sel.groupby(["Month", "HTSResult"]).size().reset_index(name="Count")
        fig_t = px.bar(
            monthly, x="Month", y="Count", color="HTSResult", barmode="group",
            title="Monthly HTS Volume by Result",
            color_discrete_map={"Positive": "#E74C3C", "Negative": "#27AE60"},
            category_orders={"Month": MONTH_ORDER},
            text_auto=True,
        )
        st.plotly_chart(_chart_layout(fig_t), use_container_width=True)

    # Population type and gender breakdown
    cl, cr = st.columns(2)
    if "PopulationType" in df_sel.columns and "HTSResult" in df_sel.columns:
        with cl:
            pop = df_sel.groupby(["PopulationType", "HTSResult"]).size().reset_index(name="Count")
            fig_pop = px.bar(
                pop, x="PopulationType", y="Count", color="HTSResult", barmode="stack",
                title="Testing by Population Type",
                color_discrete_map={"Positive": "#E74C3C", "Negative": "#27AE60"},
                text_auto=True,
            )
            st.plotly_chart(_chart_layout(fig_pop), use_container_width=True)

    if "Gender" in df_sel.columns:
        with cr:
            gender = df_sel["Gender"].value_counts().reset_index()
            gender.columns = ["Gender", "Count"]
            fig_g = px.pie(gender, names="Gender", values="Count", title="Testing by Gender", hole=0.4)
            st.plotly_chart(fig_g, use_container_width=True)

    # Provider contribution
    if "Provider" in df_sel.columns and "HTSResult" in df_sel.columns:
        st.subheader("Provider Contribution")
        prov = df_sel.groupby(["Provider", "HTSResult"]).size().reset_index(name="Count")
        fig_prov = px.bar(
            prov, x="Count", y="Provider", color="HTSResult", orientation="h",
            title="Provider Contribution to HTS",
            color_discrete_map={"Positive": "#E74C3C", "Negative": "#27AE60"},
            text_auto=True,
        )
        fig_prov.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(_chart_layout(fig_prov), use_container_width=True)

    st.divider()
    st.download_button(
        "Download HTS Data (CSV)",
        df_sel.to_csv(index=False).encode("utf-8"),
        "hts_data.csv",
        "text/csv",
    )


# ===========================================================================
# PAGE 3 - PREVENTION SERVICES
# ===========================================================================
def page_prevention() -> None:
    st.markdown("## Prevention Services")
    st.caption("KP_PREV, GBV indicators, and PrEP uptake across financial years.")
    st.divider()

    cf1, cf2 = st.columns(2)
    fy_opts = list(df_prevention["Financial_Year"].unique()) if "Financial_Year" in df_prevention.columns else []
    fy = cf1.multiselect("Financial Year", options=fy_opts, default=fy_opts[:1])
    months = cf2.multiselect("Month", options=MONTH_ORDER, default=MONTH_ORDER)

    df_p = df_prevention.copy()
    if fy and "Financial_Year" in df_p.columns:
        df_p = df_p[df_p["Financial_Year"].isin(fy)]
    if months and "Month" in df_p.columns:
        df_p = df_p[df_p["Month"].isin(months)]

    # KPI targets
    st.subheader("KP Prevention Targets")
    k1, k2, k3 = st.columns(3)
    k1.metric("KP_PREV FSW", TARGETS["KP_PREV_FSW"])
    k2.metric("KP_PREV MSM", TARGETS["KP_PREV_MSM"])
    k3.metric("KP_PREV PWID", TARGETS["KP_PREV_PWID"])

    st.divider()

    # GBV trend
    if "GBV" in df_p.columns and "Month" in df_p.columns:
        cl, cr = st.columns(2)
        with cl:
            gbv = df_p.groupby(["Month", "GBV"]).size().reset_index(name="Count")
            fig_gbv = px.bar(
                gbv, x="Month", y="Count", color="GBV",
                title="Cumulative GBV (KP) Performance",
                category_orders={"Month": MONTH_ORDER},
                text_auto=True,
            )
            st.plotly_chart(_chart_layout(fig_gbv), use_container_width=True)

        with cr:
            if "PopulationType" in df_p.columns:
                prov = df_p.groupby(["PopulationType", "GBV"]).size().reset_index(name="Count")
                fig_prov = px.bar(
                    prov, x="Count", y="PopulationType", color="GBV", orientation="h",
                    title="Provider Contribution to KP Prevention",
                    text_auto=True,
                )
                fig_prov.update_layout(yaxis=dict(categoryorder="total ascending"))
                st.plotly_chart(_chart_layout(fig_prov), use_container_width=True)

    # PrEP uptake
    st.subheader("PrEP Uptake")
    if not df_prep.empty:
        st.metric("Total PrEP Clients", len(df_prep))
        if "Month" in df_prep.columns:
            prep_monthly = df_prep.groupby("Month").size().reset_index(name="Count")
            fig_prep = px.line(
                prep_monthly, x="Month", y="Count",
                title="Monthly PrEP Uptake",
                markers=True,
                category_orders={"Month": MONTH_ORDER},
            )
            fig_prep.update_traces(line_color="#0083B8")
            st.plotly_chart(_chart_layout(fig_prep), use_container_width=True)

    st.divider()
    st.download_button(
        "Download Prevention Data (CSV)",
        df_p.to_csv(index=False).encode("utf-8"),
        "prevention_data.csv",
        "text/csv",
    )


# ===========================================================================
# PAGE 4 - HIV CARE AND TREATMENT
# ===========================================================================
def page_ct() -> None:
    st.markdown("## HIV Care and Treatment")
    st.caption("TX_CURR, TX_NEW, TX_PVLS, TB_STAT, TB_PREV and VL suppression indicators.")
    st.divider()

    cf1, cf2 = st.columns(2)
    fy_opts = list(df_ct["Financial_Year"].unique()) if "Financial_Year" in df_ct.columns else []
    fy = cf1.multiselect("Financial Year", options=fy_opts, default=fy_opts[:1])
    status_opts = list(df_ct["Status"].unique()) if "Status" in df_ct.columns else []
    status = cf2.multiselect("Treatment Status", options=status_opts, default=status_opts)

    df_c = df_ct.copy()
    if fy and "Financial_Year" in df_c.columns:
        df_c = df_c[df_c["Financial_Year"].isin(fy)]
    if status and "Status" in df_c.columns:
        df_c = df_c[df_c["Status"].isin(status)]

    # KPI scorecards
    st.subheader("Treatment Indicators")
    tx_curr = len(df_c[df_c["Status"] == "On ART"]) if "Status" in df_c.columns else 0
    tx_new = len(df_c[df_c["Status"] == "New on ART"]) if "Status" in df_c.columns else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TX_CURR (KP)", tx_curr, _pct(tx_curr, TARGETS["TX_CURR_KP"]) + " of target")
    c2.metric("TX_NEW (KP)", tx_new, _pct(tx_new, TARGETS["TX_NEW_KP"]) + " of target")
    c3.metric("TX_PVLS_N Target", TARGETS["TX_PVLS_N_KP"])
    c4.metric("TX_PVLS_D Target", TARGETS["TX_PVLS_D_KP"])

    st.divider()

    # Monthly TX trends
    if "Month" in df_c.columns and "Status" in df_c.columns:
        cl, cr = st.columns(2)
        with cl:
            curr_monthly = (
                df_c[df_c["Status"] == "On ART"]
                .groupby("Month").size().reset_index(name="TX_CURR")
            )
            fig_curr = px.line(
                curr_monthly, x="Month", y="TX_CURR",
                title="TX_CURR Monthly Trend",
                markers=True, category_orders={"Month": MONTH_ORDER},
            )
            fig_curr.update_traces(line_color="#27AE60")
            st.plotly_chart(_chart_layout(fig_curr), use_container_width=True)

        with cr:
            new_monthly = (
                df_c[df_c["Status"] == "New on ART"]
                .groupby("Month").size().reset_index(name="TX_NEW")
            )
            fig_new = px.bar(
                new_monthly, x="Month", y="TX_NEW",
                title="TX_NEW Monthly Trend",
                category_orders={"Month": MONTH_ORDER},
                text_auto=True,
                color_discrete_sequence=["#2980B9"],
            )
            st.plotly_chart(_chart_layout(fig_new), use_container_width=True)

    # Age-sex distribution
    if "AgeGroup" in df_c.columns and "Gender" in df_c.columns and "Status" in df_c.columns:
        st.subheader("TX_CURR Age-Sex Distribution")
        age_sex = (
            df_c[df_c["Status"] == "On ART"]
            .groupby(["AgeGroup", "Gender"])
            .size().reset_index(name="Count")
        )
        if not age_sex.empty:
            fig_age = px.bar(
                age_sex, x="Count", y="AgeGroup", color="Gender",
                barmode="overlay", orientation="h",
                title="TX_CURR by Age Group and Gender",
                color_discrete_map={"Female": "#E74C3C", "Male": "#2980B9"},
                text_auto=True,
            )
            st.plotly_chart(_chart_layout(fig_age), use_container_width=True)

    # TB indicators
    st.divider()
    st.subheader("TB Indicators (KP)")
    tb1, tb2, tb3 = st.columns(3)
    tb1.metric("TB_STAT Target", TARGETS["TB_STAT_KP"])
    tb2.metric("TB_PREV_N Target", TARGETS["TB_PREV_N_KP"])
    tb3.metric("TB_PREV_D Target", TARGETS["TB_PREV_D_KP"])

    st.divider()
    st.download_button(
        "Download CT Data (CSV)",
        df_c.to_csv(index=False).encode("utf-8"),
        "ct_data.csv",
        "text/csv",
    )


# ===========================================================================
# PAGE ROUTER
# ===========================================================================
PAGES = {
    "Overview": page_overview,
    "HIV Testing Services": page_hts,
    "Prevention Services": page_prevention,
    "HIV Care and Treatment": page_ct,
}

selected = st.radio(
    "Select page",
    options=list(PAGES.keys()),
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()
PAGES[selected]()
