import json
import paho.mqtt.client as mqtt
import psycopg2

DB_HOST = "safecampus-db.cldbd5ryy83y.us-east-1.rds.amazonaws.com"
DB_NAME = "safecampus"
DB_USER = "postgres"
DB_PASSWORD = "safecampus123"

TOPICO_RFID = "safecampus/rfid"
TOPICO_FUMACA = "safecampus/fumaca"


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Conectado ao MQTT")

    client.subscribe(TOPICO_RFID)
    client.subscribe(TOPICO_FUMACA)


def on_message(client, userdata, msg):

    dados = json.loads(msg.payload.decode())

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cur = conn.cursor()

    # RFID
    if msg.topic == TOPICO_RFID:

        cur.execute("""
            INSERT INTO registros_acesso
            (usuario_id, ambiente_id, status)
            VALUES (%s,%s,%s)
        """, (
            dados["usuario_id"],
            dados["ambiente_id"],
            dados["status"]
        ))

        conn.commit()

        print("Acesso registrado:", dados)

    # SENSOR DE FUMAÇA
    elif msg.topic == TOPICO_FUMACA:

        nivel = dados["nivel"]

        print("Nivel de fumaca recebido:", nivel)

        if nivel > 70:

            cur.execute("""
                INSERT INTO alertas
                (tipo, descricao)
                VALUES (%s,%s)
            """, (
                "FUMACA",
                f"Detector de fumaca acionado no ambiente {dados['ambiente_id']} - Nivel {nivel}"
            ))

            conn.commit()

            print("ALERTA DE FUMACA REGISTRADO")

    cur.close()
    conn.close()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
