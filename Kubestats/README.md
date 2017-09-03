K8s Python Example using GCP
==============

This repo will explain you how to deploy a basic python application into
kubernetes and how to execute a rolling update.

To build the application n Google Cloud run the following
	docker build -t gcr.io/[PROJECTID/kubestats:latest .


The above command is going to create a docker image of your python application
living into `src/`. We will now push the image to the container registry on GCP:

	gcloud docker -- push gcr.io/[PROJECTID]/kubestats:latest

Now you can run the following to see the pods running on your container cluster:

	kubectl apply -f replicationcontroller.yaml -f tcp_loadbalancer_service.yaml

The above command will create a replication controller that will ensure that the pods will be started on the node(s). The service will create a network load balancer that will attached the endpoints and deliver traffic to the containers on the nodes.

One you have made some changes to `src/app.py` build and push your updated app:

	docker build -t gcr.io/[PROJECTID/kubestats:latest .
	gcloud docker -- push gcr.io/[PROJECTID]/kubestats:latest

You can also run the application locally by running the following:

	docker build -t kubestats:latest . && docker run -p 5000:5000

We have the version 0.1 running, I always want to run last versions of
everything so I will update it:

        kubectl rolling-update kubestats-app -f rc-0.2.yml

