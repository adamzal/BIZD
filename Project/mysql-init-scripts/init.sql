USE zbd;

-- TABLES PRE-CREATION

CREATE TABLE IF NOT EXISTS Worker (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(40) NOT NULL,
    role ENUM('manager', 'broker') NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS Property (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    type ENUM('flat', 'building') NOT NULL,
    address VARCHAR(255) NOT NULL,
    area FLOAT NOT NULL,
    rooms INT NOT NULL,
    sqm_price FLOAT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS Client (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(40) NOT NULL,
    pesel CHAR(11) NOT NULL,
    phone VARCHAR(12) NOT NULL,
    email VARCHAR(50) NOT NULL,
    city VARCHAR(30) NOT NULL,
    postcode CHAR(6) NOT NULL
);

CREATE TABLE IF NOT EXISTS Transaction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    client_id INT,
    worker_id INT,
    tr_date DATETIME,
    final_price FLOAT NOT NULL,
    tr_status ENUM('started', 'completed', 'cancelled') NOT NULL,
    FOREIGN KEY (property_id) REFERENCES Property(ID),
    FOREIGN KEY (client_id) REFERENCES Client(ID),
    FOREIGN KEY (worker_id) REFERENCES Worker(ID)
);

CREATE TABLE IF NOT EXISTS Historical_transaction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    client_id INT,
    worker_id INT,
    tr_date DATETIME,
    final_price FLOAT NOT NULL,
    tr_status ENUM('started', 'completed', 'cancelled') NOT NULL,
    FOREIGN KEY (property_id) REFERENCES Property(ID),
    FOREIGN KEY (client_id) REFERENCES Client(ID),
    FOREIGN KEY (worker_id) REFERENCES Worker(ID)
);

CREATE TABLE IF NOT EXISTS month_count_transaction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    tr_month INT,
    tr_count INT
);

CREATE TABLE IF NOT EXISTS year_count_transaction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    tr_year INT,
    tr_count INT
);

CREATE TABLE IF NOT EXISTS year_sum_price_transaction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    tr_year INT,
    tr_sum_price FLOAT
);

CREATE TABLE IF NOT EXISTS month_sum_price_transaction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    tr_month INT,
    tr_sum_price FLOAT
);

DELIMITER //
CREATE TRIGGER after_insert_transaction
AFTER INSERT ON Transaction FOR EACH ROW
BEGIN
    DECLARE v_tr_month INT;
    DECLARE v_tr_year INT;
    DECLARE v_tr_sum_price DECIMAL(12,2);
    DECLARE v_tr_status ENUM('started', 'completed', 'cancelled');

    SET v_tr_month = MONTH(NEW.tr_date);
    SET v_tr_year = YEAR(NEW.tr_date);
    SET v_tr_sum_price = NEW.final_price;
    SET v_tr_status = NEW.tr_status;

    IF (SELECT COUNT(*) FROM month_count_transaction WHERE tr_month = v_tr_month) > 0 THEN
        UPDATE month_count_transaction
        SET tr_count = tr_count + 1
        WHERE tr_month = v_tr_month;
    ELSE
        INSERT INTO month_count_transaction (tr_month, tr_count)
        VALUES (v_tr_month, 1);
    END IF;

    IF (SELECT COUNT(*) FROM year_count_transaction WHERE tr_year = v_tr_year) > 0 THEN
        UPDATE year_count_transaction
        SET tr_count = tr_count + 1
        WHERE tr_year = v_tr_year;
    ELSE
        INSERT INTO year_count_transaction (tr_year, tr_count)
        VALUES (v_tr_year, 1);
    END IF;

    IF (SELECT COUNT(*) FROM year_sum_price_transaction WHERE tr_year = v_tr_year) > 0 THEN
        UPDATE year_sum_price_transaction
        SET tr_sum_price = tr_sum_price + v_tr_sum_price
        WHERE tr_year = v_tr_year;
    ELSE
        INSERT INTO year_sum_price_transaction (tr_year, tr_sum_price)
        VALUES (v_tr_year, v_tr_sum_price);
    END IF;

    IF (SELECT COUNT(*) FROM month_sum_price_transaction WHERE tr_month = v_tr_month) > 0 THEN
        UPDATE month_sum_price_transaction
        SET tr_sum_price = tr_sum_price + v_tr_sum_price
        WHERE tr_month = v_tr_month;
    ELSE
        INSERT INTO month_sum_price_transaction (tr_month, tr_sum_price)
        VALUES (v_tr_month, v_tr_sum_price);
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE FUNCTION IsValidPesel(p_pesel CHAR(11)) RETURNS BOOLEAN DETERMINISTIC
BEGIN
    DECLARE v_weight INT DEFAULT 1;
    DECLARE v_sum INT DEFAULT 0;
    DECLARE x INT DEFAULT 1;

    IF LENGTH(p_pesel) <> 11 THEN
        RETURN FALSE;
    END IF;

    REPEAT
        SET v_sum = v_sum + SUBSTRING(p_pesel, x, 1) * v_weight;
        SET v_weight = CASE WHEN v_weight = 9 THEN 1 ELSE v_weight + 2 END;
        IF v_weight = 5 THEN
            SET v_weight = v_weight + 2;
        END IF;
        SET x = x + 1;
    UNTIL x > 10 END REPEAT;

    SET v_sum = v_sum % 10;
    SET v_sum = CASE WHEN v_sum = 0 THEN 0 ELSE 10 - v_sum END;

    RETURN v_sum = SUBSTRING(p_pesel, 11, 1);
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_insert_client
BEFORE INSERT ON Client FOR EACH ROW
BEGIN
    DECLARE v_pesel CHAR(11);
    DECLARE v_is_pesel_valid BOOLEAN;

    SET v_pesel = NEW.pesel;
    SET v_is_pesel_valid = IsValidPesel(v_pesel);

    IF NOT v_is_pesel_valid THEN
        SET @custom_error_message = CONCAT('Invalid PESEL (', v_pesel, '). Cannot insert data into Client table.');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = @custom_error_message;
    END IF;
END;
//
DELIMITER ;
