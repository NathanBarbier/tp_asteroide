# tp_asteroide

### Lancer les containers

`docker compose up`

### Ouvrir un bash du container spark-master

`docker exec -it spark-master /bin/bash`

### Lancer les consumers

À executer dans un bash spark chacun

`/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 /app/consumer.py`\
`/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 /app/consumer_app.py`

### Lancer le front

`cd my-app`\
`npm run dev`
