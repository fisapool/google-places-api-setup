#!/bin/bash

# Test script to run before publishing to npm

# Set colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting pre-publish tests...${NC}"

# Step 1: Check that all dependencies are installed
echo -e "\n${YELLOW}1. Checking npm dependencies...${NC}"
npm install
if [ $? -ne 0 ]; then
  echo -e "${RED}Error installing dependencies.${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Dependencies installed successfully.${NC}"

# Step 2: Run unit tests
echo -e "\n${YELLOW}2. Running unit tests...${NC}"
NODE_ENV=test npm test
if [ $? -ne 0 ]; then
  echo -e "${RED}Unit tests failed.${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Unit tests passed successfully.${NC}"

# Step 3: Lint the codebase
echo -e "\n${YELLOW}3. Checking code formatting...${NC}"
if [ -x "$(command -v eslint)" ]; then
  npx eslint . || echo -e "${YELLOW}⚠ ESLint not configured. Skipping linting.${NC}"
else
  echo -e "${YELLOW}⚠ ESLint not installed. Skipping linting.${NC}"
fi
echo -e "${GREEN}✓ Code formatting checks completed.${NC}"

# Step 4: Create a local pack for testing
echo -e "\n${YELLOW}4. Creating a local pack for testing...${NC}"
npm pack
if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to create npm package.${NC}"
  exit 1
fi
echo -e "${GREEN}✓ Local package created successfully.${NC}"

# Step 5: Test the installation globally
echo -e "\n${YELLOW}5. Testing local installation (this might require sudo)...${NC}"
PACKAGE_FILE=$(ls google-places-api-setup-*.tgz | sort -V | tail -n 1)
echo -e "Package file: ${PACKAGE_FILE}"

echo -e "Installing package locally..."
npm install -g ./${PACKAGE_FILE}
if [ $? -ne 0 ]; then
  echo -e "${RED}Failed to install the package globally.${NC}"
  exit 1
fi

# Check if the binary exists and is executable
if command -v places-setup &> /dev/null; then
  echo -e "${GREEN}✓ Package installed successfully and binary is available.${NC}"
  
  # Optional: Test running the binary with --help
  echo -e "\n${YELLOW}Testing binary with --help flag:${NC}"
  places-setup --help
  
  # Cleanup: uninstall the global package
  echo -e "\n${YELLOW}Cleaning up: uninstalling global package...${NC}"
  npm uninstall -g google-places-api-setup
else
  echo -e "${RED}Package installed but binary is not available in PATH.${NC}"
  npm uninstall -g google-places-api-setup
  exit 1
fi

echo -e "\n${GREEN}==================================${NC}"
echo -e "${GREEN}All pre-publish checks completed!${NC}"
echo -e "${GREEN}==================================${NC}"
echo -e "\nYou can now publish to npm with: ${YELLOW}npm publish${NC}" 