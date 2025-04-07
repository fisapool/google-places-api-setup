# Google Places API Setup

A Node.js CLI tool that automates the Google Places API project setup process.

[![npm version](https://img.shields.io/npm/v/google-places-api-setup.svg)](https://www.npmjs.com/package/google-places-api-setup)
[![License](https://img.shields.io/npm/l/google-places-api-setup.svg)](https://github.com/fisapool/google-places-api-setup/blob/main/LICENSE)

## Overview

This tool simplifies the process of setting up a Google Cloud project with Places API enabled. It helps you:

- Create a new Google Cloud project
- Enable the Places API
- Create and configure an API key
- Apply proper API restrictions

## Prerequisites

- Node.js 14 or higher
- Google Cloud SDK installed on your system
  - Install from: https://cloud.google.com/sdk/docs/install
- A Google account with billing capabilities

## Installation

### Global Installation (Recommended)

```bash
npm install -g google-places-api-setup
```

### Local Installation

```bash
npm install google-places-api-setup
```

## Usage

### Command Line

If installed globally:

```bash
places-setup
```

With options:

```bash
places-setup --project-id=my-unique-project-id --project-name="My Project Name"
```

### Available Options

| Option | Alias | Description |
|--------|-------|-------------|
| `--project-id` | `-p` | Specify the project ID (must be globally unique) |
| `--project-name` | `-n` | Specify the project name |
| `--skip-auth` | `-s` | Skip authentication (use existing gcloud auth) |
| `--yes` | `-y` | Auto-confirm all prompts (non-interactive mode) |
| `--version` | `-v` | Show version number |
| `--help` | `-h` | Show help |

### Using in Your Project

```javascript
const { run } = require('google-places-api-setup');

run({
  projectId: 'my-places-project',
  projectName: 'My Places Project',
  skipAuth: false,
  yes: false
}).then(() => {
  console.log('Setup complete!');
}).catch(err => {
  console.error('Setup failed:', err);
});
```

## What the Tool Does

1. Checks if Google Cloud SDK is installed
2. Authenticates with Google Cloud (unless skipped)
3. Creates a new project with your specified ID and name
4. Sets the project as your current project
5. Guides you through enabling billing (required for API usage)
6. Enables the Places API services
7. Creates an API key
8. Adds appropriate restrictions to the API key (limits it to Places API only)

## Security Notes

Always keep your API key secure! Consider adding additional restrictions to your API key in the Google Cloud Console, such as:

- HTTP referrer restrictions
- IP address restrictions
- Mobile application restrictions

Visit the Google Cloud Console credentials page for your project to add these restrictions:
```
https://console.cloud.google.com/apis/credentials?project=YOUR_PROJECT_ID
```

## Troubleshooting

If you encounter any issues:

- Ensure Google Cloud SDK is properly installed and in your PATH
- Check that you have permissions to create projects in your Google account
- Verify that billing is properly set up
- Make sure you have the necessary APIs available for your account

## License

MIT 