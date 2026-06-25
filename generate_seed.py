#!/usr/bin/env python3
"""Generate seed data (.txt, 1000 lines each) for all 6 countries."""

import random
import os

BASE = "/Users/felipe.jacob/Projects/demo-lab"
N = 1000
random.seed(42)

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def write(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(str(l) for l in lines) + "\n")

def sample_n(pool, n=N):
    return [random.choice(pool) for _ in range(n)]

def unique_n(gen_func, n=N):
    seen, result = set(), []
    attempts = 0
    while len(result) < n and attempts < n * 10:
        v = gen_func()
        if v not in seen:
            seen.add(v)
            result.append(v)
        attempts += 1
    while len(result) < n:
        result.append(gen_func())
    return result

# ─── DOCUMENT GENERATORS ──────────────────────────────────────────────────────

def gen_cpf():
    d = [random.randint(0, 9) for _ in range(9)]
    v1 = sum((10 - i) * d[i] for i in range(9)) % 11
    d.append(0 if v1 < 2 else 11 - v1)
    v2 = sum((11 - i) * d[i] for i in range(10)) % 11
    d.append(0 if v2 < 2 else 11 - v2)
    s = "".join(map(str, d))
    return f"{s[:3]}.{s[3:6]}.{s[6:9]}-{s[9:]}"

def gen_cnpj():
    b = [random.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]
    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    r1 = sum(b[i] * w1[i] for i in range(12)) % 11
    b.append(0 if r1 < 2 else 11 - r1)
    w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    r2 = sum(b[i] * w2[i] for i in range(13)) % 11
    b.append(0 if r2 < 2 else 11 - r2)
    s = "".join(map(str, b))
    return f"{s[:2]}.{s[2:5]}.{s[5:8]}/{s[8:12]}-{s[12:]}"

def gen_rut_cl(is_empresa=False):
    n = random.randint(5_000_000, 25_000_000) if not is_empresa else random.randint(60_000_000, 99_000_000)
    digits = [int(c) for c in str(n)]
    weights = [2, 3, 4, 5, 6, 7, 2, 3]
    total = sum(d * w for d, w in zip(reversed(digits), weights))
    rem = 11 - (total % 11)
    dv = "0" if rem == 11 else ("K" if rem == 10 else str(rem))
    s = str(n)
    return f"{s[:-3]}.{s[-6:-3]}.{s[-3:]}-{dv}" if len(s) >= 6 else f"{s}-{dv}"

def gen_dni_ar():
    return f"{random.randint(10_000_000, 50_000_000):,}".replace(",", ".")

def gen_cuit_ar():
    prefixes = ["20", "23", "27", "30", "33"]
    p = random.choice(prefixes)
    n = random.randint(10_000_000, 99_999_999)
    body = f"{p}{n}"
    weights = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(body[i]) * weights[i] for i in range(10))
    dv = 11 - (total % 11)
    dv = 0 if dv == 11 else (1 if dv == 10 else dv)
    return f"{p}-{n}-{dv}"

def gen_curp_mx():
    letters = "AEIOU" if random.random() < 0.3 else "BCDFGHJKLMNPQRSTVWXYZ"
    vowels = "AEIOU"
    consonants = "BCDFGHJKLMNPQRSTVWXYZ"
    year = random.randint(50, 99)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    state = random.choice(["AS","BC","BS","CC","CL","CM","CS","CH","DF","DG",
                           "GT","GR","HG","JC","MC","MN","MS","NT","NL","OC",
                           "PL","QT","QR","SP","SL","SR","TC","TS","TL","VZ","YN","ZS"])
    sex = random.choice(["H", "M"])
    c1 = random.choice("AEIOU")
    c2 = random.choice("BCDFGHJKLMNPQRSTVWXYZ")
    c3 = random.choice("BCDFGHJKLMNPQRSTVWXYZ")
    c4 = random.choice("BCDFGHJKLMNPQRSTVWXYZ")
    suffix = f"{random.randint(0,9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
    name_part = f"{random.choice('AEIOU')}{random.choice(consonants)}{random.choice(vowels)}{random.choice(vowels)}"
    return f"{name_part}{year:02d}{month:02d}{day:02d}{sex}{state}{c2}{c3}{c4}{suffix}"

def gen_rfc_mx(is_empresa=False):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if is_empresa:
        prefix = "".join(random.choices(letters, k=3))
    else:
        prefix = "".join(random.choices(letters, k=4))
    year = random.randint(50, 99)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    suffix = "".join(random.choices(letters + "0123456789", k=3))
    return f"{prefix}{year:02d}{month:02d}{day:02d}{suffix}"

def gen_cedula_pa():
    prov = random.randint(1, 10)
    libro = random.randint(1, 999)
    asiento = random.randint(1, 9999)
    return f"{prov}-{libro:03d}-{asiento:04d}"

def gen_ruc_pa():
    n = random.randint(1_000_000, 9_999_999)
    tipo = random.randint(1, 2)
    digv = random.randint(1, 99)
    return f"{n}-{tipo}-{digv:02d}"

def gen_cedula_co():
    return str(random.randint(100_000_000, 1_299_999_999))

