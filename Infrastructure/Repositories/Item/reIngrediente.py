from Infrastructure.Repositories.base import Session

#Ingrediente
from Infrastructure.Models.Item.mIngrediente import Ingrediente
from API.Schemas.Itens.sIngredientes import CriacaoSchema

from Domain.__exceptions__ import Conflito

def verificar_ingrediente_existe(nome, sessao: Session):
    ingrediente = sessao.query(Ingrediente).filter(Ingrediente.nome==nome).first()
    if ingrediente:
        raise Conflito('ingrediente', 'nome', nome)

def criar_ingrediente_db(schema: CriacaoSchema, sessao:Session):
    novo = Ingrediente(schema.nome, schema.periodo)
    sessao.add(novo)
    sessao.commit()
    return {
        "message":"Ingrediente criado com sucesso!",
        "ingrediente":{
            "id":novo.id,
            "nome":novo.nome,
            "periodo":novo.periodo
        }
    }