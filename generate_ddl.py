#!/usr/bin/env python3
"""
Generate DDL + INSERT scripts for 15 countries x 4 database engines.
12 tables per country, related to each other by value (no physical FKs).
"""

import random
import os
import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
random.seed(99)

# ─── LOAD SEED DATA ───────────────────────────────────────────────────────────

def load(country, filename):
    path = f"{BASE}/countries/{country}/seed/{filename}"
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

def rd(lst):
    return random.choice(lst)

def ri(a, b):
    return random.randint(a, b)

def rdate(y1=1950, y2=2005):
    return datetime.date(ri(y1, y2), ri(1, 12), ri(1, 28)).isoformat()

def rdt(y1=2020, y2=2024):
    return f"{datetime.date(ri(y1, y2), ri(1, 12), ri(1, 28)).isoformat()} {ri(0,23):02d}:{ri(0,59):02d}:{ri(0,59):02d}"

def rcard():
    return f"{ri(4000,5999)}-{ri(1000,9999)}-{ri(1000,9999)}-{ri(1000,9999)}"

def rbankacct():
    return f"{ri(10000,99999)}-{ri(1,9)}"

def remail(nome, sobrenome):
    domains = ["gmail.com","hotmail.com","yahoo.com","outlook.com","icloud.com"]
    n = nome.lower().replace(" ","").replace("ã","a").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace("ç","c")
    s = sobrenome.lower().replace(" ","").replace("ã","a").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace("ç","c")
    return f"{n}.{s}{ri(1,999)}@{rd(domains)}"

def rip():
    return f"{ri(1,254)}.{ri(0,255)}.{ri(0,255)}.{ri(1,254)}"

def ramount(lo=10, hi=50000):
    return round(random.uniform(lo, hi), 2)

GENEROS_PT = ["M","F","M","F","M","F","M","F","Outro"]
GENEROS_ES = ["M","F","M","F","M","F","M","F","Otro"]

ESTADOS_CIVIL_PT = ["Solteiro","Casado","Divorciado","Viúvo","União Estável"]
ESTADOS_CIVIL_ES = ["Soltero","Casado","Divorciado","Viudo","Unión Libre"]

TIPOS_CONTA_PT = ["Corrente","Poupança","Salário","Investimento"]
TIPOS_CONTA_ES = ["Corriente","Ahorro","Nómina","Inversión"]

BANDEIRAS = ["Visa","Mastercard","Elo","American Express","Hipercard"]
REDES_ES = ["Visa","Mastercard","American Express","Diners Club"]

STATUS_GERAL = ["Ativo","Inativo","Pendente","Bloqueado"]
STATUS_ES = ["Activo","Inactivo","Pendiente","Bloqueado"]

TIPOS_SEGURO_PT = ["Vida","Saúde","Auto","Residencial","Empresarial","Viagem"]
TIPOS_SEGURO_ES = ["Vida","Salud","Auto","Hogar","Empresarial","Viaje"]

CARGOS_PT = ["Analista","Gerente","Diretor","Coordenador","Supervisor","Auxiliar","Assistente","Especialista","Consultor","Estagiário"]
CARGOS_ES = ["Analista","Gerente","Director","Coordinador","Supervisor","Auxiliar","Asistente","Especialista","Consultor","Practicante"]

DEPARTS = ["TI","Financeiro","RH","Comercial","Operações","Jurídico","Marketing","Logística","Compras","Produção"]
DEPARTS_ES = ["TI","Finanzas","RRHH","Comercial","Operaciones","Legal","Marketing","Logística","Compras","Producción"]

DIAGNOSTICOS_PT = ["Hipertensão","Diabetes tipo 2","Asma","Rinite alérgica","Depressão","Ansiedade","Lombalgia","Migrânea","Gastrite","Hipotireoidismo"]
DIAGNOSTICOS_ES = ["Hipertensión","Diabetes tipo 2","Asma","Rinitis alérgica","Depresión","Ansiedad","Lumbalgia","Migraña","Gastritis","Hipotiroidismo"]

MEDICAMENTOS_PT = ["Losartana 50mg","Metformina 500mg","Salbutamol spray","Loratadina 10mg","Fluoxetina 20mg","Alprazolam 0.5mg","Diclofenaco 50mg","Sumatriptano 50mg","Omeprazol 20mg","Levotiroxina 50mcg"]
MEDICAMENTOS_ES = ["Losartán 50mg","Metformina 500mg","Salbutamol spray","Loratadina 10mg","Fluoxetina 20mg","Alprazolam 0.5mg","Diclofenaco 50mg","Sumatriptán 50mg","Omeprazol 20mg","Levotiroxina 50mcg"]

TIPOS_TRANSACAO_PT = ["Transferência","Pagamento","Saque","Depósito","PIX","TED","DOC","Débito automático"]
TIPOS_TRANSACAO_ES = ["Transferencia","Pago","Retiro","Depósito","Transferencia electrónica","Débito automático","Pago de servicio","Cobro"]

ACOES_PT = ["LOGIN","LOGOUT","CONSULTA","ALTERACAO","CADASTRO","EXCLUSAO","DOWNLOAD","UPLOAD","RELATORIO","PAGAMENTO"]
ACOES_ES = ["LOGIN","LOGOUT","CONSULTA","MODIFICACION","REGISTRO","ELIMINACION","DESCARGA","SUBIDA","REPORTE","PAGO"]

INTERESSES_PT = ["Crédito pessoal","Seguro de vida","Conta digital","Investimentos","Cartão de crédito","Financiamento","Previdência","Câmbio"]
INTERESSES_ES = ["Crédito personal","Seguro de vida","Cuenta digital","Inversiones","Tarjeta de crédito","Financiamiento","Pensión","Cambio de divisas"]

FONTES_PT = ["Google Ads","Facebook","LinkedIn","Indicação","Site","Email","Evento","Parceiro"]
FONTES_ES = ["Google Ads","Facebook","LinkedIn","Referido","Sitio Web","Email","Evento","Socio"]

BANCOS_BR = ["Banco do Brasil","Itaú","Bradesco","Santander","Caixa Econômica","Nubank","Inter","C6 Bank"]
BANCOS_ES = ["Santander","BBVA","Bancolombia","Bancomer","BCI","Itaú","Davivienda","Nequi"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/113.0 Firefox/113.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0",
]

# ─── VOCABULARY PER LANGUAGE ──────────────────────────────────────────────────

V_PT = {
    "generos": GENEROS_PT, "estados_civil": ESTADOS_CIVIL_PT,
    "tipos_conta": TIPOS_CONTA_PT, "cartao_rede": BANDEIRAS,
    "status": STATUS_GERAL, "tipos_seguro": TIPOS_SEGURO_PT,
    "cargos": CARGOS_PT, "departamentos": DEPARTS,
    "diagnosticos": DIAGNOSTICOS_PT, "medicamentos": MEDICAMENTOS_PT,
    "tipos_transacao": TIPOS_TRANSACAO_PT, "acoes": ACOES_PT,
    "interesses": INTERESSES_PT, "fontes": FONTES_PT, "bancos": BANCOS_BR,
    "status_pedido": ["Processando","Enviado","Entregue","Cancelado","Devolvido"],
    "status_transacao": ["Concluída","Pendente","Rejeitada","Estornada"],
    "status_lead": ["Novo","Em contato","Qualificado","Convertido","Descartado"],
    "descricoes": ["Pagamento de fatura","Transferência","Compra online","Saque ATM","PIX recebido","Débito automático"],
    "planos_saude": ["Unimed","Amil","SulAmérica","Bradesco Saúde","Porto Seguro","Particular"],
    "segmentos": ["Tecnologia","Logística","Material de escritório","Serviços","Alimentos","Limpeza"],
    "recursos": ["/api/conta","/api/pagamento","/api/extrato","/api/usuario","/api/cartao"],
    "conta_salario": "Salário",
}

