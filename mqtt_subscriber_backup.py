import json
import paho.mqtt.client as mqtt
import psycopg2

DB_HOST = "safecampus-db.cldbd5ryy83y.us-east-1.rds.amazonaws.com"
DB_NAME = "safecampus"
DB_USER = "postgres"
DB_PASSWORD = "safecampus123"

TOPICO = "safecampus/rfid"


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Conectado ao MQTT")
    client.subscribe(TOPICO)


def on_message(client, userdata, msg):

    dados = json.loads(msg.payload.decode())

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cur = conn.cursor()

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

    cur.close()
    conn.close()

    print("Acesso registrado:", dados)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
