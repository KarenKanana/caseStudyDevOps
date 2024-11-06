# create cloudrun services
locals {
  services = [
    "frontend",
    "backend"
  ]
}

resource "google_cloud_run_v2_service" "default" {
  for_each = toset(local.services) 
  name     = "${each.key}-cloudrun-service" 
  location = var.REGION
  project = var.PROJECT_ID
  # deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
  }
}

# Create artifact registry
resource "google_artifact_registry_repository" "frontend" {
  location      = var.REGION
  repository_id = "frontend"
  description   = "frontend docker repository"
  format        = "DOCKER"

}

resource "google_artifact_registry_repository" "backend" {
  location      = var.REGION
  repository_id = "backend"
  description   = "backend docker repository"
  format        = "DOCKER"
}

# create cloud sql database
resource "google_sql_database_instance" "main" {
  name             = "main-instance"
  database_version = "POSTGRES_15"
  region           = var.REGION

  settings {
    # Second-generation instance tiers are based on the machine
    # type. See argument reference below.
    tier = "db-f1-micro"
  }
  # username = postgres 
  # passwd = 1qazZAQ!2wsxXSW@
  # dbname = postgres
  # dburl = vivid-alchemy-436608-r0:us-central1:main-instance
}