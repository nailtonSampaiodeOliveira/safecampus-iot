import psycopg2

conn = psycopg2.connect(
    host="safecampus-db.cldbd5ryy83y.us-east-1.rds.amazonaws.com",
    database="safecampus",
    user="postgres",
    password="safecampus123"
)

cur = conn.cursor()

cur.execute("SELECT * FROM usuarios;")

dados = cur.fetchall()

print(dados)

cur.close()
conn.close()
