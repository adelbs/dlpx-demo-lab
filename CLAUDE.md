# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Fictional database for demonstrating **data masking** products. Contains realistic PII data across 15 Latin American countries, 4 database engines, and 12 tables per country. No external dependencies — both scripts use only Python 3 stdlib.

## Regenerating Data

```bash
# Seed files: 150 × .txt, 1000 lines each  (random.seed = 42)
python3 generate_seed.py

# DDL + INSERTs: 60 × .sql, 120 rows/table  (random.seed = 99)
python3 generate_ddl.py
```

Change the `random.seed` value in each script to produce a different dataset.

## Directory Structure

```
generate_seed.py              ← generates countries/*/seed/*.txt
generate_ddl.py               ← generates ddl/*/*.sql

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

Document columns are suffixed with their role in each table (e.g., `cpf_titular`, `dni_cliente`, `rut_paciente`, `nit_empresa`).

## Seed Files per Country

**Brasil (PT):** `nomes`, `sobrenomes`, `enderecos_linha1`, `enderecos_linha2`, `cidades_estados`, `empresas`, `cpf`, `cnpj`, `cep`, `telefones`

**Outros países (ES):** `nombres`, `apellidos`, `direcciones_linea1`, `direcciones_linea2`, `ciudades_<subdivision>`, `empresas`, `<doc_pf>`, `<doc_pj>`, `codigo_postal`, `telefonos`

## Tables (12 per country)

All tables have 120 rows. PII columns are noted below.

| # | Brasil (PT)         | Outros países (ES)    | Key PII columns                                          |
|---|---------------------|-----------------------|----------------------------------------------------------|
| 1 | clientes            | clientes              | email, telefone, doc pessoal, data_nascimento, endereço  |
| 2 | funcionarios        | empleados             | + salario, conta_bancaria                                |
| 3 | contas_bancarias    | cuentas_bancarias     | numero_conta, saldo, doc titular                         |
| 4 | cartoes_credito     | tarjetas_credito      | numero_cartao (PCI), nome_titular                        |
| 5 | pedidos             | pedidos               | nome/doc cliente, endereço de entrega                    |
| 6 | prontuarios_medicos | historiales_medicos   | diagnóstico, medicamentos, tipo sanguíneo                |
| 7 | fornecedores        | proveedores           | nome_contato, email, telefone                            |
| 8 | transacoes          | transacciones         | conta_origem/destino, ip_origem                          |
| 9 | logs_acesso         | logs_acceso           | email_usuario, ip_address, user_agent                    |
|10 | apolices_seguro     | polizas_seguro        | titular, doc, beneficiário, prêmio mensal                |
|11 | contratos           | contratos             | contato nome/email/telefone, doc empresa                 |
|12 | leads_marketing     | leads_marketing       | nome, email, telefone                                    |

## Engine-Specific DDL Notes

| Engine     | Date type  | Identifier quoting | Batch separator | Other                        |
|------------|------------|--------------------|-----------------|------------------------------|
| PostgreSQL | TIMESTAMP  | none               | —               | —                            |
| MySQL      | DATETIME   | backticks          | —               | `CREATE DATABASE`, utf8mb4   |
| SQL Server | DATETIME2  | `[brackets]`       | GO              | `CREATE DATABASE` with `IF NOT EXISTS` |
| Oracle     | TIMESTAMP  | UPPERCASE          | /               | `TO_DATE`/`TO_TIMESTAMP` in INSERTs |
