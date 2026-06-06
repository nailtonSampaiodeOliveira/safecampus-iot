import csv
import psycopg2
import boto3

DB_HOST = "safecampus-db.cldbd5ryy83y.us-east-1.rds.amazonaws.com"
DB_NAME = "safecampus"
DB_USER = "postgres"
DB_PASSWORD = "safecampus123"
BUCKET = "safecampus-storage-2026"
ARQUIVO = "relatorio_acessos.csv"

conn = psycopg2.connect(
    host=DB_HOST, database=DB_NAME,
    user=DB_USER, password=DB_PASSWORD
)
cur = conn.cursor()
cur.execute("""
    SELECT r.id, u.nome, a.nome, r.data_hora, r.status
    FROM registros_acesso r
    JOIN usuarios u ON r.usuario_id = u.id
    JOIN ambientes a ON r.ambiente_id = a.id
    ORDER BY r.id
""")
dados = cur.fetchall()

with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    escritor.writerow(["id", "usuario", "ambiente", "data_hora", "status"])
    escritor.writerows(dados)

cur.close()
conn.close()
print("CSV gerado com sucesso!")

s3 = boto3.client("s3")
s3.upload_file(ARQUIVO, BUCKET, f"relatorios/{ARQUIVO}")
print(f"Enviado para s3://{BUCKET}/relatorios/{ARQUIVO}")
