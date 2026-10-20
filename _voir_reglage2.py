# -*- coding: utf-8 -*-
# LECTURE SEULE : on ne modifie RIEN.
import io

P = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\luciana.py"
S = r"C:\Users\Fred\Desktop\Luciana_v161_memoire2_curseur\res_zones3.txt"

txt = io.open(P, encoding="utf-8", errors="replace").read()
L = txt.splitlines()

out = []
for a, b in [(4035, 4080), (3860, 3880), (5075, 5090)]:
    out.append("=" * 70)
    out.append("LIGNES %d a %d" % (a, b))
    out.append("=" * 70)
    for n in range(a, min(b, len(L)) + 1):
        out.append("%d| %s" % (n, L[n - 1]))

out.append("")
out.append("=" * 70)
out.append("COMPTES, POUR NE PAS SE TROMPER")
out.append("=" * 70)
out.append("fins de ligne CRLF ? %s" % ("OUI" if "\r\n" in txt else "NON (LF)"))
out.append("occurrences de '_SENS_DERNIERS_CHOIX = {}' : %d" % txt.count("_SENS_DERNIERS_CHOIX = {}"))
out.append("occurrences de 'rappel = rappel_automatique(message_utilisateur, hist, debut, chien)' : %d"
           % txt.count("rappel = rappel_automatique(message_utilisateur, hist, debut, chien)"))
out.append("occurrences de 'def _rappel_ancien_actif' : %d" % txt.count("def _rappel_ancien_actif"))
out.append("occurrences de '\"rappel_ancien\"' : %d" % txt.count('"rappel_ancien"'))

io.open(S, "w", encoding="utf-8").write("\n".join(out))
print("ok, %d lignes" % len(out))
