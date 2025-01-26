# Kubeflow Local Deployment with KIND

This repository provides an easy way to spin up Kubeflow locally using **Kubernetes in Docker (KIND)**.

## Prerequisites

Before getting started, make sure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [KIND](https://kind.sigs.k8s.io/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)

## Getting Started

### 1. Set Up the Local Kubeflow Environment

To deploy Kubeflow locally using KIND, simply run the setup script:

```bash
./setup.sh
```

This script will:

- Create a local Kubernetes cluster using KIND.
- Deploy the necessary resources for Kubeflow.

### 2. Access the Kubeflow UI

Once the setup is complete, you can access the Kubeflow UI by forwarding the `ml-pipeline-ui` service to your local machine:

```bash
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

Open your browser and navigate to `http://localhost:8080` to access the Kubeflow dashboard.

### 3. Tear Down the Environment

When you're done with your local Kubeflow deployment, you can clean up all resources by running:

```bash
./teardown.sh
```

This will:

- Delete the Kubernetes cluster created by KIND.
- Remove all associated services and resources.

## Troubleshooting

- If the `kubectl port-forward` command fails, ensure that the Kubernetes cluster is running and the `ml-pipeline-ui` service is correctly deployed.
- For detailed logs, inspect the KIND cluster using:
  ```bash
  kubectl logs -n kubeflow <pod-name>
  ```

## Additional Notes

- This setup is intended for local development and testing purposes only. For production deployments, consider using a managed Kubernetes service or a more robust installation method.
