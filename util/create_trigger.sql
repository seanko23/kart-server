CREATE TRIGGER log_map_records_update
    AFTER UPDATE
    ON map_records
    FOR EACH ROW
    EXECUTE PROCEDURE log_map_records_fn();

CREATE TRIGGER log_map_records_insert
    AFTER INSERT
    ON map_records
    FOR EACH ROW
    EXECUTE PROCEDURE log_map_records_fn();
