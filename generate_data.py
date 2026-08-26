"""
Generuje syntetická (vymyšlená) data pro ukázkový e-shop dashboard.
Žádná řádka nepochází z reálné firmy ani reálného zákazníka - čísla jsou
nastavená tak, aby ukázala typické vzorce (sezónnost, geografie doručení,
retence, poměr dopravy k ceně), ne pozorování z konkrétního datasetu.
Nepodléhá tedy žádné licenci třetí strany.
"""
import numpy as np
import pandas as pd

OUT = "data"
rng = np.random.default_rng(42)

# 1. Měsíční tržby (24 měsíců, sezónnost + růstový trend)
months = pd.period_range("2023-01", "2024-12", freq="M").astype(str)
trend = np.linspace(1.0, 1.6, len(months))
seasonality = {1: 0.85, 2: 0.85, 3: 0.95, 4: 1.0, 5: 1.0, 6: 0.9, 7: 0.8, 8: 0.85,
               9: 1.0, 10: 1.1, 11: 1.45, 12: 1.35}
season_factors = np.array([seasonality[int(m.split("-")[1])] for m in months])
noise = rng.normal(1.0, 0.04, len(months))
base_orders = 900
orders = (base_orders * trend * season_factors * noise).round().astype(int)
avg_order_value = rng.normal(1450, 40, len(months)).round(0)
revenue = (orders * avg_order_value).round(2)
items = (orders * rng.normal(1.35, 0.05, len(months))).round().astype(int)

monthly = pd.DataFrame({
    "year_month": months, "revenue": revenue, "orders": orders,
    "items": items, "avg_order_value": avg_order_value,
})
total_revenue = monthly["revenue"].sum()
total_orders = monthly["orders"].sum()
monthly.to_csv(f"{OUT}/monthly_revenue.csv", index=False)

# 2. Tržby podle kategorie (podíly sečtou na 100 %)
categories = {
    "Elektronika": 0.19, "Móda a oblečení": 0.15, "Domácnost a bydlení": 0.13,
    "Sport a outdoor": 0.10, "Krása a zdraví": 0.09, "Nábytek": 0.08,
    "Hračky a hry": 0.07, "Zahrada": 0.06, "Auto-moto doplňky": 0.05,
    "Knihy a média": 0.04, "Zvířecí potřeby": 0.03, "Potraviny a drogerie": 0.01,
}
cat_df = pd.DataFrame({"category": list(categories.keys()), "share": list(categories.values())})
cat_df["revenue"] = (cat_df["share"] * total_revenue).round(2)
cat_df["orders"] = (cat_df["share"] * total_orders * rng.normal(1.0, 0.03, len(cat_df))).round().astype(int)
cat_df.drop(columns="share").sort_values("revenue", ascending=False).to_csv(
    f"{OUT}/category_revenue.csv", index=False)

# 3. Tržby podle kraje (14 krajů ČR, váha podle přibližné velikosti trhu)
regions = {
    "Praha": 0.27, "Středočeský": 0.13, "Jihomoravský": 0.11, "Moravskoslezský": 0.09,
    "Ústecký": 0.06, "Plzeňský": 0.05, "Královéhradecký": 0.05, "Olomoucký": 0.05,
    "Zlínský": 0.04, "Pardubický": 0.04, "Jihočeský": 0.04, "Vysočina": 0.03,
    "Liberecký": 0.03, "Karlovarský": 0.01,
}
reg_df = pd.DataFrame({"region": list(regions.keys()), "share": list(regions.values())})
reg_df["revenue"] = (reg_df["share"] * total_revenue).round(2)
reg_df["orders"] = (reg_df["share"] * total_orders * rng.normal(1.0, 0.03, len(reg_df))).round().astype(int)
reg_df.drop(columns="share").sort_values("revenue", ascending=False).to_csv(
    f"{OUT}/region_revenue.csv", index=False)

# 4. Doba doručení vs. hodnocení (typický vzorec: déle = hůř hodnoceno)
delivery_summary = pd.DataFrame({
    "delivery_bucket": ["0–1 den", "2–3 dny", "4–6 dní", "7–10 dní", "10+ dní"],
    "avg_review_score": [4.8, 4.6, 4.2, 3.5, 2.4],
    "orders": [4200, 9800, 6100, 1600, 400],
    "on_time_rate": [99.8, 98.9, 95.2, 78.4, 22.1],
})
delivery_summary.to_csv(f"{OUT}/delivery_review_summary.csv", index=False)

on_time_review = pd.DataFrame({"on_time": ["Ano", "Ne"], "avg_review_score": [4.55, 2.85]})
on_time_review.to_csv(f"{OUT}/on_time_review.csv", index=False)

# 5. Doba doručení a hodnocení podle kraje (Praha/Brno = distribuční centrum = nejrychlejší)
region_delivery = reg_df[["region"]].copy()
region_delivery["avg_delivery_days"] = np.select(
    [region_delivery["region"].isin(["Praha", "Středočeský"]),
     region_delivery["region"].isin(["Jihomoravský", "Plzeňský"])],
    [1.8, 2.6], default=4.2,
) + rng.normal(0, 0.25, len(region_delivery))
region_delivery["avg_delivery_days"] = region_delivery["avg_delivery_days"].round(1)
region_delivery["avg_review_score"] = (4.7 - (region_delivery["avg_delivery_days"] - 1.8) * 0.28).round(2)
region_delivery["orders"] = reg_df["orders"].values
region_delivery.sort_values("avg_delivery_days", ascending=False).to_csv(
    f"{OUT}/region_delivery_review.csv", index=False)

# 6. Retence zákazníků
repeat_customers = pd.DataFrame({
    "segment": ["Jednorázoví zákazníci", "Opakovaní zákazníci"],
    "customers": [17400, 5600],
})
repeat_customers["pct"] = (repeat_customers["customers"] / repeat_customers["customers"].sum() * 100).round(1)
repeat_customers.to_csv(f"{OUT}/repeat_customers.csv", index=False)

# 7. Poměr ceny dopravy k ceně produktu podle kategorie
freight_ratio_map = {
    "Nábytek": 38, "Zahrada": 29, "Sport a outdoor": 24, "Domácnost a bydlení": 22,
    "Auto-moto doplňky": 19, "Hračky a hry": 16, "Zvířecí potřeby": 15,
    "Móda a oblečení": 11, "Potraviny a drogerie": 10, "Krása a zdraví": 8,
    "Knihy a média": 7, "Elektronika": 5,
}
freight_df = pd.DataFrame({
    "category": list(freight_ratio_map.keys()),
    "avg_freight_ratio": list(freight_ratio_map.values()),
})
freight_df.sort_values("avg_freight_ratio", ascending=False).to_csv(
    f"{OUT}/freight_ratio_category.csv", index=False)

# 8. Platební metody (typické pro český e-shop)
payment = pd.DataFrame({
    "payment_type": ["Platební karta", "Bankovní převod", "Dobírka", "Apple Pay / Google Pay", "Splátky"],
    "total_value": [0.52, 0.20, 0.14, 0.09, 0.05],
})
payment["total_value"] = (payment["total_value"] * total_revenue).round(2)
payment.sort_values("total_value", ascending=False).to_csv(f"{OUT}/payment_methods.csv", index=False)

print("Hotovo. Syntetická data v data/:")
for name in ["monthly_revenue", "category_revenue", "region_revenue", "delivery_review_summary",
             "on_time_review", "region_delivery_review", "repeat_customers",
             "freight_ratio_category", "payment_methods"]:
    print(f"  {name}.csv")
