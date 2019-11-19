import yaml
import artifacts

def load_requirements_from(file):
    """
    create a list artifacts.Artifact instances.

    :param file: a file that conains requirements
    :return: list of found utils.Artefact instances
    """
    artifacts = []

    try:
        with open(file, 'r') as f:
            artifacts = load_yaml_reader(f)

    except:
        with open(file, 'r') as f:
            artifacts = load_plain_text_reader(f)

    return artifacts

def load_yaml_reader(reader):
    documents = yaml.safe_load_all(reader)
    list_of_artifacts = []
    for data in documents:
        requirements = data['requires']

        if isinstance(requirements, list):
            for artifact in requirements:
                if artifacts.Artifact(artifact) not in list_of_artifacts:
                    list_of_artifacts.append(artifacts.Artifact(artifact))

        if isinstance(requirements, dict):
            for artifact in requirements['stable']:
                if artifacts.Artifact(artifact) not in list_of_artifacts:
                    list_of_artifacts.append(artifacts.Artifact(artifact))

            for artifact in requirements['snapshot']:
                if artifacts.Artifact(artifact, build_type='snapshot') not in list_of_artifacts:
                    list_of_artifacts.append(artifacts.Artifact(artifact, build_type='snapshot'))

    return list_of_artifacts


def load_plain_text_reader(reader):
    list_of_artifacts = []
    for artifact in reader.readlines():
        list_of_artifacts.append(artifacts.Artifact(artifact.strip(' ')))

    return artifacts