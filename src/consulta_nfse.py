import os
import sys
from ctypes import *
from datetime import datetime

diretorio_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Diretorio do projeto: {diretorio_script}")

# Adiciona o caminho das DLLs ao PATH do sistema
dll_path = os.path.abspath(os.path.join(diretorio_script, r"ACBrLib\x64"))
os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']
sys.path.append(dll_path)

DATA_PATH = os.path.abspath(os.path.join(diretorio_script, "data"))
LOG_PATH = os.path.abspath(os.path.join(diretorio_script, r"data\logs"))
PATH_SALVAR_RESULTADO = os.path.join(diretorio_script, "data\\resultados")
PATH_SALVAR_NFSe = os.path.join(diretorio_script, "data\\resultados\\NFSe")
PATH_ACBRLIB = os.path.abspath(os.path.join(diretorio_script, "ACBrLib.INI"))

# VALORES PRA TROCAR DE ACORDO COM A EMPRESA QUE FOR BAIXAR
CERTIFICADO_PATH = os.path.abspath(os.path.join(diretorio_script, r"data\certs\cert.pfx"))
PASS_CERTIFICADO = "senha1234"
CODIGO_MUNICIPIO = "5201405"  # codigo ibge (nesse exemplo de aparecida de goiania)
CNPJ_EMITENTE = "00000000000000"
INSCRICAO_MUNICIPAL = "00000"

# Garante que as pastas existem
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


def carregar_dlls():
    """Carrega as DLLs necessárias na ordem correta"""
    try:
        # Lista de DLLs necessárias na ordem de carregamento
        dlls = [
            "libcrypto-1_1-x64.dll",
            "libssl-1_1-x64.dll",
            "libxml2.dll",
            "libxslt.dll",
            "libexslt.dll",
            "libiconv.dll",
            "ACBrNFSe64.dll"
        ]

        # Carrega cada DLL e verifica se foi carregada corretamente
        dll_handle = None
        for dll in dlls:
            dll_path_completo = os.path.join(dll_path, dll)
            try:
                dll_handle = CDLL(dll_path_completo)
            except Exception as e:
                print(f"Erro ao carregar DLL {dll}: {str(e)}")
                return None

        # Retorna a última DLL carregada (ACBrNFSe64)
        return dll_handle

    except Exception as e:
        print(f"Erro ao carregar DLLs: {str(e)}")
        return None


acbr = carregar_dlls()
if acbr is None:
    print("Erro ao carregar DLLs. Verifique se todas as DLLs estão presentes na pasta ACBrLib\\x64")
    sys.exit(1)


def inicializar_acbr():
    """Inicializa a biblioteca ACBr com as configurações necessárias"""
    try:
        retorno = acbr.NFSE_Inicializar(PATH_ACBRLIB.encode("utf-8"), "".encode("utf-8"))

        if retorno != 0:
            # se der erro olhar o motivo de acordo https://acbr.sourceforge.io/ACBrLib/NFSE_Inicializar.html campos de retorno, por exemplo, -1 quer dizer que deu falha pra inicializar a biblioteca
            print(f"Erro ao inicializar ACBr: {retorno}")
            sys.exit(1)

        # Configuração de logs
        acbr.NFSE_ConfigGravarValor(c_char_p(b"Principal"), "LogPath".encode("utf-8"), LOG_PATH.encode("utf-8"))
        acbr.NFSE_ConfigGravarValor(c_char_p(b"Principal"), "LogNivel".encode("utf-8"), str(4).encode("utf-8"))  # 4 = Log Completo

        # Configurações de certificado
        acbr.NFSE_ConfigGravarValor(c_char_p(b"DFe"), "ArquivoPFX".encode("utf-8"), CERTIFICADO_PATH.encode("utf-8"))
        acbr.NFSE_ConfigGravarValor(c_char_p(b"DFe"), "Senha".encode("utf-8"), PASS_CERTIFICADO.encode("utf-8"))

        # Configurações pra baixar as notas
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), "PathSchemas".encode("utf-8"), os.path.join(diretorio_script, "ACBrLib", "schemas", "NFSe").encode("utf-8"))
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), c_char_p(b"ExibirErroSchema"), c_char_p(b"1"))
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), c_char_p(b"Ambiente"), c_char_p(b"0"))
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), c_char_p(b"CodigoMunicipio"), CODIGO_MUNICIPIO.encode("utf-8"))
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), c_char_p(b"Emitente.CNPJ"), CNPJ_EMITENTE.encode("utf-8"))
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), c_char_p(b"Emitente.InscMun"), INSCRICAO_MUNICIPAL.encode("utf-8"))
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), "Timeout".encode("utf-8"), "30000".encode("utf-8"))  # 30 segundos
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), "LayoutNFSe".encode("utf-8"), "0".encode("utf-8"))  # usar versao do provedor

        # Configuração pra salvar os arquivos
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), "PathSalvar".encode("utf-8"), PATH_SALVAR_RESULTADO.encode("utf-8"))
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), "PathNFSe".encode("utf-8"), PATH_SALVAR_NFSe.encode("utf-8"))

        # Configurações SSL e criptografia
        acbr.NFSE_ConfigGravarValor(c_char_p(b"NFSe"), "SSLType".encode("utf-8"), "5".encode("utf-8"))  # 5 TLS 1.2
        acbr.NFSE_ConfigGravarValor(c_char_p(b"DFe"), "SSLCryptLib".encode("utf-8"), "1".encode("utf-8"))  # 1 cryOpenSsl
        acbr.NFSE_ConfigGravarValor(c_char_p(b"DFe"), "SSLHttpLib".encode("utf-8"), "3".encode("utf-8"))  # 3 httpOpenSsl
        acbr.NFSE_ConfigGravarValor(c_char_p(b"DFe"), "SSLXmlSignLib".encode("utf-8"), "4".encode("utf-8"))  # 4 xsLibXml2

        # Salva as configurações
        retorno = acbr.NFSE_ConfigGravar(PATH_ACBRLIB.encode("utf-8"))
        if retorno != 0:
            print(f"Erro ao gravar configurações. Código: {retorno}")
            return "ERRO"

    except Exception as e:
        print(f"Exceção ao inicializar ACBr: {str(e)}")
        return "ERRO"


