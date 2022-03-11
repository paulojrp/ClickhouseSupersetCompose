# Tutorial for set up Clickhouse with Superset


## Start Docker environment

```
docker-compose up
```


##  Add new datasource to Superset

- Login in Superset

Access `localhost:8088` and log in using the following credetials `admin` / `admin`.

- Create new datasource

On the top menu go to Data > Database, and create a new database using Clickhouse.

```
clickhouse+native://clickhouse-server:9000/default
```


## (Optionally ) Start Clickhouse client

You can manipulate the database by starting a new Docker container with Clickhouse client.

```
docker run -it --rm --network="clickhouse-superset" --link clickhouse_server:clickhouse-server yandex/clickhouse-client --host clickhouse-server
```
