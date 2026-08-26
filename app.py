import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Prodej a e-shop – ukázkový dashboard", layout="wide")

DATA_DIR = "data"


@st.cache_data
def load_data():
    monthly = pd.read_csv(f"{DATA_DIR}/monthly_revenue.csv")
    category = pd.read_csv(f"{DATA_DIR}/category_revenue.csv")
    region = pd.read_csv(f"{DATA_DIR}/region_revenue.csv")
    delivery = pd.read_csv(f"{DATA_DIR}/delivery_review_summary.csv")
    on_time = pd.read_csv(f"{DATA_DIR}/on_time_review.csv")
    repeat_customers = pd.read_csv(f"{DATA_DIR}/repeat_customers.csv")
    freight_ratio = pd.read_csv(f"{DATA_DIR}/freight_ratio_category.csv")
    payment = pd.read_csv(f"{DATA_DIR}/payment_methods.csv")
    return monthly, category, region, delivery, on_time, repeat_customers, freight_ratio, payment


def style(fig, height=420, y_title=None, x_title=None):
    fig.update_layout(
        height=height,
        template="plotly_white",
        font=dict(size=14),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(t=60, l=10, r=10, b=10),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")
    if y_title:
        fig.update_yaxes(title_text=y_title)
    if x_title:
        fig.update_xaxes(title_text=x_title)
    return fig


PRIMARY = "#4C78A8"
ACCENT = "#F58518"

monthly, category, region, delivery, on_time, repeat_customers, freight_ratio, payment = load_data()

st.title("Prodej a e-shop – ukázkový dashboard")
st.caption(
    "Ukázkový dashboard nad **syntetickými (vymyšlenými) daty** typického e-shopu – "
    "žádná reálná firma, žádná reálná data zákazníků. Cílem je ukázat typ analýzy "
    "(tržby v čase, top kategorie, kraje, spokojenost zákazníků, platby), ne konkrétní "
    "čísla. Data: 2023-01 až 2024-12."
)

total_revenue = monthly["revenue"].sum()
total_orders = monthly["orders"].sum()
avg_order_value = total_revenue / total_orders
avg_review = (delivery["avg_review_score"] * delivery["orders"]).sum() / delivery["orders"].sum()


def kc(value):
    return f"{value:,.0f} Kč".replace(",", " ")


col1, col2, col3, col4 = st.columns(4)
col1.metric("Tržby celkem", kc(total_revenue))
col2.metric("Objednávky celkem", f"{total_orders:,.0f}".replace(",", " "))
col3.metric("Průměrná hodnota objednávky", kc(avg_order_value))
col4.metric("Průměrné hodnocení", f"{avg_review:.2f} / 5")

st.header("1. Vývoj tržeb v čase")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=monthly["year_month"], y=monthly["revenue"], name="Tržby",
                           mode="lines+markers", line=dict(color=PRIMARY, width=3), marker=dict(size=5)))
style(fig1, y_title="Kč", x_title="Měsíc")
st.plotly_chart(fig1, use_container_width=True)

col_a, col_b = st.columns(2)
fig1b = go.Figure()
fig1b.add_trace(go.Bar(x=monthly["year_month"], y=monthly["orders"], marker_color=PRIMARY))
style(fig1b, height=360, y_title="počet objednávek")
fig1b.update_layout(title=dict(text="Počet objednávek podle měsíce", font=dict(size=15)))
col_a.plotly_chart(fig1b, use_container_width=True)

fig1c = go.Figure()
fig1c.add_trace(go.Scatter(x=monthly["year_month"], y=monthly["avg_order_value"],
                            mode="lines+markers", line=dict(color=ACCENT, width=3)))
style(fig1c, height=360, y_title="Kč")
fig1c.update_layout(title=dict(text="Průměrná hodnota objednávky", font=dict(size=15)))
col_b.plotly_chart(fig1c, use_container_width=True)

st.header("2. Top kategorie produktů podle tržeb")
cat_sorted = category.sort_values("revenue", ascending=True)
fig2 = go.Figure()
fig2.add_trace(go.Bar(y=cat_sorted["category"], x=cat_sorted["revenue"], orientation="h",
                       marker_color=PRIMARY))
