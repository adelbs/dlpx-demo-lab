#!/usr/bin/env python3
"""Generate seed data (.txt, 1000 lines each) for all 6 countries."""

import random
import os

import mexico_docs

BASE = "/Users/felipe.jacob/Projects/dlpx-demo-lab"
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
    """CURP válida (estrutura + dígito verificador) de uma pessoa fictícia."""
    nome = random.choice(MX_NOMBRES)
    sexo = "M" if nome in MX_NOMBRES_FEMENINOS else "H"
    nasc = f"{random.randint(1950, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    estado = random.choice(sorted(set(mexico_docs.CURP_ESTADOS.values())))
    return mexico_docs.curp(nome, random.choice(MX_APELLIDOS), random.choice(MX_APELLIDOS),
                            nasc, sexo, estado, random.choice([0, 0, 0, 1]))

def gen_rfc_mx():
    """RFC de persona moral válido (homoclave + dígito verificador) de uma empresa fictícia."""
    razao = (f"{random.choice(MX_EMPRESAS_NOMES)} "
             f"{random.choice(['Tecnología','Servicios','Comercial','Industrial','Construcción','Logística'])} "
             f"{random.choice(MX_EMPRESAS_TIPO)}")
    constituicao = f"{random.randint(1970, 2020)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    return mexico_docs.rfc_moral(razao, constituicao)

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
MX_NOMBRES_FEMENINOS = set(MX_NOMBRES[20:40] + MX_NOMBRES[50:])

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
    write(f"{seed_dir}/rfc.txt", unique_n(gen_rfc_mx))
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

# ─── PERU ─────────────────────────────────────────────────────────────────────

PE_NOMBRES = [
    "José","Carlos","Luis","Juan","Miguel","Jorge","César","Manuel","Víctor","Alberto",
    "Enrique","Raúl","Óscar","Ronald","Jhon","Jefferson","Anthony","Kevin","Bryan","Fernando",
    "María","Rosa","Carmen","Luz","Julia","Yolanda","Gladys","Milagros","Katherine","Yesenia",
    "Xiomara","Diana","Karen","Flor","Nancy","Elizabeth","Patricia","Silvia","Giovanna","Vanessa",
    "Edwin","Elmer","Wilson","Percy","Walter","Segundo","Hernán","Yuri","Alex","Renzo",
]

PE_APELLIDOS = [
    "Quispe","Mamani","Huamán","Flores","Rojas","Vargas","Torres","Sánchez","Ramos","Chávez",
    "Rodríguez","Vásquez","Cruz","Reyes","Gonzales","Fernández","Paredes","Aguilar","Salazar","Medina",
    "Castillo","Espinoza","Núñez","Cárdenas","Guerrero","Palacios","Vega","Ríos","Ochoa","Zapata",
    "Yupanqui","Condori","Apaza","Choque","Ttito","Tovar","Bravo","Carrasco","Del Águila","Puma",
]

PE_TIPOS_CALLE = ["Jirón","Avenida","Avenida","Calle","Pasaje","Malecón"]

PE_NOMBRES_CALLE = [
    "Los Incas","La Marina","Túpac Amaru","Grau","Arequipa","Javier Prado","Angamos","Larco",
    "Pardo","Brasil","Universitaria","De la Cultura","El Sol","Los Próceres","San Martín",
    "Tacna","Junín","Cusco","Ayacucho","Los Girasoles","Las Begonias","Ricardo Palma",
    "Bolognesi","Los Álamos","Las Orquídeas","Manco Cápac","Pachacútec","Simón Bolívar",
]

PE_COMPLEMENTOS = [
    "Dpto 101","Dpto 201","Dpto 301","Dpto 102","Dpto 202","Piso 1","Piso 2","Piso 3",
    "Interior 1","Interior 2","Mz A Lt 5","Mz B Lt 8","Urb. Los Jardines","Casa 1","Casa 2","Local 1",
]

PE_CIUDADES_DEPARTAMENTOS = [
    "Lima, Lima","Arequipa, Arequipa","Trujillo, La Libertad","Chiclayo, Lambayeque",
    "Piura, Piura","Iquitos, Loreto","Cusco, Cusco","Chimbote, Áncash","Huancayo, Junín",
    "Tacna, Tacna","Ica, Ica","Juliaca, Puno","Sullana, Piura","Pucallpa, Ucayali",
    "Cajamarca, Cajamarca","Huánuco, Huánuco","Ayacucho, Ayacucho","Puno, Puno",
    "Tumbes, Tumbes","Chincha Alta, Ica","Huaraz, Áncash","Tarapoto, San Martín",
    "Abancay, Apurímac","Moquegua, Moquegua","Huancavelica, Huancavelica",
]

PE_EMPRESAS_TIPO = ["S.A.C.","S.A.","S.R.L.","E.I.R.L."]
PE_EMPRESAS_NOMES = [
    "Andina","Peruana","Inca","Nacional","Pacífico","Cordillera","Amazónica","Altiplano",
    "Tecnológica","Comercial","Industrial","Constructora","Agrícola","Minera","Alpha","Beta",
    "Global","Digital","Smart","Prime",
]

