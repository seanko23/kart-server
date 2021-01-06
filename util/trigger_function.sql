CREATE OR REPLACE FUNCTION log_map_records_fn()
RETURNS trigger AS
$$
DECLARE
    _db_key text;
    _old_val numeric;
    _new_val numeric;
BEGIN
    FOR _db_key IN 
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'map_records' AND column_name LIKE 'map%'
    LOOP
        EXECUTE format('SELECT (($1).%I)::text, (($2).%I)::text', _db_key, _db_key)
            USING OLD, NEW
            INTO _old_val, _new_val;

            IF _new_val <> _old_val OR (_old_val IS NULL AND _new_val IS NOT NULL) THEN
                INSERT INTO map_record_logs (users_id, map_records_id, record_key, record_old, record_new, date_posted)
                    VALUES(NEW.users_id, NEW.id, _db_key, _old_val, _new_val, current_timestamp);
            END IF;

    END LOOP;
    RETURN NEW;
END;

$$
LANGUAGE 'plpgsql';
