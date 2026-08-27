def exact_match(a, b):
    return float(str(a).strip().casefold() == str(b).strip().casefold())
