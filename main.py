from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Taco API Online! O motor está rodando."}

@app.get("/alimento/{nome}")
def buscar_alimento(nome: str):
    # Aqui é onde vamos ler o seu JSON da TACO depois
    return {"status": "busca", "alimento": nome}