import random
from objects.van import Van
from objects.convoy import Convoy
from objects.package import Package
from .create_vans import create_vans
from display_result.plot_results import plot_results


def create_full_convoy(
    packages: list, vans: list[Van], priority_packages: list, name: str
) -> Convoy:
    """Skapar en ny convoy där försenade paket och paket från
    eventuella föräldrar prioriteras"""
    delta_packages = []
    delta_packages_ids = []
    added_package_ids = []
    added_priority_packages = []
    for package in packages:
        if package.id not in added_package_ids:
            delta_packages.append(package)
            delta_packages_ids.append(package.id)
    for package in packages:
        if package.deadline < 0:
            priority_packages.append(package)
    for package in priority_packages:
        if package.id in delta_packages_ids:
            for delta_package in delta_packages:
                if delta_package.id == package.id:
                    delta_packages.remove(delta_package)
                    break
    for package in priority_packages:
        for van in vans:
            if (
                van.service_weight + package.weight
                <= van.max_weight
                and package not in added_priority_packages
            ):
                van.packages.append(package)
                van.update_service_weight()
                added_priority_packages.append(package)
                break
    for van in vans:
        while_counter = 0
        while True:
            if len(delta_packages):
                rand_index = random.randint(0, len(delta_packages) - 1)
            else:
                break
            if van.service_weight + delta_packages[rand_index].weight <= van.max_weight:
                van.packages.append(delta_packages[rand_index])
                van.update_service_weight()
                van.update_gains()
                delta_packages.remove(delta_packages[rand_index])
                while_counter += 1
            elif van.service_weight > get_average_package_weight(delta_packages):
                lightest_package = get_lightest_package(delta_packages)
                if van.max_weight - van.service_weight < lightest_package.weight:
                    break
                else:
                    van.packages.append(lightest_package)
                    van.update_service_weight()
                    van.update_gains()
                    delta_packages.remove(lightest_package)
            else:
                while_counter += 1
    return Convoy(vans, name)


def get_lightest_package(packages: list[Package]) -> Package:
    """Retunerar paketet med lägst vikt som fortfarende inte är tilldelad till någon bil"""
    lightest_package = Package(9999, 9999, 9999, -9999)
    for package in packages:
        if package.weight < lightest_package.weight:
            lightest_package = package
    return lightest_package


def get_average_package_score(packages: list[Package]):
    """Retunerar snitt-värderingen av alla
    paketen i en en lista med paket"""
    if len(packages):
        total_scores = []
        for package in packages:
            total_scores.append(package.score)
        return sum(total_scores) / len(total_scores)
    else:
        return 9999


def get_average_package_weight(packages: list[Package]):
    """Retunerar snitt-vikten av alla
    paketen i en lista med paket"""
    total_weights = []
    for package in packages:
        total_weights.append(package.weight)
    return sum(total_weights) / len(total_weights)


def get_subset(parent_1: Convoy, parent_2: Convoy) -> list:
    """Skapar en lista av paket från två föräldrar"""
    duplicates = []
    packages_total = []
    for van in parent_1.vans:
        for package in van.packages[: round(len(van.packages) / 2)]:
            packages_total.append(package)
    for van in parent_2.vans:
        for package in van.packages[round(len(van.packages) / 2) : -1]:
            packages_total.append(package)
    for package in packages_total:
        if packages_total.count(package) != 1:
            duplicates.append(package)
    for duplicate in duplicates:
        packages_total.remove(duplicate)
    for i in range(random.randint(1, len(packages_total))):
        j = random.randint(0, round(len(packages_total) / 2))
        if package.score >= get_average_package_score(packages_total):
            packages_total.remove(packages_total[j])
    return packages_total


