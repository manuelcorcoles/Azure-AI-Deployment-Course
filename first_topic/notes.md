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


# 4.Develop generative AI apps that use tools
- Code interpreter tool: Write and run Python dynamically during a conversation
- Key features:
    - Dynamic Python Execution: The model writes and runs Python code in a sandboxed environment
    - File Handling: Upload, process, and download files (CSV, JSON, images, and so on)
    - Data Analysis: Perform calculations, statistical analysis, and data transformations on the fly
    - Real-time Feedback: The model sees code execution results and can iterate or fix errors
    - Complex Problem Solving: Tackle math problems, simulations, and logic puzzles through executable code

- Code_interpreter -> model analyzes the task to see if code is needed -> if so, generates code and runs results

- Best practices: 
    - Be specific: Describe the data format and expected output clearly. Many models internally use the name python tool to identify the code_interpreter tool - so use this language in your instructions.
    - Provide context: Include relevant domain knowledge in your prompts
    - Validate results: Always review AI-generated code for correctness before using in production
    - Monitor costs: Code execution adds tokens; complex operations may use more resources
    - Leverage libraries: Common packages like pandas, numpy, and matplotlib are pre-installed
    - Error handling: The model can see errors and will attempt to fix them automatically

- Limitations: Sandbox env with no external network access -> some libraries may not be available, timeout limits and memory constraints

- web_search tool:
    - Live information retrieval - Get recent information not available in static model training data
    - Source-grounded responses - Build answers from retrieved web content
    - Reduced hallucination risk - Improve reliability by checking external sources
    - Automatic query generation - The model decides when and how to search based on user intent
    - Seamless user experience - Search and response generation happen in one flow

- Limitations:
    - Results depend on what is publicly available and indexable at query time
    - Source quality can vary, so output may still require human review
    - Retrieved content may change over time, so repeated runs can produce different answers
    - Some environments may apply regional, policy, or network restrictions to web access

- file_search tool:
    - Document-grounded answers - Responses are based on your uploaded files
    - Semantic retrieval - Finds relevant passages by meaning, not only exact keyword matches
    - Vector store integration - Search across one or more indexed document collections
    - Citations and transparency - Include matched results for debugging and traceability
    - Better enterprise relevance - Use organization-specific knowledge in model outputs

- Limitations:
    - Answer quality depends on document quality, coverage, and chunk relevance
    - Very large or mixed-domain stores can return less focused context
    - Updated source files may require re-indexing before new content is searchable
    - Retrieval improves grounding but doesn't replace human review for sensitive decisions

- function tool:
    - Structured tool calls - The model emits explicit function-call requests
    - Developer-controlled execution - Your application decides how and where functions run
    - Reliable integration pattern - Call APIs, internal services, or helper utilities safely
    - Multi-turn orchestration - Return tool output and let the model continue reasoning
    - Grounded responses - Answers can include live, system-generated data

- Best practices:
    - Keep tools focused - Small, single-purpose functions are easier to control and test
    - Validate function inputs - Never trust tool arguments blindly in production systems
    - Handle errors safely - Return clear error outputs the model can reason about
    - Log tool usage - Track calls, latency, and failure rates for debugging and governance
    - Limit sensitive operations - Require explicit authorization for high-impact actions

- Limitations: 
    - The model requests function calls, but your application must run them
    - Incorrect or unexpected tool arguments can occur and should be validated
    - Tool latency can increase end-to-end response time
    - Function calling improves reliability, but final outputs still need review for critical decisions


# 5.Optimize generatie ai model performance
- Prompt engineering: Prompt components:
    - System message: Instructions that define the model's behavior, role, and constraints.
        - Start with the assistant's role: State the role and the expected outcome for a typical request.
        - Define boundaries: List the topics, actions, and content types the assistant should avoid.
        - Specify the output format: If you need a specific format, state it plainly and keep it consistent.
        - Add a "when unsure" policy: Tell the model what to do when the user's request is ambiguous, out of scope, or when the model lacks information.
    - User message: The question or input from the user.
    - Assistant message: Previous model responses, used in multi-turn conversations.
    - Examples: Sample input/output pairs that demonstrate the expected response format.

- Prompt patterns:
    - Persona pattern: Instruct model to take on a specific perspective/role
    - Format template pattern: Provide a structure/template in your prompt
    - Chain-of-thought pattern: Ask model to explain its reasoning step by step
    - Few-shot learning pattern: Provide one or more examples

- Model parameters: temperature and Top_p (randomness but by limiting the model to a subset of the most probable next tokens) -> only adjust one
- Prompt engineering keeps cost low, guides model tone, format and behavior, but might not be enough if the model does not have access to the information

- RAG:
    - Azure AI Search to store indexes
    - Azure AI Search supports keyword, semantic, vector, hybrid search 

- Fine-tuning:
    - When to fine-tune: 
        - Consistent style and tone: Your organization has a specific brand voice, and the model needs to follow it reliably across all interactions. For example, the travel agency wants every response to use a warm, encouraging tone with short paragraphs.
        - Specific output formats: You need the model to reliably produce structured output, like JSON responses following a defined schema, and few-shot examples alone aren't sufficient.
        - Reducing prompt length: Long system messages with many examples consume tokens and increase latency. Fine-tuning embeds those patterns into the model, reducing the prompt size needed for each request.
        - Distillation: You want to transfer the capabilities of a large, expensive model to a smaller, more efficient one. For example, you can collect outputs from a high-performing model and use them to fine-tune a smaller model that achieves similar quality at lower cost and latency.
        - Enhancing tool usage: When your application uses tool calling, fine-tuning with tool examples can improve the accuracy of tool selection and parameter generation.


- Types of fine-tuning:
    - Supervised fine-tuning (SFT): Train the model on a labeled dataset of prompt-and-response pairs. The model learns to produce outputs that match the patterns in your training data. This technique works best when there are clear, well-defined ways to approach a task.
    - Reinforcement fine-tuning (RFT): Optimize the model's behavior through iterative feedback, using a grader to reward better responses incrementally. RFT works well for complex or dynamic tasks where there are many possible solutions and you want to improve the model's reasoning quality.
    - Direct Preference Optimization (DPO): Align the model based on human preferences by providing preferred and non-preferred response pairs. DPO is computationally lighter than traditional reinforcement learning approaches while being equally effective at alignment.

- Fine-tuning training: Including a system message in your training data is important. Leaving it blank tends to produce lower-accuracy models. Use the same system message when you deploy your fine-tuned model for inference.

- Fine tuning challenges: 
    - Training costs: Fine-tuning has upfront costs for training and ongoing hourly costs for hosting the custom model.
    - Data quality requirements: Poor-quality or unrepresentative training data leads to overfitting, underfitting, or bias.
    - Maintenance: Fine-tuned models may need to be retrained when data changes or when updated base models are released.
    - Experimentation: Finding the right combination of hyperparameters (epochs, batch size, learning rate) requires testing and iteration.
    - Model drift: Specializing too narrowly can make the model less effective at general language tasks outside the fine-tuned domain.

- Combination of optimization strategies:
    - Prompt engineering + RAG: Behavior and context
    - Prompt engineering + fine-tuning: use when you need the model to consistently follow a specific style or format
    - RAG + fine-tuning: factual grounding and consistent behaviour

    