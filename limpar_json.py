import json

campos_desejados = [
    "id", "description", "energy_kcal", 
    "protein_g", "lipid_g", "carbohydrate_g", "fiber_g"
]

def filtrar_json(arquivo_entrada, arquivo_saida):
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        novo_json = []
        
        # Filtra os itens
        for item in dados:
            descricao = item.get("description", "").lower()
            
            # Condição: Só adiciona se "cru" NÃO estiver na descrição
            if "cru" not in descricao:
                item_filtrado = {k: item[k] for k in campos_desejados if k in item}
                novo_json.append(item_filtrado)

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(novo_json, f, indent=4, ensure_ascii=False)
        
        print(f"Sucesso! {len(novo_json)} itens processados e salvos em '{arquivo_saida}'.")
        
    except Exception as e:
        print(f"Erro ao processar: {e}")

# Substitua com seus nomes de arquivo
filtrar_json('taco.json', 'dados_sem_cru.json')