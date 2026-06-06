CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    matricula VARCHAR(20),
    tipo VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS ambientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    bloco VARCHAR(20),
    capacidade INTEGER
);

CREATE TABLE IF NOT EXISTS cartoes (
    id SERIAL PRIMARY KEY,
    uid_rfid VARCHAR(50) NOT NULL UNIQUE,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS registros_acesso (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    ambiente_id INTEGER REFERENCES ambientes(id),
    data_hora TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS alertas (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    descricao TEXT,
    data_hora TIMESTAMP DEFAULT NOW(),
    ambiente_id INTEGER REFERENCES ambientes(id)
);

INSERT INTO usuarios (nome, matricula, tipo) VALUES
('Joao Silva','2025001','ALUNO'),
('Maria Souza','2025002','PROFESSOR'),
('Carlos Lima','2025003','ADMIN')
ON CONFLICT DO NOTHING;

INSERT INTO ambientes (nome, bloco, capacidade) VALUES
('Laboratorio 01','Bloco A',30)
ON CONFLICT DO NOTHING;

INSERT INTO cartoes (uid_rfid, usuario_id) VALUES
('RFID-001', 1),('RFID-002', 2),('RFID-003', 3)
ON CONFLICT DO NOTHING;
