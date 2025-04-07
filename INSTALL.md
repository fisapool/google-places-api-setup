# Installation Guide

This guide walks you through installing all requirements for the Google Places API setup script.

## Step 1: Install Python 3.6+

### On macOS:
```bash
brew install python
```

### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### On Windows:
Download and install from [python.org](https://www.python.org/downloads/)

## Step 2: Install Google Cloud SDK

### On macOS:
```bash
brew install --cask google-cloud-sdk
```

### On Ubuntu/Debian:
```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get install apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
```

### On Windows:
Download the installer from [Google Cloud SDK website](https://cloud.google.com/sdk/docs/install#windows)

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Initialize Google Cloud SDK

This step is optional but recommended before running the setup script:

```bash
gcloud init
```

This will guide you through the basic Google Cloud setup.

## Step 5: Make the Script Executable

```bash
chmod +x setup_google_places.py
```

## Step 6: Run the Script

```bash
./setup_google_places.py
```

## Troubleshooting

### Common Issues:

1. **"gcloud: command not found"**  
   Make sure Google Cloud SDK is in your PATH. You may need to restart your terminal.

2. **Authentication Failures**  
   Try running `gcloud auth login` manually before the script.

3. **Project Creation Failures**  
   - Make sure your Google account has permissions to create projects.
   - Check if you have exceeded your project quota.
   - Project IDs must be unique across all of Google Cloud Platform.

4. **Billing Issues**  
   Ensure you have a valid credit card associated with your Google account. 