P_ANSWER = "Sì!"
N_ANSWER = "No."

WELCOME_TEXTS = [
    "Ciao! Sono Giacomo Rebecchi, uno studente del 5° anno del corso in Data "
    "Science & Business Analytics dell'Università Bocconi.",
    #
    "Per il mio lavoro di tesi, sto provando a sondare la capacità delle persone "
    "di indovinare il prezzo degli alimenti in vendita su una diffusa piattaforma "
    "di Food Delivery.",
    #
    "Ho sviluppato un modello di Deep Learning che prova anch'esso a indovinare "
    "con precisione il prezzo di questi prodotti. L'obiettivo di questo gioco è "
    "verificare se il mio modello è in grado di battere gli esseri umani in questa "
    "sfida!",
    #
    "Se sei interessato al mio progetto, puoi trovare la Repository pubblica al "
    "link https://github.com/giacomorebecchi/food-pricing. Mi puoi anche "
    "contattare all'indirizzo email personale grebecchi98@gmail.com. Sarò felice "
    "di rispondere a ogni tua curiosità!",
]

START_TEXT = "Sei pronto a giocare con me?"

READY_TEXTS = [
    "Ti spiego brevemente in cosa consiste il gioco.",
    "Ti invierò un'immagine di un cibo, accompagnata dal suo titolo e una "
    "descrizione (non sempre presente). Il tuo obiettivo è indovinare il prezzo "
    "di quel prodotto.",
    "Per giocare, a ogni messaggio (immagine + testo) che ti invierò, dovrai "
    "rispondere con il prezzo in cifre che pensi sia adeguato per il prodotto "
    "mostrato.",
    "Per favore, scrivi il prezzo in cifre, separato da un punto.",
    "Per esempio, quando ti invio un'immagine con il testo, dovrai rispondere ",
    "0.00",
    "Dove al posto degli 0 dovrai mettere le cifre corrette.",
    "Ad ogni tua risposta, risponderò con il prezzo corretto del prodotto, "
    "seguito da un nuovo turno del gioco. Quando ti stufi di giocare, "
    "puoi semplicemente smettere di rispondermi, o scrivere il comando "
    "speciale /stop.",
]

INSTRUCTIONS_TEXT = "Tutto chiaro?"

NOT_READY_TEXT = "\n\n".join(
    [
        "Grazie comunque per l'interesse! Puoi tornare a giocare quando vuoi "
        "ricominciando da capo, semplicemente scrivendo il comando /start in "
        "questa chat.",
        "Giacomo",
    ]
)

START_PLAYING_TEXT = "Bene. Incominciamo con il primo turno!"

NOT_UNDERSTOOD_INSTRUCTIONS_TEXT = "\n\n".join(
    [
        "Mi spiace che le istruzioni siano state poco chiare! Puoi contattarmi "
        "all'indirizzo email grebecchi98@gmail.com, sarò felice di aiutarti. ",
        "Altrimenti puoi ricominciare da capo, semplicemente scrivendo il comando "
        "/start.",
        "Giacomo",
    ]
)

STOP_TEXT = "\n\n".join(
    [
        "Grazie per aver giocato con me, il tuo aiuto è stato prezioso!",
        "Giacomo",
    ]
)

CANC_TEXT = "\n\n".join(
    [
        "Grazie per il tuo tempo!",
        "Giacomo",
    ]
)


def format_fractional_price(p: int) -> str:
    return "€ %.2f" % (p / 100)


def correct_price_text(correct_price: int) -> str:
    correct_price = format_fractional_price(correct_price)
    return f"Il prezzo corretto era: {correct_price}"
