# question a
def get_stats_etudiant():
    # nom, age, moyenne, notes_liste, mention
    return ("Alice Dupont", 20, 15.5, [12, 16, 18, 14, 15], "Bien")

nom, _, moyenne, _, _ = get_stats_etudiant()
print(nom, moyenne)

nom, *infos = get_stats_etudiant()
print(nom, infos)

nom, age, _, *notes, _ = get_stats_etudiant()
print(nom, age, notes)

# question b
_, _, _, notes, _ = get_stats_etudiant()

def swap_et_statistiques(nombres):
    minimum, maximum = min(nombres), max(nombres)
    moyenne = sum(nombres) / len(nombres)
    count = len(nombres)
    return (maximum, minimum, moyenne, count)

print(swap_et_statistiques(notes))

# question c
point = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]

xs, ys, zs = zip(*point)
print(xs, ys, zs)

xy_tuples = [(x, y) for x, y, _ in point]
print(xy_tuples)

somme_x = sum(xs)
somme_y = sum(ys)
somme_z = sum(zs)
print(somme_x, somme_y, somme_z)