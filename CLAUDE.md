# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Fictional database for demonstrating **data masking** products. Contains realistic PII data across 15 Latin American countries, 4 database engines, and 12 tables per country. No external dependencies — both scripts use only Python 3 stdlib.

## Regenerating Data

```bash
# Seed files: 150 × .txt, 1000 lines each  (random.seed = 42)
python3 generate_seed.py

# DDL + INSERTs: 60 × .sql, ~6.8k rows/country  (random.seed = 99)
python3 generate_ddl.py
```

Change the `random.seed` value in each script to produce a different dataset.

## Directory Structure

```
generate_seed.py              ← generates countries/*/seed/*.txt
generate_ddl.py               ← generates ddl/*/*.sql
mexico_docs.py                ← CURP / RFC (persona moral) algorithms, shared by both scripts

countries/
  <country>/seed/             ← .txt seed lists for masking (1 value/line, 1000 lines)

ddl/
  postgresql/<country>.sql
  mysql/<country>.sql
  sqlserver/<country>.sql
  oracle/<country>.sql
```

## Countries, Documents, and Regional Subdivisions

| Country     | Lang | Person ID  | Company ID       | City column   | Region column  |
|-------------|------|------------|------------------|---------------|----------------|
| brasil      | PT   | cpf        | cnpj             | cidade        | estado         |
| argentina   | ES   | dni        | cuit             | ciudad        | provincia      |
| chile       | ES   | rut        | rut_empresa      | ciudad        | region         |
| mexico      | ES   | curp       | rfc              | ciudad        | estado         |
| panama      | ES   | cedula     | ruc              | ciudad        | provincia      |
| colombia    | ES   | cedula_cc  | nit              | ciudad        | departamento   |
| peru        | ES   | dni        | ruc              | ciudad        | departamento   |
| paraguay    | ES   | ci         | ruc              | ciudad        | departamento   |
| uruguay     | ES   | ci         | rut              | ciudad        | departamento   |
| ecuador     | ES   | cedula     | ruc              | ciudad        | provincia      |
| bolivia     | ES   | ci         | nit              | ciudad        | departamento   |
| venezuela   | ES   | cedula     | rif              | ciudad        | estado         |
| costa_rica  | ES   | cedula     | cedula_juridica  | ciudad        | provincia      |
| belize      | ES*  | ssn        | tin              | ciudad        | distrito       |
| el_salvador | ES   | dui        | nit              | ciudad        | departamento   |

