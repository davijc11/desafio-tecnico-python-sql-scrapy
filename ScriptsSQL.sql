venCREATE DATABASE IF NOT EXISTS teste_instar;
USE teste_instar;

CREATE TABLE clientes (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL
    );
    
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    data DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
    );

INSERT INTO clientes (nome, email) VALUES
    ('Lucas Ribeiro', 'lucas@gmail.com'),
    ('Beatriz Oliveira', 'beatriz@gmail.com'),
    ('Gabriel Costa', 'gabriel@gmail.com'),
    ('Manuela Mendes', 'manuela@gmail.com');
    
INSERT INTO pedidos (id_cliente, data, total) VALUES
    (1, '2026-01-10', 250.00),
    (1, '2026-02-15',  80.00),
    (2, '2026-01-20', 150.00),
    (2, '2026-03-05', 200.00),
    (3, '2026-02-28',  50.00),
    (4, '2026-03-10', 320.00);
    
SELECT DISTINCT
    c.id,
    c.nome,
    c.email
FROM clientes c
INNER JOIN pedidos p ON c.id = p.id_cliente
WHERE p.total > 100
ORDER BY c.nome ASC;

SELECT
    c.id,
    c.nome,
    c.email,
    COUNT(p.id) AS total_pedidos
FROM clientes c
LEFT JOIN pedidos p ON c.id = p.id_cliente
GROUP BY c.id, c.nome, c.email
ORDER BY total_pedidos DESC;