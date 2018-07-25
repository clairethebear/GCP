Building a simple Python application on K8s
===========================

Creating a cluster:

Set up the constants for the project:
    PROJECT_ID="name_of_your_project"
	COMPUTE_ZONE="us-central1-a"
	CLUSTER_NAME="simple-python-app"

Create the cluster:
	gcloud config set project $PROJECT_ID
	gcloud config set compute/zone $COMPUTE_ZONE
	gcloud container clusters create $CLUSTER_NAME --zone $COMPUTE_ZONE

Make sure you are working on the correct cluster:
	gcloud container clusters list
	gcloud container clusters get-credentials $CLUSTER_NAME

Run the sammple application locally:

Run the application locally:
    docker build -t simplepythonapp:latest . && docker run -p 5000:5000 simplepythonapp:latest 

Or you can also run it locally using Google Container Registry:
    docker build -t gcr.io/$PROJECT_ID/simplepythonapp:latest . && docker run -p 5000:5000 gcr.io/$PROJECT_ID/simplepythonapp:latest


Deploying a pod:

First you need to push the image to container registry:
    gcloud docker -- push gcr.io/$PROJECT_ID/simplepythonapp:latest
    kubectl deploy -f pod.yaml

This will create one pod inside the cluster created earlier. Lets inspect the
pod.yaml.
        apiVersion: v1
        kind: Pod
        metadata:
          name: simplepythonapp
          spec:
            containers:
              - name: simplepythonapp
                image: gcr.io/claire-play/simplepythonapp:latest
                ports:
                - containerPort: 5000

- The apiVersion field is used to extend the Kubernetes API using API groups. [1] 
- The kind field describes what kind of object you want to create. In this case we
would like to create a pod. 
- The metadata field specifies the data that helps uniquely identify the object, including a name string, UID, and optional namespace.
- The spec field has a different format for every for every kubernetes object. [2]

[1] https://git.k8s.io/community/contributors/design-proposals/api-machinery/api-group.md
[2] https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.11/


Now you should be able to see the pod running inside the cluster:
    kubectl get pods

Exposing your pod:

If you remember when we created out pod, we also gave it a name under the
metadata field. We can use this name to expose the pod to the read world. By
default, containers are not accessible from the internet because they do not
have a public IP address. In order to expose this pod to the internet, we need
to expose it using the name that we set for it in our yaml file.

    kubectl describe pod simplepythonapp

This will give you all the details you need to expose the pod to the internet

    kubectl expose pod simplepythonapp --port=5000 --name simplepythonapp
    kubectl get service -w

The -w flag watches the changes occuring to the service. You can apply this flag
to most kubectl get commands. Now we have to wait for GCP to delegate an
available external IP address to our service.

Note: You may have also noticed another service listed when executing kubectl
get service. This service that is created by default by GKE when you create your
cluster is created so that every pod in your cluster can make API requests to
the Kubernetes Master without having to hard-code the API URL.





