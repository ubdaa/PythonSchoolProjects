commandes = [
    {"id": 1, "client": "Alice", "montant": 150.50, "date": "2025-01-15", "statut": "Livree"},
    {"id": 2, "client": "Bob", "montant": 89.99, "date": "2025-01-16", "statut": "en_cours"},
    {"id": 3, "client": "Alice", "montant": 200.00, "date": "2025-01-17", "statut": "livree"},
    {"id": 4, "client": "Charlie", "montant": 45.00, "date": "2025-01-17", "statut": "annulee"},
    {"id": 5, "client": "Bob", "montant": 320.00, "date": "2025-01-18", "statut": "livree"}
]

def analyser_commandes(commandes):
    nombre_commandes_livrees: int = 0
    
    for commande in commandes:
        if commande["statut"] == "livree":
            nombre_commandes_livrees += 1
    
    total_livrees = sum(commande["montant"] for commande in commandes if commande["statut"] == "livree")
    
    clients = {}
    for commande in commandes:
        if commande["statut"] == "livree":
            client = commande["client"]
            clients[client] = clients.get(client, 0) + commande["montant"]
    
    commandes_par_jour = {
        date: len([c for c in commandes if c["date"] == date])
        for date in dict.fromkeys(c["date"] for c in commandes)
    }
    
    moyenne_par_commande = total_livrees / nombre_commandes_livrees
    
    return {"total_livrees": total_livrees, "meilleur_client": max(clients, key=clients.get), "commandes_par_jour": commandes_par_jour, "moyenne_par_commande": moyenne_par_commande}

def trier_commandes_complexes(commandes):
    return {
        "livrees" : sorted(
            [c for c in commandes if c["statut"] == "livree"],
            key=lambda x: x["montant"],
            reverse=True
        ),
        "en_cours" : sorted(
            [c for c in commandes if c["statut"] == "en_cours"],
            key=lambda x: x["montant"],
            reverse=True
        ),
        "annulees" : sorted(
            [c for c in commandes if c["statut"] == "annulee"],
            key=lambda x: x["montant"],
            reverse=True
        )
    }

print(analyser_commandes(commandes))
print(trier_commandes_complexes(commandes))