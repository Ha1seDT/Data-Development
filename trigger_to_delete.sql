CREATE OR REPLACE FUNCTION delete_tickets_by_flight() 
RETURNS TRIGGER AS $$
BEGIN
    -- Удаляем все билеты, связанные с удаляемым рейсом
    DELETE FROM Tickets WHERE flight_id = OLD.flight_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_delete_flight_tickets
BEFORE DELETE ON Flights
FOR EACH ROW
EXECUTE FUNCTION delete_tickets_by_flight();