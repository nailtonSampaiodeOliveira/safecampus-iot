import csv
import psycopg2

DB_HOST = "safecampus-db.cldbd5ryy83y.us-east-1.rds.amazonaws.com"
DB_NAME = "safecampus"
DB_USER = "postgres"
DB_PASSWORD = "safecampus123"

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()

cur.execute("""
    SELECT
        r.id,
        u.nome,
        a.nome,
        r.data_hora,
        r.status
    FROM registros_acesso r
    JOIN usuarios u ON r.usuario_id = u.id
    JOIN ambientes a ON r.ambiente_id = a.id
    ORDER BY r.id
""")

dados = cur.fetchall()

with open("relatorio_acessos.csv", "w", newline="", encoding="utf-8") as arquivo:

    escritor = csv.writer(arquivo)

    escritor.writerow([
        "id",
        "usuario",
        "ambiente",
        "data_hora",
        "status"
    ])

    escritor.writerows(dados)

cur.close()
conn.close()

print("Relatorio gerado com sucesso!")
