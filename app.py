import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Shopping Dashboard",
    page_icon="🛍️",
    layout="wide",
)

# ── Theme toggle ─────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# ── Dynamic CSS ──────────────────────────────────────────────────────────────
if st.session_state.dark_mode:
    bg        = "#0e1117"
    card_bg   = "#1c1f26"
    text      = "#e0e0e0"
    sub_text  = "#9e9e9e"
    border    = "#2e3240"
    accent    = "#7c83fd"
    plotly_bg = "#1c1f26"
    plotly_paper = "#1c1f26"
    plotly_font  = "#e0e0e0"
    toggle_label = "☀️ Light Mode"
else:
    bg        = "#f7f9fc"
    card_bg   = "#ffffff"
    text      = "#1a1a2e"
    sub_text  = "#666666"
    border    = "#e0e0e0"
    accent    = "#4f56e8"
    plotly_bg = "#ffffff"
    plotly_paper = "#f7f9fc"
    plotly_font  = "#1a1a2e"
    toggle_label = "🌙 Dark Mode"

st.markdown(f"""
<style>
  /* Overall page */
  .stApp {{ background-color: {bg}; color: {text}; }}

  /* Sidebar */
  [data-testid="stSidebar"] {{ background-color: {card_bg}; border-right: 1px solid {border}; }}
  [data-testid="stSidebar"] * {{ color: {text} !important; }}

  /* Metric cards */
  [data-testid="stMetric"] {{
    background: {card_bg};
    border: 1px solid {border};
    border-radius: 12px;
    padding: 16px;
  }}
  [data-testid="stMetricLabel"] {{ color: {sub_text} !important; font-size: 0.8rem; }}
  [data-testid="stMetricValue"] {{ color: {text} !important; font-weight: 700; }}

  /* Dataframe */
  [data-testid="stDataFrame"] {{ border-radius: 10px; overflow: hidden; }}

  /* Headers */
  h1, h2, h3 {{ color: {text}; }}

  /* Selectbox / multiselect labels */
  label {{ color: {text} !important; }}

  /* Toggle button */
  .theme-btn button {{
    background: {accent};
    color: white !important;
    border: none;
    border-radius: 20px;
    padding: 4px 16px;
  }}

  /* Tab bar */
  [data-baseweb="tab-list"] {{ background: {card_bg}; border-radius: 10px; padding: 4px; }}
  [data-baseweb="tab"] {{ color: {sub_text} !important; }}
  [aria-selected="true"] {{ color: {accent} !important; font-weight: 600; }}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("customer_shopping_behavior.csv")

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<h2 style='color:{accent}'>🛍️ Shopping Dashboard</h2>", unsafe_allow_html=True)

    # Theme toggle
    st.markdown('<div class="theme-btn">', unsafe_allow_html=True)
    st.button(toggle_label, on_click=toggle_theme, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Filters")

    gender_opts = ["All"] + sorted(df["Gender"].unique().tolist())
    gender = st.selectbox("👤 Gender", gender_opts)

    category_opts = ["All"] + sorted(df["Category"].unique().tolist())
    category = st.selectbox("🏷️ Category", category_opts)

    season_opts = ["All"] + sorted(df["Season"].unique().tolist())
    season = st.selectbox("🌦️ Season", season_opts)

    age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
    age_range = st.slider("🎂 Age Range", age_min, age_max, (age_min, age_max))

    st.markdown("---")
    st.markdown(f"<small style='color:{sub_text}'>Dataset: {len(df):,} records</small>", unsafe_allow_html=True)

# ── Apply filters ─────────────────────────────────────────────────────────────
fdf = df.copy()
if gender   != "All": fdf = fdf[fdf["Gender"]   == gender]
if category != "All": fdf = fdf[fdf["Category"] == category]
if season   != "All": fdf = fdf[fdf["Season"]   == season]
fdf = fdf[(fdf["Age"] >= age_range[0]) & (fdf["Age"] <= age_range[1])]

# ── Helper: apply plotly theme ────────────────────────────────────────────────
def apply_theme(fig, height=350):
    fig.update_layout(
        paper_bgcolor=plotly_paper,
        plot_bgcolor=plotly_bg,
        font_color=plotly_font,
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=border, zerolinecolor=border)
    fig.update_yaxes(gridcolor=border, zerolinecolor=border)
    return fig

# ── Title row ─────────────────────────────────────────────────────────────────
st.markdown(f"<h1 style='margin-bottom:0'>🛍️ Customer Shopping Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{sub_text}'>Showing <b style='color:{accent}'>{len(fdf):,}</b> of {len(df):,} records</p>", unsafe_allow_html=True)

# ── KPI metrics ───────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("👥 Customers",        f"{len(fdf):,}")
k2.metric("💰 Avg Purchase",     f"${fdf['Purchase Amount (USD)'].mean():.0f}" if len(fdf) else "—")
k3.metric("⭐ Avg Rating",       f"{fdf['Review Rating'].mean():.2f}" if len(fdf) else "—")
k4.metric("🔁 Avg Past Orders",  f"{fdf['Previous Purchases'].mean():.1f}" if len(fdf) else "—")
k5.metric("🎂 Avg Age",          f"{fdf['Age'].mean():.0f}" if len(fdf) else "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🛒 Products", "👤 Customers", "📋 Raw Data"])

# ─── TAB 1 : Overview ────────────────────────────────────────────────────────
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Revenue by Category")
        cat_rev = fdf.groupby("Category")["Purchase Amount (USD)"].sum().reset_index()
        fig = px.bar(cat_rev, x="Category", y="Purchase Amount (USD)",
                     color="Category", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with c2:
        st.subheader("Sales by Season")
        season_data = fdf.groupby("Season")["Purchase Amount (USD)"].sum().reset_index()
        fig = px.pie(season_data, names="Season", values="Purchase Amount (USD)",
                     hole=0.45, color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Purchase Amount Distribution")
        fig = px.histogram(fdf, x="Purchase Amount (USD)", nbins=30,
                           color_discrete_sequence=[accent])
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with c4:
        st.subheader("Payment Methods")
        pay = fdf["Payment Method"].value_counts().reset_index()
        pay.columns = ["Method", "Count"]
        fig = px.bar(pay, x="Count", y="Method", orientation="h",
                     color="Method", color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

# ─── TAB 2 : Products ────────────────────────────────────────────────────────
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Top 10 Items by Revenue")
        top_items = (fdf.groupby("Item Purchased")["Purchase Amount (USD)"]
                       .sum().nlargest(10).reset_index())
        fig = px.bar(top_items, x="Purchase Amount (USD)", y="Item Purchased",
                     orientation="h", color="Purchase Amount (USD)",
                     color_continuous_scale="Blues")
        st.plotly_chart(apply_theme(fig, height=400), use_container_width=True)

    with c2:
        st.subheader("Avg Rating by Category")
        cat_rating = fdf.groupby("Category")["Review Rating"].mean().reset_index()
        fig = px.bar(cat_rating, x="Category", y="Review Rating",
                     color="Review Rating", color_continuous_scale="RdYlGn",
                     range_y=[0, 5])
        st.plotly_chart(apply_theme(fig, height=400), use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Discount vs No Discount Revenue")
        disc = fdf.groupby("Discount Applied")["Purchase Amount (USD)"].sum().reset_index()
        fig = px.pie(disc, names="Discount Applied", values="Purchase Amount (USD)",
                     color_discrete_sequence=[accent, "#ff6b6b"])
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with c4:
        st.subheader("Shipping Type Distribution")
        ship = fdf["Shipping Type"].value_counts().reset_index()
        ship.columns = ["Shipping", "Count"]
        fig = px.pie(ship, names="Shipping", values="Count", hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

# ─── TAB 3 : Customers ───────────────────────────────────────────────────────
with tab3:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Age Distribution by Gender")
        fig = px.histogram(fdf, x="Age", color="Gender", barmode="overlay",
                           nbins=25, opacity=0.7,
                           color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with c2:
        st.subheader("Purchase Frequency")
        freq = fdf["Frequency of Purchases"].value_counts().reset_index()
        freq.columns = ["Frequency", "Count"]
        fig = px.bar(freq, x="Frequency", y="Count",
                     color="Count", color_continuous_scale="Purples")
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Subscription Status")
        sub = fdf["Subscription Status"].value_counts().reset_index()
        sub.columns = ["Status", "Count"]
        fig = px.pie(sub, names="Status", values="Count",
                     color_discrete_sequence=[accent, "#e0e0e0"])
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with c4:
        st.subheader("Age vs Purchase Amount")
        fig = px.scatter(fdf.sample(min(500, len(fdf))),
                         x="Age", y="Purchase Amount (USD)",
                         color="Category", opacity=0.6, size_max=8,
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

# ─── TAB 4 : Raw Data ────────────────────────────────────────────────────────
with tab4:
    st.subheader("Filtered Dataset")
    search = st.text_input("🔍 Search any column value")
    if search:
        mask = fdf.apply(lambda col: col.astype(str).str.contains(search, case=False)).any(axis=1)
        display_df = fdf[mask]
    else:
        display_df = fdf

    st.dataframe(display_df, use_container_width=True, height=400)
    st.download_button("⬇️ Download filtered CSV",
                       display_df.to_csv(index=False).encode("utf-8"),
                       "filtered_data.csv", "text/csv")