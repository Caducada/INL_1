from objects.package import Package
from objects.convoy import Convoy
import matplotlib.pyplot as plt
import numpy as np

def plot_results(convoys: list[Convoy], packages: list[Package], r_level: int):
    if len(convoys) > 1:
        average_package_weights = []
        average_deadlines = []
        penalty_charges = []
        average_package_gains = []
        ratios = []
        starting_ratios = []
        final_ratios = []
        final_packages_list = []
        starting_packages_list = []
        starting_gains_left = []
        final_gains_left = []
        remaining_first = convoys[0].get_remaining_packages(packages)
        remaining_final = convoys[-1].get_remaining_packages(packages)
        
        for van in convoys[-1].vans:
            for package in van.packages:
                final_ratios.append(package.gain/(package.weight)/10)
                final_packages_list.append(package)
                
        for van in convoys[0].vans:
            for package in van.packages:
                starting_ratios.append(package.gain/(package.weight)/10)
                starting_packages_list.append(package)
        
        for package in packages:
            ratios.append(package.gain/(package.weight)/10)
        
        for convoy in convoys:
            package_weights = []
            package_gains = []
            deadlines = []
            delayed_packages = []

            for van in convoy.vans:
                for package in van.packages:
                    package_gains.append(package.gain)
                    package_weights.append(package.weight)
                    deadlines.append(package.deadline)
                    if package.deadline < 0:
                        delayed_packages.append(package)

            penalty_charge = sum(-package.deadline**2 for package in delayed_packages)
            penalty_charges.append(penalty_charge)
            average_package_weights.append(
                sum(package_weights) / (len(package_weights) * 10)
            )
            average_deadlines.append(sum(deadlines) / (len(deadlines) / 10))
            average_package_gains.append(sum(package_gains) / len(package_gains))
            
        for package in packages:
            if package not in final_packages_list:
                final_gains_left.append(package.gain)
            if package not in starting_packages_list:
                starting_gains_left.append(package.gain)
                

        plt.figure(1)
        plt.plot(average_deadlines, label="genomsnittlig deadline", linewidth=3)
        plt.plot(average_package_weights, label="genomsnittlig vikt", linewidth=3)
        plt.plot(average_package_gains, label="genomsnittlig förtjänst", linewidth=3)
        plt.title(f"Förändring över tid, nivå {r_level}")
        plt.legend()

        values = []
        total_packages_last = [
            package for van in convoys[-1].vans for package in van.packages
        ]
        delayed_packages_last = [
            package for package in total_packages_last if package.deadline < 0
        ]
        values.extend(
            [
                convoys[-1].get_gain_sum(),
                sum(final_gains_left),
                len(packages)-len(total_packages_last),
                convoys[-1].get_penalty_fee(packages),
                len(delayed_packages_last),
            ]
        )

        plt.figure(2, figsize=(16, 10))
        plt.barh(
            [
                f"Total förtjänst\n({convoys[-1].get_gain_sum()})",
                f"Återstående förtjänst\n({sum(final_gains_left)})",
                f"Återstående paket\n({len(packages)-len(total_packages_last)})",
                f"Återstående straff-avgift\n({convoys[-1].get_penalty_fee(packages)})",
                f"Antal försenade Paket\n({len(delayed_packages_last)})",
            ],
            values,
            color="blue",
        )
        plt.title(f"Slutgiltiga konvojen, nivå {r_level}")
        
        values = []
        total_packages_first = [
            package for van in convoys[0].vans for package in van.packages
        ]
        delayed_packages_first = [
            package for package in total_packages_first if package.deadline < 0
        ]

        values.extend(
            [
                convoys[0].get_gain_sum(),
                sum(starting_gains_left),
                len(packages) - len(total_packages_first),
                convoys[0].get_penalty_fee(packages),
                len(delayed_packages_first),
            ]
        )

        plt.figure(3, figsize=(16, 10))
        plt.barh(
            [
                f"Total förtjänst\n({convoys[0].get_gain_sum()})",
                f"Återstående förtjänst\n({sum(starting_gains_left)})",
                f"Återstående paket\n({len(packages)-len(total_packages_first)})",
                f"Återstående straff-avgift\n({convoys[0].get_penalty_fee(packages)})",
                f"Antal försenade Paket\n({len(delayed_packages_first)})",
            ],
            values,
            color="red",
        )
        plt.title(f"Ursprungliga konvojen, nivå {r_level}")
        
        plt.figure(4, figsize=(12, 8))
        values = []
        delayed_packages = []
        for package in packages:
            if package.deadline < 0:
                delayed_packages.append(package)
        values.extend(
            [   
                len(packages),
                len(starting_packages_list),
                len(final_packages_list),
            ]
        )
        
        plt.bar(
            [
                f"Antal paket — totalt\n({len(packages)})",
                f"Antal paket — ursprungliga konvojen\n({len(starting_packages_list)})",
                f"Antal paket — slutgiltiga konvojen\n({len(final_packages_list)})",
            ],
            values,
            color="green",
        )
        plt.title(f"Paket-fördelning, nivå {r_level}")

        plt.figure(5, figsize=(12, 8))
        values = []
        delayed_packages = []
        for package in packages:
            if package.deadline < 0:
                delayed_packages.append(package)
        values.extend(
            [   
                len(delayed_packages),
                len(delayed_packages_first),
                len(delayed_packages_last),
            ]
        )
        
        plt.bar(
            [
                f"Försenade paket — totalt\n({len(delayed_packages)})",
                f"Försenade paket — ursprungliga konvojen\n({len(delayed_packages_first)})",
                f"Försenade paket — slutgiltiga konvojen\n({len(delayed_packages_last)})",
            ],
            values,
            color="purple",
        )
        plt.title(f"Försenade paket, nivå {r_level}")
    
        plt.figure(6, figsize=(10, 6))
        mean = np.mean(final_ratios)
        std_dev = np.std(final_ratios)
        plt.hist(final_ratios, bins=30, alpha=0.6, color='g', edgecolor='black')
        plt.axvline(mean, color='r', linestyle='dashed', linewidth=2, label=f'Snitt fördelning: {mean:.2f}')
        plt.axvline(mean + std_dev, color='b', linestyle='dashed', linewidth=2, label=f'+1 Standardavvikelse: {mean + std_dev:.2f}')
        plt.axvline(mean - std_dev, color='b', linestyle='dashed', linewidth=2, label=f'-1 Standardavvikelse: {mean - std_dev:.2f}')
        plt.title(f'Medelvärde och standardavvikelse av den slutgiltiga konvojen, nivå {r_level}')
        plt.xlabel('Förtjänst/Vikt')
        plt.ylabel('Antal Paket')
        plt.legend()
        
        plt.figure(7, figsize=(10, 6))
        mean = np.mean(starting_ratios)
        std_dev = np.std(starting_ratios)
        plt.hist(starting_ratios, bins=30, alpha=0.6, color='g', edgecolor='black')
        plt.axvline(mean, color='r', linestyle='dashed', linewidth=2, label=f'Snitt fördelning: {mean:.2f}')
        plt.axvline(mean + std_dev, color='b', linestyle='dashed', linewidth=2, label=f'+1 Standardavvikelse: {mean + std_dev:.2f}')
        plt.axvline(mean - std_dev, color='b', linestyle='dashed', linewidth=2, label=f'-1 Standardavvikelse: {mean - std_dev:.2f}')
        plt.title(f'Medelvärde och standardavvikelse av den ursprungliga konvojen, nivå {r_level}')
        plt.xlabel('Förtjänst/Vikt')
        plt.ylabel('Antal Paket')
        plt.legend()
        
        remaining_first_ratios = []
        for package in remaining_first:
            remaining_first_ratios.append(package.gain/package.weight/10)
        
        plt.figure(8, figsize=(10, 6))
        mean = np.mean(remaining_first_ratios)
        std_dev = np.std(remaining_first_ratios)
        plt.hist(remaining_first_ratios, bins=30, alpha=0.6, color='g', edgecolor='black')
        plt.axvline(mean, color='r', linestyle='dashed', linewidth=2, label=f'Snitt fördelning: {mean:.2f}')
        plt.axvline(mean + std_dev, color='b', linestyle='dashed', linewidth=2, label=f'+1 Standardavvikelse: {mean + std_dev:.2f}')
        plt.axvline(mean - std_dev, color='b', linestyle='dashed', linewidth=2, label=f'-1 Standardavvikelse: {mean - std_dev:.2f}')
        plt.title(f'Medelvärde och standardavvikelse av uteblivna paket för den slutgiltiga konvojen, nivå {r_level}')
        plt.xlabel('Förtjänst/Vikt')
        plt.ylabel('Antal Paket')
        plt.legend()
        
        remaining_final_ratios = []
        for package in remaining_final:
            remaining_final_ratios.append(package.gain/package.weight/10)
        
        plt.figure(9, figsize=(10, 6))
        mean = np.mean(remaining_first_ratios)
        std_dev = np.std(remaining_first_ratios)
        plt.hist(remaining_first_ratios, bins=30, alpha=0.6, color='g', edgecolor='black')
        plt.axvline(mean, color='r', linestyle='dashed', linewidth=2, label=f'Snitt fördelning: {mean:.2f}')
        plt.axvline(mean + std_dev, color='b', linestyle='dashed', linewidth=2, label=f'+1 Standardavvikelse: {mean + std_dev:.2f}')
        plt.axvline(mean - std_dev, color='b', linestyle='dashed', linewidth=2, label=f'-1 Standardavvikelse: {mean - std_dev:.2f}')
        plt.title(f'Medelvärde och standardavvikelse av uteblivna paket för den ursprungliga konvojen, nivå {r_level}')
        plt.xlabel('Förtjänst/Vikt')
        plt.ylabel('Antal Paket')
        plt.legend()
        
        plt.show()        
    elif len(convoys) == 1:
        values = []
        final_gains_left = []
        final_packages =[]
        final_ratios = []
        delta_deadlines_final = []
        delayed_packages_final = []
        remaining_first = convoys[0].get_remaining_packages(packages)
        
        for van in convoys[0].vans:
            for package in van.packages:
                final_packages.append(package)
                final_ratios.append(package.gain/(package.weight)/10)
        
        for package in packages:
            if package not in final_packages:
                final_gains_left.append(package.gain)
                delta_deadlines_final.append(package.deadline)
            
        for i in range(len(convoys[0].vans)):
            for j in range(len(convoys[0].vans[i].packages)):
                if convoys[0].vans[i].packages[j].deadline < 0:
                    delayed_packages_final.append(convoys[0].vans[i].packages[j])
            
        values.extend(
            [
                convoys[0].get_gain_sum(),
                sum(final_gains_left),
                len(packages) - len(final_packages),
                convoys[0].get_penalty_fee(packages),
                len(delayed_packages_final),
            ]
        )

        plt.figure(1, figsize=(16, 6))
        plt.barh(
            [
                f"Total förtjänst\n({convoys[0].get_gain_sum()})",
                f"Återstående förtjänst\n({sum(final_gains_left)})",
                f"Återstående paket\n({len(packages) - len(final_packages)})",
                f"Återstående straff-avgift\n({convoys[0].get_penalty_fee(packages)})",
                f"Antal försenade Paket\n({len(delayed_packages_final)})",
            ],
            values,
            color="red",
        )
        plt.title(f"Slutgiltiga konvojen, nivå {r_level}")
        values = []
        delayed_packages = []
        for package in packages:
            if package.deadline < 0:
                delayed_packages.append(package)
        delayed_packages_first = [
            package for package in final_packages if package.deadline < 0
        ]
        values.extend(
            [
                len(delayed_packages),
                len(delayed_packages_first),
            ]
        )
        
        plt.figure(2, figsize=(12, 8))
        values = []
        delayed_packages = []
        for package in packages:
            if package.deadline < 0:
                delayed_packages.append(package)
        values.extend(
            [   
                len(packages),
                len(final_packages),
            ]
        )
        
        plt.bar(
            [
                f"Antal paket — totalt\n({len(packages)})",
                f"Antal paket — slutgiltiga konvojen\n({len(final_packages)})",
            ],
            values,
            color="green",
        )
        plt.title(f"Paket-fördelning, nivå {r_level}")

        plt.figure(3, figsize=(12, 8))
        values = []
        delayed_packages = []
        for package in packages:
            if package.deadline < 0:
                delayed_packages.append(package)
        values.extend(
            [   
                len(delayed_packages),
                len(delayed_packages_final)
            ]
        )
        
        plt.bar(
            [
                f"Försenade paket — totalt\n({len(delayed_packages)})",
                f"Försenade paket — slutgiltiga konvojen\n({len(delayed_packages_final)})",
            ],
            values,
            color="purple",
        )
        plt.title(f"Försenade paket, nivå {r_level}")
        
        plt.figure(4, figsize=(10, 6))
        mean = np.mean(final_ratios)
        std_dev = np.std(final_ratios)
        plt.hist(final_ratios, bins=30, alpha=0.6, color='g', edgecolor='black')
        plt.axvline(mean, color='r', linestyle='dashed', linewidth=2, label=f'Snitt fördelning: {mean:.2f}')
        plt.axvline(mean + std_dev, color='b', linestyle='dashed', linewidth=2, label=f'+1 Standardavvikelse: {mean + std_dev:.2f}')
        plt.axvline(mean - std_dev, color='b', linestyle='dashed', linewidth=2, label=f'-1 Standardavvikelse: {mean - std_dev:.2f}')
        plt.title(f'Medelvärde och standardavvikelse för den slutgiltiga konvojen, nivå {r_level}')
        plt.xlabel('Förtjänst/Vikt')
        plt.ylabel('Antal Paket')
        plt.legend()
        
        remaining_first_ratios = []
        for package in remaining_first:
            remaining_first_ratios.append(package.gain/package.weight/10)
        
        plt.figure(5, figsize=(10, 6))
        mean = np.mean(remaining_first_ratios)
        std_dev = np.std(remaining_first_ratios)
        plt.hist(remaining_first_ratios, bins=30, alpha=0.6, color='g', edgecolor='black')
        plt.axvline(mean, color='r', linestyle='dashed', linewidth=2, label=f'Snitt fördelning: {mean:.2f}')
        plt.axvline(mean + std_dev, color='b', linestyle='dashed', linewidth=2, label=f'+1 Standardavvikelse: {mean + std_dev:.2f}')
        plt.axvline(mean - std_dev, color='b', linestyle='dashed', linewidth=2, label=f'-1 Standardavvikelse: {mean - std_dev:.2f}')
        plt.title(f'Medelvärde och standardavvikelse av uteblivna paket för den slutgiltiga konvojen, nivå {r_level}')
        plt.xlabel('Förtjänst/Vikt')
        plt.ylabel('Antal Paket')
        plt.legend()
        
        plt.show()
