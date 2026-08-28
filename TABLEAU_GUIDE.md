# Návod: postavení dashboardu v Tableau Public

Data jsou stejná jako ve Streamlit appce (`data/*.csv`), jen se v Tableau nestaví kódem,
ale přetahováním polí do plátna. Postup níže odpovídá sekcím 1–6 v `app.py`.

## 0. Příprava

1. Stáhni [Tableau Public Desktop](https://public.tableau.com) (zdarma, potřeba registrace).
2. Stáhni si soubory z `data/` (8 CSV: `monthly_revenue`, `category_revenue`,
   `region_revenue`, `delivery_review_summary`, `on_time_review`, `repeat_customers`,
   `freight_ratio_category`, `payment_methods`).
3. V Tableau: **Connect → Text file** → načti postupně všech 8 CSV (každé jako
   samostatný data source, nejsou mezi sebou propojené společným klíčem).

## 1. Worksheet: Tržby a zisk v čase

- Zdroj: `monthly_revenue`
- Columns: `year_month`
- Rows: `SUM(revenue)`
- Přetáhni `SUM(profit)` na plochu grafu, zvol **Dual Axis** (pravý klik na osu → Dual Axis)
- Mark type: Line, tloušťka čáry 2–3px
- Barvy: tržby modrá (#4C78A8), zisk zelená (#54A24B)

## 2. Worksheet: Objednávky podle měsíce

- Zdroj: `monthly_revenue`
- Columns: `year_month`, Rows: `SUM(orders)`, Mark type: Bar

## 3. Worksheet: Průměrná hodnota objednávky

- Zdroj: `monthly_revenue`
- Columns: `year_month`, Rows: `AVG(avg_order_value)`, Mark type: Line

## 4. Worksheet: Top kategorie podle tržeb

- Zdroj: `category_revenue`
- Rows: `category` (seřaď sestupně podle SUM(revenue): klikni na ikonu řazení)
- Columns: `SUM(revenue)`, Mark type: Bar (horizontální - swap rows/columns)

## 5. Worksheet: Tržby podle kraje

- Zdroj: `region_revenue`
- Rows: `region`, Columns: `SUM(revenue)`, Mark type: Bar
- Filtr: Top 10 podle SUM(revenue) (pravý klik na `region` → Filter → Top → By field → Top 10)

## 6. Worksheet: Hodnocení podle doby doručení

- Zdroj: `delivery_review_summary`
- Columns: `delivery_bucket`, Rows: `AVG(avg_review_score)`, Mark type: Bar
- Seřaď ručně podle pořadí koše (0–1 den ... 10+ dní), ne abecedně

## 7. Worksheet: Hodnocení – včas vs. pozdě

- Zdroj: `on_time_review`
- Columns: `on_time`, Rows: `AVG(avg_review_score)`, Mark type: Bar
- Barva podle `on_time`: Ano = zelená, Ne = červená (Color shelf → Edit Colors)

## 8. Worksheet: Retence zákazníků

- Zdroj: `repeat_customers`
- Mark type: Pie
- Angle: `SUM(customers)`, Color: `segment`
- Volitelně: donut efekt (druhý menší kruh přes první, běžný Tableau trik)

## 9. Worksheet: Poměr dopravy k ceně

- Zdroj: `freight_ratio_category`
- Rows: `category` (seřaď sestupně podle `avg_freight_ratio`), Columns: `avg_freight_ratio`
- Mark type: Bar, filtr Top 8

## 10. Worksheet: Platební metody

- Zdroj: `payment_methods`
- Mark type: Pie, Angle: `SUM(total_value)`, Color: `payment_type`

## 11. Sestavení dashboardu

1. **New Dashboard** (ikona dole v liště se záložkami)
2. Nastav velikost plátna na **Fixed size → 1200×1600** (nebo Automatic pro responzivní)
3. Přetahuj jednotlivé worksheety na plátno v pořadí odpovídajícím sekcím 1–6 z appky
4. Přidej textový nadpis nahoru: "Prodej a e-shop – ukázkový dashboard"
5. Formátování čísel na Kč: klikni pravým na míru (např. `SUM(revenue)`) → **Format** →
   **Numbers → Custom** → zadej `#,##0 "Kč"`

## 12. Publikování

**Server → Tableau Public → Save to Tableau Public** → appka tě vyzve k přihlášení a
publikuje dashboard na veřejný odkaz `public.tableau.com/app/profile/tvůj-účet/...`,
který můžeš sdílet stejně jako Streamlit appku.
