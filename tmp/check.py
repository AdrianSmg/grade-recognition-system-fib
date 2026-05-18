from django.db import connection

cursor = connection.cursor()
cursor.execute("SELECT id, valor_upc, escala_id FROM escales_valorescala")
rows = cursor.fetchall()
problematicos = []
for row in rows:
    try:
        float(str(row[1]))
    except (ValueError, TypeError):
        problematicos.append(row)
print(f"Total: {len(problematicos)}")
for p in problematicos:
    print(p)
