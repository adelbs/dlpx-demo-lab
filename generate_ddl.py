#!/usr/bin/env python3
"""
Generate DDL + INSERT scripts for 6 countries × 4 database engines.
Tables: 12 per country, 100+ rows each.
"""

import random
import os
import datetime

BASE = "/Users/felipe.jacob/Projects/demo-lab"
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

# ─── ROW GENERATORS ───────────────────────────────────────────────────────────

def rows_brasil(n=120):
    nomes = load("brasil","nomes.txt")
    sobrenomes = load("brasil","sobrenomes.txt")
    cpfs = load("brasil","cpf.txt")
    cnpjs = load("brasil","cnpj.txt")
    cidades = load("brasil","cidades_estados.txt")
    endL1 = load("brasil","enderecos_linha1.txt")
    endL2 = load("brasil","enderecos_linha2.txt")
    ceps = load("brasil","cep.txt")
    fones = load("brasil","telefones.txt")
    empresas = load("brasil","empresas.txt")

    def row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        return {
            "id": i, "nome": nome, "sobrenome": sob,
            "email": remail(nome, sob),
            "telefone": rd(fones), "cpf": rd(cpfs),
            "data_nascimento": rdate(), "genero": rd(GENEROS_PT),
            "estado_civil": rd(ESTADOS_CIVIL_PT),
            "endereco_linha1": rd(endL1), "endereco_linha2": rd(endL2),
            "cidade": rd(cidades).split(" - ")[0],
            "estado": rd(cidades).split(" - ")[1] if " - " in rd(cidades) else "SP",
            "cep": rd(ceps), "pais": "Brasil",
        }

    def emp_row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        return {
            "id": i, "nome": nome, "sobrenome": sob,
            "email_corporativo": f"{nome.lower()}.{sob.lower()[:5]}@empresa.com.br".replace(" ",""),
            "email_pessoal": remail(nome, sob),
            "telefone": rd(fones), "cpf": rd(cpfs),
            "data_nascimento": rdate(), "cargo": rd(CARGOS_PT),
            "departamento": rd(DEPARTS),
            "salario": ramount(2000, 25000),
            "data_admissao": rdate(2010, 2023),
            "endereco_linha1": rd(endL1), "endereco_linha2": rd(endL2),
            "cidade": rd(cidades).split(" - ")[0],
            "estado": "SP", "cep": rd(ceps),
            "banco": rd(BANCOS_BR), "conta_bancaria": rbankacct(),
        }

    def conta_row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        return {
            "id": i, "numero_conta": rbankacct(),
            "agencia": str(ri(1000,9999)),
            "tipo_conta": rd(TIPOS_CONTA_PT),
            "saldo": ramount(0, 100000),
            "limite": ramount(0, 50000),
            "titular": f"{nome} {sob}",
            "cpf_titular": rd(cpfs),
            "banco": rd(BANCOS_BR),
            "data_abertura": rdate(2010, 2023),
            "status": rd(STATUS_GERAL),
        }

    def cartao_row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        return {
            "id": i, "numero_cartao": rcard(),
            "nome_titular": f"{nome} {sob}".upper(),
            "validade": f"{ri(1,12):02d}/{ri(25,30)}",
            "bandeira": rd(BANDEIRAS),
            "limite": ramount(500, 30000),
            "fatura_atual": ramount(0, 15000),
            "status": rd(STATUS_GERAL),
            "cpf_titular": rd(cpfs),
        }

    def pedido_row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        return {
            "id": i,
            "numero_pedido": f"BR{ri(100000,999999)}",
            "data_pedido": rdate(2022, 2024),
            "cliente_nome": f"{nome} {sob}",
            "cliente_cpf": rd(cpfs),
            "valor_total": ramount(50, 5000),
            "status": rd(["Processando","Enviado","Entregue","Cancelado","Devolvido"]),
            "endereco_entrega": rd(endL1),
            "complemento_entrega": rd(endL2),
            "cidade_entrega": rd(cidades).split(" - ")[0],
            "cep_entrega": rd(ceps),
        }

    def prontuario_row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        medico = rd(nomes) + " " + rd(sobrenomes)
        return {
            "id": i,
            "paciente_nome": f"{nome} {sob}",
            "paciente_cpf": rd(cpfs),
            "data_nascimento": rdate(),
            "tipo_sanguineo": rd(["A+","A-","B+","B-","AB+","AB-","O+","O-"]),
            "diagnostico": rd(DIAGNOSTICOS_PT),
            "medicamentos": rd(MEDICAMENTOS_PT),
            "medico_responsavel": f"Dr. {medico}",
            "plano_saude": rd(["Unimed","Amil","SulAmérica","Bradesco Saúde","Porto Seguro","Particular"]),
            "data_consulta": rdate(2022, 2024),
        }

    def fornecedor_row(i):
        return {
            "id": i,
            "nome_empresa": rd(empresas),
            "cnpj": rd(cnpjs),
            "nome_contato": f"{rd(nomes)} {rd(sobrenomes)}",
            "email": f"contato@{rd(empresas).split()[0].lower().replace('.','')}.com.br",
            "telefone": rd(fones),
            "endereco": rd(endL1),
            "cidade": rd(cidades).split(" - ")[0],
            "estado": "SP", "cep": rd(ceps),
            "segmento": rd(["Tecnologia","Logística","Material de escritório","Serviços","Alimentos","Limpeza"]),
        }

    def transacao_row(i):
        return {
            "id": i,
            "data_transacao": rdt(),
            "tipo": rd(TIPOS_TRANSACAO_PT),
            "valor": ramount(1, 20000),
            "conta_origem": rbankacct(),
            "conta_destino": rbankacct(),
            "descricao": rd(["Pagamento de fatura","Transferência","Compra online","Saque ATM","PIX recebido","Débito automático"]),
            "status": rd(["Concluída","Pendente","Rejeitada","Estornada"]),
            "ip_origem": rip(),
            "localizacao": rd(cidades),
        }

    def log_row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        return {
            "id": i,
            "data_hora": rdt(),
            "usuario_id": ri(1, 10000),
            "email_usuario": remail(nome, sob),
            "ip_address": rip(),
            "user_agent": rd(USER_AGENTS),
            "acao": rd(ACOES_PT),
            "recurso": rd(["/api/conta","/api/pagamento","/api/extrato","/api/usuario","/api/cartao"]),
            "status_code": rd([200,200,200,200,401,403,404,500]),
            "localizacao": rd(cidades),
        }

    def apolice_row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        return {
            "id": i,
            "numero_apolice": f"APL{ri(1000000,9999999)}",
            "titular_nome": f"{nome} {sob}",
            "titular_cpf": rd(cpfs),
            "data_nascimento": rdate(),
            "tipo_seguro": rd(TIPOS_SEGURO_PT),
            "cobertura": ramount(50000, 1000000),
            "premio_mensal": ramount(50, 800),
            "data_inicio": rdate(2020, 2023),
            "data_fim": rdate(2024, 2028),
            "beneficiario": f"{rd(nomes)} {rd(sobrenomes)}",
        }

    def contrato_row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        return {
            "id": i,
            "numero_contrato": f"CTR{ri(100000,999999)}",
            "empresa_nome": rd(empresas),
            "empresa_cnpj": rd(cnpjs),
            "contato_nome": f"{nome} {sob}",
            "contato_email": remail(nome, sob),
            "contato_telefone": rd(fones),
            "valor_contrato": ramount(10000, 5000000),
            "data_inicio": rdate(2020, 2023),
            "data_fim": rdate(2024, 2027),
            "status": rd(STATUS_GERAL),
        }

    def lead_row(i):
        nome = rd(nomes); sob = rd(sobrenomes)
        return {
            "id": i, "nome": nome, "sobrenome": sob,
            "email": remail(nome, sob),
            "telefone": rd(fones),
            "empresa": rd(empresas),
            "cargo": rd(CARGOS_PT),
            "fonte": rd(FONTES_PT),
            "data_cadastro": rdate(2022, 2024),
            "status": rd(["Novo","Em contato","Qualificado","Convertido","Descartado"]),
            "interesse": rd(INTERESSES_PT),
        }

    return {
        "clientes": [row(i) for i in range(1, n+1)],
        "funcionarios": [emp_row(i) for i in range(1, n+1)],
        "contas_bancarias": [conta_row(i) for i in range(1, n+1)],
        "cartoes_credito": [cartao_row(i) for i in range(1, n+1)],
        "pedidos": [pedido_row(i) for i in range(1, n+1)],
        "prontuarios_medicos": [prontuario_row(i) for i in range(1, n+1)],
        "fornecedores": [fornecedor_row(i) for i in range(1, n+1)],
        "transacoes": [transacao_row(i) for i in range(1, n+1)],
        "logs_acesso": [log_row(i) for i in range(1, n+1)],
        "apolices_seguro": [apolice_row(i) for i in range(1, n+1)],
        "contratos": [contrato_row(i) for i in range(1, n+1)],
        "leads_marketing": [lead_row(i) for i in range(1, n+1)],
    }


