def koren_reci(imenica):
    if imenica[-1] in ["a", "e", "i", "o", "u"]:
        k_i = imenica[:-1]
        return k_i
    else:
        k_i = imenica
        return k_i


def not_vocal(imenica):
    koren_imenice = koren_reci(imenica)
    lista_padeza = []
    nastavci = ["", "", "a", "u", "a", "e", "om", "u"]
    for i in range(8):
        formirana_rec = koren_imenice + nastavci[i]
        lista_padeza.append(formirana_rec)
    return lista_padeza


def ends_with_a(imenica):
    koren_imenice = koren_reci(imenica)
    lista_padeza = []
    if imenica[-2:] in ["ca"]:
        nastavci = ["", "a", "e", "i", "u", "e", "om", "i"]
    elif imenica[-2:] in ["na", "la", "ta"]:
        nastavci = ["", "a", "e", "i", "u", "a", "om", "i"]
    elif imenica[-2:] in ["ka"]:
        nastavci = ["", "a", "e", "i", "u", "o", "om", "i"]
    else:
        nastavci = ["", "a", "e", "i", "u", "e", "om", "i"] #čisto da ne bude greške u kodu kopirao sam nastavke iz prvog if-a
    for i in range(8):
        formirana_rec = koren_imenice + nastavci[i]
        lista_padeza.append(formirana_rec)
    return lista_padeza


def ends_with_e(imenica):
    koren_imenice = koren_reci(imenica)
    lista_padeza = []
    nastavci = ["", "e", "eta", "etu", "e", "e", "etom", "etu"]
    for i in range(8):
        formirana_rec = koren_imenice + nastavci[i]
        lista_padeza.append(formirana_rec)
    return lista_padeza


def ends_with_o(imenica):
    koren_imenice = koren_reci(imenica)
    lista_padeza = []
    nastavci = ["", "o", "a", "u", "a", "o", "om", "u"]
    for i in range(8):
        formirana_rec = koren_imenice + nastavci[i]
        lista_padeza.append(formirana_rec)
    return lista_padeza


def padezi(imenica):
    koren_imenice = koren_reci(imenica)
    lista_padeza = []
    print(f'{koren_imenice=}')
    if imenica[-1] not in ["a", "e", "i", "o", "u"]:
        lista_padeza = not_vocal(imenica)
        print(f'{lista_padeza=}')
        return lista_padeza
    elif imenica[-1] == "a":
        lista_padeza = ends_with_a(imenica)
        print(f'{lista_padeza=}')
        return lista_padeza
    elif imenica[-1] == "e":
        lista_padeza = ends_with_e(imenica)
        print(f'{lista_padeza=}')
        return lista_padeza
    elif imenica[-1] == "o":
        lista_padeza = ends_with_o(imenica)
        print(f'{lista_padeza=}')
        return lista_padeza


#todo: raskomentariši dnjie redove da bi mogao da ispituješ funkcije u terminalu:
# while True:
#     imenica = input('unesi imenicu: ')
#     print(imenica)
#     padezi(imenica)