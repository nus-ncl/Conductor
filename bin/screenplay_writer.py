'''
input: specification.yml
output: various configuration files
'''
import sys
import os
import copy
import uuid
import yaml
import jinja2
from jinja2 import Environment, PackageLoader
from .yaml_utility import yaml_parser
import operating_system
from config import default

sys.path.append('./bin/renderer')
# from renderer import *
import screenplay_renderer


def speculateURI():
    pass


def speculateOS():
    pass


def writer(screenplay_name, repository_file, event_description_file):
    repository_file_content = yaml_parser.yaml_file_load(repository_file)
    event_description_file_content = yaml_parser.yaml_file_load(event_description_file)
    output_dir = f"{default.SCREENPLAY_PATH}/{screenplay_name}"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    else:
        print(f"{output_dir} already exists!")

    screenplay = {}
    metadata = {}
    repositories = {'package': [], 'artifact': [], 'dependency': []}
    repositories_lookup_dict = {}
    instances = []
    networks = []
    events = []
    instance_class = {'name': None, 'uri': None, 'os': None, 'dependency': [], 'package': [], 'artifact': []}
    package_class = {'name': None, 'type': 'package', 'source_addr': None, 'dest_addr': '/home/{USER}/package'}
    artifact_class = {'name': None, 'type': 'unknown', 'source_addr': None, 'dest_addr': '/home/{USER}/artifact'}
    event_class = {'order': None, 'place': None, 'package': [], 'artifact': [], 'utility': None,
                   'utility_parameters': [], 'delay_before': 0, 'delay_after': 0, 'description': None}
    print(f"Start writing the screenplay")
    # metadata
    for index, package_repo in enumerate(repository_file_content['repositories']['package']):
        repositories['package'].append({'id': f"pack_{index}", 'uri': package_repo['uri']})
        repositories_lookup_dict[f"{package_repo['uri']}"]=f"pack_{index}"
    for index, artifact_repo in enumerate(repository_file_content['repositories']['artifact']):
        repositories['artifact'].append({'id': f"arti_{index}", 'uri': artifact_repo['uri']})
        repositories_lookup_dict[f"{artifact_repo['uri']}"] = f"arti_{index}"
    for index, dependency_repo in enumerate(default.DEPENDENCY):
        repositories['dependency'].append({'id': f"dependency_{index}", 'uri': dependency_repo})
        repositories_lookup_dict[f"{dependency_repo}"] = f"dependency_{index}"
    # print(repositories_lookup_dict)
    metadata['experiment_name'] = screenplay_name
    metadata['repositories'] = repositories

    # instances
    for index, event in enumerate(event_description_file_content):
        instances_name_list = yaml_parser.get_instances_name_list(instances)
        if event['subject'] not in instances_name_list:
            # create a new instance with properties
            instance_entry = copy.deepcopy(instance_class)
            instance_entry['name'] = event['subject']
            if event['supported_platforms']:
                instance_entry['os'] = event['supported_platforms']
            if event['dependency']:
                first_list = instance_entry['dependency']
                second_list = event['dependency']
                first_list.extend(second_list)
                instance_entry['dependency'] = list(set(first_list))
            if event['package']:
                for package in event['package']:
                    package_entry = copy.copy(package_class)
                    for package_repo in repository_file_content['repositories']['package']:
                        if package in package_repo['items']:
                            package_entry['source_addr'] = repositories_lookup_dict[package_repo['uri']]
                    package_entry['name'] = package
                    instance_entry['package'].append(package_entry)
            if event['artifact']:
                for artifact in event['artifact']:
                    artifact_entry = copy.copy(artifact_class)
                    artifact_entry['name'] = artifact
                    if artifact.find('//') != -1:
                        artifact_entry['type'] = 'uri'
                        artifact_entry['dest_addr'] = None
                        if f"fileserver-{artifact}" not in instances_name_list:
                            protocol = artifact.split('//')[0][:4]
                            uri = artifact.split('//')[1].split('/')[0]
                            start = artifact.split('//')[1].index('/')
                            file_path = artifact.split('//')[1][start:]
                            instance_entry_uri = copy.deepcopy(instance_class)
                            instance_entry_uri['name'] = f"fileserver-{artifact}"
                            instance_entry_uri['uri'] = uri
                            instance_entry_uri['os'] = 'linux'
                            artifact_entry_uri = copy.copy(artifact_class)
                            artifact_entry_uri['name'] = artifact.split('/')[-1]
                            if artifact[-1] == '/':
                                artifact_entry_uri['type'] = 'directory'
                                for artifact_repo in repository_file_content['repositories']['artifact']:
                                    if artifact.split('/')[-1] in artifact_repo['items']:
                                        artifact_entry_uri['source_addr'] = repositories_lookup_dict[artifact_repo['uri']]
                            else:
                                if artifact.split('.')[-1] in default.TYPE_DICT:
                                    artifact_entry_uri['type'] = default.TYPE_DICT[artifact.split('.')[-1]]
                                    for artifact_repo in repository_file_content['repositories']['artifact']:
                                        if artifact.split('/')[-1] in artifact_repo['items']:
                                            artifact_entry_uri['source_addr'] = repositories_lookup_dict[artifact_repo['uri']]
                            artifact_entry_uri['dest_addr'] = file_path
                            instance_entry_uri['artifact'].append(artifact_entry_uri)
                            if protocol == 'http':
                                instance_entry_uri['dependency'].append('samba')
                            instances.append(instance_entry_uri)
                    elif artifact[-1] == '/':
                        artifact_entry['type'] = 'directory'
                        for artifact_repo in repository_file_content['repositories']['artifact']:
                            if artifact in artifact_repo['items']:
                                artifact_entry['source_addr'] = repositories_lookup_dict[artifact_repo['uri']]
                    else:
                        if artifact.split('.')[-1] in default.TYPE_DICT:
                            artifact_entry['type'] = default.TYPE_DICT[artifact.split('.')[-1]]
                            for artifact_repo in repository_file_content['repositories']['artifact']:
                                if artifact in artifact_repo['items']:
                                    artifact_entry['source_addr'] = repositories_lookup_dict[artifact_repo['uri']]

                    instance_entry['artifact'].append(artifact_entry)
            instances.append(instance_entry)
        else:
            # revise/amend the existed instance's properties
            index = instances_name_list.index(event['subject'])
            if event['supported_platforms']:
                if instances[index]['os'] is None:
                    instances[index]['os'] = event['supported_platforms']
                else:
                    if instances[index]['os'] != event['supported_platforms']:
                        instances[index]['os'] = f"!ERROR!"
            if event['dependency']:
                first_list = instances[index]['dependency']
                second_list = event['dependency']
                first_list.extend(second_list)
                instances[index]['dependency'] = list(set(first_list))
            if event['package']:
                for package in event['package']:
                    if package not in instances[index]['package']:
                        package_entry = copy.copy(package_class)
                        for package_repo in repository_file_content['repositories']['package']:
                            if package in package_repo['items']:
                                package_entry['source_addr'] = repositories_lookup_dict[package_repo['uri']]
                        package_entry['name'] = package
                        instances[index]['package'].append(package_entry)
            if event['artifact']:
                for artifact in event['artifact']:
                    if artifact not in instances[index]['artifact']:
                        artifact_entry = copy.copy(artifact_class)
                        artifact_entry['name'] = artifact
                        if artifact.find('//') != -1:
                            artifact_entry['type'] = 'uri'
                            artifact_entry['dest_addr'] = None
                            if f"fileserver-{artifact}" not in instances_name_list:
                                protocol = artifact.split('//')[0][:4]
                                uri = artifact.split('//')[1].split('/')[0]
                                start = artifact.split('//')[1].index('/')
                                file_path = artifact.split('//')[1][start:]
                                instance_entry_uri = copy.deepcopy(instance_class)
                                instance_entry_uri['name'] = f"fileserver-{artifact}"
                                instance_entry_uri['uri'] = uri
                                instance_entry_uri['os'] = 'linux'
                                artifact_entry_uri = copy.copy(artifact_class)
                                artifact_entry_uri['name'] = artifact.split('/')[-1]
                                if artifact[-1] == '/':
                                    artifact_entry_uri['type'] = 'directory'
                                    for artifact_repo in repository_file_content['repositories']['artifact']:
                                        if artifact.split('/')[-1] in artifact_repo['items']:
                                            artifact_entry_uri['source_addr'] = repositories_lookup_dict[artifact_repo['uri']]
                                else:
                                    if artifact.split('.')[-1] in default.TYPE_DICT:
                                        artifact_entry_uri['type'] = default.TYPE_DICT[artifact.split('.')[-1]]
                                        for artifact_repo in repository_file_content['repositories']['artifact']:
                                            if artifact.split('/')[-1] in artifact_repo['items']:
                                                artifact_entry_uri['source_addr'] = repositories_lookup_dict[artifact_repo['uri']]
                                artifact_entry_uri['source_addr'] = file_path
                                artifact_entry_uri['dest_addr'] = file_path
                                instance_entry_uri['artifact'].append(artifact_entry_uri)
                                if protocol == 'http':
                                    instance_entry_uri['dependency'].append('samba')
                                instances.append(instance_entry_uri)
                        elif artifact[-1] == '/':
                            artifact_entry['type'] = 'directory'
                            for artifact_repo in repository_file_content['repositories']['artifact']:
                                if artifact in artifact_repo['items']:
                                    artifact_entry['source_addr'] = repositories_lookup_dict[artifact_repo['uri']]
                        else:
                            if artifact.split('.')[-1] in default.TYPE_DICT:
                                artifact_entry['type'] = default.TYPE_DICT[artifact.split('.')[-1]]
                                for artifact_repo in repository_file_content['repositories']['artifact']:
                                    if artifact in artifact_repo['items']:
                                        artifact_entry['source_addr'] = repositories_lookup_dict[artifact_repo['uri']]
                        instances[index]['artifact'].append(artifact_entry)
            # speculate()

    screenplay['metadata'] = metadata
    screenplay['instances'] = instances

    yaml_parser.yaml_file_dump(screenplay, f"{output_dir}/{screenplay_name}")
    # screenplay_renderer.renderer(f"{output_dir}", experiment_name, repositories, instances, networks, events)

    print(f"Screenplay is Done! Plz Check Directory: {output_dir}/{screenplay_name}")


if __name__ == "__main__":
    writer()
