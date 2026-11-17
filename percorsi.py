
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
    ("nord", "destra"): (496, 272),
    ("nord", "sinistra"): (528, 272),

    ("sud", "destra"): (592, 432),
    ("sud", "sinistra"): (560, 432),

    # Le corsie di ovest erano invertite
    ("ovest", "destra"): (464, 400),
    ("ovest", "sinistra"): (464, 368),

    # Anche quelle di est erano invertite
    ("est", "destra"): (624, 304),
    ("est", "sinistra"): (624, 336)
}
# Direzione e punto di uscita per le svolte.
USCITE = {
    # Provenienza nord
    ("nord", "destra"): ((416, 304), (-1, 0)),
    ("nord", "sinistra"): ((672, 368), (1, 0)),

    # Provenienza sud
    ("sud", "destra"): ((672, 400), (1, 0)),
    ("sud", "sinistra"): ((416, 336), (-1, 0)),

    # Provenienza ovest
    ("ovest", "destra"): ((496, 480), (0, 1)),
    ("ovest", "sinistra"): ((560, 224), (0, -1)),

    # Provenienza est
    ("est", "destra"): ((592, 224), (0, -1)),
    ("est", "sinistra"): ((528, 480), (0, 1))
}

MANOVRE_CONSENTITE = {
    "destra": ("dritto", "destra"),
    "sinistra": ("dritto", "sinistra")
}



def crea_percorso(provenienza, corsia, manovra, passi=120):

    if manovra not in MANOVRE_CONSENTITE[corsia]:
        raise ValueError(
            "Manovra non consentita per questa corsia"
        )

    if passi < 2:
        raise ValueError("Servono almeno 2 passi")

    # Punto esatto di partenza
    p0 = PARTENZE[(provenienza, corsia)]

    # Direzione di ingresso
    direzione_in = DIREZIONI[provenienza]

    # -------------------------------------------------
    # ANDARE DRITTO: percorso perfettamente rettilineo
    # -------------------------------------------------

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

        punti = []

        for i in range(passi + 1):

            t = i / passi

            x = p0[0] + (p3[0] - p0[0]) * t
            y = p0[1] + (p3[1] - p0[1]) * t

            punti.append((x, y))

        return punti, direzione_out

    # -------------------------------------------------
    # SVOLTE: UTILIZZO DELLE USCITE PRECISE
    # -------------------------------------------------

    p3, direzione_out = USCITE[
        (provenienza, manovra)
    ]

    # Differenza tra partenza e arrivo
    delta_x = p3[0] - p0[0]
    delta_y = p3[1] - p0[1]

    # Spazio disponibile lungo la direzione iniziale
    spazio_ingresso = (
        delta_x * direzione_in[0]
        + delta_y * direzione_in[1]
    )

    # Spazio disponibile lungo la direzione finale
    spazio_uscita = (
        delta_x * direzione_out[0]
        + delta_y * direzione_out[1]
    )

    # Controllo della geometria delle svolte
    prodotto_direzioni = (
        direzione_in[0] * direzione_out[0]
        + direzione_in[1] * direzione_out[1]
    )

    if prodotto_direzioni != 0:
        raise ValueError(
            "La svolta deve essere di 90 gradi"
        )

    if spazio_ingresso <= 0 or spazio_uscita <= 0:
        raise ValueError(
            f"Coordinate di uscita incoerenti: "
            f"{provenienza}, {manovra}"
        )

    # -------------------------------------------------
    # PUNTI DI CONTROLLO DINAMICI
    # -------------------------------------------------

    # Fattore geometrico per curve a 90 gradi
    fattore = 0.55228475

    # La distanza viene calcolata in base alle corsie
    maniglia_ingresso = spazio_ingresso * fattore
    maniglia_uscita = spazio_uscita * fattore

    # Primo punto: segue la direzione di arrivo
    p1 = (
        p0[0] + direzione_in[0] * maniglia_ingresso,
        p0[1] + direzione_in[1] * maniglia_ingresso
    )

    # Secondo punto: segue la direzione dell'uscita
    p2 = (
        p3[0] - direzione_out[0] * maniglia_uscita,
        p3[1] - direzione_out[1] * maniglia_uscita
    )

    # -------------------------------------------------
    # CURVA DI BEZIER CUBICA
    # -------------------------------------------------

    punti = []

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

    # Il primo e l'ultimo punto sono esattamente
    # quelli stabiliti da PARTENZE e USCITE.
    punti[0] = p0
    punti[-1] = p3

    return punti, direzione_out