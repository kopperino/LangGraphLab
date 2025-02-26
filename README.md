# LangGraphLab

LangGraphLab is a collection of example projects demonstrating how to use LangGraph, a powerful framework for building multi-agent systems and workflow orchestration with large language models (LLMs). This repository aims to provide hands-on examples to help developers and researchers learn how to effectively leverage LangGraph in various scenarios.

## Features

- Step-by-step Examples: A variety of example workflows showcasing different use cases of LangGraph.
- Multi-Agent Systems: Implementations of collaborative AI agents using LangGraph.
- No External API Dependency: Examples focus on running locally without requiring external API keys.
- Modular & Extensible: Easily modify and extend the examples for your own projects.

## Getting Started

### Prerequisites

Ensure you have Python installed (recommended version: 3.9+). Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Clone the Repository
```bash
git clone https://github.com/kopperino/LangGraphLab.git
```

### Set Up API Keys

Add your ```OPENAI_API_KEY``` to a ```.env``` file:
```bash
OPENAI_API_KEY=your_api_key_here
```

### Spin Up Local Server

To run examples using a local server, use:
```bash
langgraph dev
```


## Examples Included

* Prompt Chaining: Connecting multiple prompts in sequence.
* Parallelization: Running multiple tasks concurrently.
* Routing: Directing tasks based on conditions.
* Orchestrator-Worker: Managing tasks with orchestrators and workers.
* Evaluator-Optimizer: Evaluating and improving responses iteratively.
* Agent: Implementing AI agents with LangGraph.

## Contributing

Contributions are welcome! If you have an interesting example or improvement, feel free to open a pull request.

## License

This project is licensed under the MIT License.

## Contact

For questions or suggestions, reach out via GitHub issues.