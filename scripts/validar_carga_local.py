import argparse
import ipaddress
import math
import os
import statistics
import sys
import threading
import time
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import urlopen


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

ROTAS = (
    ("/", "Turismo de Picuí"),
    ("/guia/", "Guia Turístico de Picuí"),
    ("/mapa/", "Mapa Turístico de Picuí"),
)


@contextmanager
def iniciar_servidor_local():
    import django

    django.setup()

    from django.core.servers.basehttp import ThreadedWSGIServer, WSGIRequestHandler
    from django.core.wsgi import get_wsgi_application
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor

    executor = MigrationExecutor(connection)
    plano = executor.migration_plan(executor.loader.graph.leaf_nodes())
    if plano:
        raise RuntimeError(
            "Há migrações pendentes. Rode "
            ".\\venv\\Scripts\\python.exe manage.py migrate antes do teste."
        )

    class ServidorDeTeste(ThreadedWSGIServer):
        request_queue_size = 256

    class ManipuladorDeTeste(WSGIRequestHandler):
        def log_message(self, formato, *argumentos):
            status = argumentos[1] if len(argumentos) > 1 else ""
            if not str(status).startswith("200"):
                super().log_message(formato, *argumentos)

    servidor = ServidorDeTeste(
        ("127.0.0.1", 0),
        ManipuladorDeTeste,
    )
    servidor.set_app(get_wsgi_application())
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{servidor.server_port}"
    finally:
        servidor.shutdown()
        servidor.server_close()
        thread.join(timeout=5)


def validar_url_local(url):
    partes = urlsplit(url)
    if (
        partes.scheme != "http"
        or not partes.hostname
        or partes.username
        or partes.password
        or partes.query
        or partes.fragment
    ):
        raise ValueError("A URL deve usar http e apontar para localhost ou 127.0.0.0/8.")

    host = partes.hostname.lower()
    if host != "localhost":
        try:
            endereco = ipaddress.ip_address(host)
        except ValueError as exc:
            raise ValueError("O teste só pode acessar localhost ou 127.0.0.0/8.") from exc
        if not endereco.is_loopback:
            raise ValueError("O teste só pode acessar localhost ou 127.0.0.0/8.")

    return url.rstrip("/")


def acessar_rota(base_url, caminho, texto_esperado):
    inicio = time.perf_counter()
    try:
        with urlopen(f"{base_url}{caminho}", timeout=20) as resposta:
            status = resposta.status
            corpo = resposta.read().decode("utf-8", errors="replace")
    except HTTPError as erro:
        status = erro.code
        corpo = erro.read().decode("utf-8", errors="replace")
    except (TimeoutError, URLError, OSError) as erro:
        return caminho, None, time.perf_counter() - inicio, str(erro)

    duracao = time.perf_counter() - inicio
    if status != 200:
        return caminho, status, duracao, f"HTTP {status}"
    if texto_esperado not in corpo:
        return caminho, status, duracao, "Conteúdo esperado não encontrado"
    return caminho, status, duracao, None


def simular_cliente(base_url):
    return [
        acessar_rota(base_url, caminho, texto)
        for caminho, texto in ROTAS
    ]


def percentil(valores, percentual):
    ordenados = sorted(valores)
    indice = max(0, math.ceil(len(ordenados) * percentual) - 1)
    return ordenados[indice]


def executar_carga(base_url, quantidade_clientes):
    inicio = time.perf_counter()
    resultados = []

    with ThreadPoolExecutor(max_workers=quantidade_clientes) as executor:
        tarefas = [
            executor.submit(simular_cliente, base_url)
            for _ in range(quantidade_clientes)
        ]
        for tarefa in as_completed(tarefas):
            resultados.extend(tarefa.result())

    duracao_total = time.perf_counter() - inicio
    falhas = [resultado for resultado in resultados if resultado[3]]
    latencias = [resultado[2] for resultado in resultados]

    print(
        f"\n{quantidade_clientes} clientes simultâneos | "
        f"{len(resultados)} requisições | {duracao_total:.2f}s"
    )
    print(
        f"Latência: média {statistics.mean(latencias):.3f}s | "
        f"p95 {percentil(latencias, 0.95):.3f}s | "
        f"máxima {max(latencias):.3f}s"
    )

    for caminho, _ in ROTAS:
        amostra = [resultado for resultado in resultados if resultado[0] == caminho]
        codigos = sorted({str(resultado[1]) for resultado in amostra})
        media = statistics.mean(resultado[2] for resultado in amostra)
        print(f"  {caminho}: HTTP {', '.join(codigos)} | média {media:.3f}s")

    for caminho, status, _, erro in falhas[:10]:
        print(f"  FALHA {caminho}: {erro} (HTTP {status})")

    return not falhas


def main():
    parser = argparse.ArgumentParser(
        description="Teste controlado de carga para o servidor Django local."
    )
    parser.add_argument(
        "--url",
        help="URL local de um servidor já iniciado; sem esta opção, inicia um servidor temporário.",
    )
    parser.add_argument(
        "--clients",
        nargs="+",
        type=int,
        default=[50, 100],
        help="Quantidade de clientes simultâneos (padrão: 50 100).",
    )
    args = parser.parse_args()

    if any(quantidade < 1 or quantidade > 100 for quantidade in args.clients):
        parser.error("A quantidade deve estar entre 1 e 100 clientes.")

    try:
        if args.url:
            base_url = validar_url_local(args.url)
            sucesso = all(
                executar_carga(base_url, quantidade)
                for quantidade in args.clients
            )
        else:
            with iniciar_servidor_local() as base_url:
                print(f"Servidor temporário iniciado em {base_url}")
                sucesso = True
                for quantidade in args.clients:
                    sucesso = executar_carga(base_url, quantidade) and sucesso
    except (RuntimeError, ValueError) as erro:
        parser.error(str(erro))

    if not sucesso:
        raise SystemExit(1)

    print("\nTeste concluído: todas as páginas responderam com HTTP 200.")


if __name__ == "__main__":
    main()
