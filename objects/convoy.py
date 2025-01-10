from .van import Van
from .package import Package

class Convoy:
    def __init__(self, vans: list[Van], name="no_name") -> None:
        self.name = name
        self.vans = vans
        self.score = self.set_score()

    def set_score(self) -> float:
        """Tilldelar ett värde till en convoy"""
        package_counter = 0
        dl_total = []
        gain_total = []
        weight_total = []
        for van in self.vans:
            for package in van.packages:
                dl_total.append(package.deadline)
                gain_total.append(package.gain)
                weight_total.append(package.weight)
                package_counter += 1
        if package_counter == 0:
            return 9999
        dl_average = sum(dl_total) / len(dl_total)
        gain_average = sum(gain_total) / len(dl_total)
        weight_average = sum(weight_total) / len(weight_total)
        dl_score = -(15 ** (-1 * dl_average))
        score = dl_score - gain_average * 20 + weight_average*4
        return score

    def get_gain_sum(self) -> int:
        """Räknar ut den totala förtjänsten för en convoy"""
        gain_sum = 0
        for van in self.vans:
            for package in van.packages:
                gain_sum = gain_sum + package.gain
        return gain_sum
    
    def get_penalty_fee(self, packages:list[Package]) -> int:
        """Räknar ut den totala straff-avgiften för en convoy"""
        penalty_fee = 0
        delta_packages = []
        packages_ids = []
        for van in self.vans:
            for package in van.packages:
                packages_ids.append(package.id)
        for package in packages:
            if package.id not in packages_ids:
                delta_packages.append(package)
        for package in delta_packages:
            if package.deadline < 0:
                penalty_fee = penalty_fee + package.deadline**2
        return penalty_fee
    
    def get_remaining_packages(self, packages:list[Package]) -> list[Package]:
        """Retunerar alla paket som är kvar i lagret"""
        added_ids = []
        delta_packages = []
        for van in self.vans:
            for package in van.packages:
                added_ids.append(package.id)
        for package in packages:
            if package.id not in added_ids:
                delta_packages.append(package)
        return delta_packages

    def get_total_packages(self) -> int:
        """Retunerar det totala antalet paket i en convoy"""
        packages = []
        for van in self.vans:
            for package in van.packages:
                packages.append(package)
        return len(packages)
