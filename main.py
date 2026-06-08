import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração de CORS para permitir que seu sistema principal acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, troque pelo domínio do seu site
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega a TACO uma única vez ao iniciar
with open("taco.json", "r", encoding="utf-8") as f:
    taco_data = json.load(f)

@app.get("/buscar/{termo}")
def buscar_alimento(termo: str):
    # Exemplo simples de busca
    resultados = [a for a in taco_data if termo.lower() in a["nome_busca"].lower()]
    return {"resultados": resultados[:10]} # Limita a 10 para não poluir