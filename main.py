import database


def ler_dados_producao():
    setor = input('Setor: ').strip()
    pecas_produzidas = int(input('Peças produzidas: '))
    pecas_rejeitadas = int(input('Peças rejeitadas: '))
    custo_unitario = float(input('Custo unitário: '))
    return setor, pecas_produzidas, pecas_rejeitadas, custo_unitario


def ler_dados_atualizacao():
    setor = input('Setor (Enter mantém o atual): ').strip() or None
    produzidas = input('Peças produzidas (Enter mantém o atual): ').strip()
    rejeitadas = input('Peças rejeitadas (Enter mantém o atual): ').strip()
    custo = input('Custo unitário (Enter mantém o atual): ').strip()
    return (
        setor,
        int(produzidas) if produzidas else None,
        int(rejeitadas) if rejeitadas else None,
        float(custo) if custo else None,
    )


def exibir_registro(registro):
    print(
        f"ID: {registro['id']} | Setor: {registro['setor']} | "
        f"Produzidas: {registro['pecas_produzidas']} | "
        f"Rejeitadas: {registro['pecas_rejeitadas']} | "
        f"Custo unitário: R$ {registro['custo_unitario']:.2f}"
    )


def main():
    database.inicializar_banco()

    while True:
        print('===== CONTROLE DE PRODUÇÃO =====')
        print('1. Cadastrar Registro de Produção')
        print('2. Listar Registros de Produção')
        print('3. Consultar Registro por ID')
        print('4. Atualizar Registro de Produção')
        print('5. Excluir Registro de Produção')
        print('6. Indicar Produção')
        print('0. Sair')

        try:
            opcao = int(input('Escolha uma opção: '))

            if opcao == 0:
                print('Saindo do programa...')
                break
            if opcao == 1:
                registro_id = database.cadastrar_registro_producao(
                    *ler_dados_producao()
                )
                print(f'Registro cadastrado com ID {registro_id}.')
            elif opcao == 2:
                registros = database.listar_registros_producao()
                if not registros:
                    print('Nenhum registro de produção encontrado.')
                else:
                    for registro in registros:
                        exibir_registro(registro)
            elif opcao == 3:
                registro_id = int(input('ID do registro: '))
                registro = database.consultar_registro_por_id(registro_id)
                if registro:
                    exibir_registro(registro)
                else:
                    print('Registro não encontrado.')
            elif opcao == 4:
                registro_id = int(input('ID do registro: '))
                registro = database.consultar_registro_por_id(registro_id)
                if not registro:
                    print('Registro não encontrado.')
                    continue
                exibir_registro(registro)
                dados = ler_dados_atualizacao()
                if all(valor is None for valor in dados):
                    print('Nenhum atributo alterado.')
                elif database.atualizar_registro_producao(registro_id, *dados):
                    print('Registro atualizado com sucesso.')
            elif opcao == 5:
                registro_id = int(input('ID do registro: '))
                if database.excluir_registro_producao(registro_id):
                    print('Registro excluído com sucesso.')
                else:
                    print('Registro não encontrado.')
            elif opcao == 6:
                indicadores = database.indicar_producao()
                print(f"Registros cadastrados: {indicadores['total_registros']}")
                print(f"Peças produzidas: {indicadores['pecas_produzidas']}")
                print(f"Peças rejeitadas: {indicadores['pecas_rejeitadas']}")
                print(
                    "Taxa de rejeição: "
                    f"{indicadores['taxa_rejeicao_percentual']:.2f}%"
                )
            else:
                print('Opção inválida.')
        except ValueError:
            print('Entrada inválida. Informe um número no formato correto.')


if __name__ == '__main__':
    main()