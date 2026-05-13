## Develop generative AI apps in Azure

# 3. Develop a genAi chat app with Foundry

- Model playground -> play with models and adjust parameters
- Typical workflow:
    - 1. Explore the playground
    - 2. Generate code samples -> ready-to-use integration in your app
    - 3. Develop your application -> customize previous code to your needs
    - 4. Iterate and refine with playground

- Endpoints: Foundry provides 2 endpoints for connecting and consuming projects assets (model deployments)
    - Project endpoint and Azure OpenAI endpoint
- Client SDK: Microsoft Foundry SDK or OpenAI SDK -> slight differences but both support submitting prompts
- Authentication of production applications ususally via Microsoft Entra ID, sometimes also key-based or token-based
- Chat API: 2 modes -> Response and chat completion

- To access the project successfully, the code must run in an authenticated Azure session. For example, you can use the Azure CLI az login command to sign in before running the code.

- Use the project client to:
    Retrieve resource connections
    Access project configuration
    Enable tracing
    Manage datasets and indexes

- The OpenAI SDK is the official client library for calling the OpenAI API.

- Azure OpenAI endpoint: https://{resource-name}.openai.azure.com/openai/v1

- Use API keys with caution. Store them securely in Azure Key Vault and never include them directly in your code.

- OpenAI client handles model inference operations. Use it for:
    - Generating responses with the Responses API
    - Chat completions and image generation
    - Accessing Foundry direct models (non-Azure OpenAI models)

- When to use Foundry SDK:
    - Use the Foundry SDK when your application needs Foundry-specific capabilities:
        - Foundry Agent Service for building and managing AI agents
        - Tool invocation and approval workflows
        - Cloud evaluations for testing and validating AI responses
        - Tracing and observability for monitoring application behavior
        - Foundry direct models (non-Azure OpenAI models available through the model catalog)
        - Project metadata, connections, and governance features

- When to use the OpenAI SDK
    - Use the OpenAI SDK when you need maximum compatibility with the OpenAI API:

        - Full OpenAI API compatibility for existing code and tooling
        - Portability between OpenAI and Azure OpenAI deployments
        - Chat Completions, Responses, and Images APIs
        - Minimal dependency on Foundry-specific concepts
    - The OpenAI SDK is ideal for model inference workloads where you want existing OpenAI code to work with minimal changes. However, this approach doesn't provide Foundry-specific features like agents or evaluations.

- Responses API:
    The Responses API offers several advantages over traditional chat completions:
    - Stateful conversations: Maintains conversation context across multiple turns
    - Unified experience: Combines chat completions and Assistants API patterns
    - Foundry direct models: Works with models hosted directly in Microsoft Foundry, not just Azure OpenAI models
    - Simple integration: Access through the OpenAI-compatible client

- You can manage conversations manually -> select which messages to append and so on ->useful for customizing, conversation pruning to manage token limits and store/restore conversations from DB

- Watch out for long conversation and the context window

- Async usage: for high performance apps, asychronous client allows to make non-blocking API calls -> IDEAL for long-running requests or multiple requests concurrently

- Chat completion API:
    - Responses ar enot stateful so you have to manage them manually