V_ES = {
    "generos": GENEROS_ES, "estados_civil": ESTADOS_CIVIL_ES,
    "tipos_conta": TIPOS_CONTA_ES, "cartao_rede": REDES_ES,
    "status": STATUS_ES, "tipos_seguro": TIPOS_SEGURO_ES,
    "cargos": CARGOS_ES, "departamentos": DEPARTS_ES,
    "diagnosticos": DIAGNOSTICOS_ES, "medicamentos": MEDICAMENTOS_ES,
    "tipos_transacao": TIPOS_TRANSACAO_ES, "acoes": ACOES_ES,
    "interesses": INTERESSES_ES, "fontes": FONTES_ES, "bancos": BANCOS_ES,
    "status_pedido": ["Procesando","Enviado","Entregado","Cancelado","Devuelto"],
    "status_transacao": ["Completada","Pendiente","Rechazada","Revertida"],
    "status_lead": ["Nuevo","En contacto","Calificado","Convertido","Descartado"],
    "descricoes": ["Pago de factura","Transferencia","Compra en línea","Retiro ATM","Débito automático"],
    "planos_saude": ["AXA","SURA","Colsanitas","Cruz Blanca","Compensar","Particular"],
    "segmentos": ["Tecnología","Logística","Papelería","Servicios","Alimentos","Limpieza"],
    "recursos": ["/api/cuenta","/api/pago","/api/extracto","/api/usuario","/api/tarjeta"],
    "conta_salario": "Nómina",
}

TIPOS_SANGUE = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]

# ─── RELATIONAL DATASET BUILDER ───────────────────────────────────────────────
#
# Weak relationships (no FKs in the DDL) between the 12 tables:
#
#   clientes ──┬── cartoes_credito     (1..5 por cliente)
#              ├── pedidos             (1..20 por cliente)
#              ├── prontuarios_medicos (0..1 por cliente)
#              ├── apolices_seguro     (1..5 por cliente)
#              ├── contas_bancarias    (parte dos clientes)
#              └── leads_marketing     (parte dos clientes)
#   funcionarios ── contas_bancarias   (1 conta de salário cada — única
#                                       tabela onde o funcionário aparece)
#   fornecedores ── contratos          (1..5 por fornecedor)
#   contas_bancarias ── transacoes     (origem/destino sempre existentes)
#   logs_acesso: e-mail de todo cliente, fornecedor e funcionário (>= 10 cada)
#
# Nomes e documentos são alocados de um pool sem repetição, então nenhuma
# pessoa aparece como cliente e funcionário (ou fornecedor) ao mesmo tempo.

N_CLIENTES = 120
N_FUNCIONARIOS = 120
N_FORNECEDORES = 120
N_TRANSACOES = 500
LOGS_POR_PESSOA = (10, 13)


class IdentityPool:
    """Distribui (nome, sobrenome, documento) unicos entre os grupos de pessoas."""

    def __init__(self, nomes, sobrenomes, docs):
        pares = [(n, s) for n in dict.fromkeys(nomes) for s in dict.fromkeys(sobrenomes)]
        random.shuffle(pares)
        unicos = list(dict.fromkeys(docs))
        random.shuffle(unicos)
        self.pares, self.docs, self.i = pares, unicos, 0

    def take(self, n):
        disponivel = min(len(self.pares), len(self.docs)) - self.i
        if n > disponivel:
            raise RuntimeError(f"pool de identidades esgotado ({n} > {disponivel})")
        fatia = [(p[0], p[1], d) for p, d in
                 zip(self.pares[self.i:self.i + n], self.docs[self.i:self.i + n])]
        self.i += n
        return fatia


def wcount(max_n, alpha=1.2):
    """1..max_n, com peso maior nos valores baixos (cauda longa até max_n)."""
    pesos = [k ** -alpha for k in range(1, max_n + 1)]
    return random.choices(range(1, max_n + 1), weights=pesos)[0]


def slug(s):
    out = "".join(ch for ch in s.lower() if ch.isalnum())
    return out or "empresa"