def verificar_provedor():
    """Verifica se o que o provedor aceita de métodos, e também qual de fato é o provedor. Na pasta principal do projeto, tem um arquivo chamado ACBrNFSeXServicos.ini que lista os provedores e suas informações"""
    try:
        buffer = create_string_buffer(8192)  # Buffer maior para receber todas as informações
        tamanho = c_ulong(8192)

        # Obtém informações do provedor
        retorno = acbr.NFSE_ObterInformacoesProvedor(buffer, byref(tamanho))
        if retorno == 0:
            info_provedor = buffer.value.decode('utf-8')
            print("\nInformações do Provedor:")
            print("-" * 50)
            print(info_provedor)
            print("-" * 50)
            return True
        else:
            print(f"Erro ao obter informações do provedor. Código: {retorno}")
            return False
    except Exception as e:
        print(f"Exceção ao verificar provedor: {str(e)}")
        return False


def consultar_nfse_periodo_emitente():
    """Realiza a consulta de NFS-e por período e emitente -> https://acbr.sourceforge.io/ACBrLib/NFSE_ConsultarNFSeServicoPresta1.html"""
    try:
        tamanho_inicial = 8192
        esTamanho = c_ulong(tamanho_inicial)
        sResposta = create_string_buffer(tamanho_inicial)

        # Consulta NFS-e por período
        print("\nIniciando consulta consultar_nfse_periodo_emitente...")

        data_inicio = datetime.strptime("01/05/2025", "%d/%m/%Y")
        data_fim = datetime.strptime("20/05/2025", "%d/%m/%Y")
        ole_data_inicio = c_double((data_inicio - datetime(1899, 12, 30)).total_seconds() / (24 * 60 * 60))
        ole_data_fim = c_double((data_fim - datetime(1899, 12, 30)).total_seconds() / (24 * 60 * 60))

        acbr.NFSE_ConsultarNFSeServicoPrestadoPorPeriodo(
            ole_data_inicio,
            ole_data_fim,
            1,  # numero da pagina
            0,  # tipo periodo -> 0 = emissao
            sResposta,
            byref(esTamanho)
        )

        resposta = sResposta.value.decode('utf-8')
        print("\nResposta da consulta:")
        print("-" * 50)
        print(resposta)
        print("-" * 50)

        return resposta
    except Exception as e:
        print(f"Exceção na consulta: {str(e)}")
        return f"Erro na consulta: {str(e)}"


def consultar_nfse_por_faixa():
    """Realiza a consulta de NFS-e por faixa -> https://acbr.sourceforge.io/ACBrLib/NFSE_ConsultarNFSePorFaixa.html"""
    try:
        tamanho_inicial = 8192
        esTamanho = c_ulong(tamanho_inicial)
        sResposta = create_string_buffer(tamanho_inicial)

        # Consulta NFS-e por período
        print("\nIniciando consulta consultar_nfse_por_faixa")

        retorno = acbr.NFSE_ConsultarNFSePorFaixa(
            b'5450',  # numero nf inicial
            b'5465',  # numero nf final
            1,  # numero da pagina
            sResposta,
            byref(esTamanho)
        )
        print(f"Código de retorno: {retorno}")

        # # Obtém o último erro após a consulta
        # acbr.NFSE_UltimoRetorno(buffer_erro, byref(tamanho_erro))
        # print(f"Último retorno após a consulta: {buffer_erro.value.decode('utf-8')}")

        # if retorno != 0:
        #     print(f"Erro na consulta. Código: {retorno}")
        #     return f"Erro na consulta: {retorno}"

        resposta = sResposta.value.decode('utf-8')
        print("\nResposta da consulta:")
        print("-" * 50)
        print(resposta)
        print("-" * 50)

        return resposta
    except Exception as e:
        print(f"Exceção na consulta: {str(e)}")
        return f"Erro na consulta: {str(e)}"


def main():
    try:
        inicializar_acbr()
        # consultar_nfse_periodo_emitente()
        consultar_nfse_por_faixa()
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
    finally:
        acbr.NFSE_Finalizar()


if __name__ == "__main__":
    main()
