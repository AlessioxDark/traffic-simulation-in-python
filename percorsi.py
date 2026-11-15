
# percorsi.py

DIREZIONI = {
    "nord": (0, 1),
    "sud": (0, -1),
    "ovest": (1, 0),
    "est": (-1, 0)
}

# Coordinate del CENTRO delle auto sulla linea di arresto.
# La corsia è indicata rispetto alla direzione di marcia.

PARTENZE = {
    ("nord", "destra"): (560, 272),
    ("nord", "sinistra"): (592, 272),

    ("sud", "destra"): (528, 432),
    ("sud", "sinistra"): (496, 432),

    ("ovest", "destra"): (464, 336),
    ("ovest", "sinistra"): (464, 304),

    ("est", "destra"): (624, 368),
    ("est", "sinistra"): (624, 400)
}

# Direzione e punto di uscita per le svolte.
USCITE = {
    ("nord", "destra"): ((416, 368), (-1, 0)),
    ("nord", "sinistra"): ((672, 336), (1, 0)),

    ("sud", "destra"): ((672, 336), (1, 0)),
    ("sud", "sinistra"): ((416, 368), (-1, 0)),

    ("ovest", "destra"): ((560, 480), (0, 1)),
    ("ovest", "sinistra"): ((528, 224), (0, -1)),

    ("est", "destra"): ((528, 224), (0, -1)),
    ("est", "sinistra"): ((560, 480), (0, 1))
}

MANOVRE_CONSENTITE = {
    "destra": ("dritto", "destra"),
    "sinistra": ("dritto", "sinistra")
}


def crea_percorso(provenienza, corsia, manovra, passi=120):

    if manovra not in MANOVRE_CONSENTITE[corsia]:
        raise ValueError("Manovra non consentita per questa corsia")

    p0 = PARTENZE[(provenienza, corsia)]

    direzione_in = DIREZIONI[provenienza]

    if manovra == "dritto":

        if provenienza == "nord":
            p3 = (p0[0], 480)
        elif provenienza == "sud":
            p3 = (p0[0], 224)
        elif provenienza == "ovest":
            p3 = (672, p0[1])
        else:
            p3 = (416, p0[1])

        direzione_out = direzione_in

    else:
        p3, direzione_out = USCITE[(provenienza, manovra)]

    # Punti di controllo della curva.
    distanza = 64

    p1 = (
        p0[0] + direzione_in[0] * distanza,
        p0[1] + direzione_in[1] * distanza
    )

    p2 = (
        p3[0] - direzione_out[0] * distanza,
        p3[1] - direzione_out[1] * distanza
    )

    punti = []

    # Curva di Bezier cubica.
    for i in range(passi + 1):

        t = i / passi
        u = 1 - t

        x = (
            u**3 * p0[0]
            + 3 * u**2 * t * p1[0]
            + 3 * u * t**2 * p2[0]
            + t**3 * p3[0]
        )

        y = (
            u**3 * p0[1]
            + 3 * u**2 * t * p1[1]
            + 3 * u * t**2 * p2[1]
            + t**3 * p3[1]
        )

        punti.append((x, y))

    return punti, direzione_out
