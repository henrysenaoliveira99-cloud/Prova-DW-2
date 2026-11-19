# Controller de PAGINAS - todas as rotas daqui respondem HTML ou
# redirecionamento.

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session
from models.palestrante import Palestrante
from dao.palestrante_dao import PalestranteDAO

palestrante_bp = Blueprint("palestrante", __name__)

@evento_bp.before_request
def exigir_login():
    if not session.get("usuario_id"):
        flash("Faca login para continuar.")
        return redirect(url_for("auth.login"))



# ===== ITEM 5 ========================================================
# Hoje qualquer pessoa abre as paginas deste Blueprint sem entrar no
# sistema. Escreva aqui a protecao, em um ponto so.
# =====================================================================


# Listagem (GET) e cadastro (POST) na mesma rota
@palestrante_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        palestrante = Palestrante(
            nome=request.form["nome"],
            tema=request.form["tema"],
            minutos=request.form["minutos"]
        )
        PalestranteDAO.salvar(palestrante)
        flash("Palestrante cadastrado.")
        return redirect(url_for("palestrante.index"))

    def contador():
        session["visitas"] = session.get("visitas", 0) + 1
    # ===== ITEM 3 ====================================================
    # Conte aqui, na SESSAO, quantas vezes esta pessoa abriu a listagem.
    # A chave deve se chamar "visitas". O template ja exibe o valor.
    # =================================================================

    return render_template("index.html", palestrantes=PalestranteDAO.listar())

contador = {"total": 0}

# Edicao - GET mostra o formulario preenchido
@palestrante_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    palestrante = PalestranteDAO.buscar_por_id(id)

{% extends "base.html" %}
{% block titulo %}Editar Registro{% endblock %}
{% block conteudo %}
<h2>Editar</h2>
<form method="post">
    <input name="nome" value="{{ palestrante.nome }}" required>
    <button type="submit">Salvar</button>
    </form>
{% endblock %}

    # ===== ITEM 4 ====================================================
    # O formulario de edicao e enviado para esta rota por POST, mas nada
    # e gravado. Trate aqui o envio: grave a alteracao e volte a listagem.
    # =================================================================

    return render_template("editar.html", palestrante=palestrante)


# Exclusao
@palestrante_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    palestrante = PalestranteDAO.buscar_por_id(id)
    PalestranteDAO.excluir(palestrante)
    flash("Palestrante excluido.")
    return redirect(url_for("palestrante.index"))



