import yaml
import os
import artifacts

def load_requirements_from(file):
    """
    create a list artifacts.Artifact instances.

    :param file: a file that conains requirements
    :return: list of found utils.Artefact instances
    """
    assert os.path.isfile(file), "'{}' is not a file or doesn't exists !!".format(file)

    list_of_artifacts = []

    try:
        with open(file, 'r') as f:
            list_of_artifacts = load_yaml_reader(f)

    except:
        with open(file, 'r') as f:
            list_of_artifacts = load_plain_text_reader(f)

    return list_of_artifacts

def load_yaml_reader(reader):
    documents = yaml.safe_load_all(reader)
    list_of_artifacts = []
    for data in documents:
        requirements = data['requires']

        if isinstance(requirements, list):
            for artifact_description in requirements:
                artifact = artifacts.Artifact(artifact_description)
                if artifact not in list_of_artifacts:
                    list_of_artifacts.append(artifact)

        if isinstance(requirements, dict):
            if 'stable' in requirements.keys():
                for artifact_description in requirements['stable']:
                    artifact = artifacts.Artifact(artifact_description)
                    if artifact not in list_of_artifacts:
                        list_of_artifacts.append(artifact)
            if 'snapshot' in requirements.keys():
                for artifact_description in requirements['snapshot']:
                    artifact = artifacts.Artifact(artifact_description, build_type='snapshot')
                    if artifact not in list_of_artifacts:
                        list_of_artifacts.append(artifact)

    return list_of_artifacts


def load_plain_text_reader(reader):
    list_of_artifacts = []
    for artifact in reader.readlines():
        list_of_artifacts.append(artifacts.Artifact(artifact.strip(' ')))

    return list_of_artifacts