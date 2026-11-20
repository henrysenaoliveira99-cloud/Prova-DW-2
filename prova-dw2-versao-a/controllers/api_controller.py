# Controller da API - as rotas daqui respondem DADOS em JSON.
#
#   Metodo   Endereco                 O que faz       Sucesso   Recusas
#   GET      /api/palestrantes            lista todos     200       401
#   GET      /api/palestrantes/<id>       devolve um      200       401 404   <- ITEM 7
#   DELETE   /api/palestrantes/<id>       remove          204       401 404   <- ITEM 9
#
# Toda recusa tem o mesmo formato: {"erro": "mensagem"}.

from flask import Blueprint, request, session, jsonify
from models.palestrante import Palestrante
from dao.palestrante_dao import PalestranteDAO

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.before_request
def exigir_login():
    if not session.get("usuario_id"):
        return jsonify({"erro": "Autenticacao necessaria."}), 401


@api_bp.route("/palestrantes", methods=["GET"])
def listar():
    lista = []

    for palestrante in PalestranteDAO.listar():
        lista.append(palestrante.para_dicionario())

    return jsonify(lista)

@api_bp.route("/palestrante/<int:id>", methods=["GET"])
def api_buscar(id):
    evento = EventoDAO.buscar_por_id(id)
    if not evento:
        return jsonify({"erro": "Registro nao encontrado."}), 404
    return jsonify(evento.para_dicionario()), 200


# ===== ITEM 7 ========================================================
# Escreva aqui a rota GET /api/palestrantes/<id>, que devolve UM registro.
# Se o id nao existir, a resposta e 404 com {"erro": "Palestrante nao encontrado."}.
# =====================================================================

function excluirPorFetch(id) {
    fetch("/api/eventos/" + id, { method: "DELETE" })
        .then(function (r) {
            if (r.ok) {
                console.log("Excluido! Status:", r.status); // 204
            }
            return r.text(); // nunca use r.json() no DELETE 204!
        });
}

@evento_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    evento = EventoDAO.buscar_por_id(id)
    EventoDAO.excluir(evento)
    flash("Registro excluido com sucesso.")
    return redirect(url_for("evento.index"))


# ===== ITEM 9 ========================================================
# Escreva aqui a rota DELETE /api/palestrantes/<id>, que remove UM registro.
# Sucesso: 204, sem corpo. Se o id nao existir: 404 com
# {"erro": "Palestrante nao encontrado."}.
# =====================================================================