def build_dataset(cfg):
    country = cfg["country"]
    pt = cfg["lang"] == "pt"
    V = V_PT if pt else V_ES
    doc_label, doc_emp_label = cfg["doc_label"], cfg["doc_emp_label"]
    city_label = cfg["city_label"]

    nomes      = load(country, "nomes.txt" if pt else "nombres.txt")
    sobrenomes = load(country, "sobrenomes.txt" if pt else "apellidos.txt")
    end1       = load(country, "enderecos_linha1.txt" if pt else "direcciones_linea1.txt")
    end2       = load(country, "enderecos_linha2.txt" if pt else "direcciones_linea2.txt")
    ceps       = load(country, "cep.txt" if pt else "codigo_postal.txt")
    fones      = load(country, "telefones.txt" if pt else "telefonos.txt")
    empresas   = load(country, "empresas.txt")
    docs       = load(country, cfg["doc_file"])
    docs_emp   = load(country, cfg["doc_emp_file"])
    cidades    = load(country, cfg["city_file"])

    sep = " - " if pt else ","

    def split_city(s):
        partes = s.split(sep)
        if len(partes) >= 2:
            return partes[0].strip(), partes[1].strip()
        return s.strip(), ""

    pool = IdentityPool(nomes, sobrenomes, docs)
    emails_usados = set()
    contas_usadas = set()

    def email_unico(nome, sob):
        for _ in range(100):
            e = remail(nome, sob)
            if e not in emails_usados:
                emails_usados.add(e)
                return e
        e = f"{slug(nome)}.{slug(sob)}{len(emails_usados)}@gmail.com"
        emails_usados.add(e)
        return e

    def conta_unica():
        while True:
            c = rbankacct()
            if c not in contas_usadas:
                contas_usadas.add(c)
                return c

    def pessoa(ident):
        nome, sob, doc = ident
        cidade, regiao = split_city(rd(cidades))
        return {
            "nome": nome, "sobrenome": sob, "doc": doc,
            "nome_completo": f"{nome} {sob}",
            "email": email_unico(nome, sob),
            "telefone": rd(fones),
            "nascimento": rdate(),
            "genero": rd(V["generos"]),
            "estado_civil": rd(V["estados_civil"]),
            "end1": rd(end1), "end2": rd(end2),
            "cidade": cidade, "regiao": regiao, "cep": rd(ceps),
        }

    # ── pessoas (identidades mutuamente exclusivas) ───────────────────────────
    clientes  = [pessoa(t) for t in pool.take(N_CLIENTES)]
    funcs     = [pessoa(t) for t in pool.take(N_FUNCIONARIOS)]
    contatos  = [pessoa(t) for t in pool.take(N_FORNECEDORES)]
    medicos   = [pessoa(t) for t in pool.take(15)]
    benefs    = [pessoa(t) for t in pool.take(40)]
    leads_ext = [pessoa(t) for t in pool.take(100)]

    dominio_corp = "empresa.com.br" if pt else f"empresa.{country[:2]}.com"
    for f in funcs:
        f["cargo"] = rd(V["cargos"])
        f["departamento"] = rd(V["departamentos"])
        f["salario"] = ramount(2000, 25000) if pt else ramount(1500, 20000)
        f["admissao"] = rdate(2010, 2023)
        f["banco"] = rd(V["bancos"])
        f["conta"] = conta_unica()
        f["email_corp"] = f"{slug(f['nome'])}.{slug(f['sobrenome'])}@{dominio_corp}"

    # ── fornecedores (empresa + contato, ambos exclusivos) ────────────────────
    empresas_livres = list(dict.fromkeys(empresas))
    random.shuffle(empresas_livres)
    docs_emp_livres = list(dict.fromkeys(docs_emp))
    random.shuffle(docs_emp_livres)
    tld = ".com.br" if pt else ".com"
    prefixo_email = "contato@" if pt else "contacto@"

    fornecedores = []
    for idx, contato in enumerate(contatos):
        emp = empresas_livres[idx]
        cidade, regiao = split_city(rd(cidades))
        fornecedores.append({
            "empresa": emp,
            "doc_emp": docs_emp_livres[idx],
            "contato": contato,
            "email": f"{prefixo_email}{slug(emp.split()[0])}{idx + 1}{tld}",
            "telefone": contato["telefone"],
            "endereco": rd(end1),
            "cidade": cidade, "regiao": regiao, "cep": rd(ceps),
            "segmento": rd(V["segmentos"]),
        })
    empresas_nao_fornecedoras = empresas_livres[len(contatos):] or empresas_livres

    # ── contas bancárias: 1 por funcionário + parte dos clientes ─────────────
    contas = []
    for f in funcs:
        contas.append({
            "numero": f["conta"], "tipo": V["conta_salario"],
            "titular": f["nome_completo"], "doc": f["doc"], "banco": f["banco"],
        })
    for c in random.sample(clientes, ri(80, 100)):
        contas.append({
            "numero": conta_unica(), "tipo": rd(V["tipos_conta"]),
            "titular": c["nome_completo"], "doc": c["doc"], "banco": rd(V["bancos"]),
        })
    random.shuffle(contas)

    # ── tabelas ───────────────────────────────────────────────────────────────
    t_clientes, t_funcionarios, t_contas, t_cartoes = [], [], [], []
    t_pedidos, t_prontuarios, t_fornecedores, t_transacoes = [], [], [], []
    t_logs, t_apolices, t_contratos, t_leads = [], [], [], []

    for c in clientes:
        if pt:
            t_clientes.append({
                "nome": c["nome"], "sobrenome": c["sobrenome"], "email": c["email"],
                "telefone": c["telefone"], "cpf": c["doc"],
                "data_nascimento": c["nascimento"], "genero": c["genero"],
                "estado_civil": c["estado_civil"],
                "endereco_linha1": c["end1"], "endereco_linha2": c["end2"],
                "cidade": c["cidade"], "estado": c["regiao"], "cep": c["cep"],
                "pais": cfg["pais"],
            })
        else:
            t_clientes.append({
                "nombre": c["nome"], "apellido": c["sobrenome"], "email": c["email"],
                "telefono": c["telefone"], doc_label: c["doc"],
                "fecha_nacimiento": c["nascimento"], "genero": c["genero"],
                "estado_civil": c["estado_civil"],
                "direccion_linea1": c["end1"], "direccion_linea2": c["end2"],
                "ciudad": c["cidade"], city_label: c["regiao"],
                "codigo_postal": c["cep"], "pais": cfg["pais"],
            })

    for f in funcs:
        if pt:
            t_funcionarios.append({
                "nome": f["nome"], "sobrenome": f["sobrenome"],
                "email_corporativo": f["email_corp"], "email_pessoal": f["email"],
                "telefone": f["telefone"], "cpf": f["doc"],
                "data_nascimento": f["nascimento"], "cargo": f["cargo"],
                "departamento": f["departamento"], "salario": f["salario"],
                "data_admissao": f["admissao"],
                "endereco_linha1": f["end1"], "endereco_linha2": f["end2"],
                "cidade": f["cidade"], "estado": f["regiao"], "cep": f["cep"],
                "banco": f["banco"], "conta_bancaria": f["conta"],
            })
        else:
            t_funcionarios.append({
                "nombre": f["nome"], "apellido": f["sobrenome"],
                "email_corporativo": f["email_corp"], "email_personal": f["email"],
                "telefono": f["telefone"], doc_label: f["doc"],
                "fecha_nacimiento": f["nascimento"], "cargo": f["cargo"],
                "departamento": f["departamento"], "salario": f["salario"],
                "fecha_ingreso": f["admissao"],
                "direccion_linea1": f["end1"], "direccion_linea2": f["end2"],
                "ciudad": f["cidade"], "codigo_postal": f["cep"],
                "banco": f["banco"], "cuenta_bancaria": f["conta"],
            })

    for ct in contas:
        if pt:
            t_contas.append({
                "numero_conta": ct["numero"], "agencia": str(ri(1000, 9999)),
                "tipo_conta": ct["tipo"], "saldo": ramount(0, 100000),
                "limite": ramount(0, 50000), "titular": ct["titular"],
                "cpf_titular": ct["doc"], "banco": ct["banco"],
                "data_abertura": rdate(2010, 2023), "status": rd(V["status"]),
            })
        else:
            t_contas.append({
                "numero_cuenta": ct["numero"], "sucursal": str(ri(100, 9999)),
                "tipo_cuenta": ct["tipo"], "saldo": ramount(0, 100000),
                "limite": ramount(0, 50000), "titular": ct["titular"],
                doc_label + "_titular": ct["doc"], "banco": ct["banco"],
                "fecha_apertura": rdate(2010, 2023), "estado": rd(V["status"]),
            })

    for c in clientes:
        for _ in range(wcount(5)):
            if pt:
                t_cartoes.append({
                    "numero_cartao": rcard(),
                    "nome_titular": c["nome_completo"].upper(),
                    "validade": f"{ri(1,12):02d}/{ri(25,30)}",
                    "bandeira": rd(V["cartao_rede"]),
                    "limite": ramount(500, 30000), "fatura_atual": ramount(0, 15000),
                    "status": rd(V["status"]), "cpf_titular": c["doc"],
                })
            else:
                t_cartoes.append({
                    "numero_tarjeta": rcard(),
                    "nombre_titular": c["nome_completo"].upper(),
                    "vencimiento": f"{ri(1,12):02d}/{ri(25,30)}",
                    "red": rd(V["cartao_rede"]),
                    "limite": ramount(500, 30000), "factura_actual": ramount(0, 15000),
                    "estado": rd(V["status"]), doc_label + "_titular": c["doc"],
                })

    prefixo_pedido = "BR" if pt else country[:2].upper()
    for c in clientes:
        for _ in range(wcount(20, 0.9)):
            if pt:
                t_pedidos.append({
                    "numero_pedido": f"{prefixo_pedido}{ri(100000,999999)}",
                    "data_pedido": rdate(2022, 2024),
                    "cliente_nome": c["nome_completo"], "cliente_cpf": c["doc"],
                    "valor_total": ramount(50, 5000), "status": rd(V["status_pedido"]),
                    "endereco_entrega": c["end1"], "complemento_entrega": c["end2"],
                    "cidade_entrega": c["cidade"], "cep_entrega": c["cep"],
                })
            else:
                t_pedidos.append({
                    "numero_pedido": f"{prefixo_pedido}{ri(100000,999999)}",
                    "fecha_pedido": rdate(2022, 2024),
                    "nombre_cliente": c["nome_completo"], doc_label + "_cliente": c["doc"],
                    "monto_total": ramount(50, 5000), "estado": rd(V["status_pedido"]),
                    "direccion_entrega": c["end1"], "complemento_entrega": c["end2"],
                    "ciudad_entrega": c["cidade"], "codigo_postal_entrega": c["cep"],
                })

    for c in random.sample(clientes, int(len(clientes) * 0.8)):
        medico = rd(medicos)["nome_completo"]
        if pt:
            t_prontuarios.append({
                "paciente_nome": c["nome_completo"], "paciente_cpf": c["doc"],
                "data_nascimento": c["nascimento"], "tipo_sanguineo": rd(TIPOS_SANGUE),
                "diagnostico": rd(V["diagnosticos"]), "medicamentos": rd(V["medicamentos"]),
                "medico_responsavel": f"Dr. {medico}",
                "plano_saude": rd(V["planos_saude"]), "data_consulta": rdate(2022, 2024),
            })
        else:
            t_prontuarios.append({
                "nombre_paciente": c["nome_completo"], doc_label + "_paciente": c["doc"],
                "fecha_nacimiento": c["nascimento"], "tipo_sangre": rd(TIPOS_SANGUE),
                "diagnostico": rd(V["diagnosticos"]), "medicamentos": rd(V["medicamentos"]),
                "medico_responsable": f"Dr. {medico}",
                "seguro_medico": rd(V["planos_saude"]), "fecha_consulta": rdate(2022, 2024),
            })

    for fo in fornecedores:
        if pt:
            t_fornecedores.append({
                "nome_empresa": fo["empresa"], "cnpj": fo["doc_emp"],
                "nome_contato": fo["contato"]["nome_completo"], "email": fo["email"],
                "telefone": fo["telefone"], "endereco": fo["endereco"],
                "cidade": fo["cidade"], "estado": fo["regiao"], "cep": fo["cep"],
                "segmento": fo["segmento"],
            })
        else:
            t_fornecedores.append({
                "nombre_empresa": fo["empresa"], doc_emp_label: fo["doc_emp"],
                "nombre_contacto": fo["contato"]["nome_completo"], "email": fo["email"],
                "telefono": fo["telefone"], "direccion": fo["endereco"],
                "ciudad": fo["cidade"], "codigo_postal": fo["cep"],
                "segmento": fo["segmento"],
            })

    numeros_conta = [ct["numero"] for ct in contas]
    for _ in range(N_TRANSACOES):
        origem, destino = random.sample(numeros_conta, 2)
        if pt:
            t_transacoes.append({
                "data_transacao": rdt(), "tipo": rd(V["tipos_transacao"]),
                "valor": ramount(1, 20000), "conta_origem": origem, "conta_destino": destino,
                "descricao": rd(V["descricoes"]), "status": rd(V["status_transacao"]),
                "ip_origem": rip(), "localizacao": rd(cidades),
            })
        else:
            t_transacoes.append({
                "fecha_transaccion": rdt(), "tipo": rd(V["tipos_transacao"]),
                "monto": ramount(1, 20000), "cuenta_origen": origem, "cuenta_destino": destino,
                "descripcion": rd(V["descricoes"]), "estado": rd(V["status_transacao"]),
                "ip_origen": rip(), "ubicacion": rd(cidades),
            })

    usuarios_log = (
        [(1000 + i, c["email"]) for i, c in enumerate(clientes, 1)]
        + [(2000 + i, f["email_corp"]) for i, f in enumerate(funcs, 1)]
        + [(3000 + i, fo["email"]) for i, fo in enumerate(fornecedores, 1)]
    )
    for uid, email in usuarios_log:
        for _ in range(ri(*LOGS_POR_PESSOA)):
            if pt:
                t_logs.append({
                    "data_hora": rdt(), "usuario_id": uid, "email_usuario": email,
                    "ip_address": rip(), "user_agent": rd(USER_AGENTS),
                    "acao": rd(V["acoes"]), "recurso": rd(V["recursos"]),
                    "status_code": rd([200, 200, 200, 200, 401, 403, 404, 500]),
                    "localizacao": rd(cidades),
                })
            else:
                t_logs.append({
                    "fecha_hora": rdt(), "usuario_id": uid, "email_usuario": email,
                    "ip_address": rip(), "user_agent": rd(USER_AGENTS),
                    "accion": rd(V["acoes"]), "recurso": rd(V["recursos"]),
                    "codigo_estado": rd([200, 200, 200, 200, 401, 403, 404, 500]),
                    "ubicacion": rd(cidades),
                })
    random.shuffle(t_logs)

    for c in clientes:
        for _ in range(wcount(5)):
            beneficiario = rd(benefs)["nome_completo"]
            if pt:
                t_apolices.append({
                    "numero_apolice": f"APL{ri(1000000,9999999)}",
                    "titular_nome": c["nome_completo"], "titular_cpf": c["doc"],
                    "data_nascimento": c["nascimento"], "tipo_seguro": rd(V["tipos_seguro"]),
                    "cobertura": ramount(50000, 1000000), "premio_mensal": ramount(50, 800),
                    "data_inicio": rdate(2020, 2023), "data_fim": rdate(2024, 2028),
                    "beneficiario": beneficiario,
                })
            else:
                t_apolices.append({
                    "numero_poliza": f"POL{ri(1000000,9999999)}",
                    "nombre_titular": c["nome_completo"], doc_label + "_titular": c["doc"],
                    "fecha_nacimiento": c["nascimento"], "tipo_seguro": rd(V["tipos_seguro"]),
                    "cobertura": ramount(50000, 1000000), "prima_mensual": ramount(50, 800),
                    "fecha_inicio": rdate(2020, 2023), "fecha_fin": rdate(2024, 2028),
                    "beneficiario": beneficiario,
                })

    for fo in fornecedores:
        for _ in range(wcount(5)):
            if pt:
                t_contratos.append({
                    "numero_contrato": f"CTR{ri(100000,999999)}",
                    "empresa_nome": fo["empresa"], "empresa_cnpj": fo["doc_emp"],
                    "contato_nome": fo["contato"]["nome_completo"],
                    "contato_email": fo["email"], "contato_telefone": fo["telefone"],
                    "valor_contrato": ramount(10000, 5000000),
                    "data_inicio": rdate(2020, 2023), "data_fim": rdate(2024, 2027),
                    "status": rd(V["status"]),
                })
            else:
                t_contratos.append({
                    "numero_contrato": f"CTR{ri(100000,999999)}",
                    "nombre_empresa": fo["empresa"], doc_emp_label + "_empresa": fo["doc_emp"],
                    "nombre_contacto": fo["contato"]["nome_completo"],
                    "email_contacto": fo["email"], "telefono_contacto": fo["telefone"],
                    "monto_contrato": ramount(10000, 5000000),
                    "fecha_inicio": rdate(2020, 2023), "fecha_fin": rdate(2024, 2027),
                    "estado": rd(V["status"]),
                })

    # leads: parte dos clientes + pessoas novas — nunca funcionários ou fornecedores
    n_leads_clientes = ri(35, 55)
    pessoas_lead = random.sample(clientes, n_leads_clientes) + leads_ext[:130 - n_leads_clientes]
    random.shuffle(pessoas_lead)
    for p in pessoas_lead:
        if pt:
            t_leads.append({
                "nome": p["nome"], "sobrenome": p["sobrenome"], "email": p["email"],
                "telefone": p["telefone"], "empresa": rd(empresas_nao_fornecedoras),
                "cargo": rd(V["cargos"]), "fonte": rd(V["fontes"]),
                "data_cadastro": rdate(2022, 2024), "status": rd(V["status_lead"]),
                "interesse": rd(V["interesses"]),
            })
        else:
            t_leads.append({
                "nombre": p["nome"], "apellido": p["sobrenome"], "email": p["email"],
                "telefono": p["telefone"], "empresa": rd(empresas_nao_fornecedoras),
                "cargo": rd(V["cargos"]), "fuente": rd(V["fontes"]),
                "fecha_registro": rdate(2022, 2024), "estado": rd(V["status_lead"]),
                "interes": rd(V["interesses"]),
            })

    nomes_tabelas = (
        ["clientes", "funcionarios", "contas_bancarias", "cartoes_credito", "pedidos",
         "prontuarios_medicos", "fornecedores", "transacoes", "logs_acesso",
         "apolices_seguro", "contratos", "leads_marketing"]
        if pt else
        ["clientes", "empleados", "cuentas_bancarias", "tarjetas_credito", "pedidos",
         "historiales_medicos", "proveedores", "transacciones", "logs_acceso",
         "polizas_seguro", "contratos", "leads_marketing"]
    )
    tabelas = [t_clientes, t_funcionarios, t_contas, t_cartoes, t_pedidos, t_prontuarios,
               t_fornecedores, t_transacoes, t_logs, t_apolices, t_contratos, t_leads]

    resultado = {}
    for nome_tabela, linhas in zip(nomes_tabelas, tabelas):
        for i, linha in enumerate(linhas, 1):
            linha["id"] = i
        resultado[nome_tabela] = linhas
    return resultado

