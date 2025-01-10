import os
from scripts.get_optimal_convoy import get_optimal_convoy
from scripts.get_packages import get_packages
from scripts.read_csv import read_csv


# Rekomenderade värden på r_level: (0-1)
# Rekommenderade värden på break_point: (10-99)

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    get_optimal_convoy(get_packages(read_csv("lagerstatus.csv")), r_level=1, break_point=10)
    # get_optimal_convoy(get_packages(read_csv("lagerstatus2.csv")), r_level=1, break_point=10)
    # get_optimal_convoy(get_packages(read_csv("lagerstatus3.csv")), r_level=1, break_point=10)
    # get_optimal_convoy(get_packages(read_csv("lagerstatus4.csv")), r_level=1, break_point=10)
    # get_optimal_convoy(get_packages(read_csv("lagerstatusX.csv")), r_level=1, break_point=10)
