# SafeCampus — Segurança e Controle de Acesso em Ambientes Acadêmicos

Projeto IoT End-to-End com arquitetura em nuvem AWS.
Disciplina: Engenharia da Computação — Projeto IoT | CESUPA

## Arquitetura

- **EC2** (Ubuntu t3.micro) — Broker MQTT Mosquitto + Backend Flask
- **RDS** (PostgreSQL) — Banco de dados em sub-rede privada
- **S3** (safecampus-storage-2026) — Relatórios CSV e logs de auditoria
- **VPC** — Sub-rede pública (EC2) e privada (RDS)

## Sensores Simulados

- `simulador.py` — Simula leitores RFID de controle de acesso
- `simulador_fumaca.py` — Simula detectores de fumaça

## Estrutura do Projeto
cat > ~/safecampus/README.md << 'EOF'
# SafeCampus — Segurança e Controle de Acesso em Ambientes Acadêmicos

Projeto IoT End-to-End com arquitetura em nuvem AWS.
Disciplina: Engenharia da Computação — Projeto IoT | CESUPA

## Arquitetura

- **EC2** (Ubuntu t3.micro) — Broker MQTT Mosquitto + Backend Flask
- **RDS** (PostgreSQL) — Banco de dados em sub-rede privada
- **S3** (safecampus-storage-2026) — Relatórios CSV e logs de auditoria
- **VPC** — Sub-rede pública (EC2) e privada (RDS)

## Sensores Simulados

- `simulador.py` — Simula leitores RFID de controle de acesso
- `simulador_fumaca.py` — Simula detectores de fumaça

## Estrutura do Projeto
safecampus/
├── app.py                  # Dashboard Flask (rotas: /, /usuarios, /acessos, /alertas, /ocupacao, /relatorio)
├── mqtt_subscriber.py      # Subscriber MQTT — recebe dados e grava no RDS
├── simulador.py            # Simulador RFID
├── simulador_fumaca.py     # Simulador detector de fumaça
├── gerar_relatorio.py      # Gera CSV e envia para S3
├── schema.sql              # Script SQL de criação do banco
└── README.md

## Como Executar

### Pré-requisitos

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients python3-pip git -y
python3 -m venv venv
source venv/bin/activate
pip install flask psycopg2-binary paho-mqtt boto3
```

### Iniciar o sistema

```bash
cd ~/safecampus
source venv/bin/activate
python3 mqtt_subscriber.py &
python3 app.py &
curl ifconfig.me  # IP público atual
```

### Simular sensores

```bash
python3 simulador.py         # Publica eventos RFID
python3 simulador_fumaca.py  # Publica eventos de fumaça
```

### Gerar relatório CSV e enviar ao S3

```bash
python3 gerar_relatorio.py
```

## Banco de Dados

Executar `schema.sql` no PostgreSQL RDS:

```bash
psql -h <RDS_HOST> -U postgres -d safecampus -f schema.sql
```

### Tabelas

- `usuarios` — Alunos, professores e administradores
- `cartoes` — Cartões RFID vinculados a usuários
- `ambientes` — Laboratórios e salas monitoradas
- `registros_acesso` — Histórico de acessos com status
- `alertas` — Alertas de segurança (fumaça, acesso fora de horário)

## Tópicos MQTT

| Tópico | Dados |
|--------|-------|
| `campus/acesso` | `{"usuario_id": 1, "ambiente_id": 1, "status": "AUTORIZADO"}` |
| `campus/fumaca` | `{"tipo": "FUMACA", "descricao": "Detector acionado"}` |

## Serviços AWS

| Serviço | Configuração |
|---------|-------------|
| EC2 | t3.micro, Ubuntu 24.04, sub-rede pública |
| RDS | PostgreSQL, db.t3.micro, sub-rede privada |
| S3 | safecampus-storage-2026 |
| VPC | 10.0.0.0/16, us-east-1 |
