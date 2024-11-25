CREATE TABLE Driver (
    id SERIAL PRIMARY KEY,  -- Автоинкрементируемый идентификатор
    name VARCHAR(255) NOT NULL,  -- Имя водителя
    experience INT NOT NULL,  -- Опыт работы
    phone BIGINT NOT NULL,  -- Телефон
    email VARCHAR(255) NOT NULL,  -- Электронная почта
    status VARCHAR(50) NOT NULL DEFAULT 'available'  -- Статус водителя с дефолтным значением
);

CREATE TABLE Vehicle (
    id SERIAL PRIMARY KEY,  -- Автоинкрементируемый идентификатор
    brand VARCHAR(255) NOT NULL,  -- Бренд автомобиля
    reg_num VARCHAR(50) NOT NULL UNIQUE,  -- Регистрационный номер
    mileage INT NOT NULL,  -- Пробег
    status VARCHAR(50) NOT NULL DEFAULT 'available'  -- Статус автомобиля с дефолтным значением
);

CREATE TABLE Task (
    id SERIAL PRIMARY KEY,  -- Автоинкрементируемый идентификатор
    route VARCHAR(255) NOT NULL,  -- Маршрут
    driver_id INT NOT NULL,  -- Ссылка на водителя
    status VARCHAR(50) NOT NULL,  -- Статус задачи
    car_id INT NOT NULL,  -- Ссылка на автомобиль
    CONSTRAINT fk_driver FOREIGN KEY (driver_id) REFERENCES Driver (id) ON DELETE CASCADE,
    CONSTRAINT fk_vehicle FOREIGN KEY (car_id) REFERENCES Vehicle (id) ON DELETE CASCADE
);



-- Функция для обновления статусов водителя и транспорта
CREATE OR REPLACE FUNCTION update_statuses_on_task_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Если задача добавляется со статусом 'pending'
    IF TG_OP = 'INSERT' AND NEW.status = 'pending' THEN
        UPDATE Driver SET status = 'unavailable' WHERE id = NEW.driver_id;
        UPDATE Vehicle SET status = 'unavailable' WHERE id = NEW.car_id;
    END IF;

    -- Если статус задачи обновляется на 'finished'
    IF TG_OP = 'UPDATE' AND NEW.status = 'finished' AND OLD.status <> 'finished' THEN
        UPDATE Driver SET status = 'available' WHERE id = NEW.driver_id;
        UPDATE Vehicle SET status = 'available' WHERE id = NEW.car_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер на вставку задачи
CREATE TRIGGER task_insert_trigger
AFTER INSERT ON Task
FOR EACH ROW
EXECUTE FUNCTION update_statuses_on_task_change();

-- Триггер на обновление статуса задачи
CREATE TRIGGER task_update_trigger
AFTER UPDATE OF status ON Task
FOR EACH ROW
EXECUTE FUNCTION update_statuses_on_task_change();


INSERT INTO Driver (name, experience, phone, email, status)
VALUES
    ('Иван Иванов', 5, 79211234567, 'ivan@example.com', 'available'),
    ('Петр Петров', 10, 79219876543, 'petr@example.com', 'available'),
    ('Анна Смирнова', 7, 79212345678, 'anna@example.com', 'available'),
    ('Сергей Кузнецов', 3, 79214567890, 'sergey@example.com', 'available');

INSERT INTO Vehicle (brand, reg_num, mileage, status)
VALUES
    ('Toyota', 'A123BC77', 100000, 'available'),
    ('Honda', 'B456DE78', 50000, 'available'),
    ('Ford', 'C789FG79', 150000, 'available'),
    ('BMW', 'D012HI80', 20000, 'available');


INSERT INTO Task (route, driver_id, status, car_id)
VALUES
    ('Route 1', 1, 'finished', 1),
    ('Route 2', 2, 'finished', 2),
    ('Route 3', 3, 'finished', 3),
    ('Route 4', 4, 'finished', 4);



INSERT INTO Task (route, driver_id, status, car_id)
VALUES ('New Route', 1, 'pending', 1);


SELECT * FROM Driver 
SELECT * FROM Vehicle
SELECT * FROM Task

ALTER TABLE Task
ALTER COLUMN status SET DEFAULT 'pending';

DELETE FROM Driver Where id = 1


CREATE OR REPLACE FUNCTION check_driver_and_vehicle_availability()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем статус водителя
    IF (SELECT status FROM Driver WHERE id = NEW.driver_id) != 'available' THEN
        RAISE EXCEPTION 'Driver with ID %s is unavailable', NEW.driver_id;
    END IF;

    -- Проверяем статус автомобиля
    IF (SELECT status FROM Vehicle WHERE id = NEW.car_id) != 'available' THEN
        RAISE EXCEPTION 'Vehicle with ID %s is unavailable', NEW.car_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER before_task_insert
BEFORE INSERT ON Task
FOR EACH ROW
EXECUTE FUNCTION check_driver_and_vehicle_availability();


CREATE OR REPLACE FUNCTION update_driver_vehicle_on_task_delete()
RETURNS TRIGGER AS $$
BEGIN
    -- Обновляем статус водителя на 'available'
    UPDATE Driver
    SET status = 'available'
    WHERE id = OLD.driver_id;

    -- Обновляем статус автомобиля на 'available'
    UPDATE Vehicle
    SET status = 'available'
    WHERE id = OLD.car_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER on_task_delete
AFTER DELETE ON Task
FOR EACH ROW
WHEN (OLD.status = 'pending')
EXECUTE FUNCTION update_driver_vehicle_on_task_delete();