def gen_dni_pe():
    return str(random.randint(10_000_000, 79_999_999))

def gen_ruc_pe():
    tipo = random.choice(["10", "20"])
    body = f"{tipo}{random.randint(0, 99_999_999):08d}"
    weights = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(body[i]) * weights[i] for i in range(10))
    check = 11 - (total % 11)
    check = 0 if check >= 10 else check
    return f"{body}{check}"

def gen_pe_cp():
    return f"{random.randint(10000, 19999)}"

def gen_pe_phone():
    return f"+51 9{random.randint(10,99)} {random.randint(100,999)} {random.randint(100,999)}"

def gen_peru():
    seed_dir = f"{BASE}/countries/peru/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(PE_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(PE_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(PE_TIPOS_CALLE)} {random.choice(PE_NOMBRES_CALLE)} {random.randint(1, 2999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(PE_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_departamentos.txt", sample_n(PE_CIUDADES_DEPARTAMENTOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(PE_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Minería','Agrícola'])} {random.choice(PE_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/dni.txt", unique_n(gen_dni_pe))
    write(f"{seed_dir}/ruc.txt", unique_n(gen_ruc_pe))
    write(f"{seed_dir}/codigo_postal.txt", [gen_pe_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_pe_phone() for _ in range(N)])
    print("Perú: done")

# ─── PARAGUAY ─────────────────────────────────────────────────────────────────

PY_NOMBRES = [
    "José","Juan","Carlos","Diego","Ramón","Pedro","Fabián","Rodrigo","Óscar","Derlis",
    "Cristian","Gustavo","Marcelo","Hugo","Nelson","Arnaldo","Rubén","Vicente","Blas","Aníbal",
    "María","Rosa","Gloria","Liz","Nancy","Cynthia","Zunilda","Celeste","Lourdes","Fátima",
    "Rocío","Sara","Mirna","Perla","Nilda","Ramona","Sonia","Yenny","Belén","Selva",
]

PY_APELLIDOS = [
    "González","Benítez","Cáceres","Fernández","García","Rodríguez","Duarte","Ortiz","Ayala","Espínola",
    "Mendoza","Vera","Villalba","Franco","Ramírez","Insfrán","Aquino","Ovelar","Riveros","Sosa",
    "Acosta","Gómez","Zárate","Sánchez","Ferreira","Cabral","Chamorro","Recalde","Bogado","Núñez",
]

PY_TIPOS_CALLE = ["Calle","Avenida","Avenida","Mariscal"]

PY_NOMBRES_CALLE = [
    "Palma","Mariscal López","Eusebio Ayala","España","Brasil","Aviadores del Chaco",
    "Perú","San Martín","Constitución","Colón","Yegros","Cerro Corá","Independencia Nacional",
    "25 de Mayo","14 de Mayo","Artigas","Choferes del Chaco","General Santos","Molas López",
]

PY_COMPLEMENTOS = [
    "Casa 1","Casa 2","Dpto 1","Dpto 2","Piso 1","Piso 2","Local 1","Local 2",
    "Barrio Obrero","Barrio San Roque","Km 5","Km 12",
]

PY_CIUDADES_DEPARTAMENTOS = [
    "Asunción, Central","Ciudad del Este, Alto Paraná","Encarnación, Itapúa",
    "Luque, Central","San Lorenzo, Central","Capiatá, Central","Lambaré, Central",
    "Fernando de la Mora, Central","Limpio, Central","Ñemby, Central","Pedro Juan Caballero, Amambay",
    "Coronel Oviedo, Caaguazú","Villarrica, Guairá","Caacupé, Cordillera",
    "Concepción, Concepción","Pilar, Ñeembucú","Caazapá, Caazapá","Salto del Guairá, Canindeyú",
]

PY_EMPRESAS_TIPO = ["S.A.","S.R.L.","E.A.S."]
PY_EMPRESAS_NOMES = [
    "Guaraní","Paraguaya","Del Este","Central","Nacional","Ñandutí","Itapúa","Pantanal",
    "Tecnológica","Comercial","Industrial","Agropecuaria","Alpha","Global","Digital","Prime",
]

def gen_ci_py():
    return str(random.randint(1_000_000, 6_999_999))

def gen_ruc_py():
    n = random.randint(80_000_000, 89_999_999)
    weights = [2, 3, 4, 5, 6, 7, 2, 3]
    digits = [int(c) for c in str(n)]
    total = sum(d * w for d, w in zip(reversed(digits), weights))
    dv = 11 - (total % 11)
    dv = 0 if dv >= 10 else dv
    return f"{n}-{dv}"

def gen_py_cp():
    return f"{random.randint(1000, 9999)}"

def gen_py_phone():
    return f"+595 9{random.randint(70,99)} {random.randint(100,999)} {random.randint(100,999)}"

def gen_paraguay():
    seed_dir = f"{BASE}/countries/paraguay/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(PY_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(PY_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(PY_TIPOS_CALLE)} {random.choice(PY_NOMBRES_CALLE)} {random.randint(1, 2999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(PY_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_departamentos.txt", sample_n(PY_CIUDADES_DEPARTAMENTOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(PY_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Agropecuaria'])} {random.choice(PY_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/ci.txt", unique_n(gen_ci_py))
    write(f"{seed_dir}/ruc.txt", unique_n(gen_ruc_py))
    write(f"{seed_dir}/codigo_postal.txt", [gen_py_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_py_phone() for _ in range(N)])
    print("Paraguay: done")

# ─── URUGUAY ──────────────────────────────────────────────────────────────────

UY_NOMBRES = [
    "Mateo","Bruno","Franco","Nicolás","Federico","Diego","Rodrigo","Álvaro","Gonzalo","Emiliano",
    "Fabián","Gastón","Ignacio","Joaquín","Leonel","Marcelo","Rafael","Sebastián","Tabaré","Walter",
    "Lucía","Valentina","Camila","Florencia","Agustina","Belén","Cecilia","Daiana","Estefanía","Gimena",
    "Ivana","Julieta","Karina","Lorena","Micaela","Noelia","Paola","Romina","Silvana","Yamila",
]

UY_APELLIDOS = [
    "Rodríguez","González","Fernández","Pérez","Suárez","Martínez","Sosa","Romero","Silva","Pereira",
    "Rivero","Correa","Ramos","Cabrera","Acosta","Da Silva","Ferreira","Gómez","Machado","Olivera",
    "Bentancur","Umpiérrez","Etcheverry","Castro","Núñez","Techera","Píriz","Alonso","Larrosa","Camejo",
]

UY_TIPOS_CALLE = ["Calle","Avenida","Bulevar","Rambla"]

UY_NOMBRES_CALLE = [
    "18 de Julio","Rambla República de México","Bulevar Artigas","Colonia","Rivera",
    "Constituyente","Agraciada","Millán","Propios","8 de Octubre","Larrañaga","Garzón",
    "Comercio","Sarandí","25 de Agosto","Yi","San José","Andes","Convención","Ejido",
]

UY_COMPLEMENTOS = [
    "Apto 101","Apto 201","Apto 301","Piso 1","Piso 2","Local 1","Local 2",
    "Casa","Solar 1","Solar 2","Fondo",
]

UY_CIUDADES_DEPARTAMENTOS = [
    "Montevideo, Montevideo","Salto, Salto","Paysandú, Paysandú","Las Piedras, Canelones",
    "Rivera, Rivera","Maldonado, Maldonado","Tacuarembó, Tacuarembó","Melo, Cerro Largo",
    "Mercedes, Soriano","Artigas, Artigas","Minas, Lavalleja","San José de Mayo, San José",
    "Durazno, Durazno","Florida, Florida","Treinta y Tres, Treinta y Tres","Rocha, Rocha",
    "Fray Bentos, Río Negro","Colonia del Sacramento, Colonia","Trinidad, Flores","Canelones, Canelones",
]

UY_EMPRESAS_TIPO = ["S.A.","S.R.L.","Ltda."]
UY_EMPRESAS_NOMES = [
    "Oriental","Charrúa","Rioplatense","Uruguaya","Nacional","Costa","Pampero","Austral",
    "Tecnológica","Comercial","Industrial","Agropecuaria","Alpha","Global","Digital","Prime",
]

def gen_ci_uy():
    n = random.randint(1_000_000, 5_999_999)
    s = f"{n:07d}"
    weights = [2, 9, 8, 7, 6, 3, 4]
    total = sum(int(s[i]) * weights[i] for i in range(7))
    dv = (10 - (total % 10)) % 10
    return f"{s[0]}.{s[1:4]}.{s[4:7]}-{dv}"

def gen_rut_uy():
    return f"21{random.randint(100000,999999)}{random.randint(0,9)}018"

def gen_uy_cp():
    return f"{random.randint(10000, 99999)}"

def gen_uy_phone():
    return f"+598 9{random.randint(1,9)} {random.randint(100,999)} {random.randint(100,999)}"

def gen_uruguay():
    seed_dir = f"{BASE}/countries/uruguay/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(UY_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(UY_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(UY_TIPOS_CALLE)} {random.choice(UY_NOMBRES_CALLE)} {random.randint(1, 2999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(UY_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_departamentos.txt", sample_n(UY_CIUDADES_DEPARTAMENTOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(UY_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Agropecuaria'])} {random.choice(UY_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/ci.txt", unique_n(gen_ci_uy))
    write(f"{seed_dir}/rut.txt", unique_n(gen_rut_uy))
    write(f"{seed_dir}/codigo_postal.txt", [gen_uy_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_uy_phone() for _ in range(N)])
    print("Uruguay: done")

# ─── ECUADOR ──────────────────────────────────────────────────────────────────

EC_NOMBRES = [
    "Carlos","Luis","José","Juan","Miguel","Andrés","Diego","Fernando","Xavier","Iván",
    "Wilson","Byron","Christian","Edison","Franklin","Marlon","Patricio","Ramiro","Vinicio","Wladimir",
    "María","Rosa","Carmen","Gladys","Mónica","Verónica","Janeth","Karina","Lorena","Diana",
    "Fabiola","Gabriela","Jenny","Katty","Mayra","Nancy","Paulina","Silvia","Tatiana","Ximena",
]

EC_APELLIDOS = [
    "Vera","Vélez","Cedeño","Zambrano","Loor","Mendoza","Alcívar","Macías","Bravo","Delgado",
    "Sánchez","Rodríguez","Pérez","Suárez","Vargas","Chávez","Torres","Andrade","Villacís","Ortega",
    "Guamán","Chuquimarca","Sisalima","Cajamarca","Quinatoa","Toapanta","Yépez","Salazar","Naranjo","Rea",
]

EC_TIPOS_CALLE = ["Calle","Avenida","Avenida","Pasaje"]

EC_NOMBRES_CALLE = [
    "Amazonas","10 de Agosto","6 de Diciembre","9 de Octubre","Naciones Unidas","Shyris",
    "República","Colón","Patria","Malecón Simón Bolívar","Portete","García Moreno",
    "Rocafuerte","Bolívar","Sucre","Guayas","Kennedy","Los Ceibos","Urdesa Central","Kennedy Norte",
]

EC_COMPLEMENTOS = [
    "Depto 101","Depto 201","Piso 1","Piso 2","Ciudadela Norte","Ciudadela Sur",
    "Conjunto Los Álamos","Casa 1","Casa 2","Local 1","Mz 5 Villa 12",
]

EC_CIUDADES_PROVINCIAS = [
    "Quito, Pichincha","Guayaquil, Guayas","Cuenca, Azuay","Santo Domingo, Santo Domingo de los Tsáchilas",
    "Machala, El Oro","Durán, Guayas","Manta, Manabí","Portoviejo, Manabí","Loja, Loja",
    "Ambato, Tungurahua","Riobamba, Chimborazo","Esmeraldas, Esmeraldas","Quevedo, Los Ríos",
    "Ibarra, Imbabura","Milagro, Guayas","Latacunga, Cotopaxi","Tulcán, Carchi","Babahoyo, Los Ríos",
    "Nueva Loja, Sucumbíos","Puyo, Pastaza",
]

EC_EMPRESAS_TIPO = ["S.A.","Cía. Ltda.","S.A.S."]
EC_EMPRESAS_NOMES = [
    "Andina","Ecuatoriana","Pacífico","Amazónica","Nacional","Sierra","Costa","Austral",
    "Tecnológica","Comercial","Industrial","Agrícola","Alpha","Global","Digital","Prime",
]

def gen_cedula_ec():
    prov = random.randint(1, 24)
    resto = random.randint(0, 9999999)
    body = f"{prov:02d}{resto:07d}"[:9]
    weights = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for i, ch in enumerate(body):
        d = int(ch) * weights[i]
        if d > 9:
            d -= 9
        total += d
    dv = (10 - (total % 10)) % 10
    return f"{body}{dv}"

def gen_ruc_ec():
    return f"{gen_cedula_ec()}001"

def gen_ec_cp():
    return f"{random.randint(100000, 999999)}"

def gen_ec_phone():
    return f"+593 9{random.randint(10,99)} {random.randint(100,999)} {random.randint(1000,9999)}"

def gen_ecuador():
    seed_dir = f"{BASE}/countries/ecuador/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(EC_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(EC_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(EC_TIPOS_CALLE)} {random.choice(EC_NOMBRES_CALLE)} {random.randint(1, 2999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(EC_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_provincias.txt", sample_n(EC_CIUDADES_PROVINCIAS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(EC_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Agrícola'])} {random.choice(EC_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/cedula.txt", unique_n(gen_cedula_ec))
    write(f"{seed_dir}/ruc.txt", unique_n(gen_ruc_ec))
    write(f"{seed_dir}/codigo_postal.txt", [gen_ec_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_ec_phone() for _ in range(N)])
    print("Ecuador: done")

# ─── BOLIVIA ──────────────────────────────────────────────────────────────────

BO_NOMBRES = [
    "Juan","Carlos","José","Luis","Miguel","Freddy","Gonzalo","Édgar","Wilson","Fernando",
    "Ronald","Marco","Álvaro","Rubén","Erick","Iván","Óscar","Raúl","Sergio","Vladimir",
    "María","Rosa","Carmen","Elizabeth","Gladys","Verónica","Lourdes","Jhanet","Nelly","Beatriz",
    "Fabiola","Gabriela","Karina","Lidia","Mónica","Nancy","Patricia","Silvia","Teresa","Zulma",
]

BO_APELLIDOS = [
    "Mamani","Quispe","Choque","Condori","Flores","Vargas","Rodríguez","Fernández","Gutiérrez","Torrez",
    "Rojas","Colque","Apaza","Chura","Calle","Ticona","Villca","Copa","Callisaya","Mollo",
    "Guzmán","Terrazas","Justiniano","Áñez","Suárez","Roca","Peña","Vaca","Zapata","Salvatierra",
]

BO_TIPOS_CALLE = ["Calle","Avenida","Avenida"]

BO_NOMBRES_CALLE = [
    "Illimani","Murillo","Mariscal Santa Cruz","Camacho","Ballivián","Arce","Ecuador",
    "Villazón","6 de Agosto","20 de Octubre","Busch","América","Heroínas","Aroma",
    "Sucre","Bolívar","Litoral","Beni","Cochabamba","Potosí",
]

BO_COMPLEMENTOS = [
    "Depto 1","Depto 2","Piso 1","Piso 2","Zona Norte","Zona Sur",
    "Casa 1","Casa 2","Edificio Central","Local 1",
]

BO_CIUDADES_DEPARTAMENTOS = [
    "La Paz, La Paz","Santa Cruz de la Sierra, Santa Cruz","Cochabamba, Cochabamba",
    "Sucre, Chuquisaca","Oruro, Oruro","Tarija, Tarija","Potosí, Potosí",
    "El Alto, La Paz","Trinidad, Beni","Cobija, Pando","Montero, Santa Cruz",
    "Quillacollo, Cochabamba","Yacuiba, Tarija","Riberalta, Beni","Warnes, Santa Cruz",
    "Villazón, Potosí","Camiri, Santa Cruz","Llallagua, Potosí","Tupiza, Potosí","Sacaba, Cochabamba",
]

BO_EMPRESAS_TIPO = ["S.A.","S.R.L.","Ltda."]
BO_EMPRESAS_NOMES = [
    "Andina","Boliviana","Illimani","Altiplano","Nacional","Amazónica","Kollasuyo","Oriental",
    "Tecnológica","Comercial","Industrial","Minera","Alpha","Global","Digital","Prime",
]

BO_EXT = ["LP", "CB", "SC", "OR", "PT", "CH", "TJ", "BE", "PD"]

def gen_ci_bo():
    n = random.randint(1_000_000, 9_999_999)
    return f"{n} {random.choice(BO_EXT)}"

def gen_nit_bo():
    return str(random.randint(1_000_000_010, 9_999_999_999))

def gen_bo_cp():
    return f"{random.randint(1000, 9999)}"

def gen_bo_phone():
    return f"+591 {random.choice(['6','7'])}{random.randint(1000000,9999999)}"

def gen_bolivia():
    seed_dir = f"{BASE}/countries/bolivia/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(BO_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(BO_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(BO_TIPOS_CALLE)} {random.choice(BO_NOMBRES_CALLE)} {random.randint(1, 2999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(BO_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_departamentos.txt", sample_n(BO_CIUDADES_DEPARTAMENTOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(BO_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Minería'])} {random.choice(BO_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/ci.txt", unique_n(gen_ci_bo))
    write(f"{seed_dir}/nit.txt", unique_n(gen_nit_bo))
    write(f"{seed_dir}/codigo_postal.txt", [gen_bo_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_bo_phone() for _ in range(N)])
    print("Bolivia: done")

# ─── VENEZUELA ────────────────────────────────────────────────────────────────

VE_NOMBRES = [
    "José","Juan","Carlos","Luis","Miguel","Jesús","Ángel","Franklin","Yorman","Yeison",
    "Wilmer","Deivis","Yonathan","Yosmar","Eduardo","Rafael","Alexis","Gabriel","Ricardo","Simón",
    "María","Carmen","Rosa","Yajaira","Yolimar","Yusmary","Deisy","Génesis","Oriana","Rosmery",
    "Carla","Diana","Elizabeth","Fabiana","Gabriela","Karina","Lorena","Mariangel","Nairobis","Patricia",
]

VE_APELLIDOS = [
    "Rodríguez","González","Hernández","López","Martínez","Pérez","García","Rojas","Sánchez","Ramírez",
    "Torres","Flores","Rivas","Silva","Suárez","Blanco","Colmenares","Marcano","Guerra","Contreras",
    "Escalona","Fuenmayor","Marín","Bastidas","Chirinos","Fajardo","Uzcátegui","Vielma","Zambrano","Peña",
]

VE_TIPOS_CALLE = ["Calle","Avenida","Avenida","Carrera"]

VE_NOMBRES_CALLE = [
    "Bolívar","Francisco de Miranda","Urdaneta","Sucre","Libertador","Andrés Bello",
    "Los Próceres","Fuerzas Armadas","San Martín","Baralt","Las Delicias","Los Ilustres",
    "El Paraíso","La Paz","Las Acacias","Los Cortijos","La Candelaria","5 de Julio",
]

VE_COMPLEMENTOS = [
    "Edif. Los Robles Piso 2","Edif. Miranda Piso 3","Res. La Trinidad","Res. Los Chaguaramos",
    "Apto 1","Apto 2","Casa 1","Casa 2","Local 1","Urb. El Bosque",
]

VE_CIUDADES_ESTADOS = [
    "Caracas, Distrito Capital","Maracaibo, Zulia","Valencia, Carabobo","Barquisimeto, Lara",
    "Maracay, Aragua","Ciudad Guayana, Bolívar","San Cristóbal, Táchira","Maturín, Monagas",
    "Barcelona, Anzoátegui","Mérida, Mérida","Cabimas, Zulia","Turmero, Aragua",
    "Cumaná, Sucre","Barinas, Barinas","Puerto La Cruz, Anzoátegui","Guarenas, Miranda",
    "Los Teques, Miranda","Punto Fijo, Falcón","Guanare, Portuguesa","Coro, Falcón",
]

VE_EMPRESAS_TIPO = ["C.A.","S.A.","S.R.L."]
VE_EMPRESAS_NOMES = [
    "Andina","Venezolana","Caribe","Llanera","Nacional","Bolivariana","Guayanesa","Oriental",
    "Tecnológica","Comercial","Industrial","Petrolera","Alpha","Global","Digital","Prime",
]

def gen_cedula_ve():
    return f"V-{random.randint(5_000_000, 29_999_999)}"

def gen_rif_ve():
    n = random.randint(10_000_000, 99_999_999)
    return f"J-{n}-{random.randint(0,9)}"

def gen_ve_cp():
    return f"{random.randint(1000, 9999)}"

def gen_ve_phone():
    area = random.choice(["0412","0414","0416","0424","0426"])
    return f"{area}-{random.randint(1000000,9999999)}"

def gen_venezuela():
    seed_dir = f"{BASE}/countries/venezuela/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(VE_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(VE_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(VE_TIPOS_CALLE)} {random.choice(VE_NOMBRES_CALLE)} {random.randint(1, 2999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(VE_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_estados.txt", sample_n(VE_CIUDADES_ESTADOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(VE_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Petrolera'])} {random.choice(VE_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/cedula.txt", unique_n(gen_cedula_ve))
    write(f"{seed_dir}/rif.txt", unique_n(gen_rif_ve))
    write(f"{seed_dir}/codigo_postal.txt", [gen_ve_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_ve_phone() for _ in range(N)])
    print("Venezuela: done")

# ─── COSTA RICA ───────────────────────────────────────────────────────────────

CR_NOMBRES = [
    "José","Carlos","Luis","Juan","Miguel","Andrés","Diego","Fernando","Esteban","Kevin",
    "Randall","Jeffry","Warner","Mainor","Minor","Jafeth","Alonso","Gerardo","Ricardo","Óscar",
    "María","Ana","Carmen","Rosa","Marlen","Yorleny","Xinia","Kattia","Grettel","Shirley",
    "Diana","Fabiola","Gabriela","Karla","Lorena","Mónica","Natalia","Patricia","Silvia","Vanessa",
]

CR_APELLIDOS = [
    "Rodríguez","González","Hernández","Jiménez","Mora","Vargas","Castro","Chacón","Solano","Araya",
    "Rojas","Sánchez","Ramírez","Fernández","Alvarado","Zúñiga","Salas","Elizondo","Quesada","Barrantes",
    "Cordero","Villalobos","Segura","Ureña","Brenes","Campos","Madrigal","Monge","Navarro","Pérez",
]

CR_TIPOS_CALLE = ["Calle","Avenida","Barrio"]

CR_NOMBRES_CALLE = [
    "Central","Los Yoses","La Sabana","Escazú Centro","San Pedro","Rohrmoser","Curridabat",
    "Paseo Colón","Amón","Otoya","La California","Sabanilla","Guadalupe Centro","Moravia Centro",
    "Tibás Centro","Barrio México","Barrio Escalante","Los Ángeles","Del Mall","Del Parque",
]

CR_COMPLEMENTOS = [
    "100 mts norte de la iglesia","200 mts sur del parque","Casa 1","Casa 2",
    "Apto 101","Apto 201","Contiguo a la escuela","Frente al supermercado","Local 1","Local 2",
]

CR_CIUDADES_PROVINCIAS = [
    "San José, San José","Alajuela, Alajuela","Cartago, Cartago","Heredia, Heredia",
    "Liberia, Guanacaste","Puntarenas, Puntarenas","Limón, Limón","Desamparados, San José",
    "San Francisco, Heredia","Curridabat, San José","Escazú, San José","Tibás, San José",
    "Turrialba, Cartago","Grecia, Alajuela","San Carlos, Alajuela","Pérez Zeledón, San José",
    "Nicoya, Guanacaste","Santa Cruz, Guanacaste","Golfito, Puntarenas","Guápiles, Limón",
]

CR_EMPRESAS_TIPO = ["S.A.","Sociedad de Responsabilidad Limitada","Ltda."]
CR_EMPRESAS_NOMES = [
    "Tica","Costarricense","Central","Pacífica","Caribeña","Nacional","Volcánica","Tropical",
    "Tecnológica","Comercial","Industrial","Agrícola","Alpha","Global","Digital","Prime",
]

def gen_cedula_cr():
    return f"{random.randint(1,9)}-{random.randint(0,999):04d}-{random.randint(0,9999):04d}"

def gen_cedula_juridica_cr():
    return f"3-101-{random.randint(100000,999999)}"

def gen_cr_cp():
    return f"{random.randint(10000, 99999)}"

def gen_cr_phone():
    return f"+506 {random.choice(['6','7','8'])}{random.randint(100,999)}-{random.randint(1000,9999)}"

def gen_costa_rica():
    seed_dir = f"{BASE}/countries/costa_rica/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(CR_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(CR_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(CR_TIPOS_CALLE)} {random.choice(CR_NOMBRES_CALLE)} {random.randint(1, 999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(CR_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_provincias.txt", sample_n(CR_CIUDADES_PROVINCIAS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(CR_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Agrícola'])} {random.choice(CR_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/cedula.txt", unique_n(gen_cedula_cr))
    write(f"{seed_dir}/cedula_juridica.txt", unique_n(gen_cedula_juridica_cr))
    write(f"{seed_dir}/codigo_postal.txt", [gen_cr_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_cr_phone() for _ in range(N)])
    print("Costa Rica: done")

# ─── BELIZE ───────────────────────────────────────────────────────────────────
# Belize is officially English-speaking, but ~30% of the population is Spanish-speaking
# Mestizo, plus Garifuna and Maya communities. Seed names reflect that mix; the table
# schema stays Spanish-language for consistency with the rest of the generation pipeline.

BZ_NOMBRES = [
    "John","Michael","David","James","Robert","William","Andrew","Kevin","Marlon","Shane",
    "Carlos","Luis","José","Pedro","Miguel","Antonio","Marvin","Elroy","Ruben","Iván",
    "Mary","Patricia","Linda","Barbara","Susan","Jennifer","Michelle","Sandra","Yvette","Dorla",
    "María","Rosa","Carmen","Ana","Elena","Isabel","Yolanda","Sharon","Kim","Andrea",
]

BZ_APELLIDOS = [
    "Flowers","Young","Gentle","Usher","Reneau","Neal","Longsworth","Andrewin","Palacio","Nuñez",
    "Gonzalez","Perez","Cruz","Mendez","Novelo","Requena","Guerra","Escalante","Pott","Ellis",
    "Arana","Alamina","Sanchez","Coleman","Bood","Castillo","Vasquez","Zabaneh","Belisle","Anderson",
]

BZ_TIPOS_CALLE = ["Calle","Street","Avenue"]

BZ_NOMBRES_CALLE = [
    "Albert Street","Regent Street","Queen Street","Freetown Road","Central American Boulevard",
    "Vernon Street","North Front Street","Cemetery Road","Baymen Avenue","Hummingbird Highway",
    "Chetumal Street","Bella Vista","Coney Drive","Kelly Street","St. Thomas Street",
    "Independence Avenue","Prince Street","Fabers Road","Faber's Village","George Price Highway",
]

BZ_COMPLEMENTOS = [
    "Apt 1","Apt 2","Unit 1","Unit 2","Lot 5","Lot 12","Back Street",
    "Near the market","Yarborough Area","Kings Park",
]

BZ_CIUDADES_DISTRITOS = [
    "Belize City, Belize","Belmopan, Cayo","San Ignacio, Cayo","Orange Walk Town, Orange Walk",
    "Corozal Town, Corozal","Dangriga, Stann Creek","Punta Gorda, Toledo","San Pedro, Belize",
    "Benque Viejo del Carmen, Cayo","Santa Elena, Cayo","Ladyville, Belize","Hattieville, Belize",
    "Independence, Stann Creek","Placencia, Stann Creek","Punta Gorda Town, Toledo",
]

BZ_EMPRESAS_TIPO = ["Ltd.","Limited","Co."]
BZ_EMPRESAS_NOMES = [
    "Belize","Caribbean","Reef","Cayo","Tropical","National","Maya","Baymen",
    "Technology","Trading","Import & Export","Agro","Alpha","Global","Digital","Prime",
]

def gen_ssn_bz():
    return f"{random.randint(100,999)}-{random.randint(10,99)}-{random.randint(1000,9999)}"

def gen_tin_bz():
    return f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}"

def gen_bz_cp():
    return f"{random.randint(1000, 9999)}"

def gen_bz_phone():
    return f"+501 {random.choice(['6','2','3','7'])}{random.randint(10,99)}-{random.randint(1000,9999)}"

def gen_belize():
    seed_dir = f"{BASE}/countries/belize/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(BZ_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(BZ_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.randint(1, 199)} {random.choice(BZ_NOMBRES_CALLE)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(BZ_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_distritos.txt", sample_n(BZ_CIUDADES_DISTRITOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(BZ_EMPRESAS_NOMES)} {random.choice(['Technology','Services','Trading','Import & Export','Agro'])} {random.choice(BZ_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/ssn.txt", unique_n(gen_ssn_bz))
    write(f"{seed_dir}/tin.txt", unique_n(gen_tin_bz))
    write(f"{seed_dir}/codigo_postal.txt", [gen_bz_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_bz_phone() for _ in range(N)])
    print("Belize: done")

# ─── EL SALVADOR ──────────────────────────────────────────────────────────────

SV_NOMBRES = [
    "José","Carlos","Luis","Juan","Miguel","Óscar","Ricardo","Mauricio","Roberto","Douglas",
    "Wilfredo","Nelson","Salvador","Rodrigo","Ernesto","Edwin","Vladimir","Balmore","Elmer","Marvin",
    "María","Ana","Carmen","Rosa","Xiomara","Ondina","Marisol","Reina","Yesenia","Kenia",
    "Diana","Fabiola","Gabriela","Karla","Lorena","Mónica","Natalia","Patricia","Silvia","Vanessa",
]

SV_APELLIDOS = [
    "Hernández","García","Martínez","López","González","Rodríguez","Pérez","Sánchez","Ramírez","Cruz",
    "Flores","Gómez","Rivas","Ortiz","Mejía","Alvarado","Ayala","Chávez","Guevara","Escobar",
    "Menjívar","Amaya","Portillo","Cortez","Argueta","Pineda","Rauda","Serrano","Vásquez","Zelaya",
]

SV_TIPOS_CALLE = ["Calle","Avenida","Avenida","Pasaje","Colonia"]

SV_NOMBRES_CALLE = [
    "Roosevelt","Rubén Darío","Cuscatlán","Masferrer","Independencia","Los Héroes",
    "El Progreso","San Antonio Abad","Juan Pablo II","Bulevar del Ejército","Sur",
    "Bulevar de Los Próceres","Arce","Delgado","Concepción","Morazán","Escalón","Miramonte",
]

SV_COMPLEMENTOS = [
    "Casa 1","Casa 2","Apto 101","Apto 201","Local 1","Local 2",
    "Residencial Las Flores","Colonia Escalón","Contiguo a la escuela","Frente al parque",
]

SV_CIUDADES_DEPARTAMENTOS = [
    "San Salvador, San Salvador","Santa Ana, Santa Ana","San Miguel, San Miguel",
    "Soyapango, San Salvador","Mejicanos, San Salvador","Santa Tecla, La Libertad",
    "Apopa, San Salvador","Delgado, San Salvador","Sonsonate, Sonsonate","Ahuachapán, Ahuachapán",
    "Usulután, Usulután","San Vicente, San Vicente","La Unión, La Unión","Zacatecoluca, La Paz",
    "Cojutepeque, Cuscatlán","Chalatenango, Chalatenango","Sensuntepeque, Cabañas","Ilobasco, Cabañas",
    "Nueva San Salvador, La Libertad","Metapán, Santa Ana",
]

SV_EMPRESAS_TIPO = ["S.A. de C.V.","S.A."]
SV_EMPRESAS_NOMES = [
    "Cuscatleca","Salvadoreña","Centroamericana","Nacional","Pacífica","Volcánica","Azul",
    "Tecnológica","Comercial","Industrial","Agrícola","Alpha","Global","Digital","Prime",
]

def gen_dui_sv():
    n = random.randint(10_000_000, 99_999_999)
    return f"{n}-{random.randint(0,9)}"

def gen_nit_sv():
    return f"{random.randint(1000,9999)}-{random.randint(100000,999999)}-{random.randint(100,999)}-{random.randint(0,9)}"

def gen_sv_cp():
    return f"{random.randint(1000, 9999)}"

def gen_sv_phone():
    return f"+503 {random.choice(['6','7'])}{random.randint(100,999)}-{random.randint(1000,9999)}"

def gen_el_salvador():
    seed_dir = f"{BASE}/countries/el_salvador/seed"
    write(f"{seed_dir}/nombres.txt", sample_n(SV_NOMBRES))
    write(f"{seed_dir}/apellidos.txt", sample_n(SV_APELLIDOS))
    write(f"{seed_dir}/direcciones_linea1.txt",
          [f"{random.choice(SV_TIPOS_CALLE)} {random.choice(SV_NOMBRES_CALLE)} {random.randint(1, 999)}" for _ in range(N)])
    write(f"{seed_dir}/direcciones_linea2.txt", sample_n(SV_COMPLEMENTOS))
    write(f"{seed_dir}/ciudades_departamentos.txt", sample_n(SV_CIUDADES_DEPARTAMENTOS))
    write(f"{seed_dir}/empresas.txt",
          [f"{random.choice(SV_EMPRESAS_NOMES)} {random.choice(['Tecnología','Servicios','Comercial','Industrial','Agrícola'])} {random.choice(SV_EMPRESAS_TIPO)}" for _ in range(N)])
    write(f"{seed_dir}/dui.txt", unique_n(gen_dui_sv))
    write(f"{seed_dir}/nit.txt", unique_n(gen_nit_sv))
    write(f"{seed_dir}/codigo_postal.txt", [gen_sv_cp() for _ in range(N)])
    write(f"{seed_dir}/telefonos.txt", [gen_sv_phone() for _ in range(N)])
    print("El Salvador: done")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    gen_brasil()
    gen_argentina()
    gen_chile()
    gen_mexico()
    gen_panama()
    gen_colombia()
    gen_peru()
    gen_paraguay()
    gen_uruguay()
    gen_ecuador()
    gen_bolivia()
    gen_venezuela()
    gen_costa_rica()
    gen_belize()
    gen_el_salvador()
    print("\nAll seed data generated successfully.")
