from pathlib import Path
import re
import requests

url = "https://modern-sql.com/reserved-words-empirical-list.html"
text = requests.get(url).text

words = {}
for (y, word) in re.findall(r'y="(\d+)"><tspan class="code.*?">(.+?)</tspan>', text):
    words[str(int(y) - 14)] = word

words_by_dialect = {}
dialect = None
for chunk in text.split('<g class="hoverable">'):
    if m := re.search(r'rotate\(-45\)">(.+?)</text>', chunk):
        dialect = m[1]
        words_by_dialect[dialect] = []
        for (href, y) in re.findall(r'<use href="#(.+?)" transform="translate\(\d+,(\d+)\)"/>', chunk):
            if href != "none":
                words_by_dialect[dialect].append(words[y])

dialects = {
    "Apache Derby": "",
    "BigQuery": "",
    "Db2 (LUW)": "",
    "H2": "",
    "MariaDB": "",
    "MySQL": "mysql.yaml",
    "Oracle DB": "oracle.yaml",
    "PostgreSQL": "postgresql.yaml",
    "SQL Server": "mssql.yaml",
    "SQLite": "sqlite.yaml",
}

for (dialect, filename) in dialects.items():
    if not filename:
        continue
    alternative = "|".join(words_by_dialect[dialect])
    path = Path("mocodo", "resources", "relation_templates", filename)
    text = path.read_text(encoding="utf8")
    text = re.sub(r"('Protect reserved keywords'\n    search: ).+", fr"\1'(?i)^({alternative})$'", text)
    path.write_text(text, encoding="utf8")
    print(f"{filename} updated.")