# ─── SQL ESCAPING ─────────────────────────────────────────────────────────────

NUMERIC_TYPES = ("INT", "DECIMAL", "NUMBER", "NUMERIC", "BIGINT", "SMALLINT", "FLOAT")

def is_numeric(ctype):
    return ctype.upper().startswith(NUMERIC_TYPES)

def esc(v):
    if v is None:
        return "NULL"
    s = str(v).replace("'", "''")
    return f"'{s}'"

def val(v, ctype):
    """Numeric columns go in unquoted: a quoted '1234.56' depends on the
    session's decimal separator (ORA-01722 when NLS_NUMERIC_CHARACTERS is ',')."""
    if v is None or v == "":
        return "NULL"
    if is_numeric(ctype):
        return str(v)
    return esc(v)

# ─── DDL SCHEMAS ──────────────────────────────────────────────────────────────

SCHEMAS_BR = {
    "clientes": [
        ("id","INT"), ("nome","VARCHAR(100)"), ("sobrenome","VARCHAR(100)"),
        ("email","VARCHAR(150)"), ("telefone","VARCHAR(30)"), ("cpf","VARCHAR(20)"),  # PII
        ("data_nascimento","DATE"), ("genero","VARCHAR(10)"), ("estado_civil","VARCHAR(20)"),
        ("endereco_linha1","VARCHAR(200)"), ("endereco_linha2","VARCHAR(100)"),
        ("cidade","VARCHAR(100)"), ("estado","VARCHAR(5)"), ("cep","VARCHAR(10)"), ("pais","VARCHAR(50)"),
    ],
    "funcionarios": [
        ("id","INT"), ("nome","VARCHAR(100)"), ("sobrenome","VARCHAR(100)"),
        ("email_corporativo","VARCHAR(150)"), ("email_pessoal","VARCHAR(150)"),  # PII
        ("telefone","VARCHAR(30)"), ("cpf","VARCHAR(20)"),  # PII
        ("data_nascimento","DATE"), ("cargo","VARCHAR(100)"), ("departamento","VARCHAR(100)"),
        ("salario","DECIMAL(12,2)"),  # PII
        ("data_admissao","DATE"),
        ("endereco_linha1","VARCHAR(200)"), ("endereco_linha2","VARCHAR(100)"),
        ("cidade","VARCHAR(100)"), ("estado","VARCHAR(5)"), ("cep","VARCHAR(10)"),
        ("banco","VARCHAR(100)"), ("conta_bancaria","VARCHAR(30)"),  # PII
    ],
    "contas_bancarias": [
        ("id","INT"), ("numero_conta","VARCHAR(30)"),  # PII
        ("agencia","VARCHAR(10)"), ("tipo_conta","VARCHAR(30)"),
        ("saldo","DECIMAL(14,2)"),  # PII
        ("limite","DECIMAL(14,2)"), ("titular","VARCHAR(200)"),
        ("cpf_titular","VARCHAR(20)"),  # PII
        ("banco","VARCHAR(100)"), ("data_abertura","DATE"), ("status","VARCHAR(20)"),
    ],
    "cartoes_credito": [
        ("id","INT"), ("numero_cartao","VARCHAR(25)"),  # PII/PCI
        ("nome_titular","VARCHAR(200)"),  # PII
        ("validade","VARCHAR(8)"), ("bandeira","VARCHAR(30)"),
        ("limite","DECIMAL(12,2)"), ("fatura_atual","DECIMAL(12,2)"),
        ("status","VARCHAR(20)"), ("cpf_titular","VARCHAR(20)"),  # PII
    ],
    "pedidos": [
        ("id","INT"), ("numero_pedido","VARCHAR(20)"), ("data_pedido","DATE"),
        ("cliente_nome","VARCHAR(200)"),  # PII
        ("cliente_cpf","VARCHAR(20)"),  # PII
        ("valor_total","DECIMAL(12,2)"), ("status","VARCHAR(30)"),
        ("endereco_entrega","VARCHAR(200)"), ("complemento_entrega","VARCHAR(100)"),
        ("cidade_entrega","VARCHAR(100)"), ("cep_entrega","VARCHAR(10)"),
    ],
    "prontuarios_medicos": [
        ("id","INT"), ("paciente_nome","VARCHAR(200)"),  # PII
        ("paciente_cpf","VARCHAR(20)"),  # PII
        ("data_nascimento","DATE"),  # PII
        ("tipo_sanguineo","VARCHAR(5)"),  # PII
        ("diagnostico","VARCHAR(200)"),  # PII
        ("medicamentos","VARCHAR(200)"),  # PII
        ("medico_responsavel","VARCHAR(200)"),
        ("plano_saude","VARCHAR(100)"), ("data_consulta","DATE"),
    ],
    "fornecedores": [
        ("id","INT"), ("nome_empresa","VARCHAR(200)"), ("cnpj","VARCHAR(20)"),
        ("nome_contato","VARCHAR(200)"),  # PII
        ("email","VARCHAR(150)"),  # PII
        ("telefone","VARCHAR(30)"),  # PII
        ("endereco","VARCHAR(200)"), ("cidade","VARCHAR(100)"),
        ("estado","VARCHAR(5)"), ("cep","VARCHAR(10)"), ("segmento","VARCHAR(100)"),
    ],
    "transacoes": [
        ("id","INT"), ("data_transacao","DATETIME"), ("tipo","VARCHAR(50)"),
        ("valor","DECIMAL(14,2)"), ("conta_origem","VARCHAR(30)"),  # PII
        ("conta_destino","VARCHAR(30)"),  # PII
        ("descricao","VARCHAR(200)"), ("status","VARCHAR(30)"),
        ("ip_origem","VARCHAR(50)"),  # PII
        ("localizacao","VARCHAR(100)"),
    ],
    "logs_acesso": [
        ("id","INT"), ("data_hora","DATETIME"), ("usuario_id","INT"),
        ("email_usuario","VARCHAR(150)"),  # PII
        ("ip_address","VARCHAR(50)"),  # PII
        ("user_agent","VARCHAR(300)"),  # PII
        ("acao","VARCHAR(50)"), ("recurso","VARCHAR(200)"),
        ("status_code","INT"), ("localizacao","VARCHAR(100)"),
    ],
    "apolices_seguro": [
        ("id","INT"), ("numero_apolice","VARCHAR(20)"),
        ("titular_nome","VARCHAR(200)"),  # PII
        ("titular_cpf","VARCHAR(20)"),  # PII
        ("data_nascimento","DATE"),  # PII
        ("tipo_seguro","VARCHAR(50)"), ("cobertura","DECIMAL(14,2)"),
        ("premio_mensal","DECIMAL(10,2)"),  # PII
        ("data_inicio","DATE"), ("data_fim","DATE"),
        ("beneficiario","VARCHAR(200)"),  # PII
    ],
    "contratos": [
        ("id","INT"), ("numero_contrato","VARCHAR(20)"),
        ("empresa_nome","VARCHAR(200)"), ("empresa_cnpj","VARCHAR(20)"),
        ("contato_nome","VARCHAR(200)"),  # PII
        ("contato_email","VARCHAR(150)"),  # PII
        ("contato_telefone","VARCHAR(30)"),  # PII
        ("valor_contrato","DECIMAL(16,2)"), ("data_inicio","DATE"),
        ("data_fim","DATE"), ("status","VARCHAR(20)"),
    ],
    "leads_marketing": [
        ("id","INT"), ("nome","VARCHAR(100)"),  # PII
        ("sobrenome","VARCHAR(100)"),  # PII
        ("email","VARCHAR(150)"),  # PII
        ("telefone","VARCHAR(30)"),  # PII
        ("empresa","VARCHAR(200)"), ("cargo","VARCHAR(100)"),
        ("fonte","VARCHAR(50)"), ("data_cadastro","DATE"),
        ("status","VARCHAR(30)"), ("interesse","VARCHAR(100)"),
    ],
}