def get_optimal_convoy(
    packages: list, r_level: int, break_point: int
) -> Convoy | None:
    """Försöker skapa den bästa möjliga convoyen"""
    convoy_list_first = []
    convoy_list_second = []
    unchanged = 0
    leaders_total = []
    if r_level < 0:
        print("Invalid r_level")
        return
    elif not len(packages):
        print("Invalid ammount of packages, (0)")
        return
    while True:
        if not len(convoy_list_first) or not len(convoy_list_second):
            if r_level == 0:
                convoy_list_first = [
                    create_full_convoy(packages, create_vans(), [], "Pilot1_set1"),
                    create_full_convoy(packages, create_vans(), [], "Pilot2_set1"),
                    create_full_convoy(packages, create_vans(), [], "Pilot3_set1"),
                    create_full_convoy(packages, create_vans(), [], "pilot4_set1"),
                ]
                convoy_list_second = [
                    create_full_convoy(packages, create_vans(), [], "Pilot1_set2"),
                    create_full_convoy(packages, create_vans(), [], "Pilot2_set2"),
                    create_full_convoy(packages, create_vans(), [], "Pilot3_set2"),
                    create_full_convoy(packages, create_vans(), [], "Pilot4_set2"),
                ]
            else:
                convoy_list_first = [
                    get_optimal_convoy(packages, r_level - 1, break_point),
                    get_optimal_convoy(packages, r_level - 1, break_point),
                    get_optimal_convoy(packages, r_level - 1, break_point),
                    get_optimal_convoy(packages, r_level - 1, break_point),
                ]
                convoy_list_second = [
                    get_optimal_convoy(packages, r_level - 1, break_point),
                    get_optimal_convoy(packages, r_level - 1, break_point),
                    get_optimal_convoy(packages, r_level - 1, break_point),
                    get_optimal_convoy(packages, r_level - 1, break_point),
                ]
            best_convoy_first = Convoy(create_vans())
            best_convoy_second = Convoy(create_vans())
            for convoy in convoy_list_second:
                convoy.score = convoy.set_score()
                if convoy.score < best_convoy_second.score:
                    best_convoy_second = convoy
            for convoy in convoy_list_first:
                convoy.score = convoy.set_score()
                if convoy.score < best_convoy_first.score:
                    best_convoy_first = convoy
            convoy_list_first.remove(best_convoy_first)
            convoy_list_second.remove(best_convoy_second)
            if best_convoy_first.score <= best_convoy_second.score:
                leader = Convoy(
                    create_vans(),
                    "Leader",
                )
                for i in range(len(leader.vans)):
                    for package in best_convoy_first.vans[i].packages:
                        leader.vans[i].packages.append(package)
                for van in leader.vans:
                    van.update_gains()
                    van.update_service_weight()
                leader.score = leader.set_score()
                print(f"Bästa score: {leader.score}")
                print(f"Nivå: {r_level}")
                print(f"Oförändrad: {unchanged}/{break_point}")
                print("<------------------------------------>")
                leaders_total.append(leader)
            else:
                leader = Convoy(
                    create_vans(),
                    "Leader",
                )
                for i in range(len(leader.vans)):
                    for package in best_convoy_second.vans[i].packages:
                        leader.vans[i].packages.append(package)
                for van in leader.vans:
                    van.update_gains()
                    van.update_service_weight()
                leader.score = leader.set_score()
                print(f"Bästa score: {leader.score}")
                print(f"Nivå: {r_level}")
                print(f"Oförändrad: {unchanged}/{break_point}")
                print("<------------------------------------>")
                leaders_total.append(leader)
        
        else:
            if unchanged == break_point:
                plot_results(leaders_total, packages, r_level)
                return leader             
            rand_index = random.randint(1, 3)
            parent_1_set_1 = Convoy(
                create_vans(),
                "Parent_1_set_1",
            )
            parent_2_set_1 = Convoy(
                create_vans(),
                "Parent_2_set_1",
            )
            parent_1_set_2 = Convoy(
                create_vans(),
                "Parent_1_set_2",
            )
            parent_2_set_2 = Convoy(
                create_vans(),
                "Parent_2_set_2",
            )
            rand_index = random.randint(1, len(convoy_list_first) - 1)
            for i in range(len(best_convoy_first.vans)):
                for package in best_convoy_first.vans[i].packages:
                    parent_1_set_1.vans[i].packages.append(package)
            for i in range(len(convoy_list_first[rand_index].vans)):
                for package in convoy_list_first[0].vans[i].packages:
                    parent_2_set_1.vans[i].packages.append(package)
            rand_index = random.randint(1, len(convoy_list_second) - 1)
            for i in range(len(best_convoy_second.vans)):
                for package in best_convoy_second.vans[i].packages:
                    parent_1_set_2.vans[i].packages.append(package)
            for i in range(len(convoy_list_second[rand_index].vans)):
                for package in convoy_list_first[0].vans[i].packages:
                    parent_2_set_2.vans[i].packages.append(package)
            child_1_subset = get_subset(parent_1_set_1, parent_2_set_2)
            child_2_subset = get_subset(parent_2_set_2, parent_1_set_1)
            child_3_subset = get_subset(parent_1_set_2, parent_2_set_1)
            child_4_subset = get_subset(parent_2_set_1, parent_1_set_2)
            convoy_list_first = [
                parent_1_set_1,
                parent_1_set_2,
                create_full_convoy(packages, create_vans(), child_1_subset, "Child_1"),
                create_full_convoy(packages, create_vans(), child_2_subset, "Child_2"),
            ]
            convoy_list_second = [
                parent_2_set_1,
                parent_2_set_2,
                create_full_convoy(packages, create_vans(), child_3_subset, "Child_3"),
                create_full_convoy(packages, create_vans(), child_4_subset, "Child_4"),
            ]
            best_convoy_first = Convoy(create_vans())
            best_convoy_second = Convoy(create_vans())
            for convoy in convoy_list_second:
                convoy.score = convoy.set_score()
                if convoy.score < best_convoy_second.score:
                    best_convoy_second = convoy
            for convoy in convoy_list_first:
                convoy.score = convoy.set_score()
                if convoy.score < best_convoy_first.score:
                    best_convoy_first = convoy
            if best_convoy_first.score < best_convoy_second.score:
                if best_convoy_first.score < leader.score:
                    leader = Convoy(
                        create_vans(),
                        "Leader",
                    )
                    for i in range(len(leader.vans)):
                        for package in best_convoy_first.vans[i].packages:
                            leader.vans[i].packages.append(package)
                    for van in leader.vans:
                        van.update_gains()
                        van.update_service_weight()
                    leader.score = leader.set_score()
                    print(f"Bästa score: {leader.score}")
                    leaders_total.append(leader)
                    unchanged = 0
                else:
                    print(f"Bästa score: {leader.score}")
                    unchanged += 1
                print(f"Nivå: {r_level}")
                print(f"Oförändrad: {unchanged}/{break_point}")
                print("<------------------------------------>")
            else:
                if best_convoy_second.score < leader.score:
                    leader = Convoy(
                        create_vans(),
                        "Leader",
                    )
                    for i in range(len(leader.vans)):
                        for package in best_convoy_second.vans[i].packages:
                            leader.vans[i].packages.append(package)
                    for van in leader.vans:
                        van.update_gains()
                        van.update_service_weight()
                    leader.score = leader.set_score()
                    print(f"Bästa score: {leader.score}")
                    leaders_total.append(leader)
                    unchanged = 0
                else:
                    print(f"Bästa score: {leader.score}")
                    unchanged += 1
                print(f"Nivå: {r_level}")
                print(f"Oförändrad: {unchanged}/{break_point}")
                print("<------------------------------------>")

