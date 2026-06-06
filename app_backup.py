from flask import Flask
import psycopg2

app = Flask(__name__)

DB_HOST = "safecampus-db.cldbd5ryy83y.us-east-1.rds.amazonaws.com"
DB_NAME = "safecampus"
DB_USER = "postgres"
DB_PASSWORD = "safecampus123"

@app.route("/")
def home():
    return "SafeCampus funcionando!"

@app.route("/usuarios")
def usuarios():

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cur = conn.cursor()

    cur.execute("""
        SELECT id,nome,matricula,tipo
        FROM usuarios
        ORDER BY id
    """)

    dados = cur.fetchall()

    html = "<h1>Usuarios SafeCampus</h1>"

    for usuario in dados:
        html += f"""
        <p>
        ID: {usuario[0]}<br>
        Nome: {usuario[1]}<br>
        Matricula: {usuario[2]}<br>
        Tipo: {usuario[3]}
        </p>
        <hr>
        """

    cur.close()
    conn.close()

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
