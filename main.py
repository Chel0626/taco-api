import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. RESOLVENDO O ERRO DE CORS
# Isso avisa ao servidor que ele pode aceitar requisições do seu localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem (localhost ou seu domínio final)
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, etc.
    allow_headers=["*"],
)

# 2. CARREGANDO A TABELA TACO
# Como você disse que o arquivo já está na raiz, vamos carregá-lo na memória
try:
    with open("taco.json", "r", encoding="utf-8") as f:
        taco_data = json.load(f)
except FileNotFoundError:
    taco_data = []
    print("Aviso: Arquivo taco.json não encontrado na raiz.")

# Rota de teste
@app.get("/")
def read_root():
    return {"status": "Taco API Online", "alimentos_carregados": len(taco_data)}

# 3. RESOLVENDO O ERRO 404 (A rota de busca)
@app.get("/buscar/{termo}")
def buscar_alimento(termo: str):
    resultados = []
    
    for alimento in taco_data:
        # Pega o nome do alimento no JSON (ajuste a chave se seu json usar "nome" em vez de "nome_busca")
        nome_busca = alimento.get("nome_busca", alimento.get("nome", ""))
        
        # Se o termo digitado estiver no nome do alimento
        if termo.lower() in nome_busca.lower():
            resultados.append({
                "id": alimento.get("id", str(len(resultados))),
                "nome_exibicao": alimento.get("nome_exibicao", nome_busca),
                "cho": alimento.get("cho", 0),
                "ptn": alimento.get("ptn", 0),
                "lip": alimento.get("lip", 0)
            })
            
        # Limita a 15 resultados para não travar o front-end
        if len(resultados) >= 15:
            break
            
    return {"resultados": resultados}