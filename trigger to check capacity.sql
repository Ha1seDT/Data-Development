CREATE FUNCTION check_aircraft_capacity() RETURNS TRIGGER AS $$
DECLARE
    max_capacity INT;
    current_count INT;
BEGIN
    -- Получаем вместимость самолета
    SELECT capacity INTO max_capacity 
    FROM Aircrafts 
    WHERE aircraft_id = (SELECT aircraft_id FROM Flights WHERE flight_id = NEW.flight_id LIMIT 1);

    -- Считаем уже проданные билеты
    SELECT COUNT(*) INTO current_count 
    FROM Tickets 
    WHERE flight_id = NEW.flight_id;

    -- Проверяем, есть ли свободные места
    IF current_count >= max_capacity THEN
        RAISE EXCEPTION 'Самолет заполнен';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_capacity
BEFORE INSERT ON Tickets
FOR EACH ROW
EXECUTE FUNCTION check_aircraft_capacity();
