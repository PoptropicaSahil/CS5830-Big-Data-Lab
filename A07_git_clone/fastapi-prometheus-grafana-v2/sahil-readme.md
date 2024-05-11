https://github.com/docker/compose/issues/11168#issuecomment-1800362132

install pyyml first then docker-compose
# Assignment on Docker, Prometheus and Grafana

## Easy Direct Usage

Simply run the following command

``` bash
docker-compose up
```

The three containers and their respective ports are given at:
* FastAPI: http://localhost:8000/
* Prometheus: http://localhost:9090/
* Grafana: http://localhost:3000/

> The main code is the `main.py` file
> Since the keras model is kept in the `./app` directory, the path to the keras model in the Swagger UI should be written as: `./mnist-model.keras`


# Task-wise pointers:

## TASK 1

Repo Structure
```bash
project/
├── app/
│   └── main.py
├── config/
│   ├── prometheus.yml
│   └── grafana/
│       ├── provisioning/
│       │   ├── dashboards/
│       │   │   └── dashboard.yml
│       │   └── datasources/
│       │       └── datasource.yml
│       └── grafana.ini
└── requirements.txt
```
### Setting up Prometheus and Grafana
- I downlaoded the offical Prometheus and Grafana softwares from their respective websites and placed them in the root project directory (haven't included it in GitHub )
- Ran the main field simply by `python -m app.main`

- Starting Prometheus:
> - Download Prometheus from `https://prometheus.io/download/`, extract it 
> - Copy the `config/prometheus.yml` file from my project to the Prometheus directory
> - Run the following command : `./prometheus --config.file=prometheus.yml`

- Starting Grafana :
> - Download Prometheus from `https://grafana.com/grafana/download`, extract it 
> - Copy the `config/grafana` directory from my project to the Prometheus directory
> - Run the following command : `./bin/grafana-server --homepath=./config/grafana`


### Adding Gauges
- All the required gauges and counters are added to the `main.py` file with corresponding logic

### Testing via other devices
- Opened the command prompt from Windows and ran `ipconfig`. Under the Wireless LAN adapter Wi-Fi, I got my IPv4 Address as `192.168.10.105`
- From another device connected to the same network, I typed the url : `http://192.168.10.105:8000.`
- Could acccess and test my API with this endpoint
<img src="readme_images/from-phone.jpg" width="500"/>




<!-- when only the app without docker -->
./mnist-model.keras

<!-- 1 CPUs -->
![alt text](readme_images/one-cpu.png)

![alt text](readme_images/one-cpu-better.png)


<!-- try on other device -->
![alt text](readme_images/from-phone.jpg)