def build_schema_es(doc_label, doc_emp_label, city_label):
    return {
        "clientes": [
            ("id","INT"), ("nombre","VARCHAR(100)"), ("apellido","VARCHAR(100)"),
            ("email","VARCHAR(150)"), ("telefono","VARCHAR(30)"), (doc_label,"VARCHAR(25)"),
            ("fecha_nacimiento","DATE"), ("genero","VARCHAR(10)"), ("estado_civil","VARCHAR(20)"),
            ("direccion_linea1","VARCHAR(200)"), ("direccion_linea2","VARCHAR(100)"),
            ("ciudad","VARCHAR(100)"), (city_label,"VARCHAR(100)"),
            ("codigo_postal","VARCHAR(15)"), ("pais","VARCHAR(50)"),
        ],
        "empleados": [
            ("id","INT"), ("nombre","VARCHAR(100)"), ("apellido","VARCHAR(100)"),
            ("email_corporativo","VARCHAR(150)"), ("email_personal","VARCHAR(150)"),
            ("telefono","VARCHAR(30)"), (doc_label,"VARCHAR(25)"),
            ("fecha_nacimiento","DATE"), ("cargo","VARCHAR(100)"), ("departamento","VARCHAR(100)"),
            ("salario","DECIMAL(12,2)"),
            ("fecha_ingreso","DATE"),
            ("direccion_linea1","VARCHAR(200)"), ("direccion_linea2","VARCHAR(100)"),
            ("ciudad","VARCHAR(100)"), ("codigo_postal","VARCHAR(15)"),
            ("banco","VARCHAR(100)"), ("cuenta_bancaria","VARCHAR(30)"),
        ],
        "cuentas_bancarias": [
            ("id","INT"), ("numero_cuenta","VARCHAR(30)"),
            ("sucursal","VARCHAR(10)"), ("tipo_cuenta","VARCHAR(30)"),
            ("saldo","DECIMAL(14,2)"),
            ("limite","DECIMAL(14,2)"), ("titular","VARCHAR(200)"),
            (doc_label+"_titular","VARCHAR(25)"),
            ("banco","VARCHAR(100)"), ("fecha_apertura","DATE"), ("estado","VARCHAR(20)"),
        ],
        "tarjetas_credito": [
            ("id","INT"), ("numero_tarjeta","VARCHAR(25)"),
            ("nombre_titular","VARCHAR(200)"),
            ("vencimiento","VARCHAR(8)"), ("red","VARCHAR(30)"),
            ("limite","DECIMAL(12,2)"), ("factura_actual","DECIMAL(12,2)"),
            ("estado","VARCHAR(20)"), (doc_label+"_titular","VARCHAR(25)"),
        ],
        "pedidos": [
            ("id","INT"), ("numero_pedido","VARCHAR(20)"), ("fecha_pedido","DATE"),
            ("nombre_cliente","VARCHAR(200)"),
            (doc_label+"_cliente","VARCHAR(25)"),
            ("monto_total","DECIMAL(12,2)"), ("estado","VARCHAR(30)"),
            ("direccion_entrega","VARCHAR(200)"), ("complemento_entrega","VARCHAR(100)"),
            ("ciudad_entrega","VARCHAR(100)"), ("codigo_postal_entrega","VARCHAR(15)"),
        ],
        "historiales_medicos": [
            ("id","INT"), ("nombre_paciente","VARCHAR(200)"),
            (doc_label+"_paciente","VARCHAR(25)"),
            ("fecha_nacimiento","DATE"),
            ("tipo_sangre","VARCHAR(5)"),
            ("diagnostico","VARCHAR(200)"),
            ("medicamentos","VARCHAR(200)"),
            ("medico_responsable","VARCHAR(200)"),
            ("seguro_medico","VARCHAR(100)"), ("fecha_consulta","DATE"),
        ],
        "proveedores": [
            ("id","INT"), ("nombre_empresa","VARCHAR(200)"), (doc_emp_label,"VARCHAR(25)"),
            ("nombre_contacto","VARCHAR(200)"),
            ("email","VARCHAR(150)"),
            ("telefono","VARCHAR(30)"),
            ("direccion","VARCHAR(200)"), ("ciudad","VARCHAR(100)"),
            ("codigo_postal","VARCHAR(15)"), ("segmento","VARCHAR(100)"),
        ],
        "transacciones": [
            ("id","INT"), ("fecha_transaccion","DATETIME"), ("tipo","VARCHAR(50)"),
            ("monto","DECIMAL(14,2)"), ("cuenta_origen","VARCHAR(30)"),
            ("cuenta_destino","VARCHAR(30)"),
            ("descripcion","VARCHAR(200)"), ("estado","VARCHAR(30)"),
            ("ip_origen","VARCHAR(50)"),
            ("ubicacion","VARCHAR(100)"),
        ],
        "logs_acceso": [
            ("id","INT"), ("fecha_hora","DATETIME"), ("usuario_id","INT"),
            ("email_usuario","VARCHAR(150)"),
            ("ip_address","VARCHAR(50)"),
            ("user_agent","VARCHAR(300)"),
            ("accion","VARCHAR(50)"), ("recurso","VARCHAR(200)"),
            ("codigo_estado","INT"), ("ubicacion","VARCHAR(100)"),
        ],
        "polizas_seguro": [
            ("id","INT"), ("numero_poliza","VARCHAR(20)"),
            ("nombre_titular","VARCHAR(200)"),
            (doc_label+"_titular","VARCHAR(25)"),
            ("fecha_nacimiento","DATE"),
            ("tipo_seguro","VARCHAR(50)"), ("cobertura","DECIMAL(14,2)"),
            ("prima_mensual","DECIMAL(10,2)"),
            ("fecha_inicio","DATE"), ("fecha_fin","DATE"),
            ("beneficiario","VARCHAR(200)"),
        ],
        "contratos": [
            ("id","INT"), ("numero_contrato","VARCHAR(20)"),
            ("nombre_empresa","VARCHAR(200)"), (doc_emp_label+"_empresa","VARCHAR(25)"),
            ("nombre_contacto","VARCHAR(200)"),
            ("email_contacto","VARCHAR(150)"),
            ("telefono_contacto","VARCHAR(30)"),
            ("monto_contrato","DECIMAL(16,2)"), ("fecha_inicio","DATE"),
            ("fecha_fin","DATE"), ("estado","VARCHAR(20)"),
        ],
        "leads_marketing": [
            ("id","INT"), ("nombre","VARCHAR(100)"),
            ("apellido","VARCHAR(100)"),
            ("email","VARCHAR(150)"),
            ("telefono","VARCHAR(30)"),
            ("empresa","VARCHAR(200)"), ("cargo","VARCHAR(100)"),
            ("fuente","VARCHAR(50)"), ("fecha_registro","DATE"),
            ("estado","VARCHAR(30)"), ("interes","VARCHAR(100)"),
        ],
    }

