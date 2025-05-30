import requests
import logging
from flask import current_app # Para logging dentro do contexto da aplicação Flask
from flask_restx import Namespace, Resource, fields

pd = Namespace("produtos_externos", description="Operações com produtos da API externa")

product_output_model = pd.model('ProdutoExterno', {
    'id': fields.Integer(readonly=True, description='ID do produto na API externa'),
    'title': fields.String(readonly=True, description='Título do produto'),
    'price': fields.Float(readonly=True, description='Preço do produto'),
    'image': fields.String(readonly=True, description='URL da imagem do produto'),
    'description': fields.String(readonly=True, description='Descrição do produto'),
    'category': fields.String(readonly=True, description='Categoria do produto')
})

@pd.route("/produtos") 
class ProdutosExternosLista(Resource): 
    # @pd.doc("Obter lista de todos os produtos externos")
    # @pd.response(200, "Lista de produtos obtida com sucesso", model=[product_output_model]) # Documenta a resposta
    # @pd.response(503, "Serviço externo indisponível ou erro ao buscar produtos")
    @pd.marshal_list_with(product_output_model) # Serializa a lista de saída usando o modelo
    def get(self):
        produtos_externos = obter_produtos_externos()

        if produtos_externos is None:            
            pd.abort(503, "Não foi possível buscar os produtos da API externa no momento.")

        produtos_formatados = []
        if produtos_externos is not None:
            for produto in produtos_externos:
                if isinstance(produto, dict):
                     # A FakeStoreAPI geralmente inclui description e category, mas para garantir:
                    produtos_formatados.append({
                        "id": produto.get("id"),
                        "title": produto.get("title"),
                        "price": produto.get("price"),
                        "image": produto.get("image"),
                        "description": produto.get("description", ""), # Garante string vazia se ausente
                        "category": produto.get("category", "")      # Garante string vazia se ausente
                    })

        return produtos_formatados
        
def obter_produtos_externos():
    url = "https://fakestoreapi.com/products"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        
        produtos = response.json()
        if not isinstance(produtos, list):
            pd.abort(f"API externa ({url}) não retornou uma lista. Tipo recebido: {type(produtos)}")
            return None
        return produtos
    except requests.exceptions.HTTPError as e:
        pd.abort(f"Erro HTTP ao buscar produtos da API externa: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        pd.abort(f"Erro de requisição ao buscar produtos da API externa ({url}): {e}")
        return None
    except ValueError as e: # Erro de decodificação JSON
        pd.abort(f"Erro ao decodificar JSON da resposta da API externa ({url}): {e}")
        return None
            
