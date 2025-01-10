from objects.package import Package


def get_packages(data: dict) -> list:
    """Hämtar paket från en CSV-fil"""
    items = []
    value_counts = sorted(
        [
            len(data["Paket_id"]),
            len(data["Vikt"]),
            len(data["Förtjänst"]),
            len(data["Deadline"]),
        ],
        key=None,
    )
    for i in range(value_counts[0]):
        try:
            temp_id = data["Paket_id"][str(i)]
        except KeyError:
            temp_id = None
        try:
            temp_weight = data["Vikt"][str(i)]
        except KeyError:
            temp_id = None
        try:
            temp_gain = data["Förtjänst"][str(i)]
        except KeyError:
            temp_gain = None
        try:
            temp_deadline = data["Deadline"][str(i)]
        except KeyError:
            temp_deadline = None
        items.append(
            Package(int(temp_id), temp_weight * 10, int(temp_gain), int(temp_deadline))
        )
    items = tuple(items)
    return items
