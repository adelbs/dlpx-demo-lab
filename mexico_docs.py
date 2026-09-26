"""
CURP e RFC (persona moral) do México, derivados dos dados da pessoa/empresa.

Regras seguidas (RENAPO / SAT):

CURP (18): 1ª letra + 1ª vogal interna do 1º sobrenome, 1ª letra do 2º
sobrenome, 1ª letra do nome, AAMMDD de nascimento, sexo (H/M), estado (2),
1ª consoante interna de 1º sobrenome, 2º sobrenome e nome, diferenciador de
homonímia (dígito se nascido antes de 2000, letra a partir de 2000) e dígito
verificador (módulo 10).

RFC persona moral (12): 3 letras da razão social, AAMMDD de constituição,
homoclave (2) e dígito verificador (módulo 11).
"""

import unicodedata

CURP_ESTADOS = {
    "Aguascalientes": "AS", "Baja California": "BC", "Baja California Sur": "BS",
    "Campeche": "CC", "Coahuila": "CL", "Colima": "CM", "Chiapas": "CS",
    "Chihuahua": "CH", "CDMX": "DF", "Ciudad de México": "DF", "Durango": "DG",
    "Guanajuato": "GT", "Guerrero": "GR", "Hidalgo": "HG", "Jalisco": "JC",
    "Estado de México": "MC", "Michoacán": "MN", "Morelos": "MS", "Nayarit": "NT",
    "Nuevo León": "NL", "Oaxaca": "OC", "Puebla": "PL", "Querétaro": "QT",
    "Quintana Roo": "QR", "San Luis Potosí": "SP", "Sinaloa": "SL", "Sonora": "SR",
    "Tabasco": "TC", "Tamaulipas": "TS", "Tlaxcala": "TL", "Veracruz": "VZ",
    "Yucatán": "YN", "Zacatecas": "ZS",
}

# Anexo 2 do Instructivo Normativo da CURP: a 2ª letra vira "X".
PALAVRAS_INCONVENIENTES = set("""
BACA BAKA BUEI BUEY CACA CACO CAGA CAGO CAKA CAKO COGE COGI COJA COJE COJI COJO
COLA CULO FALO FETO GETA GUEI GUEY JETA JOTO KACA KACO KAGA KAGO KAKA KAKO KOGE
KOGI KOJA KOJE KOJI KOJO KOLA KULO LILO LOCA LOCO LOKA LOKO MAME MAMO MEAR MEAS
MEON MIAR MION MOCO MOKO MULA MULO NACA NACO PEDA PEDO PENE PIPI PITO POPO PUTA
PUTO QULO RATA ROBA ROBE ROBO RUIN SENO TETA VACA VAGA VAGO VAKA VUEI VUEY WUEI
WUEY
""".split())

PARTICULAS = {"DA", "DAS", "DE", "DEL", "DER", "DI", "DIE", "DD", "EL", "LA",
              "LOS", "LAS", "LE", "LES", "MAC", "MC", "VAN", "VON", "Y"}
NOMES_COMUNS = {"MARIA", "MA", "MA.", "JOSE", "J", "J."}

VOGAIS = "AEIOU"
CURP_ALFABETO = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
RFC_ALFABETO = "0123456789ABCDEFGHIJKLMN&OPQRSTUVWXYZ Ñ"
HOMOCLAVE_ALFABETO = "123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"


def normalizar(s):
    """Maiúsculas, sem acentos, preservando o Ñ."""
    s = s.upper().replace("Ñ", "\0")
    s = "".join(ch for ch in unicodedata.normalize("NFD", s)
                if unicodedata.category(ch) != "Mn")
    return s.replace("\0", "Ñ")


def _palavras(s, ignorar=PARTICULAS):
    ps = [p for p in normalizar(s).split() if p not in ignorar]
    return ps or normalizar(s).split()


def _vogal_interna(p):
    return next((c for c in p[1:] if c in VOGAIS), "X")


def _consoante_interna(p):
    c = next((c for c in p[1:] if c.isalpha() and c not in VOGAIS), "X")
    return "X" if c == "Ñ" else c


def _inicial(p):
    return "X" if not p or p[0] == "Ñ" else p[0]


def curp_dv(base17):
    total = sum(CURP_ALFABETO.index(c) * (18 - i) for i, c in enumerate(base17))
    return str((10 - total % 10) % 10)


