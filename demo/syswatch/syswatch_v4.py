import argparse
from collector import collect_all_info, collect_info_continuous
from traitement import export_csv
from stats import calculer_moyennes
from syswatch_v2 import show_system_info, show_cpu, show_memory, show_disk
from database import MetricsDatabase
from models import SystemCollector

parser = argparse.ArgumentParser(description="Gestionnaire des tâches système")
parser.add_argument('--continu', action='store_true', help="Exécuter en mode continu")
parser.add_argument('--intervalle', type=int, default=5, help="Intervalle de temps entre les relevés (en secondes)")
parser.add_argument('--nombre', type=int, default=12, help="Nombre de relevés à effectuer")
parser.add_argument('--stats', action='store_true', help="Calculer les statistiques à partir d'un fichier CSV")
args = parser.parse_args()



if args.stats:
    stats = calculer_moyennes('syswatch_data.csv')
    print(stats)
elif args.continu:
    try:
        print("=== SysWatch v3.0 ===")
        for data in collect_info_continuous(args.intervalle, args.nombre):
            show_system_info(data["system"])
            show_cpu(data["cpu"])
            show_memory(data["memory"])
            show_disk(data["disk"])
            print("\nTimestamp:", data["timestamp"])
            export_csv([data], 'syswatch_data.csv')
    except KeyboardInterrupt:
        print("Collecte interrompue.")
else:
    data = collect_all_info()
    print("=== SysWatch v3.0 ===")
    show_system_info(data["system"])
    show_cpu(data["cpu"])
    show_memory(data["memory"])
    show_disk(data["disk"])
    print("\nTimestamp:", data["timestamp"])
    export_csv([data], 'syswatch_data.csv')