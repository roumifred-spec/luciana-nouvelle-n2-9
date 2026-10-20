# -*- coding: utf-8 -*-
# Compare le fichier QUI TOURNE avec la version du depot, en ignorant les fins de ligne.
def lire(chemin):
    with open(chemin, "rb") as f:
        return f.read().replace(b"\r\n", b"\n")

serv = r"C:\Users\Fred\Desktop\luciana_v96\luciana_v96\luciana.py"
anc  = r"C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\_ancien.py"
corr = r"C:\Users\Fred\Desktop\Anciennes_versions_Luciana\luciana_v75\luciana.py"

a = lire(anc)
s = lire(serv)
c = lire(corr)

print("octets ancien (depot, avant croix) :", len(a))
print("octets service (ce qui tourne)     :", len(s))
print("octets corrige (avec la croix)     :", len(c))
print("SERVICE == ANCIEN (hors fins de ligne) :", s == a)
print("nombre de lignes corrige :", c.count(b"\n") + 1)

if s != a:
    n = min(len(s), len(a))
    i = 0
    while i < n and s[i] == a[i]:
        i += 1
    print("PREMIERE DIFFERENCE a l'octet", i)
    d = 70
    print("ancien  :", a[max(0, i-d):i+d].decode("utf-8", "replace").replace("\n", "\\n"))
    print("service :", s[max(0, i-d):i+d].decode("utf-8", "replace").replace("\n", "\\n"))
else:
    print("=> le fichier qui tourne est EXACTEMENT la base du depot : on peut poser la croix dessus.")