def curp(nome, sobrenome1, sobrenome2, nascimento, sexo, estado, homonimia=0):
    """
    nascimento: 'AAAA-MM-DD'; sexo: 'H' ou 'M'; estado: nome ou código de 2 letras;
    homonimia: índice do diferenciador (0 = '0' ou 'A').
    """
    ap1 = "".join(_palavras(sobrenome1))
    ap2 = "".join(_palavras(sobrenome2)) if sobrenome2 else ""
    nomes = _palavras(nome)
    n = nomes[1] if len(nomes) > 1 and nomes[0] in NOMES_COMUNS else nomes[0]

    letras = _inicial(ap1) + _vogal_interna(ap1) + (_inicial(ap2) if ap2 else "X") + _inicial(n)
    if letras in PALAVRAS_INCONVENIENTES:
        letras = letras[0] + "X" + letras[2:]

    ano, mes, dia = nascimento[:10].split("-")
    uf = estado if estado in CURP_ESTADOS.values() else CURP_ESTADOS.get(estado, "NE")
    consoantes = (_consoante_interna(ap1) + (_consoante_interna(ap2) if ap2 else "X")
                  + _consoante_interna(n))
    difer = (str(homonimia % 10) if int(ano) < 2000
             else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[homonimia % 26])

    base = f"{letras}{ano[2:]}{mes}{dia}{sexo}{uf}{consoantes}{difer}"
    return base + curp_dv(base)


# ─── RFC persona moral ────────────────────────────────────────────────────────

REGIMES = ["S. DE R.L. DE C.V.", "S.A.P.I. DE C.V.", "S.A. DE C.V.", "S. EN C.",
           "S. DE R.L.", "S.C.", "S.A.", "A.C.", "SAS"]
PALAVRAS_IGNORADAS_RFC = PARTICULAS | {
    "COMPAÑIA", "CIA", "CIA.", "SOCIEDAD", "SOC", "SOC.", "COOPERATIVA", "COOP",
    "PARA", "POR", "CON", "AL", "EN", "THE", "OF", "AND", "COMPANY", "CO", "CO.",
}


def _sem_regime(razao):
    r = normalizar(razao).strip()
    for reg in REGIMES:
        if r.endswith(" " + reg):
            return r[: -len(reg)].strip()
    return r


def _homoclave(nome):
    codigos = []
    for c in nome:
        if c == " ":
            codigos.append("00")
        elif c.isdigit():
            codigos.append(f"0{c}")
        elif c in "&Ñ":
            codigos.append("10")
        elif "A" <= c <= "I":
            codigos.append(str(11 + ord(c) - ord("A")))
        elif "J" <= c <= "R":
            codigos.append(str(21 + ord(c) - ord("J")))
        elif "S" <= c <= "Z":
            codigos.append(str(32 + ord(c) - ord("S")))
    s = "0" + "".join(codigos)
    total = sum(int(s[i:i + 2]) * int(s[i + 1]) for i in range(len(s) - 1))
    q, r = divmod(total % 1000, 34)
    return HOMOCLAVE_ALFABETO[q] + HOMOCLAVE_ALFABETO[r]


def rfc_dv(base):
    base = base.rjust(12)
    total = sum(RFC_ALFABETO.index(c) * (13 - i) for i, c in enumerate(base))
    return RFC_ALFABETO[(11 - total) % 11]


def rfc_moral(razao_social, constituicao):
    """razao_social: nome da empresa; constituicao: 'AAAA-MM-DD'."""
    nome = _sem_regime(razao_social)
    ps = [p.strip(".,") for p in nome.split()]
    ps = [p for p in ps if p and p not in PALAVRAS_IGNORADAS_RFC] or ps
    if len(ps) >= 3:
        letras = ps[0][0] + ps[1][0] + ps[2][0]
    elif len(ps) == 2:
        letras = ps[0][0] + ps[1][:2]
    else:
        letras = ps[0][:3]
    letras = letras.ljust(3, "X")

    ano, mes, dia = constituicao[:10].split("-")
    limpo = " ".join(p for p in "".join(c for c in nome if c.isalnum() or c in " &Ñ").split())
    base = f"{letras}{ano[2:]}{mes}{dia}{_homoclave(limpo)}"
    return base + rfc_dv(base)
