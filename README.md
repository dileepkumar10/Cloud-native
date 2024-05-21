# 🚀🚀 Cloud Native Monitoring Application on Kubernetes 🚀🚀

This project demonstrates how to deploy a Flask application on Kubernetes, utilizing various AWS services.


## **Prerequisites** !

(Things to have before starting the projects)

- [x]  AWS Account.
- [x]  Programmatic access and AWS configured with CLI.
- [x]  Python3 Installed.
- [x]  Docker and Kubectl installed.
- [x]  Code editor (Vscode)

### Programmatic Access and AWS CLI Configuration

Follow the [official AWS CLI documentation](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) to install and configure AWS CLI.

After installing the AWS CLI, configure it by running:

```sh

aws configure

```

<img width="434" alt="Screenshot 2024-05-17 at 1 43 02 PM" src="https://github.com/dileepkumar10/Aws-Project/assets/59137957/44837fa0-3173-4fdc-98a8-578a80e9347e">


Aws Access key ID you will get it in Aws IAM or on the aws console top right you will see the your profile click on it —> Go to security credentials —> go to Access keys.
you can create new access key enter the access key and secret key in the aws CLI.


# ✨Let’s Start the Project ✨

## **Part 1: Deploying the Flask application locally**

<img width="423" alt="Screenshot 2024-05-17 at 2 22 36 PM" src="https://github.com/dileepkumar10/Aws-Project/assets/59137957/4a2f82c3-75ec-4343-b229-2e9307960608">

### **Step 1: Install dependencies**

For installing dependencies run below command 
requirement.txt have required dependencies

```
pip3 install -r requirements.txt

```

### **Step 3: Run the application**

To run the application, navigate to the root directory of the project and execute the following command:

```
python3 app.py

```

This will start the Flask server on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

## **Part 2: Dockerizing the Flask application**

### **Step 1: Create a Dockerfile**

Create a **`Dockerfile`** in the root directory of the project with the following contents:

```
# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Set the environment variables for the Flask app
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which the Flask app will run
EXPOSE 5000

# Start the Flask app when the container is run
CMD ["flask", "run"]
```

### **Step 2: Build the Docker image**

To build the Docker image, execute the following command:

```
docker build -t <image_name> .

```

### **Step 3: Run the Docker container**

To run the Docker container, execute the following command:

```
docker run -p 5000:5000 <image_name>

```

This will start the Flask server in a Docker container on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

## **Part 3: Pushing the Docker image to ECR**

### **Step 1: Create an ECR repository**

Create an ECR repository using Python:

ecr.py
```
import boto3

# Create an ECR client
ecr_client = boto3.client('ecr')

# Create a new ECR repository
repository_name = 'my-ecr-repo'
response = ecr_client.create_repository(repositoryName=repository_name)

# Print the repository URI
repository_uri = response['repository']['repositoryUri']
print(repository_uri)
```

To run the ecr.py, execute the following command:

```
python3 ecr.py

```

Once it is executed go  to the Amazon Elastic Container Registry  console in aws.
The ecr repository will be created.

### **Step 2: Push the Docker image to ECR**

Select the ecr repository on the top you will see the view push commands click on it.
Copy those commands and execute it in vs code 

Push the Docker image to ECR using the push commands on the console:

```
docker push <ecr_repo_uri>:<tag>

```

## **Part 4: Creating an EKS cluster and deploying the app using Python**

### **Step 1: Create an EKS cluster**

Create an EKS cluster and add node group

Once it is created need to update the kubeconfig file.
To update the kubeconfig, execute the following command:

```
aws eks update-kubeconfig —name <clustername>

```

### **Step 2: Create a node group**

Create a node group in the EKS cluster.

### **Step 3: Create deployment and service**

```jsx
from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "my-flask-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "my-flask-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="568373317874.dkr.ecr.us-east-1.amazonaws.com/my-cloud-native-repo:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)
```

Note: make sure to edit the name of the image on line 25 with your image Uri.

- Once you run this file by running “python3 eks.py” deployment and service will be created.
- Check by running following commands:

```jsx
kubectl get deployment -n default (check deployments)
kubectl get service -n default (check service)
kubectl get pods -n default (to check the pods)
```

Once your pod is up and running, run the port-forward to expose the service

```bash

kubectl port-forward service/<service_name> 5000:5000

```

If any issue like pod not running or any other issue in pods to chekc this excecute below command

```
kubectl describe pods <pod name>

```

The command kubectl describe pods <pod_name> is used to get detailed information about a specific Kubernetes pod. 
When you use kubectl describe pods followed by the name of a pod, it provides a comprehensive overview of that particular pod's configuration, status, and events.
