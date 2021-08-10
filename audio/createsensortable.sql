DROP TABLE IF EXISTS public."raw_sensordata";

CREATE TABLE public."raw_sensordata"
(
    index bigint,
    millitime bigint,
    band bigint,
    value bigint
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."raw_sensordata"
    OWNER to pythonuser;
