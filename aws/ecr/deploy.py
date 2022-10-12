import avionix
from kubernetes import client
from kubernetes import config

resource_class = {
    "liveoak-sandbox": "liveoaktechnologies/test",
    "liveoak-prod": "liveoaktechnologies/prod-us",
    "liveoak-prod-eu": "liveoaktechnologies/prod-eu",
    "statefarm": "liveoaktechnologies/statefarm",
}

config.load_kube_config()
v1 = client.CoreV1Api()

all_context, current_context = config.list_kube_config_contexts()

print(current_context)
