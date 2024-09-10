from prometheus_client import Counter, Gauge

resource_charge_metric = Gauge('battery_charge', 'Carga disponivel no sensor', ['sensor'])
resource_unavailable_metric = Counter('unavailable', 'Escassez energética do sensor', ['sensor'])
resource_harvest_metric = Gauge('harvest_system', 'Recurso coletado', ['sensor'])

