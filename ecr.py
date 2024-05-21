import boto3

ecr_client=boto3.client('ecr')

repository_name="mycloud-native2"

try:
    response = ecr_client.create_repository(repositoryName=repository_name)
    repository_uri = response['repository']['repositoryUri']
    print("Repository created successfully. URI:", repository_uri)
except ecr_client.exceptions.RepositoryAlreadyExistsException:
    print("Repository already exists.")
    response = ecr_client.describe_repositories(repositoryNames=[repository_name])
    repository_uri = response['repositories'][0]['repositoryUri']
    print("Repository URI:", repository_uri)

#response = ecr_client.create_repository(repositoryName = repository_name)

#repository_uri= ['repository']['repositoryUri']
#print(repository_uri)