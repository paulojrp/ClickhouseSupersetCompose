-- Creation auxiliar table to generate random values
CREATE TABLE monitoring_rnd
(
    ts_bucket DateTime,
    label_key String,
    label_value String,
    rules Nested
    (
        id String,
        confusion_matrix Tuple(UInt16, UInt16, UInt16, UInt16),
        triggered Array(String)
    ),
    models Nested
    (
        id String,
        scores Array(UInt16)
    )
)
ENGINE = GenerateRandom(1, 5, 3);

-- Insert random values
set max_partitions_per_insert_block=10000

INSERT INTO monitoring
    SELECT * FROM monitoring_rnd
    LIMIT 10000;

-- Drop auxiliary table
DROP TABLE monitoring_rnd;
