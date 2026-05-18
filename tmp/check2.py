from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT id, valor_upc, escala_id FROM escales_valorescala ORDER BY length(cast(valor_upc as text)) DESC LIMIT 20")
rows = cursor.fetchall()
for row in rows:
    print(row)
