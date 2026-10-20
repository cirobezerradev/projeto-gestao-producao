import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database
import main


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path_patch = patch.object(
            database,
            "DATABASE_PATH",
            Path(self.temp_dir.name) / "producao_teste.db",
        )
        self.database_path_patch.start()
        database.inicializar_banco()

    def tearDown(self):
        self.database_path_patch.stop()
        self.temp_dir.cleanup()

    def criar_registro(self):
        return database.cadastrar_registro_producao(
            "Montagem", 100, 10, 2.5
        )

    def test_cadastrar_listar_e_consultar_registro(self):
        registro_id = self.criar_registro()

        esperado = {
            "id": registro_id,
            "setor": "Montagem",
            "pecas_produzidas": 100,
            "pecas_rejeitadas": 10,
            "custo_unitario": 2.5,
        }
        self.assertEqual(database.consultar_registro_por_id(registro_id), esperado)
        self.assertEqual(database.listar_registros_producao(), [esperado])
        self.assertIsNone(database.consultar_registro_por_id(999))

    def test_atualizacao_parcial_preserva_campos_vazios_e_aceita_zero(self):
        registro_id = self.criar_registro()

        atualizado = database.atualizar_registro_producao(
            registro_id, pecas_produzidas=0
        )

        self.assertTrue(atualizado)
        self.assertEqual(
            database.consultar_registro_por_id(registro_id),
            {
                "id": registro_id,
                "setor": "Montagem",
                "pecas_produzidas": 0,
                "pecas_rejeitadas": 10,
                "custo_unitario": 2.5,
            },
        )
        self.assertFalse(database.atualizar_registro_producao(999, setor="Corte"))

    def test_excluir_registro(self):
        registro_id = self.criar_registro()

        self.assertTrue(database.excluir_registro_producao(registro_id))
        self.assertFalse(database.excluir_registro_producao(registro_id))
        self.assertEqual(database.listar_registros_producao(), [])

    def test_indicadores_sem_registros(self):
        self.assertEqual(
            database.indicar_producao(),
            {
                "total_registros": 0,
                "pecas_produzidas": 0,
                "pecas_rejeitadas": 0,
                "taxa_rejeicao_percentual": 0,
            },
        )

    def test_indicadores_agregam_registros(self):
        self.criar_registro()
        database.cadastrar_registro_producao("Pintura", 300, 15, 1.25)

        self.assertEqual(
            database.indicar_producao(),
            {
                "total_registros": 2,
                "pecas_produzidas": 400,
                "pecas_rejeitadas": 25,
                "taxa_rejeicao_percentual": 6.25,
            },
        )

    def test_campos_vazios_na_atualizacao_sao_preservados(self):
        with patch("builtins.input", side_effect=["", "0", " ", ""]):
            dados = main.ler_dados_atualizacao()

        self.assertEqual(dados, (None, 0, None, None))


if __name__ == "__main__":
    unittest.main()