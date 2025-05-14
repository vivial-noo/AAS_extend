# AAS_extend

This project primarily uses the **Agents-SDK** to construct multiple agents that perform **data fusion** based on the AAS services provided by the **AAS-BaSyx-Python** library. It involves data exchange between different AAS servers, interactions among AAS instances on the same server, and the integration of external data sources (currently including **HTTP**, **MySQL**, and **local files** such as **Excel** and **TXT** files).

## Basic Setup

(Coming soon...)

## Model Support

This project supports integration with common large language models (LLMs), such as **ChatGPT-4o** and **DeepSeek R1**.

### Model Embedding

The system automatically retrieves the latest **IDTA templates**, generates JSON-based training datasets and vector embeddings. By leveraging **model embedding**, the system optimizes token usage for querying and performing CRUD (Create, Read, Update, Delete) operations on submodels, avoiding exceeding the token limit of the LLM API.

## Agents Overview

A top-level **Triage Agent** is responsible for dispatching tasks to three primary types of agents:

- **AAS_AGENT**  
- **FUSION_AGENT**  
- **DATA_AGENT**

### Triage Agent

The **Triage Agent** acts as a coordinator that delegates incoming requests to appropriate lower-level agents based on task type.

### AAS_AGENT

The **AAS_AGENT** handles natural language queries to match and retrieve AAS templates. It supports operations such as:

- Querying existing templates via natural language
- Creating, updating, and deleting submodels and their properties
- Automatically matching templates and generating compliant submodels

These functionalities are implemented using the **AAS-BaSyx-Python** SDK, with additional toolflows for submodel manipulation.

### FUSION_AGENT

The **FUSION_AGENT** is responsible for:

- Data format conversion  
- Arithmetic and logic operations  
- Serialization and deserialization  
- Preparing data for submodel construction  

### DATA_AGENT

The **DATA_AGENT** manages access to external data sources, such as:

- HTTP APIs  
- MySQL databases  
- Local files (e.g., Excel, TXT)  

### MCP Servers

Common utility functions for **AAS_AGENT** operations are encapsulated in `AAS_Server.py`.

(More details coming...)
