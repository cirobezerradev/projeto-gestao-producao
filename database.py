import sqlite3
from contextlib import contextmanager
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("producao_db")


def conectar_banco():
    conexao = sqlite3.connect(DATABASE_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute(
        """
        CREATE TABLE IF NOT EXISTS producao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setor TEXT NOT NULL,
            pecas_produzidas INTEGER NOT NULL,
            pecas_rejeitadas INTEGER NOT NULL,
            custo_unitario REAL NOT NULL
        )
        """
    )
    return conexao


@contextmanager
def _conexao_gerenciada():
    conexao = conectar_banco()
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def inicializar_banco():
    conexao = conectar_banco()
    conexao.close()


def cadastrar_registro_producao(
    setor, pecas_produzidas, pecas_rejeitadas, custo_unitario
):
    with _conexao_gerenciada() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO producao (
                setor, pecas_produzidas, pecas_rejeitadas, custo_unitario
            ) VALUES (?, ?, ?, ?)
            """,
            (setor, pecas_produzidas, pecas_rejeitadas, custo_unitario),
        )
        return cursor.lastrowid


def listar_registros_producao():
    with _conexao_gerenciada() as conexao:
        registros = conexao.execute(
            "SELECT * FROM producao ORDER BY id"
        ).fetchall()
        return [dict(registro) for registro in registros]


def consultar_registro_por_id(registro_id):
    with _conexao_gerenciada() as conexao:
        registro = conexao.execute(
            "SELECT * FROM producao WHERE id = ?", (registro_id,)
        ).fetchone()
        return dict(registro) if registro else None


def atualizar_registro_producao(
    registro_id,
    setor=None,
    pecas_produzidas=None,
    pecas_rejeitadas=None,
    custo_unitario=None,
):
    with _conexao_gerenciada() as conexao:
        cursor = conexao.execute(
            """
            UPDATE producao
            SET setor = COALESCE(?, setor),
                pecas_produzidas = COALESCE(?, pecas_produzidas),
                pecas_rejeitadas = COALESCE(?, pecas_rejeitadas),
                custo_unitario = COALESCE(?, custo_unitario)
            WHERE id = ?
            """,
            (
                setor,
                pecas_produzidas,
                pecas_rejeitadas,
                custo_unitario,
                registro_id,
            ),
        )
        return cursor.rowcount > 0


def excluir_registro_producao(registro_id):
    with _conexao_gerenciada() as conexao:
        cursor = conexao.execute(
            "DELETE FROM producao WHERE id = ?", (registro_id,)
        )
        return cursor.rowcount > 0


def indicar_producao():
    with _conexao_gerenciada() as conexao:
        totais = conexao.execute(
            """
            SELECT
                COUNT(*) AS total_registros,
                COALESCE(SUM(pecas_produzidas), 0) AS pecas_produzidas,
                COALESCE(SUM(pecas_rejeitadas), 0) AS pecas_rejeitadas
            FROM producao
            """
        ).fetchone()

    indicadores = dict(totais)
    pecas_produzidas = indicadores["pecas_produzidas"]
    pecas_rejeitadas = indicadores["pecas_rejeitadas"]
    indicadores["taxa_rejeicao_percentual"] = (
        pecas_rejeitadas / pecas_produzidas * 100 if pecas_produzidas else 0
    )
    return indicadores


if __name__ == "__main__":
    inicializar_banco()