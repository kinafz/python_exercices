CREATE TABLE IF NOT EXISTS tickets (
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	titre VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    priorite ENUM('faible', 'moyenne', 'haute') NOT NULL,
    statut ENUM('ouvert', 'en_cours', 'fermé') NOT NULL DEFAULT 'ouvert',
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);