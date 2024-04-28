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