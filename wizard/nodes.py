nodes = {
    "dht22": {
        "pin": {"type": "int", "default": 4, "list": "radio"},
        "interval": {"type": "int", "default": 60},
    },
    "http": {
        "url": {"type": "str", "default": "", "list": "radio"},
        "interval": {"type": "int", "default": 60},
    },
    "relais": {
        "pin": {"type": "int", "default": [4], "list": "checkbox"},
        "interval": {"type": "int", "default": 60},
    },
    "pir": {
        "pin": {"type": "int", "default": 4, "list": "radio"},
        "interval": {"type": "int", "default": 60},
    },
    "switch": {
        "pin": {"type": "int", "default": 4, "list": "radio"},
        "interval": {"type": "int", "default": 60},
    },
    "led": {
        "pin": {"type": "int", "default": 2, "list": "radio"},
        "interval": {"type": "int", "default": 60},
    },
}
