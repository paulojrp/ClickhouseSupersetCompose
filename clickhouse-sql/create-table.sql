-- Creation of table
CREATE TABLE monitoring
(
    ts_bucket DateTime,
    label_key String,
    label_value String,
    rules Nested
    (
        id String,
        confusion_matrix Tuple(UInt64, UInt64, UInt64, UInt64),
        triggered Array(String)
    ),
    models Nested
    (
        id String,
        scores Array(UInt64)
    )
)
ENGINE = MergeTree
PARTITION BY toYYYYMMDD(ts_bucket)
PRIMARY KEY (ts_bucket, label_key, label_value)
ORDER BY (ts_bucket, label_key, label_value);