def rows_es(country, doc_pf_file, doc_pj_file, city_file, n=120):
    nomes = load(country,"nombres.txt")
    apels = load(country,"apellidos.txt")
    docs  = load(country, doc_pf_file)
    docs_emp = load(country, doc_pj_file)
    cidades = load(country, city_file)
    endL1 = load(country,"direcciones_linea1.txt")
    endL2 = load(country,"direcciones_linea2.txt")
    cps   = load(country,"codigo_postal.txt")
    fones = load(country,"telefonos.txt")
    empresas = load(country,"empresas.txt")

    CITY_KEY = {"argentina":"provincia","chile":"region","mexico":"estado","panama":"provincia","colombia":"departamento"}
    CITY_LABEL = CITY_KEY.get(country, "estado")

    DOC_LABELS = {
        "argentina": ("dni","cuit"),
        "chile": ("rut","rut_empresa"),
        "mexico": ("curp","rfc"),
        "panama": ("cedula","ruc"),
        "colombia": ("cedula_cc","nit"),
    }
    doc_label, doc_emp_label = DOC_LABELS.get(country, ("documento","doc_empresa"))

    pais_nombres = {
        "argentina":"Argentina","chile":"Chile","mexico":"México","panama":"Panamá","colombia":"Colombia"
    }
    pais = pais_nombres.get(country, country.capitalize())

    def split_city(s):
        parts = s.split(",")
        return (parts[0].strip(), parts[1].strip()) if len(parts) >= 2 else (s, "")

    def row(i):
        nom = rd(nomes); ap = rd(apels)
        city, region = split_city(rd(cidades))
        return {
            "id": i, "nombre": nom, "apellido": ap,
            "email": remail(nom, ap),
            "telefono": rd(fones), doc_label: rd(docs),
            "fecha_nacimiento": rdate(), "genero": rd(GENEROS_ES),
            "estado_civil": rd(ESTADOS_CIVIL_ES),
            "direccion_linea1": rd(endL1), "direccion_linea2": rd(endL2),
            "ciudad": city, CITY_LABEL: region,
            "codigo_postal": rd(cps), "pais": pais,
        }

    def emp_row(i):
        nom = rd(nomes); ap = rd(apels)
        city, region = split_city(rd(cidades))
        return {
            "id": i, "nombre": nom, "apellido": ap,
            "email_corporativo": f"{nom.lower()}.{ap.lower()[:5]}@empresa.{country[:2]}.com".replace(" ",""),
            "email_personal": remail(nom, ap),
            "telefono": rd(fones), doc_label: rd(docs),
            "fecha_nacimiento": rdate(), "cargo": rd(CARGOS_ES),
            "departamento": rd(DEPARTS_ES),
            "salario": ramount(1500, 20000),
            "fecha_ingreso": rdate(2010, 2023),
            "direccion_linea1": rd(endL1), "direccion_linea2": rd(endL2),
            "ciudad": city, "codigo_postal": rd(cps),
            "banco": rd(BANCOS_ES), "cuenta_bancaria": rbankacct(),
        }

    def cuenta_row(i):
        nom = rd(nomes); ap = rd(apels)
        return {
            "id": i, "numero_cuenta": rbankacct(),
            "sucursal": str(ri(100, 9999)),
            "tipo_cuenta": rd(TIPOS_CUENTA_ES if country != "brasil" else TIPOS_CONTA_PT),
            "saldo": ramount(0, 100000),
            "limite": ramount(0, 50000),
            "titular": f"{nom} {ap}",
            doc_label + "_titular": rd(docs),
            "banco": rd(BANCOS_ES),
            "fecha_apertura": rdate(2010, 2023),
            "estado": rd(STATUS_ES),
        }

    def tarjeta_row(i):
        nom = rd(nomes); ap = rd(apels)
        return {
            "id": i, "numero_tarjeta": rcard(),
            "nombre_titular": f"{nom} {ap}".upper(),
            "vencimiento": f"{ri(1,12):02d}/{ri(25,30)}",
            "red": rd(REDES_ES),
            "limite": ramount(500, 30000),
            "factura_actual": ramount(0, 15000),
            "estado": rd(STATUS_ES),
            doc_label + "_titular": rd(docs),
        }

    def pedido_row(i):
        nom = rd(nomes); ap = rd(apels)
        city, _ = split_city(rd(cidades))
        return {
            "id": i,
            "numero_pedido": f"{country[:2].upper()}{ri(100000,999999)}",
            "fecha_pedido": rdate(2022, 2024),
            "nombre_cliente": f"{nom} {ap}",
            doc_label + "_cliente": rd(docs),
            "monto_total": ramount(50, 5000),
            "estado": rd(["Procesando","Enviado","Entregado","Cancelado","Devuelto"]),
            "direccion_entrega": rd(endL1),
            "complemento_entrega": rd(endL2),
            "ciudad_entrega": city,
            "codigo_postal_entrega": rd(cps),
        }

    def historial_row(i):
        nom = rd(nomes); ap = rd(apels)
        medico = rd(nomes) + " " + rd(apels)
        return {
            "id": i,
            "nombre_paciente": f"{nom} {ap}",
            doc_label + "_paciente": rd(docs),
            "fecha_nacimiento": rdate(),
            "tipo_sangre": rd(["A+","A-","B+","B-","AB+","AB-","O+","O-"]),
            "diagnostico": rd(DIAGNOSTICOS_ES),
            "medicamentos": rd(MEDICAMENTOS_ES),
            "medico_responsable": f"Dr. {medico}",
            "seguro_medico": rd(["AXA","SURA","Colsanitas","Cruz Blanca","Compensar","Particular"]),
            "fecha_consulta": rdate(2022, 2024),
        }

    def proveedor_row(i):
        return {
            "id": i,
            "nombre_empresa": rd(empresas),
            doc_emp_label: rd(docs_emp),
            "nombre_contacto": f"{rd(nomes)} {rd(apels)}",
            "email": f"contacto@{rd(empresas).split()[0].lower().replace('.','')}.com",
            "telefono": rd(fones),
            "direccion": rd(endL1),
            "ciudad": split_city(rd(cidades))[0],
            "codigo_postal": rd(cps),
            "segmento": rd(["Tecnología","Logística","Papelería","Servicios","Alimentos","Limpieza"]),
        }

    def transaccion_row(i):
        return {
            "id": i,
            "fecha_transaccion": rdt(),
            "tipo": rd(TIPOS_TRANSACAO_ES),
            "monto": ramount(1, 20000),
            "cuenta_origen": rbankacct(),
            "cuenta_destino": rbankacct(),
            "descripcion": rd(["Pago de factura","Transferencia","Compra en línea","Retiro ATM","Débito automático"]),
            "estado": rd(["Completada","Pendiente","Rechazada","Revertida"]),
            "ip_origen": rip(),
            "ubicacion": rd(cidades),
        }

    def log_row(i):
        nom = rd(nomes); ap = rd(apels)
        return {
            "id": i,
            "fecha_hora": rdt(),
            "usuario_id": ri(1, 10000),
            "email_usuario": remail(nom, ap),
            "ip_address": rip(),
            "user_agent": rd(USER_AGENTS),
            "accion": rd(ACOES_ES),
            "recurso": rd(["/api/cuenta","/api/pago","/api/extracto","/api/usuario","/api/tarjeta"]),
            "codigo_estado": rd([200,200,200,200,401,403,404,500]),
            "ubicacion": rd(cidades),
        }

    def poliza_row(i):
        nom = rd(nomes); ap = rd(apels)
        return {
            "id": i,
            "numero_poliza": f"POL{ri(1000000,9999999)}",
            "nombre_titular": f"{nom} {ap}",
            doc_label + "_titular": rd(docs),
            "fecha_nacimiento": rdate(),
            "tipo_seguro": rd(TIPOS_SEGURO_ES),
            "cobertura": ramount(50000, 1000000),
            "prima_mensual": ramount(50, 800),
            "fecha_inicio": rdate(2020, 2023),
            "fecha_fin": rdate(2024, 2028),
            "beneficiario": f"{rd(nomes)} {rd(apels)}",
        }

    def contrato_row(i):
        nom = rd(nomes); ap = rd(apels)
        return {
            "id": i,
            "numero_contrato": f"CTR{ri(100000,999999)}",
            "nombre_empresa": rd(empresas),
            doc_emp_label + "_empresa": rd(docs_emp),
            "nombre_contacto": f"{nom} {ap}",
            "email_contacto": remail(nom, ap),
            "telefono_contacto": rd(fones),
            "monto_contrato": ramount(10000, 5000000),
            "fecha_inicio": rdate(2020, 2023),
            "fecha_fin": rdate(2024, 2027),
            "estado": rd(STATUS_ES),
        }

    def lead_row(i):
        nom = rd(nomes); ap = rd(apels)
        return {
            "id": i, "nombre": nom, "apellido": ap,
            "email": remail(nom, ap),
            "telefono": rd(fones),
            "empresa": rd(empresas),
            "cargo": rd(CARGOS_ES),
            "fuente": rd(FONTES_ES),
            "fecha_registro": rdate(2022, 2024),
            "estado": rd(["Nuevo","En contacto","Calificado","Convertido","Descartado"]),
            "interes": rd(INTERESSES_ES),
        }

    return {
        "clientes": [row(i) for i in range(1, n+1)],
        "empleados": [emp_row(i) for i in range(1, n+1)],
        "cuentas_bancarias": [cuenta_row(i) for i in range(1, n+1)],
        "tarjetas_credito": [tarjeta_row(i) for i in range(1, n+1)],
        "pedidos": [pedido_row(i) for i in range(1, n+1)],
        "historiales_medicos": [historial_row(i) for i in range(1, n+1)],
        "proveedores": [proveedor_row(i) for i in range(1, n+1)],
        "transacciones": [transaccion_row(i) for i in range(1, n+1)],
        "logs_acceso": [log_row(i) for i in range(1, n+1)],
        "polizas_seguro": [poliza_row(i) for i in range(1, n+1)],
        "contratos": [contrato_row(i) for i in range(1, n+1)],
        "leads_marketing": [lead_row(i) for i in range(1, n+1)],
    }