# ─── DDL RENDERERS ────────────────────────────────────────────────────────────

def pg_type(t):
    return t.replace("DATETIME","TIMESTAMP")

def ora_type(t):
    m = {"INT":"NUMBER(10)", "DECIMAL(12,2)":"NUMBER(12,2)", "DECIMAL(14,2)":"NUMBER(14,2)",
         "DECIMAL(16,2)":"NUMBER(16,2)", "DECIMAL(10,2)":"NUMBER(10,2)",
         "DATETIME":"TIMESTAMP", "DATE":"DATE"}
    return m.get(t, t)

def ss_type(t):
    return t.replace("DATETIME","DATETIME2")

def my_type(t):
    return t

def render_pg(schema_name, schema, rows_dict, db_type="pg"):
    lines = []
    lines.append(f"-- ============================================================")
    lines.append(f"-- Schema: {schema_name.upper()} | Engine: PostgreSQL")
    lines.append(f"-- PII columns marked with -- [PII]")
    lines.append(f"-- ============================================================\n")

    for tbl, cols in schema.items():
        lines.append(f"DROP TABLE IF EXISTS {tbl};")
        lines.append(f"CREATE TABLE {tbl} (")
        col_defs = []
        for cname, ctype in cols:
            col_defs.append(f"    {cname} {pg_type(ctype)}")
        lines.append(",\n".join(col_defs))
        lines.append(");\n")

    for tbl, cols in schema.items():
        rows = rows_dict.get(tbl, [])
        if not rows:
            continue
        col_names = [c[0] for c in cols]
        lines.append(f"-- {tbl}: {len(rows)} rows")
        for row in rows:
            vals = ", ".join(val(row.get(c, ""), ctype) for c, ctype in cols)
            lines.append(f"INSERT INTO {tbl} ({', '.join(col_names)}) VALUES ({vals});")
        lines.append("")

    return "\n".join(lines)

