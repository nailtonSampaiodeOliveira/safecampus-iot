import json
import paho.mqtt.publish as publish

mensagem = {
    "usuario_id": 1,
    "ambiente_id": 1,
    "status": "AUTORIZADO"
}

publish.single(
    "safecampus/rfid",
    json.dumps(mensagem),
    hostname="localhost"
)

print("Acesso enviado para o MQTT")
