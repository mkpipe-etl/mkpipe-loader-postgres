# mkpipe-loader-postgres

PostgreSQL loader plugin for [MkPipe](https://github.com/mkpipe-etl/mkpipe). Writes Spark DataFrames into PostgreSQL tables via JDBC.

## Documentation

For more detailed documentation, please visit the [GitHub repository](https://github.com/mkpipe-etl/mkpipe).

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

## Connection Configuration

```yaml
connections:
  pg_target:
    variant: postgresql
    host: localhost
    port: 5432
    database: mydb
    schema: public
    user: myuser
    password: mypassword
```

---

## Table Configuration

```yaml
pipelines:
  - name: source_to_pg
    source: my_source
    destination: pg_target
    tables:
      - name: source_table
        target_name: public.stg_table
        replication_method: full
        batchsize: 10000
```

---

## Write Parallelism & Throughput

Two parameters control write performance:

```yaml
      - name: source_table
        target_name: public.stg_table
        replication_method: full
        batchsize: 10000        # rows per JDBC batch insert (default: 10000)
        write_partitions: 4     # coalesce DataFrame to N partitions before writing
```

### How they work

- **`batchsize`**: rows buffered before sending one `INSERT` statement. PostgreSQL handles 5,000–10,000 well; very large batches (>100K) can increase memory pressure.
- **`write_partitions`**: calls `coalesce(N)` on the DataFrame, reducing concurrent JDBC connections to PostgreSQL.

### Performance Notes

- PostgreSQL's `COPY` protocol is faster than JDBC for bulk loads, but mkpipe uses JDBC for portability.
- For large loads, `write_partitions: 4–8` with `batchsize: 10000` is a reliable baseline.
- If the target table has many indexes or constraints, writes will be slower — consider disabling indexes during bulk loads.

---

## All Table Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | string | required | Source table name |
| `target_name` | string | required | PostgreSQL destination table name |
| `replication_method` | `full` / `incremental` | `full` | Replication strategy |
| `batchsize` | int | `10000` | Rows per JDBC batch insert |
| `write_partitions` | int | — | Coalesce DataFrame to N partitions before writing |
| `dedup_columns` | list | — | Columns used for `mkpipe_id` hash deduplication |
| `tags` | list | `[]` | Tags for selective pipeline execution |
| `pass_on_error` | bool | `false` | Skip table on error instead of failing |