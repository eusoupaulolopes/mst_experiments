from prometheus_client import Gauge

battery_charge_metric = Gauge('battery_charge', 'Carga disponivel no sensor', ['sensor'])

