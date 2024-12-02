import pytest
from app import app, db
from app.models import Aluno

@pytest.fixture(scope='module')
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        db.session.remove()
        db.drop_all()

def test_add_aluno(client):
    # Dados do aluno a ser adicionado
    novo_aluno = {
        'nome': 'João',
        'sobrenome': 'Silva',
        'turma': '1A',
        'disciplinas': 'Matemática, Português'
    }

    # Enviar uma requisição POST para adicionar o aluno
    response = client.post('/alunos', json=novo_aluno)
    assert response.status_code == 201

    # Verificar se o aluno foi adicionado ao banco de dados
    aluno = Aluno.query.filter_by(nome='João', sobrenome='Silva').first()
    assert aluno is not None
    assert aluno.turma == '1A'
    assert aluno.disciplinas == 'Matemática, Português'