def gen_nit_co():
    n = random.randint(800_000_000, 999_999_999)
    dv = random.randint(0, 9)
    return f"{n:,}-{dv}".replace(",", ".")

# ─── BRASIL ───────────────────────────────────────────────────────────────────

BR_NOMES = [
    "João","Pedro","Lucas","Gabriel","Matheus","Rafael","Gustavo","Felipe","Bruno","Carlos",
    "André","Rodrigo","Henrique","Diego","Eduardo","Marcelo","Thiago","Alexandre","Fernando","Paulo",
    "Vinicius","Leonardo","Ricardo","Marco","Antonio","José","Luis","Daniel","Sergio","Roberto",
    "Ana","Maria","Julia","Beatriz","Camila","Fernanda","Larissa","Amanda","Bruna","Vanessa",
    "Patricia","Renata","Juliana","Natalia","Mariana","Leticia","Aline","Cristina","Sandra","Monica",
    "Claudia","Alessandra","Michele","Roberta","Priscila","Isabela","Gabriela","Carolina","Débora","Elaine",
    "Marcos","Caio","Leandro","Fábio","Igor","Murilo","Otávio","Tiago","Wendel","Yuri"
]

BR_SOBRENOMES = [
    "Silva","Santos","Oliveira","Souza","Rodrigues","Ferreira","Alves","Pereira","Lima","Gomes",
    "Costa","Ribeiro","Martins","Carvalho","Almeida","Lopes","Sousa","Fernandes","Vieira","Barbosa",
    "Rocha","Dias","Nascimento","Andrade","Moreira","Nunes","Marques","Machado","Mendes","Freitas",
    "Castro","Cardoso","Ramos","Araújo","Cavalcanti","Moraes","Pinto","Correia","Miranda","Teixeira",
    "Cunha","Monteiro","Campos","Aguiar","Batista","Melo","Cruz","Fonseca","Farias","Borges",
    "Tavares","Azevedo","Rezende","Guimarães","Pires","Matos","Brito","Coelho","Xavier","Braga"
]

BR_TIPOS_LOGRADOURO = ["Rua","Rua","Avenida","Avenida","Alameda","Travessa","Estrada","Via"]

BR_NOMES_LOGRADOURO = [
    "das Flores","das Acácias","dos Pinheiros","do Sol","da Paz","das Palmeiras","do Carmo","das Nações",
    "Brasil","São Paulo","Rio de Janeiro","Minas Gerais","Bahia","Goiás","Paraná",
    "Getúlio Vargas","Presidente Kennedy","Dom Pedro I","Dom Pedro II","Tiradentes","Sete de Setembro",
    "Quinze de Novembro","Vinte e Um de Abril","Treze de Maio","Dezoito de Abril",
    "Marechal Deodoro","Floriano Peixoto","Santos Dumont","Barão do Rio Branco","José Bonifácio",
    "João Pessoa","Rui Barbosa","Duque de Caxias","Marquês de Pombal","Visconde de Taunay",
    "das Araucárias","dos Pássaros","das Esmeraldas","dos Ipês","das Mangueiras",
    "Nova Lima","Nova Esperança","Nova Conquista","Nova Aurora","Primavera",
    "Central","Principal","Comercial","Industrial","Universitária",
    "das Laranjeiras","dos Lírios","das Orquídeas","das Rosas","dos Cravos",
]

BR_COMPLEMENTOS = [
    "Apto 11","Apto 21","Apto 31","Apto 42","Apto 53","Apto 64","Apto 72","Apto 81","Apto 93","Apto 101",
    "Bloco A Apto 12","Bloco B Apto 23","Bloco C Apto 34","Bloco D Apto 45","Bloco E Apto 56",
    "Casa 1","Casa 2","Casa 3","Casa 4","Casa 5",
    "Sala 101","Sala 201","Sala 301","Sala 12","Sala 22",
    "Cobertura 1","Cobertura 2","Fundos","Sobreloja","Térreo",
    "Apto 201","Apto 301","Apto 401","Apto 102","Apto 202",
]

BR_CIDADES_ESTADOS = [
    "São Paulo - SP","Rio de Janeiro - RJ","Belo Horizonte - MG","Salvador - BA","Fortaleza - CE",
    "Curitiba - PR","Manaus - AM","Recife - PE","Porto Alegre - RS","Goiânia - GO",
    "Belém - PA","Guarulhos - SP","Campinas - SP","São Luís - MA","São Gonçalo - RJ",
    "Maceió - AL","Natal - RN","Campo Grande - MS","Teresina - PI","João Pessoa - PB",
    "Osasco - SP","Ribeirão Preto - SP","Jaboatão dos Guararapes - PE","Contagem - MG",
    "Uberlândia - MG","Sorocaba - SP","Aracaju - SE","Feira de Santana - BA","Cuiabá - MT",
    "Joinville - SC","Juiz de Fora - MG","Aparecida de Goiânia - GO","Londrina - PR",
    "Porto Velho - RO","Serra - ES","Caxias do Sul - RS","Florianópolis - SC",
    "Mogi das Cruzes - SP","Betim - MG","Ananindeua - PA","Santos - SP","Diadema - SP",
    "Niterói - RJ","Olinda - PE","Piracicaba - SP","Macapá - AP","Cabo Frio - RJ",
    "Vila Velha - ES","São José dos Campos - SP","Jundiaí - SP",
]

