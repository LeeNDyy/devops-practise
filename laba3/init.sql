DROP TABLE IF EXISTS users CASCADE;

-- Создать новую таблицу
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 100),
    town VARCHAR(100) NOT NULL
);

INSERT INTO users (name, surname, age, town)
SELECT
    (ARRAY['John', 'Mike', 'Tom', 'Alex', 'Chris'])[floor(random() * 5 + 1)],
    (ARRAY['Smith', 'Brown', 'Johnson', 'Taylor', 'Davis'])[floor(random() * 5 + 1)],
    floor(random() * 50 + 20)::int,  -- Age 20-69
    (ARRAY['New York', 'Chicago', 'Boston', 'Seattle', 'Austin'])[floor(random() * 5 + 1)]
FROM generate_series(1, 100000) AS i;