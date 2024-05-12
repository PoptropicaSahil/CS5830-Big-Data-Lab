## Repo structure

```bash
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── models.py
├── config/
│   ├── prometheus.yml
│   └── grafana/
│       ├── provisioning/
│       │   ├── dashboards/
│       │   │   └── dashboard.yml
│       │   └── datasources/
│       │       └── datasource.yml
│       └── grafana.ini
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── requirements.txt
└── README.md
```


Using venv of a05 only
### STEPS
docker run -d -p 9090:9090 --name prometheus prom/prometheus
docker run -d -p 3000:3000 --name grafana -v /path/to/config/grafana:/etc/grafana/provisioning grafana/grafana