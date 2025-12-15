from collector import collect_all_info, collect_info_continuous

def bytes_to_gigabytes(octets):
    return f"{octets / (1024 ** 3):.2f} GB"

def show_system_info(data_sys):
    print("\n=== Système ===")
    print("OS:", data_sys["OS"])
    print("Version:", data_sys["Version"])
    print("Architecture:", data_sys["Architecture"])
    print("Hostname:", data_sys["Hostname"])
    print("Python:", data_sys["Python"])

def show_cpu(data_cpu):
    print("\n=== CPU ===")
    print("Coeurs physiques:", data_cpu["Coeurs physiques"])
    print("Coeurs logiques:", data_cpu["Coeurs logiques"])
    print("Utilisation:", data_cpu["Pourcentage d'utilisation"], "%")
    
def show_memory(data_mem):
    total = data_mem["Total"]
    available = data_mem["Disponible"]
    percent = data_mem["Pourcentage d'utilisation"]
    print("\n=== Mémoire ===")
    print("Total:", bytes_to_gigabytes(total))
    print("Disponible:", bytes_to_gigabytes(available))
    print("Utilisation:", percent, "%")
    
def show_disk(data_disk):
    print("\n=== Disques ===")
    for mountpoint, usage in data_disk.items():
        print(f"{mountpoint} : {usage}%")
        
def main():
    print("=== SysWatch v2.0 ===")
    data = collect_all_info()
    show_system_info(data["system"])
    show_cpu(data["cpu"])
    show_memory(data["memory"])
    show_disk(data["disk"])
    print("\nTimestamp:", data["timestamp"])