K8s Python Example using GCP
==============

This repo will explain how to deploy a basic python application into
kubernetes, how to execute a rolling update and how to create a deployment file.

To build the application in Google Cloud run the following
	docker build -t gcr.io/[PROJECTID]/kubestats:latest .


The above command is going to create a docker image of your python application
living in `src/`. We will now push the image to the container registry on GCP:

	gcloud docker -- push gcr.io/[PROJECTID]/kubestats:latest

Now you can run the following to see the pods running on your container cluster:

	kubectl apply -f replicationcontroller.yaml -f tcp_loadbalancer_service.yaml

The above command will create a replication controller that will ensure that the pods will be started on the node(s). The service will create a network load balancer thats attached to endpoints that have the label 'Kubestats' and deliver traffic to the containers on the nodes.

One you have made some changes to `src/app.py` build and push your updated app:

	docker build -t gcr.io/[PROJECTID/kubestats:v1 .
	gcloud docker -- push gcr.io/[PROJECTID]/kubestats:v1

You can also run the application locally by running the following:

	docker build -t kubestats:latest . && docker run -p 5000:5000

Create a deployment file
=======================

If we want to make an update to our binary and push it to our nodes we need to edit the replication controller with 

1. The path of our new registy file
2. The new version of the application - replacing every instances of V1 with V2. 
3. Update the name of the replication controller - or else kubectl will give out to us for using the old name.

There are a few drawbacks to using a rolling update manifest for all of our updates:
1. No audit trail
2. We need two replication controller manifests that are interchangable every time we want to make an update.
3. Because this is being run on the client side - this is susceptible to network interruptions.

To save time and provide reliability - we can create a deployment file and this will take care of the heavy lifting when we want to safely update our application.

Make an update to your binary and run the build and push commands.

	docker build -t gcr.io/kubernetes-playground-176304/kubestats:v2 .
	gcloud docker -- push gcr.io/kubernetes-playground-176304/kubestats:v2

Now all we have to do is find the deployment name by doing
	kubectl get svc

We need this so that we can apply the new image to the deployment - in our case it shoudl be called kubestats-service
	kubectl set image deployments/kubestats kubestats=gcr.io/kubernetes-playground-176304/kubestats:v2

Once this is done we can see our pods being deleted and replcae by the updated pods.


Create an Ingress
=================

An ingress load balancer offers more support for SSL termination, routing rules
etc..

This works by connecting to the backend service that we created earlier. The
ingress points to the service which has the routing information to find our
pods.



[1] Good write up on difference between using RC vs Deploy manifests for launches: https://ryaneschinger.com/blog/rolling-updates-kubernetes-replication-controllers-vs-deployments/
