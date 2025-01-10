from objects.van import Van

def create_vans() -> list:
    """Skapar tio bilar"""
    vans = []
    for i in range(10):
        vans.append(Van(f"bil_{i+1}"))
    return vans