import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def testar_newton():
    url = f"{BASE_URL}/newton"
    dados = {
        "funcao": "x**3 - x - 2",
        "x0": 1.5,
        "tolerancia": 0.0001,
        "max_iter": 20
    }
    resp = requests.post(url, json=dados)
    print("\n=== NEWTON ===")
    print("Status:", resp.status_code)
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

def testar_bissecao():
    url = f"{BASE_URL}/bissecao"
    dados = {
        "funcao": "x**3 - x - 2",
        "a": 1,
        "b": 2,
        "tolerancia": 0.0001,
        "max_iter": 50
    }
    resp = requests.post(url, json=dados)
    print("\n=== BISSEÇÃO ===")
    print("Status:", resp.status_code)
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

def testar_gauss():
    url = f"{BASE_URL}/gauss"
    dados = {
        "matriz": [
            [2, 3, 8],   # 2x + 3y = 8
            [1, -1, 0]   # 1x - 1y = 0
        ],
        "usar_pivoteamento": True
    }
    resp = requests.post(url, json=dados)
    print("\n=== GAUSS ===")
    print("Status:", resp.status_code)
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    testar_newton()
    testar_bissecao()
    testar_gauss()