BR_EMPRESAS_RAZAO = [
    "Tech","Soluções","Serviços","Comércio","Indústria","Grupo","Holdings","Empreendimentos",
    "Construtora","Distribuidora","Importadora","Exportadora","Tecnologia","Sistemas","Logística",
    "Consultoria","Assessoria","Investimentos","Participações","Engenharia"
]
BR_EMPRESAS_TIPO = ["Ltda","S.A.","S/A","ME","EPP","Eireli","SS"]
BR_EMPRESAS_NOMES = [
    "Alpha","Beta","Delta","Omega","Nexus","Apex","Prime","Elite","Master","Global",
    "Nacional","Brasil","Tropical","Verde","Azul","Solar","Terra","Vida","Forte","Rio",
    "Serra","Vale","Mar","Sul","Norte","Leste","Oeste","Central","Imperial","Royal",
    "Ágil","Rápida","Eficaz","Segura","Precisa","Inovadora","Digital","Smart","Future","Vision"
]

def gen_br_cep():
    return f"{random.randint(1000,99999):05d}-{random.randint(0,999):03d}"

def gen_br_phone():
    ddd = random.choice(["11","21","31","41","51","61","71","81","91","19","27","47","48","62","63","65","66","67","68","69","82","83","84","85","86","87","88","89","92","93","94","95","96","97","98","99"])
    return f"({ddd}) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"

