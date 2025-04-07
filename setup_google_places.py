#!/usr/bin/env python3

import subprocess
import json
import os
import time
from typing import Optional

def run_command(command: str) -> tuple[bool, str]:
    """Run a shell command and return success status and output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Error: {e.stderr}"

def check_gcloud_installed() -> bool:
    """Check if gcloud CLI is installed."""
    success, _ = run_command("gcloud --version")
    return success

def authenticate_gcloud() -> bool:
    """Authenticate with Google Cloud."""
    print("Authenticating with Google Cloud...")
    success, output = run_command("gcloud auth login")
    if not success:
        print("Failed to authenticate with Google Cloud")
        return False
    print("Authentication successful!")
    return True

def create_project(project_id: str, project_name: str) -> bool:
    """Create a new Google Cloud project."""
    print(f"Creating project {project_id}...")
    success, output = run_command(f"gcloud projects create {project_id} --name='{project_name}'")
    if not success:
        print(f"Failed to create project {project_id}")
        return False
    print(f"Project {project_id} created successfully!")
    return True

def set_project(project_id: str) -> bool:
    """Set the current project."""
    print(f"Setting current project to {project_id}...")
    success, output = run_command(f"gcloud config set project {project_id}")
    if not success:
        print(f"Failed to set project to {project_id}")
        return False
    print(f"Project set to {project_id}!")
    return True

def enable_billing(project_id: str) -> bool:
    """Enable billing for the project."""
    print("You need to enable billing for this project.")
    print("To do this, visit: https://console.cloud.google.com/billing/linkedaccount?project=" + project_id)
    input("Press Enter once you've enabled billing...")
    return True

def enable_places_api(project_id: str) -> bool:
    """Enable the Places API for the project."""
    print("Enabling Places API...")
    success, output = run_command(f"gcloud services enable places-backend.googleapis.com places.googleapis.com --project={project_id}")
    if not success:
        print("Failed to enable Places API")
        return False
    print("Places API enabled successfully!")
    return True

def create_api_key(project_id: str) -> Optional[str]:
    """Create an API key for the project."""
    print("Creating API key...")
    key_name = "places-api-key"
    success, output = run_command(f"gcloud alpha services api-keys create --display-name='{key_name}' --project={project_id}")
    
    if not success:
        print("Failed to create API key")
        return None
    
    # Extract the key ID from the output
    try:
        # Wait for the key to be created
        time.sleep(5)
        
        # List keys and find the one we just created
        success, output = run_command(f"gcloud alpha services api-keys list --project={project_id} --format=json")
        if not success:
            print("Failed to list API keys")
            return None
            
        keys = json.loads(output)
        key_id = None
        for key in keys:
            if key.get("displayName") == key_name:
                key_id = key.get("uid") or key.get("name").split("/")[-1]
                break
                
        if not key_id:
            print("Could not find the created API key")
            return None
            
        # Get the actual API key string
        success, output = run_command(f"gcloud alpha services api-keys get-key-string {key_id} --project={project_id}")
        if not success:
            print("Failed to get API key string")
            return None
            
        # Extract the key string from output
        key_data = json.loads(output)
        api_key = key_data.get("keyString")
        
        if not api_key:
            print("Could not extract API key string")
            return None
            
        print("API key created successfully!")
        return api_key
        
    except Exception as e:
        print(f"Error processing API key: {str(e)}")
        return None

def restrict_api_key(project_id: str, key_name: str) -> bool:
    """Add API restrictions to the key."""
    print("Adding restrictions to API key...")
    success, output = run_command(
        f"gcloud alpha services api-keys update {key_name} "
        f"--api-target=service=places-backend.googleapis.com "
        f"--api-target=service=places.googleapis.com "
        f"--project={project_id}"
    )
    if not success:
        print("Failed to add restrictions to API key")
        return False
    print("API key restrictions added successfully!")
    return True

def main():
    print("=== Google Places API Setup Script ===")
    
    # Check if gcloud is installed
    if not check_gcloud_installed():
        print("Google Cloud SDK (gcloud) is not installed. Please install it first.")
        print("Visit: https://cloud.google.com/sdk/docs/install")
        return

    # Get project details from user
    project_id = input("Enter your project ID (must be unique, e.g., my-places-project-12345): ")
    project_name = input("Enter your project name (e.g., My Places Project): ")

    # Authenticate with Google Cloud
    if not authenticate_gcloud():
        return

    # Create project
    if not create_project(project_id, project_name):
        return
        
    # Set as current project
    if not set_project(project_id):
        return

    # Prompt for billing
    if not enable_billing(project_id):
        return

    # Enable Places API
    if not enable_places_api(project_id):
        return

    # Create API key
    api_key = create_api_key(project_id)
    if not api_key:
        return

    # Get key name for restrictions
    success, output = run_command(f"gcloud alpha services api-keys list --project={project_id} --format=json")
    if success:
        keys = json.loads(output)
        for key in keys:
            if "keyString" in output and api_key in output:
                key_name = key.get("name").split("/")[-1]
                # Restrict API key
                restrict_api_key(project_id, key_name)
                break

    print("\n=== Setup completed successfully! ===")
    print(f"Project ID: {project_id}")
    print(f"API Key: {api_key}")
    print("\nIMPORTANT: Save your API key securely and never share it publicly!")
    print("You may want to add HTTP referrer restrictions in the Google Cloud Console.")
    print("Visit: https://console.cloud.google.com/apis/credentials?project=" + project_id)

if __name__ == "__main__":
    main() 