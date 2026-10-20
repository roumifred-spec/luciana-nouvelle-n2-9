# -*- coding: utf-8 -*-
# Analyse des mesures du 12/10 relevees dans controle_memoire_sens.jsonl (recopiees telles quelles).
paires = [(56, 78.4), (177, 198.6), (12, 134.8), (4, 78.3), (3, 115.2), (22, 218.9), (8, 45.2),
          (11, 117.0), (45, 154.3), (104, 438.2), (19, 209.8), (15, 124.0), (71, 214.3),
          (13, 126.9), (6, 67.3), (14, 61.0), (230, 138.1), (82, 208.5), (29, 40.5), (20, 139.1),
          (16, 103.8), (24, 61.7), (10, 144.6), (8, 0.9), (48, 117.3), (78, 324.7), (46, 105.2),
          (121, 1461.7), (64, 84.5), (62, 164.2), (88, 177.2), (52, 269.6)]
dix = [(31, 76.6), (4, 32.1), (3, 16.5), (2, 17.1), (7, 0.8), (2, 18.5), (11, 21.1), (166, 114.2),
       (10, 38.3), (151, 84.0), (58, 137.5), (26, 130.7), (5, 30.6), (208, 173.8)]


def stats(nom, paires):
    n = len(paires)
    sp = sum(p for p, _ in paires)
    ss = sum(s for _, s in paires)
    mp, ms = sp / n, ss / n
    cov = sum((p - mp) * (s - ms) for p, s in paires) / n
    vp = sum((p - mp) ** 2 for p, _ in paires) / n
    vs = sum((s - ms) ** 2 for _, s in paires) / n
    b = cov / vp
    a = ms - b * mp
    print("--- %s ---" % nom)
    print("  %d mises a jour, %d passages, %.1f s au total" % (n, sp, ss))
    print("  cout APPARENT par passage : %.2f s" % (ss / sp))
    print("  correlation passages/secondes : %.3f" % (cov / ((vp * vs) ** 0.5)))
    print("  droite : secondes = %.1f + %.3f * passages" % (a, b))
    print("  => part FIXE par mise a jour : %.1f s | part VRAIMENT variable : %.3f s/passage" % (a, b))
    petits = [(p, s) for p, s in paires if p <= 15]
    if petits:
        print("  tres petits lots (<=15 passages) : %s" % petits)
        print("     -> %.1f s en moyenne pour %.1f passages seulement"
              % (sum(s for _, s in petits) / len(petits), sum(p for p, _ in petits) / len(petits)))
    print("  mini observe : %.1f s | maxi observe : %.1f s" % (min(s for _, s in paires),
                                                               max(s for _, s in paires)))


stats("10/10/2026 (64 000 passages)", dix)
stats("12/10/2026 (73 693 passages)", paires)
