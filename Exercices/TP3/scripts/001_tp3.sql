CREATE TABLE IF NOT EXISTS releases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    version VARCHAR(50),
    tag_git VARCHAR(50),
    date_creation DATETIME
);

CREATE TABLE IF NOT EXISTS environnements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50) UNIQUE CHECK (nom IN ('dev', 'staging', 'prod'))
);

CREATE TABLE IF NOT EXISTS deploiements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_release INT,
    id_env INT,
    etat ENUM('planifié', 'validé', 'en_cours', 'réussi', 'échec', 'annulé'),
    date_deploiement DATETIME,
    FOREIGN KEY (id_release) REFERENCES releases(id),
    FOREIGN KEY (id_env) REFERENCES environnements(id)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    action TEXT,
    message TEXT,
    timestamp DATETIME
);

INSERT INTO environnements(nom)
SELECT * FROM (SELECT 'dev') AS tmp1
WHERE NOT EXISTS (
    SELECT 1 FROM environnements WHERE nom = 'dev'
) LIMIT 1;

INSERT INTO environnements(nom)
SELECT * FROM (SELECT 'staging') AS tmp2
WHERE NOT EXISTS (
    SELECT 1 FROM environnements WHERE nom = 'staging'
) LIMIT 1;

INSERT INTO environnements(nom)
SELECT * FROM (SELECT 'prod') AS tmp3
WHERE NOT EXISTS (
    SELECT 1 FROM environnements WHERE nom = 'prod'
) LIMIT 1;