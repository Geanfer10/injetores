#!/usr/bin/env python3
"""
Busca os itens do board "Controle de Troca de Filtros dos Injetores" no
Monday.com e grava data.json na raiz do repositório para o painel HTML ler.

Requer a variável de ambiente MONDAY_API_TOKEN (definida como secret do
repositório no GitHub Actions).
"""

import json
import os
import sys
from datetime import datetime, timezone

import requests

BOARD_ID = 18426569141
API_URL = "https://api.monday.com/v2"

COLUMN_IDS = [
    "text_mm67rksy",  # Tag
    "text_mm67x2pz",  # Quantidade
    "color_mm67127w",  # Frequência
    "date_mm675wvh",  # Última Execução
    "date_mm678xmf",  # Próxima Execução
    "color_mm67y1nf",  # Status da Troca
    "text_mm67d2c5",  # Responsável pela Troca
    "text_mm674x81",  # Ordem de Manutenção
]

QUERY = """
query ($boardId: [ID!], $columnIds: [String!]) {
  boards(ids: $boardId) {
    items_page(limit: 200) {
      items {
        id
        name
        column_values(ids: $columnIds) {
          id
          text
        }
      }
    }
  }
}
"""


def fetch_items(token: str):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    payload = {
        "query": QUERY,
        "variables": {"boardId": [BOARD_ID], "columnIds": COLUMN_IDS},
    }
    resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    body = resp.json()

    if "errors" in body:
        raise RuntimeError(f"Erro na API do Monday: {body['errors']}")

    boards = body["data"]["boards"]
    if not boards:
        raise RuntimeError("Board não encontrado — verifique o BOARD_ID e o token.")

    return boards[0]["items_page"]["items"]


def qtd_to_int(text):
    if not text:
        return 0
    digits = "".join(ch for ch in text if ch.isdigit())
    return int(digits) if digits else 0


def transform(items):
    result = []
    for item in items:
        cols = {c["id"]: c["text"] for c in item["column_values"]}
        result.append(
            {
                "local": item["name"],
                "tag": cols.get("text_mm67rksy") or "",
                "qtd": qtd_to_int(cols.get("text_mm67x2pz")),
                "freq": cols.get("color_mm67127w") or "",
                "ultima": cols.get("date_mm675wvh") or None,
                "proxima": cols.get("date_mm678xmf") or None,
                "status": cols.get("color_mm67y1nf") or "Pendente",
                "responsavel": cols.get("text_mm67d2c5") or None,
                "om": cols.get("text_mm674x81") or None,
            }
        )
    return result


def main():
    token = os.environ.get("MONDAY_API_TOKEN")
    if not token:
        print("ERRO: variável de ambiente MONDAY_API_TOKEN não definida.", file=sys.stderr)
        sys.exit(1)

    items = fetch_items(token)
    data = transform(items)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "board_id": BOARD_ID,
        "items": data,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"OK: {len(data)} itens gravados em data.json")


if __name__ == "__main__":
    main()
