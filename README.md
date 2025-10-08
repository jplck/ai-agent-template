# AI Agent Template

A template for building AI agents using Azure AI Foundry and the Agent Framework.

## Features

- **Azure AI Foundry**: Leverages Azure's AI services for agent orchestration
- **Agent Framework DevUI**: Interactive web interface for testing and debugging agents
- **Infrastructure as Code**: Bicep templates for reproducible Azure deployments
- **Dev Container**: Pre-configured development environment

## Quick Start with DevUI

The fastest way to start experimenting with agents is using the **Agent Framework DevUI** - an interactive web interface for building, testing, and debugging your AI agents.

### Prerequisites

- Python 3.12+
- Azure subscription with access to Azure AI Foundry

### Get Started in 3 Steps

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your environment** (see [full setup guide](#getting-started) for Azure deployment)
   ```bash
   # Create a .env file with your Azure AI credentials
   PROJECT_ENDPOINT="your-endpoint-url"
   PROJECT_API_KEY="your-api-key"
   ```

3. **Launch the DevUI**
   ```bash
   devui ./src --port=8093
   ```

The DevUI will open in your browser at `http://localhost:8093`, where you can:
- 🧪 **Test agents interactively** with a chat interface
- 🔍 **Debug workflows** and inspect agent responses
- 📊 **View conversation history** and trace execution
- ⚡ **Iterate quickly** without writing test code

### DevUI Command Options

```bash
# Basic usage
devui ./src --port=8093

# Custom configuration
devui ./src --port=8080 --no-auto-open --host=0.0.0.0

# Available options:
# --port        Port number (default: 8000)
# --host        Host address (default: 127.0.0.1)
# --auto-open   Auto-open browser (default: true)
```

---

## Full Setup Guide

For a complete Azure deployment with infrastructure provisioning:

## Prerequisites

- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- [Docker](https://docs.docker.com/get-docker/) (for dev container)
- [VS Code](https://code.visualstudio.com/) with [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Azure subscription with access to Azure AI Foundry

## Getting Started

### 1. Open in Dev Container

This repository includes a dev container configuration for a consistent development environment.

1. Open the repository in VS Code
2. When prompted, click **"Reopen in Container"** (or run `Dev Containers: Reopen in Container` from the command palette)
3. Wait for the container to build and start

The dev container includes:
- Python 3.12
- Azure Developer CLI (azd)
- Azure CLI
- GitHub CLI
- Git and other essential tools

### 2. Deploy Azure Infrastructure

Use Azure Developer CLI to provision the required Azure resources:

```bash
# Login to Azure
azd auth login

# Provision and deploy infrastructure
azd up
```

This command will:
- Prompt you to select an Azure subscription
- Ask for an environment name (e.g., "dev", "prod")
- Choose an Azure region
- Provision Azure AI Foundry resources (workspace, project, models)
- Deploy the infrastructure defined in `infra/main.bicep`
- Create a `.env` file with the necessary credentials

### 3. Verify Environment Variables

After running `azd up`, check that your `.env` file was created with the required variables:

```bash
cat .env
```

Expected variables:
```
AZURE_ENV_NAME="your-env-name"
AZURE_LOCATION="your-location"
AZURE_SUBSCRIPTION_ID="your-subscription-id"
PROJECT_API_KEY="your-api-key"
PROJECT_ENDPOINT="your-endpoint-url"
```

**Note**: The `.env` file is automatically ignored by git to protect your credentials.

### 4. Install Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or if using the dev container, this should already be done via the `postCreateCommand`.

### 5. Run the Application

#### Recommended: DevUI (Interactive Web Interface)

The **DevUI** provides the best development experience with an interactive web interface for testing agents:

```bash
devui ./src --port=8093
```

See the [Quick Start with DevUI](#quick-start-with-devui) section above for more details and options.

#### Alternative: Run Python Script Directly

```bash
python src/app.py
```

#### Alternative: Debug with VS Code

1. Open `src/app.py` in VS Code
2. Press **F5** or click **Run > Start Debugging**
3. The launch configuration will:
   - Load environment variables from `.env`
   - Start the application in debug mode
   - Allow you to set breakpoints and inspect variables

The launch configuration is defined in `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "envFile": "${workspaceFolder}/.env"
    }
  ]
}
```

## Project Structure

```
.
├── .devcontainer/          # Dev container configuration
│   ├── devcontainer.json   # Container settings and features
│   └── Dockerfile          # Minimal Python container
├── infra/                  # Azure infrastructure (Bicep)
│   ├── main.bicep          # Main infrastructure template
│   ├── main.parameters.json
│   └── modules/            # Modular Bicep files
├── src/                    # Application source code
│   └── app.py              # Main application entry point
├── .env                    # Environment variables (git-ignored)
├── .gitignore              # Git ignore rules
├── azure.yaml              # Azure Developer CLI configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Authentication

The application uses **API key authentication** with Azure AI Foundry. Environment variables are loaded from `.env` using `python-dotenv`.

Example:
```python
from azure.core.credentials import AzureKeyCredential

chat_client = AzureOpenAIChatClient(
    deployment_name="gpt-4.1",
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    api_key=os.getenv("PROJECT_API_KEY")
)
```

## Development

### Debugging

- Set breakpoints in VS Code
- Press **F5** to start debugging
- Use the Debug Console to inspect variables
- The `.env` file is automatically loaded

### Making Changes

1. Modify code in `src/app.py`
2. Update infrastructure in `infra/` Bicep files
3. Run `azd up` to redeploy infrastructure changes
4. Test locally before committing

### Updating Dependencies

```bash
# Add new packages to requirements.txt
pip install <package-name>
pip freeze > requirements.txt
```

## Cleanup

To delete all Azure resources created by this project:

```bash
azd down
```

This will remove all provisioned resources and help avoid unnecessary Azure costs.

## Troubleshooting

### Authentication Errors (401)

If you see `Error code: 401 - Unauthorized`:

1. Verify `.env` file exists and contains `PROJECT_API_KEY` and `PROJECT_ENDPOINT`
2. Run `azd up` to regenerate credentials
3. Ensure `python-dotenv` is installed: `pip install python-dotenv`

### Missing Environment Variables

If environment variables aren't loading:

1. Check that `.env` file exists in the project root
2. Verify `load_dotenv()` is called at the top of `src/app.py`
3. Restart the debugger to reload environment variables

### Azure Resources Not Found

If resources aren't provisioned:

1. Run `azd up` to create infrastructure
2. Check the Azure portal for resource status
3. Verify you have proper permissions in your Azure subscription

## Learn More

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Agent Framework](https://github.com/microsoft/agent-framework)
- [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

## License

See [LICENSE](LICENSE) file for details.
