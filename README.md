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

## Estrutura do Projeto

1. Pasta ACBrLib tem:
    - schemas da prefeitura que são necessários baixados direto do projeto exemplo
    - x64 com as dlss do projeto exemplo (usando a opção do Single Thread ST)
2. Pasta src com os códigos das consultas
    - No arquivo consulta_nfse.py tem dois métodos de consulta, um pelo emitente passando período inicial e final. E outro passando o número da nota início e fim.
3. Arquivo ACbrLib.INI arquivo de inicialização do projeto
4. Pasta data onde deve configurar o certificado, e nela vai mostrar os logs quando executar o projeto bem como resultado da consulta

## Observações:

Lembrando que esse projeto está usando a DLL das versões demo, portanto, de acordo cita https://www.projetoacbr.com.br/forum/topic/63052-acbrlib-demo-download-livre/ é possível utilizar somente em ambiente de homologação na prefeitura, ou seja, quando consultar a nota provavelmente vai dar erro informando:
```
<ListaMensagemRetorno>
    <MensagemRetorno>
        <Codigo>E043</Codigo>
        <Mensagem>Inscrição Municipal do prestador do serviço não encontrada na base de dados do município.</Mensagem>
        <Correcao>Não existe registro de inscrição municipal que corresponda ao número informado.</Correcao>
    </MensagemRetorno>
    <MensagemRetorno>
        <Codigo>E259</Codigo>
        <Mensagem>CNPJ/CPF não encontrado na base de dados.</Mensagem>
        <Correcao>Confira o número do CNPJ/CPF informado. Caso esteja correto, o prestador do serviço não está inscrito no município.</Correcao>
    </MensagemRetorno>
    <MensagemRetorno>
        <Codigo>L090</Codigo>
        <Mensagem>Usuário não tem autorização para solicitar o serviço.</Mensagem>
        <Correcao>Apenas o prestador ou pessoas autorizadas podem solicitar este serviço.</Correcao>
    </MensagemRetorno>
</ListaMensagemRetorno>
```
Essa mensagem é apresentado porquê como a consulta não é no ambiente de produção ele não encontra a empresa. Pra resolver, precisa utilizar a DLL compilada pela versão PRO