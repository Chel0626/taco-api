import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. RESOLVENDO O ERRO DE CORS
# Isso avisa ao servidor que ele pode aceitar requisições do seu localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],    allow_credentials=True,
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
    
    for item in taco_data:
        # A chave correta para o nome é "description"
        nome_busca = item.get("description", "")
        
        if termo.lower() in nome_busca.lower():
            # Pegando os valores e garantindo que não sejam nulos
            cho = float(item.get("carbohydrate_g") or 0)
            ptn = float(item.get("protein_g") or 0)
            lip = float(item.get("lipid_g") or 0)
            kcal = float(item.get("energy_kcal") or 0)

            resultados.append({
                "id": str(item.get("id", len(resultados))),
                "nome_exibicao": nome_busca,
                # Arredondando para 1 casa decimal para ficar bonito na UI
                "cho": round(cho, 1),
                "ptn": round(ptn, 1),
                "lip": round(lip, 1),
                "kcal": round(kcal, 1)
            })
            
        # Limita a 15 resultados para o dropdown não ficar gigante
        if len(resultados) >= 15:
            break
            
    return {"resultados": resultados}