CREATE TABLE test (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50),
    password VARCHAR(50)
);
INSERT INTO test (id, name, password) VALUES
    ('1', 'test_name_a', 'test_password_a'),
    ('2', 'test_name_b', 'test_password_b'),
    ('3', 'test_name_c', 'test_password_c');