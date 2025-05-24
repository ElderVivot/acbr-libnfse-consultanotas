# ACBRLibNFSe Consulta de Notas das Prefeituras

## Descrição

Projeto exemplo em Python pra Consulta de Notas das Prefeituras. No site https://svn.code.sf.net/p/acbr/code/trunk2/Projetos/ACBrLib/Demos/Python/ não tem nenhum exemplo nessa linguagem com essa finalidade

## Principais Tecnologias Utilizadas

- Python 3.11
- Projeto ACBR

## Como executar o projeto localmente

1. Clonar o repositório
2. Executar o comando `poetry install` para instalar as dependências
3. Executar o comando `poetry shell` para ativar o ambiente virtual
4. Executar o comando `python src/consulta_nfse.py` para executar
5. OBS.: Na arquivo consulta_nfse.py tem que informar os dados que estão logo abaixo do comentário "# VALORES PRA TROCAR DE ACORDO COM A EMPRESA QUE FOR BAIXAR"

## Estrutura do Projeto (AWS)

1. Pasta ACBrLib tem:
    - schemas da prefeitura que são necessários baixados direto do projeto exemplo
    - x64 com as dlss do projeto exemplo (usando a opção do Single Thread ST)
2. Pasta src com os códigos das consultas
3. Arquivo ACbrLib.INI arquivo de inicialização do projeto