def gen_brasil():
    seed_dir = f"{BASE}/countries/brasil/seed"
    write(f"{seed_dir}/nomes.txt", sample_n(BR_NOMES))
    write(f"{seed_dir}/sobrenomes.txt", sample_n(BR_SOBRENOMES))
    write(f"{seed_dir}/enderecos_linha1.txt",
          [f"{random.choice(BR_TIPOS_LOGRADOURO)} {random.choice(BR_NOMES_LOGRADOURO)}, {random.randint(1, 9999)}" for _ in range(N)])
    write(f"{seed_dir}/enderecos_linha2.txt", sample_n(BR_COMPLEMENTOS))
    write(f"{seed_dir}/cidades_estados.txt", sample_n(BR_CIDADES_ESTADOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(BR_EMPRESAS_NOMES)} {random.choice(BR_EMPRESAS_RAZAO)} {random.choice(BR_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/cpf.txt", unique_n(gen_cpf))
    write(f"{seed_dir}/cnpj.txt", unique_n(gen_cnpj))
    write(f"{seed_dir}/cep.txt", [gen_br_cep() for _ in range(N)])
    write(f"{seed_dir}/telefones.txt", [gen_br_phone() for _ in range(N)])
    print("Brasil: done")

# ─── ARGENTINA ────────────────────────────────────────────────────────────────

AR_NOMBRES = [
    "Mateo","Santiago","Benjamín","Valentín","Lucas","Tomás","Facundo","Nicolás","Agustín","Sebastián",
    "Martín","Diego","Rodrigo","Alejandro","Leandro","Hernán","Ezequiel","Damián","Cristian","Gustavo",
    "Valentina","Sofía","Martina","Isabella","Luciana","Camila","Florencia","Natalia","Alejandra","Romina",
    "Soledad","Vanesa","Paola","Verónica","Claudia","Daniela","Gabriela","Cecilia","Nadia","Lorena",
    "Franco","Emiliano","Pablo","Marcelo","Ignacio","Juan","Carlos","Fernando","Alberto","Ricardo",
    "María","Ana","Laura","Paula","Silvana","Graciela","Patricia","Sandra","Mónica","Elena"
]

AR_APELLIDOS = [
    "García","González","Rodríguez","López","Martínez","Pérez","Sánchez","Romero","Torres","Flores",
    "Acosta","Benítez","Díaz","Ferreyra","Giménez","Herrera","Ibáñez","Juárez","Medina","Navarro",
    "Ortiz","Peralta","Quiroga","Ruiz","Suárez","Vera","Aguirre","Blanco","Castro","Domínguez",
    "Escobar","Figueroa","Gutiérrez","Molina","Núñez","Ojeda","Ponce","Reyes","Salinas","Vargas",
    "Alvarez","Bravo","Cabrera","Delgado","Espinoza","Fonseca","Guerrero","Leiva","Mansilla","Paredes"
]

AR_TIPOS_CALLE = ["Calle","Avenida","Avenida","Boulevard","Pasaje","Diagonal"]

AR_NOMBRES_CALLE = [
    "San Martín","Belgrano","Rivadavia","Mitre","Sarmiento","Corrientes","Santa Fe","Córdoba",
    "Las Heras","Callao","Florida","Lavalle","Tucumán","Viamonte","Paraguay","Charcas",
    "Libertad","Reconquista","Suipacha","Maipú","Esmeralda","San Juan","Independencia",
    "Avellaneda","Carabobo","Boyacá","Gaona","Nazca","Cuenca","Galicia",
    "Cabildo","Monroe","Olazábal","Juramento","Sucre","Arcos","Virrey del Pino",
    "Melián","Núñez","Cramer","Villanueva","Elcano","Moldes","Zabala","Blanco Encalada",
    "Valentín Alsina","Tres Sargentos","Reconquista","25 de Mayo","Leandro Alem",
]

AR_COMPLEMENTOS = [
    "Piso 1 Depto A","Piso 2 Depto B","Piso 3 Depto C","Piso 4 Depto D","Piso 5 Depto E",
    "PB Depto 1","PB Depto 2","PB Depto 3","1° A","1° B","2° A","2° B","3° A","3° B",
    "Depto 11","Depto 21","Depto 31","Depto 12","Depto 22","Depto 32",
    "Casa","Local 1","Local 2","Oficina 101","Oficina 201",
]

AR_CIUDADES_PROVINCIAS = [
    "Buenos Aires, Buenos Aires","Córdoba, Córdoba","Rosario, Santa Fe","Mendoza, Mendoza",
    "La Plata, Buenos Aires","Tucumán, Tucumán","Mar del Plata, Buenos Aires","Salta, Salta",
    "Santa Fe, Santa Fe","San Juan, San Juan","Resistencia, Chaco","Santiago del Estero, Santiago del Estero",
    "Corrientes, Corrientes","Posadas, Misiones","Bahía Blanca, Buenos Aires","Paraná, Entre Ríos",
    "Neuquén, Neuquén","Formosa, Formosa","San Salvador de Jujuy, Jujuy","Río Cuarto, Córdoba",
    "Quilmes, Buenos Aires","Lanús, Buenos Aires","General San Martín, Buenos Aires","Lomas de Zamora, Buenos Aires",
    "Almirante Brown, Buenos Aires","Berazategui, Buenos Aires","Merlo, Buenos Aires","Morón, Buenos Aires",
    "Tigre, Buenos Aires","San Isidro, Buenos Aires","Vicente López, Buenos Aires","Avellaneda, Buenos Aires",
    "Comodoro Rivadavia, Chubut","Río Gallegos, Santa Cruz","Ushuaia, Tierra del Fuego",
    "San Luis, San Luis","Catamarca, Catamarca","La Rioja, La Rioja","Viedma, Río Negro","Rawson, Chubut",
]

AR_EMPRESAS_TIPO = ["S.A.","S.R.L.","SAS","SA","SRL"]
AR_EMPRESAS_NOMES = [
    "Pampa","Gaucho","Sur","Norte","Federal","Imperial","Real","Gran","Nuevo","Nacional",
    "Río de la Plata","Andina","Patagónica","Porteña","Bonaerense","Rioplatense","Austral","Cordillerana",
    "Grupo","Corporación","Compañía","Sociedad","Empresa","Industria","Comercio","Servicio",
    "Alpha","Beta","Delta","Omega","Prime","Elite","Global","Tech","Digital","Smart"
]
AR_EMPRESAS_RUBROS = [
    "Tecnología","Servicios","Comercial","Industrial","Constructora","Logística","Alimentaria",
    "Agropecuaria","Energética","Financiera","Inmobiliaria","Textil","Química","Farmacéutica"
]

def gen_ar_cp():
    return str(random.randint(1000, 9999))

def gen_ar_phone():
    area = random.choice(["011","0221","0351","0261","0381","0387","0223","0379","0342","0264"])
    return f"{area} {random.randint(1000,9999)}-{random.randint(1000,9999)}"

def gen_argentina():
    seed_dir = f"{BASE}/countries/argentina/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(AR_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(AR_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(AR_TIPOS_CALLE)} {random.choice(AR_NOMBRES_CALLE)} {random.randint(1, 9999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(AR_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_provincias.txt", sample_n(AR_CIUDADES_PROVINCIAS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(AR_EMPRESAS_NOMES)} {random.choice(AR_EMPRESAS_RUBROS)} {random.choice(AR_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/dni.txt", unique_n(gen_dni_ar))
    write(f"{seed_dir}/cuit.txt", unique_n(gen_cuit_ar))
    write(f"{seed_dir}/codigo_postal.txt", [gen_ar_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_ar_phone() for _ in range(N)])
    print("Argentina: done")

# ─── CHILE ────────────────────────────────────────────────────────────────────

CL_NOMBRES = [
    "Matías","Sebastián","Diego","Felipe","Nicolás","Cristóbal","Ignacio","Rodrigo","Andrés","Gonzalo",
    "Francisco","Patricio","Claudio","Sergio","Mauricio","Ricardo","Eduardo","Pablo","Leonardo","Hernán",
    "Valentina","Camila","Daniela","Francisca","Javiera","Constanza","Catalina","Fernanda","Gabriela","Natalia",
    "Carolina","Verónica","Patricia","Alejandra","Claudia","Pamela","Yasna","Isidora","Antonia","Monserrat",
    "Carlos","Juan","Luis","Mario","Miguel","Jorge","Roberto","Víctor","René","Álvaro",
    "María","Ana","Rosa","Isabel","Lorena","Angélica","Marcela","Soledad","Elizabeth","Sandra"
]

CL_APELLIDOS = [
    "González","Muñoz","Rojas","Díaz","Pérez","Soto","Contreras","Silva","Martínez","Sepúlveda",
    "Morales","Rodríguez","López","Fuentes","Hernández","Torres","Araya","Flores","Espinoza","Valenzuela",
    "Castillo","Ramírez","Reyes","Gutiérrez","Castro","Vargas","Álvarez","Vásquez","Figueroa","Bravo",
    "Acuña","Aguilera","Ahumada","Alarcón","Andrade","Arias","Barrientos","Carrasco","Cárdenas","Cortés",
    "Gallardo","Garrido","Guerra","Ibáñez","Lara","Leiva","Medina","Miranda","Molina","Navarro"
]

CL_TIPOS_CALLE = ["Calle","Avenida","Avenida","Pasaje","Camino","Villa"]

CL_NOMBRES_CALLE = [
    "Alameda","Providencia","Apoquindo","Irarrázaval","Grecia","Los Militares","Kennedy","Vicuña Mackenna",
    "Mapocho","Bulnes","Serrano","Estado","Bandera","Compañía","Agustinas","Monjitas","Moneda",
    "Carmen","Coquimbo","Talca","Chillán","Concepción","Valparaíso","Antofagasta","Iquique",
    "Los Leones","Pedro de Valdivia","Luis Pasteur","Holanda","Condell","Manuel Montt","Salvador",
    "España","Francia","Italia","Alemania","Portugal","Brasil","Argentina","Colombia",
    "Independencia","O'Higgins","Prat","Matta","San Martín","Carrera","Balmaceda","Arturo Prat",
]

CL_COMPLEMENTOS = [
    "Depto 1","Depto 2","Depto 3","Depto 4","Depto 101","Depto 201","Depto 301",
    "Piso 1","Piso 2","Piso 3","Casa 1","Casa 2","Casa 3",
    "Block A Depto 1","Block B Depto 2","Block C Depto 3",
    "Interior","Local 1","Local 2","Oficina 1","Oficina 2",
]

CL_CIUDADES_REGIONES = [
    "Santiago, Región Metropolitana","Valparaíso, Región de Valparaíso","Concepción, Región del Biobío",
    "La Serena, Región de Coquimbo","Antofagasta, Región de Antofagasta","Temuco, Región de La Araucanía",
    "Rancagua, Región de O'Higgins","Talca, Región del Maule","Arica, Región de Arica y Parinacota",
    "Puerto Montt, Región de Los Lagos","Iquique, Región de Tarapacá","Coquimbo, Región de Coquimbo",
    "Osorno, Región de Los Lagos","Valdivia, Región de Los Ríos","Chillán, Región de Ñuble",
    "Calama, Región de Antofagasta","Punta Arenas, Región de Magallanes","Copiapó, Región de Atacama",
    "Quilpué, Región de Valparaíso","Villa Alemana, Región de Valparaíso","San Antonio, Región de Valparaíso",
    "Los Ángeles, Región del Biobío","Coronel, Región del Biobío","Talcahuano, Región del Biobío",
    "Puente Alto, Región Metropolitana","Maipú, Región Metropolitana","Las Condes, Región Metropolitana",
    "La Florida, Región Metropolitana","Peñalolén, Región Metropolitana","Ñuñoa, Región Metropolitana",
]

CL_EMPRESAS_TIPO = ["S.A.","SpA","Ltda.","E.I.R.L.","SPA","SA"]
CL_EMPRESAS_NOMES = [
    "Andina","Patagónica","Austral","Chilena","Nacional","Central","Sur","Norte","Pacífico","Cordillera",
    "Atacama","Araucanía","Mapuche","Rapanui","Cobre","Plata","Oro","Vino","Salmón","Pesca",
    "Tecnológica","Comercial","Industrial","Constructora","Agrícola","Minera","Energía","Servicios"
]

def gen_cl_cp():
    return f"{random.randint(1000000, 9999999)}"

def gen_cl_phone():
    return f"+56 {random.randint(2,9)} {random.randint(1000,9999)} {random.randint(1000,9999)}"

def gen_chile():
    seed_dir = f"{BASE}/countries/chile/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(CL_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(CL_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(CL_TIPOS_CALLE)} {random.choice(CL_NOMBRES_CALLE)} {random.randint(1, 9999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(CL_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_regiones.txt", sample_n(CL_CIUDADES_REGIONES))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(CL_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Minería','Agrícola','Construcción'])} {random.choice(CL_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/rut_personas.txt", unique_n(lambda: gen_rut_cl(False)))
    write(f"{seed_dir}/rut_empresas.txt", unique_n(lambda: gen_rut_cl(True)))
    write(f"{seed_dir}/codigo_postal.txt", [gen_cl_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_cl_phone() for _ in range(N)])
    print("Chile: done")

# ─── MÉXICO ───────────────────────────────────────────────────────────────────

MX_NOMBRES = [
    "José","Juan","Carlos","Miguel","Francisco","Jorge","Alejandro","Ricardo","Roberto","Fernando",
    "Eduardo","Manuel","Sergio","Marco","David","Luis","Andrés","Daniel","Pablo","Rafael",
    "María","Ana","Laura","Claudia","Patricia","Alejandra","Verónica","Gabriela","Diana","Sofía",
    "Fernanda","Mariana","Karla","Leticia","Rosa","Elena","Adriana","Norma","Silvia","Berenice",
    "Jesús","Pedro","Antonio","Arturo","Gerardo","Víctor","Héctor","Raúl","Ernesto","Guillermo",
    "Gloria","Guadalupe","Alicia","Martha","Teresa","Irene","Pilar","Esperanza","Carmen","Dolores"
]

MX_APELLIDOS = [
    "García","Hernández","Martínez","López","González","Pérez","Sánchez","Ramírez","Cruz","Flores",
    "Reyes","Torres","Morales","Jiménez","Vázquez","Álvarez","Ruiz","Romero","Vargas","Díaz",
    "Castillo","Mendoza","Chávez","Rojas","Gutiérrez","Ortiz","Delgado","Herrera","Moreno","Núñez",
    "Ramos","Navarro","Ríos","Sandoval","Guerrero","Aguilar","Alvarado","Espinoza","Medina","Fuentes",
    "Domínguez","Guzmán","Contreras","Orozco","Montoya","Salinas","Miranda","Velázquez","Cabrera","Lara"
]

MX_TIPOS_CALLE = ["Calle","Avenida","Avenida","Boulevard","Calzada","Privada","Cerrada","Circuito"]

MX_NOMBRES_CALLE = [
    "Juárez","Hidalgo","Morelos","Insurgentes","Reforma","Revolución","Independencia","Constitución",
    "Madero","Carranza","Obregón","Cárdenas","Ávila Camacho","López Mateos","Echeverría",
    "Universidad","Tecnológico","Nacional","Federal","Central","Principal","Comercial",
    "Las Palmas","Los Pinos","Los Olivos","Las Flores","Los Robles","Las Américas",
    "Cuauhtémoc","Azteca","Tolteca","Maya","Zapoteca","Olmeca","Mixteca",
    "San Rafael","San Juan","San Pedro","San Pablo","Santa María","Santa Ana",
    "Del Valle","Del Bosque","Del Prado","Del Lago","Del Sol","De la Paz",
]

MX_COMPLEMENTOS = [
    "Interior 1","Interior 2","Depto 1","Depto 2","Piso 1","Piso 2","Piso 3",
    "Local A","Local B","Edificio A","Edificio B","Torre 1","Torre 2",
    "Fraccionamiento","Manzana 1 Lote 2","Col. Centro","Col. Norte",
]

MX_CIUDADES_ESTADOS = [
    "Ciudad de México, CDMX","Guadalajara, Jalisco","Monterrey, Nuevo León",
    "Puebla, Puebla","Tijuana, Baja California","León, Guanajuato",
    "Juárez, Chihuahua","Zapopan, Jalisco","Mérida, Yucatán","Mexicali, Baja California",
    "San Luis Potosí, San Luis Potosí","Aguascalientes, Aguascalientes",
    "Acapulco, Guerrero","Heroica Mérida, Yucatán","Querétaro, Querétaro",
    "Chihuahua, Chihuahua","Morelia, Michoacán","Cancún, Quintana Roo",
    "Veracruz, Veracruz","Culiacán, Sinaloa","Hermosillo, Sonora",
    "Saltillo, Coahuila","Naucalpan, Estado de México","Ecatepec, Estado de México",
    "Tlalnepantla, Estado de México","Torreón, Coahuila","Durango, Durango",
    "Tepic, Nayarit","Xalapa, Veracruz","Villahermosa, Tabasco",
    "Oaxaca, Oaxaca","Tuxtla Gutiérrez, Chiapas","Tlaxcala, Tlaxcala",
    "Pachuca, Hidalgo","Colima, Colima","Campeche, Campeche",
]

MX_EMPRESAS_TIPO = ["S.A. de C.V.","S. de R.L. de C.V.","S.A.","S. de R.L.","A.C."]
MX_EMPRESAS_NOMES = [
    "Azteca","Nacional","Mexicana","Del Norte","Del Sur","Central","Federal","Gran","Nuevo","Real",
    "Tecnológica","Industrial","Comercial","Constructora","Agrícola","Energética","Financiera",
    "Alpha","Beta","Delta","Omega","Prime","Elite","Global","Digital","Smart","Future"
]

def gen_mx_cp():
    return f"{random.randint(1000, 99999):05d}"

def gen_mx_phone():
    area = random.choice(["55","33","81","222","664","477","656","33","999","686"])
    return f"+52 {area} {random.randint(1000,9999)} {random.randint(1000,9999)}"

def gen_mexico():
    seed_dir = f"{BASE}/countries/mexico/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(MX_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(MX_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(MX_TIPOS_CALLE)} {random.choice(MX_NOMBRES_CALLE)} {random.randint(1, 9999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(MX_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_estados.txt", sample_n(MX_CIUDADES_ESTADOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(MX_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Construcción','Logística'])} {random.choice(MX_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/curp.txt", unique_n(gen_curp_mx))
    write(f"{seed_dir}/rfc.txt", unique_n(lambda: gen_rfc_mx(False)))
    write(f"{seed_dir}/codigo_postal.txt", [gen_mx_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_mx_phone() for _ in range(N)])
    print("México: done")

# ─── PANAMÁ ───────────────────────────────────────────────────────────────────

PA_NOMBRES = [
    "José","Juan","Carlos","Miguel","Francisco","Alejandro","Ricardo","Roberto","Fernando","Eduardo",
    "Manuel","Sergio","Marco","David","Luis","Andrés","Daniel","Rafael","Ángel","Antonio",
    "María","Ana","Laura","Claudia","Patricia","Alejandra","Verónica","Gabriela","Diana","Sofía",
    "Fernanda","Mariana","Karla","Leticia","Rosa","Elena","Adriana","Norma","Silvia","Carmen",
    "Rogelio","Iván","Omar","Armando","Arturo","Gerardo","Víctor","Héctor","Raúl","Ernesto",
    "Gloria","Guadalupe","Alicia","Martha","Teresa","Irene","Pilar","Esperanza","Isabel","Lucía"
]

PA_APELLIDOS = [
    "García","González","Rodríguez","López","Martínez","Pérez","Sánchez","Romero","Torres","Flores",
    "Herrera","Morales","Jiménez","Reyes","Cruz","Vargas","Castillo","Ramos","Mendoza","Chávez",
    "Pittí","Guardia","Broce","Aizpurúa","Miró","Arias","Fábrega","Icaza","Pereira","Barría",
    "Moreno","Ruiz","Domínguez","Castro","Delgado","Ortiz","Gutiérrez","Guerrero","Medina","Aguilar",
    "Molina","Navarro","Salinas","Miranda","Espinoza","Figueroa","Núñez","Cabrera","Vega","Lara"
]

PA_TIPOS_CALLE = ["Calle","Avenida","Avenida","Vía","Calle Principal"]

PA_NOMBRES_CALLE = [
    "Balboa","Central","Roosevelt","Ricardo J. Alfaro","Transistmica","Cincuentenario",
    "Brasil","España","Colombia","México","Argentina","Venezuela","Perú","Ecuador",
    "Omar Torrijos","Belisario Porras","Arnulfo Arias","Domingo Díaz","Mártires",
    "Tumba Muerto","12 de Octubre","17 de Abril","3 de Noviembre","28 de Noviembre",
    "El Dorado","Albrook","Clayton","Ancón","Miraflores","Pedro Miguel","Gamboa",
]

PA_COMPLEMENTOS = [
    "Apto 1","Apto 2","Apto 3","Piso 1","Piso 2","Piso 3","Planta Baja",
    "Edificio A","Edificio B","Torre 1","Torre 2","Local 1","Local 2",
    "Casa 1","Casa 2","Residencial Norte","Residencial Sur",
]

PA_CIUDADES_PROVINCIAS = [
    "Ciudad de Panamá, Panamá","San Miguelito, Panamá","Colón, Colón",
    "David, Chiriquí","Santiago, Veraguas","Chitré, Herrera",
    "Las Tablas, Los Santos","La Chorrera, Panamá Oeste","Penonomé, Coclé",
    "Changuinola, Bocas del Toro","El Porvenir, Guna Yala",
    "Arraiján, Panamá Oeste","La Palma, Darién","Metetí, Darién",
    "Aguadulce, Coclé","Natá, Coclé","Ocú, Herrera","Macaracas, Los Santos",
    "Bocas del Toro, Bocas del Toro","Almirante, Bocas del Toro",
]

PA_EMPRESAS_TIPO = ["S.A.","Corp.","Inc.","Ltda.","S. de R.L."]
PA_EMPRESAS_NOMES = [
    "Panamá","Canalera","Istmeña","Panameña","Nacional","Central","Pacífica","Atlántica",
    "Tecnológica","Comercial","Industrial","Constructora","Logística","Financiera",
    "Alpha","Beta","Delta","Global","Digital","Smart","Prime","Elite"
]

def gen_pa_cp():
    return f"{random.randint(100, 999):03d}{random.randint(0, 99):02d}"

def gen_pa_phone():
    prefix = random.choice(["6","6","6","2","2","3","4"])
    return f"+507 {prefix}{random.randint(100,999)}-{random.randint(1000,9999)}"

def gen_panama():
    seed_dir = f"{BASE}/countries/panama/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(PA_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(PA_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(PA_TIPOS_CALLE)} {random.choice(PA_NOMBRES_CALLE)} {random.randint(1, 999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(PA_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_provincias.txt", sample_n(PA_CIUDADES_PROVINCIAS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(PA_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Logística'])} {random.choice(PA_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/cedula.txt", unique_n(gen_cedula_pa))
    write(f"{seed_dir}/ruc.txt", unique_n(gen_ruc_pa))
    write(f"{seed_dir}/codigo_postal.txt", [gen_pa_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_pa_phone() for _ in range(N)])
    print("Panamá: done")

# ─── COLOMBIA ─────────────────────────────────────────────────────────────────

CO_NOMBRES = [
    "Santiago","Sebastián","Camilo","Andrés","Felipe","Juan","Carlos","Daniel","David","Alejandro",
    "Miguel","Sergio","Ricardo","Fernando","Nicolás","Diego","Mauricio","Hernán","Gustavo","Jorge",
    "Valentina","Mariana","Sara","Isabella","Juliana","Daniela","Luisa","Natalia","Alejandra","Claudia",
    "Sofía","Gabriela","Paola","Fernanda","Diana","Catalina","Manuela","Verónica","Adriana","Lorena",
    "Pablo","Álvaro","Mario","Ernesto","Víctor","Óscar","Iván","Rafael","Germán","Luis",
    "Patricia","Sandra","Mónica","Elena","Marcela","Pilar","Rosa","Teresa","Beatriz","Liliana"
]

CO_APELLIDOS = [
    "García","Rodríguez","Martínez","López","González","Pérez","Sánchez","Ramírez","Cruz","Torres",
    "Vargas","Flores","Morales","Jiménez","Reyes","Herrera","Castillo","Ortiz","Ramos","Díaz",
    "Gómez","Moreno","Ruiz","Silva","Muñoz","Álvarez","Romero","Guerrero","Medina","Aguilar",
    "Parra","Ospina","Arias","Suárez","Quintero","Cárdenas","Castro","Gutiérrez","Molina","Salazar",
    "Giraldo","Londoño","Henao","Escobar","Montoya","Vélez","Zapata","Restrepo","Mesa","Bedoya"
]

CO_TIPOS_CALLE = ["Calle","Carrera","Avenida","Diagonal","Transversal","Circular"]

CO_NOMBRES_CALLE = [
    "El Dorado","Las Américas","Boyacá","Séptima","Novena","Décima","Once","Trece","Quince",
    "El Libertador","Simón Bolívar","Santander","Sucre","Nariño","Caldas","Córdoba",
    "El Salitre","La Esperanza","El Restrepo","Kennedy","Bosa","Fontibón","Engativá",
    "Galerías","Chapinero","Usaquén","Suba","Ciudad Jardín","El Poblado","Laureles",
    "El Prado","San Fernando","Belén","Robledo","Manrique","Aranjuez","Santa Cruz",
    "Manga","El Centro","Bocagrande","Castillogrande","El Cabrero","Pie de la Popa",
]

CO_COMPLEMENTOS = [
    "Apto 101","Apto 201","Apto 301","Apto 401","Apto 102","Apto 202","Apto 302",
    "Interior 1","Interior 2","Interior 3","Piso 1","Piso 2","Piso 3",
    "Casa 1","Casa 2","Torre A Apto 1","Torre B Apto 2","Local 1","Local 2",
    "Of. 101","Of. 201","Bodega 1","Bodega 2",
]

CO_CIUDADES_DEPARTAMENTOS = [
    "Bogotá, Cundinamarca","Medellín, Antioquia","Cali, Valle del Cauca",
    "Barranquilla, Atlántico","Cartagena, Bolívar","Cúcuta, Norte de Santander",
    "Soledad, Atlántico","Ibagué, Tolima","Bucaramanga, Santander",
    "Soacha, Cundinamarca","Santa Marta, Magdalena","Villavicencio, Meta",
    "Pereira, Risaralda","Bello, Antioquia","Valledupar, Cesar",
    "Montería, Córdoba","Itagüí, Antioquia","Pasto, Nariño","Manizales, Caldas",
    "Buenaventura, Valle del Cauca","Neiva, Huila","Palmira, Valle del Cauca",
    "Armenia, Quindío","Sincelejo, Sucre","Popayán, Cauca","Floridablanca, Santander",
    "Envigado, Antioquia","Dosquebradas, Risaralda","Riohacha, La Guajira",
    "Quibdó, Chocó","Mocoa, Putumayo","Leticia, Amazonas","Puerto Inírida, Guainía",
]

CO_EMPRESAS_TIPO = ["S.A.S.","S.A.","Ltda.","S.A.S","E.A.T."]
CO_EMPRESAS_NOMES = [
    "Colombia","Nacional","Andina","Cafetera","Pacífica","Atlántica","Bogotana","Antioqueña",
    "Tecnológica","Comercial","Industrial","Constructora","Agrícola","Energética","Financiera",
    "Alpha","Beta","Delta","Global","Digital","Smart","Prime","Elite","Innovadora","Progresiva"
]

def gen_co_cp():
    return f"{random.randint(100000, 999999)}"

def gen_co_phone():
    prefix = random.choice(["300","301","302","303","304","305","310","311","312","313","314","315","316","317","318","319","320","321","322","323","350","360"])
    return f"+57 {prefix} {random.randint(100,999)} {random.randint(1000,9999)}"

def gen_colombia():
    seed_dir = f"{BASE}/countries/colombia/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(CO_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(CO_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(CO_TIPOS_CALLE)} {random.randint(1,150)} {'#' if random.random()>0.3 else 'No.'} {random.randint(1,99)}-{random.randint(1,99)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(CO_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_departamentos.txt", sample_n(CO_CIUDADES_DEPARTAMENTOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(CO_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Construcción','Logística'])} {random.choice(CO_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/cedula_cc.txt", unique_n(gen_cedula_co))
    write(f"{seed_dir}/nit.txt", unique_n(gen_nit_co))
    write(f"{seed_dir}/codigo_postal.txt", [gen_co_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_co_phone() for _ in range(N)])
    print("Colombia: done")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    gen_brasil()
    gen_argentina()
    gen_chile()
    gen_mexico()
    gen_panama()
    gen_colombia()
    print("\nAll seed data generated successfully.")
