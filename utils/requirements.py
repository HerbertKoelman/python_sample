import utils.artifact, yaml

def load_requirements_from(file):
    """
    create a list utils.Artifact instances.

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
    artifacts = []
    for data in documents:
        requirements = data['requires']

        if isinstance(requirements, list):
            for artifact in requirements:
                if utils.Artifact(artifact) not in artifacts:
                    artifacts.append(utils.Artifact(artifact))

        if isinstance(requirements, dict):
            for artifact in requirements['stable']:
                if utils.Artifact(artifact) not in artifacts:
                    artifacts.append(utils.Artifact(artifact))

            for artifact in requirements['snapshot']:
                if utils.Artifact(artifact, build_type='snapshot') not in artifacts:
                    artifacts.append(utils.Artifact(artifact, build_type='snapshot'))

    return artifacts


def load_plain_text_reader(reader):
    artifacts = []
    for artifact in reader.readlines():
        artifacts.append(utils.Artifact(artifact.strip(' ')))

    return artifacts