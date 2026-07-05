#!/usr/bin/env python3
# dry-run-selectores.py — Dry-run de selectores DERIVADO DEL MANIFIESTO.
#
# Lee en stdin UN objeto (JSON) ya convertido por kubectl desde un YAML de
# fallo, extrae el selector REAL del manifiesto (no uno tecleado por el
# operador), lo valida contra las invariantes del piloto y, si es válido,
# pregunta a kubectl qué pods exactos resolvería. Cualquier violación -> NO PASA.
#
# Uso (desde la raíz del paquete; Chaos Mesh ya instalado en Fase 2):
#   kubectl create --dry-run=client -o json -f manifiestos/40-experiments/f1-podkill-cnpg.yaml \
#       | python3 manifiestos/scripts/dry-run-selectores.py
#   (--dry-run=server es equivalente; client evita el webhook y basta con que
#    los CRD de Chaos Mesh estén instalados, lo cual ocurre desde la Fase 2.)
#
# Solo Python stdlib (json, sys, subprocess). Sin PyYAML, sin yq.
# Exit 0 = PASA ; Exit 1 = NO PASA (abortar, ver ABORTO.md).

import json
import subprocess
import sys

NS_LAB      = "pg-chaos-lab"
CLUSTER_KEY = "cnpg.io/cluster"
CLUSTER_VAL = "pglab-cnpg-exp"
ROLE_KEY    = "cnpg.io/instanceRole"

# Mecanismos de selección aceptados en un *Chaos. Cualquier otro
# (expressionSelectors, pods:, fieldSelectors, nodeSelectors,
# annotationSelectors...) hace que el alcance NO sea demostrable con este
# dry-run -> NO PASA por precaución (la ausencia no se lee como seguridad).
SEL_CHAOS_OK = {"namespaces", "labelSelectors"}


def fail(reason):
    print(f"  VEREDICTO: NO PASA — {reason}")
    print("  --> ABORTAR. No se inyecta nada. Ver ABORTO.md.")
    sys.exit(1)


def kubectl_pods(namespace, label_selector):
    """Pods que kubectl resuelve para (namespace, selector). Read-only."""
    out = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace,
         "-l", label_selector, "-o", "json"],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        fail(f"kubectl get pods falló en ns={namespace}: {out.stderr.strip()}")
    return json.loads(out.stdout).get("items", [])


def selector_to_arg(labels):
    return ",".join(f"{k}={v}" for k, v in sorted(labels.items()))


def check_labels(labels, where):
    """Valida el mapa de labels: clúster correcto y no rol aislado."""
    has_cluster = CLUSTER_KEY in labels
    has_role    = ROLE_KEY in labels
    if not has_cluster and has_role:
        fail(f"selector de ROL AISLADO en {where}: usa {ROLE_KEY} sin "
             f"{CLUSTER_KEY} — alcanzaría los primarios de TODOS los clústeres")
    if not has_cluster:
        fail(f"selector en {where} sin {CLUSTER_KEY} — alcance no acotado al lab")
    if labels[CLUSTER_KEY] != CLUSTER_VAL:
        fail(f"NOMBRE DE CLÚSTER ALTERADO en {where}: "
             f"{CLUSTER_KEY}={labels[CLUSTER_KEY]!r}, se esperaba {CLUSTER_VAL!r}")


def verify_pods(namespace, labels):
    """Muestra los pods resueltos y exige que todos sean del lab/exp."""
    sel = selector_to_arg(labels)
    print(f"  namespace          : {namespace}")
    print(f"  selector de labels : {sel}")
    pods = kubectl_pods(namespace, sel)
    print("  EL MANIFIESTO SELECCIONARÍA ESTOS PODS:")
    if not pods:
        print("    (ninguno)")
        fail("el manifiesto no resuelve a ningún pod; no se puede confirmar "
             "el alcance (¿está desplegado pglab-cnpg-exp?)")
    bad = []
    for p in pods:
        pns   = p["metadata"]["namespace"]
        pname = p["metadata"]["name"]
        pclus = p["metadata"].get("labels", {}).get(CLUSTER_KEY, "<sin-label>")
        node  = p["spec"].get("nodeName", "?")
        offending = (pns != NS_LAB) or (pclus != CLUSTER_VAL)
        mark = "   !!! FUERA DE ALCANCE" if offending else ""
        print(f"    {pns}/{pname}  [{CLUSTER_KEY}={pclus}]  nodo={node}{mark}")
        if offending:
            bad.append(f"{pns}/{pname}")
    if bad:
        fail(f"selecciona pods fuera de {NS_LAB}/{CLUSTER_VAL}: {', '.join(bad)}")
    print(f"  --> {len(pods)} pod(s), TODOS en {NS_LAB} y del clúster {CLUSTER_VAL}")


def main():
    obj  = json.load(sys.stdin)
    kind = obj.get("kind", "<sin-kind>")
    name = obj.get("metadata", {}).get("name", "<sin-nombre>")
    print(f"  kind: {kind}   nombre: {name}")

    if kind == "NetworkPolicy":
        # Una NetworkPolicy solo afecta pods de su PROPIO namespace.
        ns = obj.get("metadata", {}).get("namespace")
        if ns != NS_LAB:
            fail(f"NetworkPolicy en namespace {ns!r}, debe estar en {NS_LAB!r}")
        psel = obj.get("spec", {}).get("podSelector", {})
        if "matchExpressions" in psel:
            fail("podSelector usa matchExpressions — alcance no demostrable, "
                 "revísalo a mano")
        labels = psel.get("matchLabels", {})
        if not labels:
            fail("podSelector vacío — aplicaría a TODOS los pods del namespace")
        check_labels(labels, "podSelector")
        verify_pods(ns, labels)
        print("  VEREDICTO: PASA")
        return

    if kind.endswith("Chaos"):
        sel  = obj.get("spec", {}).get("selector", {})
        mode = obj.get("spec", {}).get("mode", "<sin-mode>")
        print(f"  mode: {mode}")
        extra = set(sel.keys()) - SEL_CHAOS_OK
        if extra:
            fail(f"selector usa mecanismos no soportados {sorted(extra)} — "
                 f"alcance no demostrable con este dry-run, revísalo a mano")
        nss = sel.get("namespaces", [])
        if nss != [NS_LAB]:
            fail(f"namespaces del selector = {nss}, debe ser EXACTAMENTE "
                 f"[{NS_LAB}] (¿segundo namespace añadido o namespace ajeno?)")
        labels = sel.get("labelSelectors", {})
        if not labels:
            fail(f"labelSelectors vacío — con mode={mode} alcanzaría todo el ns")
        check_labels(labels, "labelSelectors")
        verify_pods(NS_LAB, labels)
        print("  VEREDICTO: PASA")
        return

    fail(f"kind no reconocido: {kind} — este dry-run solo cubre *Chaos "
         "y NetworkPolicy")


if __name__ == "__main__":
    main()