TIPOS_CUENTA_ES = ["Corriente","Ahorro","Nómina","Inversión"]
TIPOS_TRANSACAO_ES = ["Transferencia","Pago","Retiro","Depósito","Transferencia electrónica","Débito automático"]
FONTES_ES = ["Google Ads","Facebook","LinkedIn","Referido","Sitio Web","Email","Evento","Socio"]
INTERESSES_ES = ["Crédito personal","Seguro de vida","Cuenta digital","Inversiones","Tarjeta de crédito","Financiamiento","Pensión","Cambio de divisas"]

# ─── SQL ESCAPING ─────────────────────────────────────────────────────────────

def esc(v):
    if v is None:
        return "NULL"
    s = str(v).replace("'", "''")
    return f"'{s}'"

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
            vals = ", ".join(esc(row.get(c, "")) for c in col_names)
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
            vals = ", ".join(esc(row.get(c, "")) for c in col_names)
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
            vals = ", ".join(esc(row.get(c, "")) for c in col_names)
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
        lines.append(f"/")
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
                    vals.append(esc(v))
            lines.append(f"INSERT INTO {tbl.upper()} ({col_str}) VALUES ({', '.join(vals)});")
        lines.append("")

    return "\n".join(lines)

# ─── COUNTRY CONFIGS ─────────────────────────────────────────────────────────

