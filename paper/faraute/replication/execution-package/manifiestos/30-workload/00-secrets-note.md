# Credenciales (Camino B — solo CNPG)

- El operador CNPG crea automaticamente el secret `pglab-cnpg-exp-app`
  (usuario `lab`, base de datos `labdb`) al desplegar el cluster.
  Cadena rw: host=`pglab-cnpg-exp-rw.pg-chaos-lab.svc` puerto 5432.
- Los pods de carga (`pgbench-cnpg`) y verificacion (`tx-verifier-cnpg`) leen la
  password de ese secret (ver el bloque `env` de cada manifiesto).

No se usan credenciales de Zalando: Camino B no despliega ese operador.
