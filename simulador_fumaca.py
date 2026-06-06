import json
import random
import paho.mqtt.publish as publish

nivel = random.randint(50, 100)

mensagem = {
    "sensor": "fumaca",
    "ambiente_id": 1,
    "nivel": nivel
}

publish.single(
    "safecampus/fumaca",
    json.dumps(mensagem),
    hostname="localhost"
)

print("Nivel de fumaca enviado:", nivel)
