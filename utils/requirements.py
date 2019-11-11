import utils.artifacts, yaml

def load_requirements_from(file):
    """
    create a list utils.Artifact instances. Instances are initialized using the list found in the passed YAML file at key
    'requires'
    :param file: a YAML file that conains at least a key entry 'requires'
    :return: list of found utils.Artefact instances
    """
    artifacts = []

    with open(file, 'r') as f:
        documents = yaml.safe_load_all(f)

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