COUNTRY_CONFIGS = {
    "brasil": {
        "rows_fn": lambda: rows_brasil(),
        "schema": SCHEMAS_BR,
        "name": "brasil",
    },
    "argentina": {
        "rows_fn": lambda: rows_es("argentina","dni.txt","cuit.txt","ciudades_provincias.txt"),
        "schema": build_schema_es("dni","cuit","provincia"),
        "name": "argentina",
    },
    "chile": {
        "rows_fn": lambda: rows_es("chile","rut_personas.txt","rut_empresas.txt","ciudades_regiones.txt"),
        "schema": build_schema_es("rut","rut_empresa","region"),
        "name": "chile",
    },
    "mexico": {
        "rows_fn": lambda: rows_es("mexico","curp.txt","rfc.txt","ciudades_estados.txt"),
        "schema": build_schema_es("curp","rfc","estado"),
        "name": "mexico",
    },
    "panama": {
        "rows_fn": lambda: rows_es("panama","cedula.txt","ruc.txt","ciudades_provincias.txt"),
        "schema": build_schema_es("cedula","ruc","provincia"),
        "name": "panama",
    },
    "colombia": {
        "rows_fn": lambda: rows_es("colombia","cedula_cc.txt","nit.txt","ciudades_departamentos.txt"),
        "schema": build_schema_es("cedula_cc","nit","departamento"),
        "name": "colombia",
    },
}

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    for country, cfg in COUNTRY_CONFIGS.items():
        print(f"Generating {country}...", end=" ", flush=True)
        rows_dict = cfg["rows_fn"]()
        schema = cfg["schema"]
        name = cfg["name"]

        pg_sql = render_pg(name, schema, rows_dict)
        my_sql = render_mysql(name, schema, rows_dict)
        ss_sql = render_sqlserver(name, schema, rows_dict)
        ora_sql = render_oracle(name, schema, rows_dict)

        for engine, content in [("postgresql", pg_sql), ("mysql", my_sql),
                                  ("sqlserver", ss_sql), ("oracle", ora_sql)]:
            path = f"{BASE}/ddl/{engine}/{name}.sql"
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

        print("done")

    print("\nAll DDL files generated.")

if __name__ == "__main__":
    main()