def render_mysql(schema_name, schema, rows_dict):
    lines = []
    lines.append(f"-- ============================================================")
    lines.append(f"-- Schema: {schema_name.upper()} | Engine: MySQL 8")
    lines.append(f"-- PII columns marked with -- [PII]")
    lines.append(f"-- ============================================================\n")
    lines.append(f"CREATE DATABASE IF NOT EXISTS demo_{schema_name};")
    lines.append(f"USE demo_{schema_name};\n")

    for tbl, cols in schema.items():
        lines.append(f"DROP TABLE IF EXISTS `{tbl}`;")
        lines.append(f"CREATE TABLE `{tbl}` (")
        col_defs = [f"    `{cname}` {my_type(ctype)}" for cname, ctype in cols]
        lines.append(",\n".join(col_defs))
        lines.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n")

    for tbl, cols in schema.items():
        rows = rows_dict.get(tbl, [])
        if not rows:
            continue
        col_names = [c[0] for c in cols]
        col_str = ", ".join(f"`{c}`" for c in col_names)
        lines.append(f"-- {tbl}: {len(rows)} rows")
        for row in rows:
            vals = ", ".join(val(row.get(c, ""), ctype) for c, ctype in cols)
            lines.append(f"INSERT INTO `{tbl}` ({col_str}) VALUES ({vals});")
        lines.append("")

    return "\n".join(lines)

def render_sqlserver(schema_name, schema, rows_dict):
    lines = []
    lines.append(f"-- ============================================================")
    lines.append(f"-- Schema: {schema_name.upper()} | Engine: SQL Server")
    lines.append(f"-- PII columns marked with -- [PII]")
    lines.append(f"-- ============================================================\n")
    lines.append(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'demo_{schema_name}')")
    lines.append(f"    CREATE DATABASE [demo_{schema_name}];")
    lines.append(f"GO")
    lines.append(f"USE [demo_{schema_name}];")
    lines.append(f"GO\n")

    for tbl, cols in schema.items():
        lines.append(f"IF OBJECT_ID(N'dbo.{tbl}', N'U') IS NOT NULL DROP TABLE dbo.{tbl};")
        lines.append(f"CREATE TABLE dbo.{tbl} (")
        col_defs = [f"    [{cname}] {ss_type(ctype)}" for cname, ctype in cols]
        lines.append(",\n".join(col_defs))
        lines.append(");\nGO\n")

    for tbl, cols in schema.items():
        rows = rows_dict.get(tbl, [])
        if not rows:
            continue
        col_names = [c[0] for c in cols]
        col_str = ", ".join(f"[{c}]" for c in col_names)
        lines.append(f"-- {tbl}: {len(rows)} rows")
        for row in rows:
            vals = ", ".join(val(row.get(c, ""), ctype) for c, ctype in cols)
            lines.append(f"INSERT INTO dbo.{tbl} ({col_str}) VALUES ({vals});")
        lines.append("GO\n")

    return "\n".join(lines)

