#!/usr/bin/env python3
"""Tests for check_vault.py (VAULT-STARTER v4, section 9).

Standard library only, so CI needs nothing but Python:

    python3 scripts/test_check_vault.py

The suite follows the method's own rule from section 8.5: a green report is
not a measurement. The demo vault passing proves little on its own, so every
defect the auditor claims to detect is also built on purpose in a temporary
vault, and the test asserts the auditor reports it. If one of those controls
stops firing, a green run on a real vault means nothing.

Every case drives the real CLI through a subprocess and reads its --json
output, so the entry point and argument parsing are exercised too.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
SCRIPT = os.path.join(AQUI, "check_vault.py")
EXAMPLES = os.path.join(REPO, "examples")

# The auditor estimates tokens as bytes // 4.
def bytes_para(tokens):
    return "x" * (tokens * 4 + 4)


def auditar(root, *extra):
    r = subprocess.run([sys.executable, SCRIPT, root, "--json", *extra],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise AssertionError(f"check_vault.py exited {r.returncode}:\n{r.stderr}")
    return json.loads(r.stdout)


def mensajes(reporte):
    todos = list(reporte["hallazgos"])
    for eje in reporte["ejes"]:
        todos += eje["hallazgos"]
    return [(h["nivel"], h["msg"]) for h in todos]


def escribir(root, rel, texto):
    ruta = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    return ruta


def vault_minimo(root, eje="Vault", current_state="# Current State\n2026-09-11\n"):
    """The smallest axis the auditor accepts without axis-level findings."""
    escribir(root, f"{eje}/20-State/Current-State.md", current_state)
    escribir(root, f"{eje}/SCHEMA.md", "# SCHEMA\n")
    escribir(root, f"{eje}/LOG.md", "# LOG\n")
    escribir(root, f"{eje}/00-Index.md", "# Index\n")


class ConVaultTemporal(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="vault-test-")
        escribir(self.root, "CLAUDE.md", "# rules\n")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)


class DemoVault(unittest.TestCase):
    """The shipped fixture must stay green and clean."""

    def test_fixture_is_green_with_one_axis(self):
        r = auditar(EXAMPLES)
        self.assertEqual([e["nombre"] for e in r["ejes"]], ["demo-vault"])
        self.assertEqual(r["arranque_semaforo"], "verde")
        self.assertEqual(r["techos"], r["techos_default"])

    def test_fixture_has_no_axis_findings(self):
        r = auditar(EXAMPLES)
        self.assertEqual(r["ejes"][0]["hallazgos"], [])

    def test_fixture_pieces_are_discovered_by_name(self):
        roles = {p["rol"] for p in auditar(EXAMPLES)["ejes"][0]["piezas"]}
        self.assertEqual(roles, {"current-state", "log", "index", "lecciones", "metodo"})


class Controles(ConVaultTemporal):
    """Each defect built on purpose. If one of these stops firing, the
    auditor has gone blind to it and a green report proves nothing."""

    def test_clean_minimal_vault_has_no_axis_findings(self):
        # Baseline for the controls below: same builder, no defect.
        vault_minimo(self.root)
        r = auditar(self.root)
        self.assertEqual(r["ejes"][0]["hallazgos"], [])

    def test_current_state_over_ceiling(self):
        vault_minimo(self.root, current_state=bytes_para(2600))
        r = auditar(self.root)
        estado = r["ejes"][0]["piezas"][0]
        self.assertEqual(estado["rol"], "current-state")
        self.assertIn("sobre_techo", estado)
        self.assertTrue(any("supera el techo" in m for _, m in mensajes(r)))

    def test_log_over_ceiling(self):
        vault_minimo(self.root)
        escribir(self.root, "Vault/LOG.md", bytes_para(40100))
        r = auditar(self.root)
        self.assertTrue(any("LOG-Archivo" in m for _, m in mensajes(r)))

    def test_two_entry_points_in_one_axis(self):
        vault_minimo(self.root)
        escribir(self.root, "Vault/20-State/viejo/Current-State.md", "# dup\n")
        r = auditar(self.root)
        self.assertTrue(any("2 archivos Current-State.md" in m for _, m in mensajes(r)))

    def test_moved_ceiling_is_reported_and_applied(self):
        vault_minimo(self.root)
        escribir(self.root, "vault-config.json",
                 json.dumps({"techos": {"current_state": 3000}}))
        r = auditar(self.root)
        self.assertEqual(r["techos"]["current_state"], 3000)
        self.assertTrue(any("TECHO MODIFICADO" in m for _, m in mensajes(r)))

    def test_startup_traffic_light_turns_amber_then_red(self):
        vault_minimo(self.root)
        escribir(self.root, "CLAUDE.md", bytes_para(12000))
        self.assertEqual(auditar(self.root)["arranque_semaforo"], "amarillo")
        escribir(self.root, "CLAUDE.md", bytes_para(31000))
        self.assertEqual(auditar(self.root)["arranque_semaforo"], "rojo")

    def test_imports_count_toward_startup_and_missing_ones_are_errors(self):
        vault_minimo(self.root)
        escribir(self.root, "docs/big.md", bytes_para(12000))
        escribir(self.root, "CLAUDE.md", "# rules\n@docs/big.md\n@docs/gone.md\n")
        r = auditar(self.root)
        self.assertGreaterEqual(r["imports_tokens"], 12000)
        self.assertEqual(r["arranque_semaforo"], "amarillo")
        self.assertIn(("error", "@docs/gone.md se auto-carga pero no existe."), mensajes(r))

    def test_axis_without_method_file(self):
        vault_minimo(self.root)
        os.remove(os.path.join(self.root, "Vault", "SCHEMA.md"))
        self.assertTrue(any("Sin SCHEMA.md" in m for _, m in mensajes(auditar(self.root))))

    def test_no_entry_point_at_all(self):
        self.assertIn(("error", "No se encontro ningun Current-State.md."),
                      mensajes(auditar(self.root)))


class MultiEje(ConVaultTemporal):
    """Section 3.6: several independent vaults, measured separately."""

    def setUp(self):
        super().setUp()
        vault_minimo(self.root, eje="Juego")
        vault_minimo(self.root, eje="Cartera", current_state=bytes_para(12000))

    def test_axes_are_discovered_and_worst_case_rules(self):
        r = auditar(self.root)
        self.assertEqual(sorted(e["nombre"] for e in r["ejes"]), ["Cartera", "Juego"])
        self.assertEqual(r["arranque_semaforo"], "amarillo")
        self.assertTrue(any(n == "info" and "multi-eje" in m for n, m in mensajes(r)))

    def test_axis_filter_measures_only_that_axis(self):
        r = auditar(self.root, "--eje", "juego")
        self.assertEqual([e["nombre"] for e in r["ejes"]], ["Juego"])
        self.assertEqual(r["arranque_semaforo"], "verde")


@unittest.skipUnless(shutil.which("git"), "git not installed")
class Privacidad(ConVaultTemporal):
    """A private file that git would commit is the one error that leaks data."""

    def setUp(self):
        super().setUp()
        vault_minimo(self.root)
        escribir(self.root, "Vault/20-State/Notas-Privadas.md", "secret\n")
        subprocess.run(["git", "init", "-q", self.root], check=True)

    def fugas(self):
        return [m for n, m in mensajes(auditar(self.root)) if n == "error" and "FUGA" in m]

    def test_unignored_private_file_is_a_leak(self):
        self.assertEqual(len(self.fugas()), 1)

    def test_ignored_private_file_is_not_a_leak(self):
        escribir(self.root, ".gitignore", "Notas-Privadas*\n")
        self.assertEqual(self.fugas(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
