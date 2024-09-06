DROP TABLE IF EXISTS exchange_rates;
DROP TABLE IF EXISTS currencies;
PRAGMA foreign_keys = ON;
PRAGMA encoding='UTF-8';
CREATE TABLE currencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    sign TEXT NOT NULL
);
CREATE TABLE exchange_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_currency_id INTEGER NOT NULL,
    target_currency_id INTEGER NOT NULL,
    rate DECIMAL(6,4) NOT NULL,
    FOREIGN KEY(base_currency_id) REFERENCES currencies(id),
    FOREIGN KEY(target_currency_id) REFERENCES currencies(id)
);
--CONSTRAINT fk_base_currency_id FOREIGN KEY(base_currency_id) REFERENCES currencies(id);
--CONSTRAINT fk_target_currency_id FOREIGN KEY(target_currency_id) REFERENCES currencies(id);
CREATE UNIQUE INDEX IF NOT EXISTS  base_target_idx ON exchange_rates (base_currency_id, target_currency_id);