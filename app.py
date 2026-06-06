from flask import Flask
import psycopg2
from datetime import datetime

app = Flask(__name__)

DB_HOST = "safecampus-db.cldbd5ryy83y.us-east-1.rds.amazonaws.com"
DB_NAME = "safecampus"
DB_USER = "postgres"
DB_PASSWORD = "safecampus123"

def get_conn():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

@app.route("/")
def home():
    return """
    <h1>SafeCampus</h1>
    <ul>
        <li><a href="/usuarios">Usuarios</a></li>
        <li><a href="/acessos">Historico de Acessos</a></li>
        <li><a href="/alertas">Alertas de Seguranca</a></li>
        <li><a href="/ocupacao">Ocupacao por Ambiente</a></li>
        <li><a href="/relatorio">Relatorio de Uso</a></li>
    </ul>
    """

@app.route("/usuarios")
def usuarios():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, matricula, tipo FROM usuarios ORDER BY id")
    dados = cur.fetchall()
    cur.close(); conn.close()
    html = "<h1>Usuarios SafeCampus</h1>"
    for u in dados:
        html += f"<p>ID: {u[0]}<br>Nome: {u[1]}<br>Matricula: {u[2]}<br>Tipo: {u[3]}</p><hr>"
    return html

@app.route("/acessos")
def acessos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.id, u.nome, a.nome, r.data_hora, r.status
        FROM registros_acesso r
        JOIN usuarios u ON r.usuario_id = u.id
        JOIN ambientes a ON r.ambiente_id = a.id
        ORDER BY r.id DESC
    """)
    dados = cur.fetchall()
    cur.close(); conn.close()
    html = "<h1>Historico de Acessos - SafeCampus</h1>"
    for a in dados:
        html += f"<p>ID: {a[0]}<br>Usuario: {a[1]}<br>Ambiente: {a[2]}<br>Data/Hora: {a[3]}<br>Status: {a[4]}</p><hr>"
    return html

@app.route("/alertas")
def alertas():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, tipo, descricao, data_hora FROM alertas ORDER BY id DESC")
    dados = cur.fetchall()
    cur.close(); conn.close()
    html = "<h1>Alertas de Seguranca - SafeCampus</h1>"
    for a in dados:
        html += f"<p>ID: {a[0]}<br>Tipo: {a[1]}<br>Descricao: {a[2]}<br>Data/Hora: {a[3]}</p><hr>"
    return html

@app.route("/ocupacao")
def ocupacao():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            a.id,
            a.nome,
            a.bloco,
            a.capacidade,
            COUNT(CASE WHEN r.status = 'AUTORIZADO' AND r.data_hora >= NOW() - INTERVAL '1 hour' THEN 1 END) AS presentes
        FROM ambientes a
        LEFT JOIN registros_acesso r ON a.id = r.ambiente_id
        GROUP BY a.id, a.nome, a.bloco, a.capacidade
        ORDER BY a.bloco, a.nome
    """)
    dados = cur.fetchall()
    cur.close(); conn.close()

    html = "<h1>Ocupacao por Ambiente - SafeCampus</h1>"
    html += f"<p><small>Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</small></p>"
    html += "<table border='1' cellpadding='8' cellspacing='0'>"
    html += "<tr><th>Ambiente</th><th>Bloco</th><th>Capacidade</th><th>Presentes (1h)</th><th>Status</th></tr>"
    for d in dados:
        presentes = d[4] or 0
        capacidade = d[3] or 0
        pct = round((presentes / capacidade * 100)) if capacidade > 0 else 0
        if pct >= 80:
            status = "LOTADO"
        elif pct >= 50:
            status = "OCUPADO"
        elif presentes > 0:
            status = "EM USO"
        else:
            status = "LIVRE"
        html += f"<tr><td>{d[1]}</td><td>{d[2]}</td><td>{capacidade}</td><td>{presentes}</td><td><b>{status}</b></td></tr>"
    html += "</table>"
    html += "<br><a href='/'>Voltar</a>"
    return html

@app.route("/relatorio")
def relatorio():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            a.nome AS ambiente,
            COUNT(r.id) AS total_acessos,
            COUNT(CASE WHEN r.status = 'AUTORIZADO' THEN 1 END) AS autorizados,
            COUNT(CASE WHEN r.status = 'NEGADO' THEN 1 END) AS negados,
            MAX(r.data_hora) AS ultimo_acesso
        FROM ambientes a
        LEFT JOIN registros_acesso r ON a.id = r.ambiente_id
        GROUP BY a.nome
        ORDER BY total_acessos DESC
    """)
    dados = cur.fetchall()
    cur.close(); conn.close()

    html = "<h1>Relatorio de Uso dos Laboratorios - SafeCampus</h1>"
    html += f"<p><small>Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</small></p>"
    html += "<table border='1' cellpadding='8' cellspacing='0'>"
    html += "<tr><th>Ambiente</th><th>Total Acessos</th><th>Autorizados</th><th>Negados</th><th>Ultimo Acesso</th></tr>"
    for d in dados:
        html += f"<tr><td>{d[0]}</td><td>{d[1]}</td><td>{d[2]}</td><td>{d[3]}</td><td>{d[4]}</td></tr>"
    html += "</table>"
    html += "<br><a href='/'>Voltar</a>"
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
