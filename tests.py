import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# --- NOVOS TESTES: COMMIT 2 ---

def test_create_question_with_invalid_points():
    """Garante que a questão rejeita pontuações fora do limite (1 a 100)."""
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=0)
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=101)

def test_add_choice_empty_text():
    """Garante que uma escolha não pode ter texto vazio."""
    question = Question(title='q1')
    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')

def test_add_choice_text_too_long():
    """Garante que uma escolha não pode exceder 100 caracteres."""
    question = Question(title='q1')
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice('a' * 101)

def test_add_multiple_choices_increments_id():
    """Testa se IDs são gerados sequencialmente ao adicionar múltiplas escolhas."""
    question = Question(title='q1')
    c1 = question.add_choice('A')
    c2 = question.add_choice('B')
    
    assert len(question.choices) == 2
    assert c1.id == 1
    assert c2.id == 2

def test_remove_choice_by_id_success():
    """Testa a remoção bem-sucedida de uma escolha."""
    question = Question(title='q1')
    question.add_choice('A')
    question.add_choice('B')
    
    question.remove_choice_by_id(1)
    
    assert len(question.choices) == 1
    assert question.choices[0].text == 'B'

def test_remove_choice_by_invalid_id():
    """Garante que tentar remover um ID inexistente lança erro."""
    question = Question(title='q1')
    question.add_choice('A')
    
    with pytest.raises(Exception, match='Invalid choice id 99'):
        question.remove_choice_by_id(99)

def test_remove_all_choices():
    """Testa se a função de limpar as escolhas funciona."""
    question = Question(title='q1')
    question.add_choice('A')
    question.add_choice('B')
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_set_correct_choices():
    """Testa a atribuição do status 'is_correct' passando IDs."""
    question = Question(title='q1')
    question.add_choice('A')
    question.add_choice('B')
    
    question.set_correct_choices([2])
    
    assert not question.choices[0].is_correct # ID 1 (A)
    assert question.choices[1].is_correct     # ID 2 (B)

def test_correct_selected_choices_success():
    """Testa a correção de alternativas, retornando apenas os acertos."""
    question = Question(title='q1', max_selections=2)
    question.add_choice('A', is_correct=False)
    question.add_choice('B', is_correct=True)
    question.add_choice('C', is_correct=True)
    
    # Usuário selecionou A (1) e B (2). Só deve retornar o acerto que é o B (2).
    correct_selections = question.correct_selected_choices([1, 2])
    
    assert correct_selections == [2]

def test_correct_selected_choices_exceeds_max():
    """Garante a trava que impede o usuário de selecionar mais opções do que o permitido."""
    question = Question(title='q1', max_selections=1)
    question.add_choice('A')
    question.add_choice('B')
    
    with pytest.raises(Exception, match='Cannot select more than 1 choices'):
        question.correct_selected_choices([1, 2])

