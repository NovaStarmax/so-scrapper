# Integration Test
from scraper import get_lasted_questions_page

def test_get_lasted_questions_page():
    questions = get_lasted_questions_page()
    
    assert isinstance(questions, list), "La sortie n'est pas une liste"

    # Vérifie que la liste n'est pas vide
    assert len(questions) > 0, "La liste des questions est vide"

    # Vérifie que la première question contient les champs clés
    first = questions[0]
    for key in ["title", "link", "summary", "tags", "author", "date"]:
        assert key in first, f"Le champ '{key}' est manquant dans la première question"

# If response == 200 : requetêts https
# If soup == True : Analyse du html
# If questions > 0 : Extraction des données
# If insert_questions() == True : Insertions bdd

# Errors handlings :

# Pour chaques erreures, avoir un message explicite