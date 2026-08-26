# Prodej a e-shop – ukázkový dashboard

Demo dashboard nad **syntetickými (vymyšlenými) daty** typického e-shopu – žádná reálná
firma, žádná reálná data zákazníků, žádná závislost na licenci třetí strany.

Účel: ukázka typu analýzy pro potenciální klienty (tržby v čase, top kategorie, kraje,
vztah doby doručení a spokojenosti zákazníka, retence, platební metody) – **ne** prodej
samotných dat ani reálná data konkrétní firmy.

## Data

Všechna data v `data/` generuje `generate_data.py` (numpy/pandas, pevný random seed pro
reprodukovatelnost). Čísla jsou nastavená tak, aby ukázala typické vzorce (sezónnost,
geografie doručení, retence, poměr dopravy k ceně), ne pozorování z reálného zdroje.

Pro přegenerování:

```bash
python3 generate_data.py
```

## Spuštění

```bash
pip install -r requirements.txt
streamlit run app.py
```