def render_oracle(schema_name, schema, rows_dict):
    lines = []
    lines.append(f"-- ============================================================")
    lines.append(f"-- Schema: {schema_name.upper()} | Engine: Oracle")
    lines.append(f"-- PII columns marked with -- [PII]")
    lines.append(f"-- ============================================================\n")

    for tbl, cols in schema.items():
        lines.append(f"BEGIN EXECUTE IMMEDIATE 'DROP TABLE {tbl.upper()}'; EXCEPTION WHEN OTHERS THEN NULL; END;")
        lines.append(f"")
        lines.append(f"CREATE TABLE {tbl.upper()} (")
        col_defs = [f"    {cname.upper()} {ora_type(ctype)}" for cname, ctype in cols]
        lines.append(",\n".join(col_defs))
        lines.append(");\n")

    for tbl, cols in schema.items():
        rows = rows_dict.get(tbl, [])
        if not rows:
            continue
        col_names = [c[0] for c in cols]
        col_str = ", ".join(c.upper() for c in col_names)
        lines.append(f"-- {tbl.upper()}: {len(rows)} rows")
        for row in rows:
            vals = []
            for c, (_, ct) in zip(col_names, cols):
                v = row.get(c, "")
                if "DATE" in ct or "TIMESTAMP" in ct:
                    if "TIMESTAMP" in ct or "DATETIME" in ct:
                        vals.append(f"TO_TIMESTAMP({esc(v)}, 'YYYY-MM-DD HH24:MI:SS')")
                    else:
                        vals.append(f"TO_DATE({esc(v)}, 'YYYY-MM-DD')")
                else:
                    vals.append(val(v, ct))
            lines.append(f"INSERT INTO {tbl.upper()} ({col_str}) VALUES ({', '.join(vals)});")
        lines.append("")

    return "\n".join(lines)

# ─── COUNTRY CONFIGS ─────────────────────────────────────────────────────────

COUNTRY_CONFIGS = {
    "brasil":      {"lang": "pt", "pais": "Brasil",      "doc_label": "cpf",       "doc_emp_label": "cnpj",            "city_label": "estado",       "doc_file": "cpf.txt",       "doc_emp_file": "cnpj.txt",            "city_file": "cidades_estados.txt"},
    "argentina":   {"lang": "es", "pais": "Argentina",   "doc_label": "dni",       "doc_emp_label": "cuit",            "city_label": "provincia",    "doc_file": "dni.txt",       "doc_emp_file": "cuit.txt",            "city_file": "ciudades_provincias.txt"},
    "chile":       {"lang": "es", "pais": "Chile",       "doc_label": "rut",       "doc_emp_label": "rut_empresa",     "city_label": "region",       "doc_file": "rut_personas.txt", "doc_emp_file": "rut_empresas.txt", "city_file": "ciudades_regiones.txt"},
    "mexico":      {"lang": "es", "pais": "México",      "doc_label": "curp",      "doc_emp_label": "rfc",             "city_label": "estado",       "doc_file": "curp.txt",      "doc_emp_file": "rfc.txt",             "city_file": "ciudades_estados.txt"},
    "panama":      {"lang": "es", "pais": "Panamá",      "doc_label": "cedula",    "doc_emp_label": "ruc",             "city_label": "provincia",    "doc_file": "cedula.txt",    "doc_emp_file": "ruc.txt",             "city_file": "ciudades_provincias.txt"},
    "colombia":    {"lang": "es", "pais": "Colombia",    "doc_label": "cedula_cc", "doc_emp_label": "nit",             "city_label": "departamento", "doc_file": "cedula_cc.txt", "doc_emp_file": "nit.txt",             "city_file": "ciudades_departamentos.txt"},
    "peru":        {"lang": "es", "pais": "Perú",        "doc_label": "dni",       "doc_emp_label": "ruc",             "city_label": "departamento", "doc_file": "dni.txt",       "doc_emp_file": "ruc.txt",             "city_file": "ciudades_departamentos.txt"},
    "paraguay":    {"lang": "es", "pais": "Paraguay",    "doc_label": "ci",        "doc_emp_label": "ruc",             "city_label": "departamento", "doc_file": "ci.txt",        "doc_emp_file": "ruc.txt",             "city_file": "ciudades_departamentos.txt"},
    "uruguay":     {"lang": "es", "pais": "Uruguay",     "doc_label": "ci",        "doc_emp_label": "rut",             "city_label": "departamento", "doc_file": "ci.txt",        "doc_emp_file": "rut.txt",             "city_file": "ciudades_departamentos.txt"},
    "ecuador":     {"lang": "es", "pais": "Ecuador",     "doc_label": "cedula",    "doc_emp_label": "ruc",             "city_label": "provincia",    "doc_file": "cedula.txt",    "doc_emp_file": "ruc.txt",             "city_file": "ciudades_provincias.txt"},
    "bolivia":     {"lang": "es", "pais": "Bolivia",     "doc_label": "ci",        "doc_emp_label": "nit",             "city_label": "departamento", "doc_file": "ci.txt",        "doc_emp_file": "nit.txt",             "city_file": "ciudades_departamentos.txt"},
    "venezuela":   {"lang": "es", "pais": "Venezuela",   "doc_label": "cedula",    "doc_emp_label": "rif",             "city_label": "estado",       "doc_file": "cedula.txt",    "doc_emp_file": "rif.txt",             "city_file": "ciudades_estados.txt"},
    "costa_rica":  {"lang": "es", "pais": "Costa Rica",  "doc_label": "cedula",    "doc_emp_label": "cedula_juridica", "city_label": "provincia",    "doc_file": "cedula.txt",    "doc_emp_file": "cedula_juridica.txt", "city_file": "ciudades_provincias.txt"},
    "belize":      {"lang": "es", "pais": "Belice",      "doc_label": "ssn",       "doc_emp_label": "tin",             "city_label": "distrito",     "doc_file": "ssn.txt",       "doc_emp_file": "tin.txt",             "city_file": "ciudades_distritos.txt"},
    "el_salvador": {"lang": "es", "pais": "El Salvador", "doc_label": "dui",       "doc_emp_label": "nit",             "city_label": "departamento", "doc_file": "dui.txt",       "doc_emp_file": "nit.txt",             "city_file": "ciudades_departamentos.txt"},
}

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    for country, cfg in COUNTRY_CONFIGS.items():
        print(f"Generating {country}...", end=" ", flush=True)
        cfg = dict(cfg, country=country)
        rows_dict = build_dataset(cfg)
        schema = (SCHEMAS_BR if cfg["lang"] == "pt"
                  else build_schema_es(cfg["doc_label"], cfg["doc_emp_label"], cfg["city_label"]))

        renderers = [
            ("postgresql", render_pg(country, schema, rows_dict)),
            ("mysql",      render_mysql(country, schema, rows_dict)),
            ("sqlserver",  render_sqlserver(country, schema, rows_dict)),
            ("oracle",     render_oracle(country, schema, rows_dict)),
        ]
        for engine, content in renderers:
            path = f"{BASE}/ddl/{engine}/{country}.sql"
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"done ({sum(len(r) for r in rows_dict.values())} rows)")

    print("\nAll DDL files generated.")

if __name__ == "__main__":
    main()