style(fig2, height=480, x_title="Kč")
st.plotly_chart(fig2, use_container_width=True)

st.header("3. Tržby podle kraje zákazníka (top 10)")
region_sorted = region.sort_values("revenue", ascending=False).head(10).sort_values("revenue")
fig3 = go.Figure()
fig3.add_trace(go.Bar(y=region_sorted["region"], x=region_sorted["revenue"], orientation="h",
                       marker_color=ACCENT))
style(fig3, height=420, x_title="Kč")
st.plotly_chart(fig3, use_container_width=True)

st.header("4. Doba doručení vs. spokojenost zákazníka")
st.caption("Jasně vidět: čím déle objednávka jede, tím nižší hodnocení dává zákazník.")
col_c, col_d = st.columns(2)

fig4 = go.Figure()
fig4.add_trace(go.Bar(x=delivery["delivery_bucket"], y=delivery["avg_review_score"],
                       marker_color=PRIMARY))
style(fig4, height=380, y_title="průměrné hodnocení (1–5)")
fig4.update_layout(title=dict(text="Hodnocení podle doby doručení", font=dict(size=15)))
col_c.plotly_chart(fig4, use_container_width=True)

fig5 = go.Figure()
fig5.add_trace(go.Bar(x=on_time["on_time"], y=on_time["avg_review_score"],
                       marker_color=["#54A24B", "#E45756"]))
style(fig5, height=380, y_title="průměrné hodnocení (1–5)", x_title="Doručeno včas?")
fig5.update_layout(title=dict(text="Hodnocení: včas vs. pozdě", font=dict(size=15)))
col_d.plotly_chart(fig5, use_container_width=True)

st.header("5. Retence zákazníků a poměr dopravy k ceně")
repeat_pct = repeat_customers.loc[repeat_customers["segment"] == "Opakovaní zákazníci", "pct"].iloc[0]
st.markdown(
    f"Jen **{repeat_pct:.1f} %** zákazníků u tohoto e-shopu nakoupilo víckrát než jednou "
    f"({repeat_customers.loc[repeat_customers['segment']=='Opakovaní zákazníci','customers'].iloc[0]:,} "
    f"z {repeat_customers['customers'].sum():,} zákazníků). Velká část obchodu tak stojí "
    f"na akvizici nových zákazníků, ne na jejich udržení — typický signál, že chybí důvod "
    f"se vracet (věrnostní program, remarketing, e-mail po nákupu)."
)

col_g, col_h = st.columns(2)
fig9 = go.Figure()
fig9.add_trace(go.Pie(labels=repeat_customers["segment"], values=repeat_customers["customers"], hole=0.5,
                       marker=dict(colors=["#E45756", "#54A24B"])))
fig9.update_layout(height=380, template="plotly_white", font=dict(size=14), margin=dict(t=20))
col_g.plotly_chart(fig9, use_container_width=True)

top_freight = freight_ratio.sort_values("avg_freight_ratio", ascending=False).head(8).sort_values("avg_freight_ratio")
fig10 = go.Figure()
fig10.add_trace(go.Bar(y=top_freight["category"], x=top_freight["avg_freight_ratio"], orientation="h",
                        marker_color=ACCENT))
style(fig10, height=380, x_title="doprava jako % ceny produktu")
fig10.update_layout(title=dict(text="Nejvyšší poměr dopravy k ceně (top 8 kategorií)", font=dict(size=15)))
col_h.plotly_chart(fig10, use_container_width=True)
st.caption(f"Průměr napříč kategoriemi: {freight_ratio['avg_freight_ratio'].mean():.0f} % "
           "— u některých kategorií doprava tvoří velkou část ceny produktu.")

st.header("6. Platební metody")
fig6 = go.Figure()
fig6.add_trace(go.Pie(labels=payment["payment_type"], values=payment["total_value"], hole=0.5))
fig6.update_layout(height=420, template="plotly_white", font=dict(size=14), margin=dict(t=20))
st.plotly_chart(fig6, use_container_width=True)
