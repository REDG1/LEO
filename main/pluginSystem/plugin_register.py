from main.pluginSystem.dataProviderCore import dataProviderCore


#from typing import Any, Callable

dataProv_creation_func = {}


def register(dataProv_name, creation_func ):
    dataProv_creation_func[dataProv_name] = creation_func


def unregister(dataProv_name) -> None:
    dataProv_creation_func.pop(dataProv_name, None)


def create(dataProv_name,host_p):
    try:
        creator_func = dataProv_creation_func[dataProv_name]
    except KeyError:
        raise ValueError(f"unknown algorithm name {dataProv_name!r}") from None
    return creator_func(host_p)

def getDPNames():
    return dataProv_creation_func.keys()
