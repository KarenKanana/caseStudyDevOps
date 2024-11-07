# Project Deployment to Google Cloud with GitHub Actions
This repository contains a frontend (JavaScript) and backend (Python Flask) application. The project deploys containerized applications to Google Cloud Run using GitHub Actions for CI/CD.

## Prerequisites
- Google Cloud SDK installed and configured
- Terraform installed
- GitHub account with access to create repositories

## Setup Instructions
### 1. Authenticate with Google Cloud
Open a terminal and authenticate with your Google Cloud account:

`gcloud auth login`

Then set the project:

`gcloud config set project YOUR_GCP_PROJECT_ID`

### 2. Deploy Infrastructure with Terraform
Navigate to the directory containing the Terraform scripts and initialize Terraform:

`terraform init`

Apply the Terraform configuration to create necessary resources (Cloud Run services, Cloud SQL instances, etc.):

`terraform apply`

Review the plan, then confirm the changes to deploy resources. Make a note of the created resources, such as Cloud SQL instance connection names, which will be required later.

### 3. Create Service Account Key
In the Google Cloud Console, navigate to `IAM & Admin > Service Accounts`.
Select or create a service account with permissions to manage Cloud Run, Cloud SQL, and Container Registry.

Generate a JSON key for this service account:
Click Add `Key > Create New Key`, select `JSON`, and download it.
Store this JSON key securely, as it will be required for GitHub Actions.

### 4. Set up GitHub Secrets
To allow GitHub Actions to access Google Cloud resources, add the following secrets in your GitHub repository:

- `GCP_PROJECT_ID`: Your Google Cloud project ID.
- `GCP_SA_KEY`: The JSON content of your service account key. Paste the content of the downloaded key file.
- `GCP_REGION`: The region where your resources are deployed (e.g., us-central1).
- `DATABASE_URI`: The connection URI for your Cloud SQL instance. This should include username, password, and database details.
To add these secrets:

Go to your GitHub repository, then `Settings > Secrets and variables > Actions > New repository secret`.
Add each secret by name and paste in the corresponding value.

### 5. Push Code to GitHub
Push the code to your GitHub repository. This triggers the GitHub Actions workflow to build and deploy the containers to Cloud Run.

```
git add .
git commit -m "Initial deployment"
git push origin main
```

**Workflow Details**
The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) is configured to:

- Check for changes in the FE/ and BE/ directories.
- Build Docker images for the frontend and backend if changes are detected.
- Push the images to Google Container Registry.
- Deploy updated services to Cloud Run.
