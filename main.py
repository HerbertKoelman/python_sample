import utils

if __name__ == '__main__':  # nécessaire que si on veut eviter que ce code soit systématiquement exécuté. Que ce soit comme import ou programme

    for found in utils.load_requirements_from('tests/sample.yml'):
        print(found.id())
