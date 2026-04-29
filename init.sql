
CREATE TABLE Usuarios (
    UsuarioID SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    DataNascimento DATE,
    Prioridade INTEGER CHECK (Prioridade BETWEEN 1 AND 3),
    Email VARCHAR(255) UNIQUE NOT NULL,
    Saldo DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE Inscricoes (
    InscricaoID SERIAL PRIMARY KEY,
    UsuarioID INTEGER NOT NULL REFERENCES Usuarios(UsuarioID) ON DELETE CASCADE,
   
    EventoID INTEGER DEFAULT 101, 
    Status VARCHAR(20) DEFAULT 'Espera' CHECK (Status IN ('Espera', 'Confirmada', 'Cancelada')),
    ValorPago DECIMAL(10,2) DEFAULT 0,
    Tipo VARCHAR(30),
    DataInscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Log_Auditoria (
    AuditoriaID SERIAL PRIMARY KEY,
    
    InscricaoID INTEGER REFERENCES Inscricoes(InscricaoID) ON DELETE CASCADE,
    Motivo VARCHAR(255) NOT NULL,
    DataAuditoria TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


TRUNCATE TABLE Usuarios RESTART IDENTITY CASCADE;


INSERT INTO Usuarios (Nome, Email, Prioridade, Saldo) VALUES 
('Matheus Oliveira', 'matheus.dev@email.com', 1, 150.00),
('Ana Beatriz Silva', 'ana.beatriz@email.com', 2, 100.00),
('Bruno Henrique Santos', 'bruno.henrique@email.com', 3, 100.00),
('Carla Fernanda Souza', 'carla.fernan@email.com', 1, 100.00),
('Diego Rodrigues Lima', 'diego.lima@email.com', 2, 100.00),
('Juliana Maria Costa', 'ju.costa@email.com', 3, 100.00);


INSERT INTO Inscricoes (UsuarioID, EventoID, Tipo, ValorPago, Status) VALUES 
(1, 101, 'VIP', 500.00, 'Confirmada'),       
(2, 101, 'ATIVISTA', 150.00, 'Confirmada'),  
(3, 101, 'VOLUNTÁRIO', 50.00, 'Confirmada'),
(4, 101, 'VIP', 500.00, 'Confirmada'),       
(6, 101, 'NORMAL', 100.00, 'Confirmada');