\* Belize's official language is English; the table/column schema stays Spanish for pipeline consistency, but seed names reflect Belize's actual English/Creole/Mestizo/Garifuna demographic mix (see `generate_seed.py`'s Belize section).

**México — derived documents.** In the DDL, CURP and RFC are *computed from the
row*, not taken from the seed: the CURP comes from `nombre`, `apellido`
(two surnames, paterno + materno), `fecha_nacimiento`, `genero` (F→M, M→H)
and the residence `estado`, with a valid check digit; the supplier RFC
(persona moral, 12 chars) comes from `nombre_empresa` plus a random
incorporation date, with homoclave and check digit. The seed lists `curp.txt` /
`rfc.txt` also hold valid values (independent of any row).

**Gender.** `genero` (`M`/`F`) is derived from the first name by
`genero()` in `generate_ddl.py`: names ending in "a" are female, plus the
explicit `NOMES_FEMININOS` set. When adding names to a country's seed list,
add female names that don't end in "a" to that set.

Document columns are suffixed with their role in each table (e.g., `cpf_titular`, `dni_cliente`, `rut_paciente`, `nit_empresa`).

## Seed Files per Country

**Brasil (PT):** `nomes`, `sobrenomes`, `enderecos_linha1`, `enderecos_linha2`, `cidades_estados`, `empresas`, `cpf`, `cnpj`, `cep`, `telefones`

**Outros países (ES):** `nombres`, `apellidos`, `direcciones_linea1`, `direcciones_linea2`, `ciudades_<subdivision>`, `empresas`, `<doc_pf>`, `<doc_pj>`, `codigo_postal`, `telefonos`

## Tables (12 per country)

Row counts vary per table because the tables are related (see below). PII
columns are noted below.

| # | Brasil (PT)         | Outros países (ES)    | Rows      | Key PII columns                                          |
|---|---------------------|-----------------------|-----------|----------------------------------------------------------|
| 1 | clientes            | clientes              | 120       | email, telefone, doc pessoal, data_nascimento, endereço  |
| 2 | funcionarios        | empleados             | 120       | + salario, conta_bancaria                                |
| 3 | contas_bancarias    | cuentas_bancarias     | ~200-220  | numero_conta, saldo, doc titular                         |
| 4 | cartoes_credito     | tarjetas_credito      | ~250      | numero_cartao (PCI), nome_titular                        |
| 5 | pedidos             | pedidos               | ~600      | nome/doc cliente, endereço de entrega                    |
| 6 | prontuarios_medicos | historiales_medicos   | 96        | diagnóstico, medicamentos, tipo sanguíneo                |
| 7 | fornecedores        | proveedores           | 120       | nome_contato, email, telefone                            |
| 8 | transacoes          | transacciones         | 500       | conta_origem/destino, ip_origem                          |
| 9 | logs_acesso         | logs_acceso           | ~4100     | email_usuario, ip_address, user_agent                    |
|10 | apolices_seguro     | polizas_seguro        | ~280      | titular, doc, beneficiário, prêmio mensal                |
|11 | contratos           | contratos             | ~250      | contato nome/email/telefone, doc empresa                 |
|12 | leads_marketing     | leads_marketing       | 130       | nome, email, telefone                                    |

## Relationships (by value — no FKs or constraints in the DDL)

Every table is joined to another only by matching values (name, document,
account number, e-mail). Nothing is enforced physically, so masking can break
or preserve consistency at will.

```
clientes (120) ──┬── cartoes_credito      1..5 por cliente (todo cliente tem >= 1)
                 ├── pedidos              1..20 por cliente (todo cliente tem >= 1)
                 ├── prontuarios_medicos  0..1 por cliente (80% dos clientes)
                 ├── apolices_seguro      1..5 por cliente (todo cliente tem >= 1)
                 ├── contas_bancarias     80-100 clientes têm conta
                 └── leads_marketing      35-55 clientes viram lead
funcionarios ─── contas_bancarias         1 conta de salário cada, dados idênticos
fornecedores ─── contratos                1..5 por fornecedor
contas_bancarias ─── transacoes           conta_origem/destino sempre existem
logs_acesso ─── e-mail de todo cliente, fornecedor e funcionário (>= 10 cada)
```

Exclusion rules honored by `generate_ddl.py`:

* **Funcionários** só aparecem em `funcionarios` e na sua conta em
  `contas_bancarias` (o e-mail corporativo também vai para `logs_acesso`).
  Nome e documento de funcionário não existem em nenhuma outra tabela.
* **Fornecedores** (contatos) não são clientes nem funcionários.
* **leads_marketing** não contém funcionários nem fornecedores — apenas parte
  dos clientes mais pessoas novas.
* Nomes de médicos (`medico_responsavel`) e beneficiários de apólice também
  vêm de pools próprios, sem colidir com clientes/funcionários/fornecedores.

Identidades (nome + documento) são distribuídas por `IdentityPool` sem
repetição, o que garante essas exclusões.

## Engine-Specific DDL Notes

| Engine     | Date type  | Identifier quoting | Batch separator | Other                        |
|------------|------------|--------------------|-----------------|------------------------------|
| PostgreSQL | TIMESTAMP  | none               | —               | —                            |
| MySQL      | DATETIME   | backticks          | —               | `CREATE DATABASE`, utf8mb4   |
| SQL Server | DATETIME2  | `[brackets]`       | GO              | `CREATE DATABASE` with `IF NOT EXISTS` |
| Oracle     | TIMESTAMP  | UPPERCASE          | —               | `TO_DATE`/`TO_TIMESTAMP` in INSERTs; no `/` after the anonymous `BEGIN ... END;` block (many clients reject it) |
