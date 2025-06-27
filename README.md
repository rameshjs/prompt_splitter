# Prompt Splitter

## Project Description

Prompt Splitter is a web-based tool designed to assist users in managing large text prompts for AI models, such as ChatGPT. Many AI models have input limitations, often measured in "tokens." Exceeding these limits can lead to truncated responses or errors. This application intelligently segments extensive text inputs into smaller, manageable parts, ensuring that the full context of your prompt is processed by the AI.

## Features

*   **Token Limit Management**: Automatically splits your prompt to fit within typical AI model token constraints.
*   **Context Preservation**: Each generated split part includes specific instructions for the AI, guiding it to store information and wait for subsequent parts, thereby maintaining the full context across interactions.
*   **User-Friendly Interface**: Provides a simple and intuitive interface for inputting text, setting split sizes, and copying generated parts.
*   **Customizable Split Size**: Offers control over the maximum size of each split part (in characters), allowing fine-tuning for different AI models or specific use cases.

## How to Run Locally

Follow these steps to set up and run the Prompt Splitter application on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

*   Python 3.8 or higher
*   pip (Python package installer)
*   venv (for creating virtual environments, usually comes with Python)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/rameshjs/prompt_splitter.git
    cd prompt-splitter
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows:
    # .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the FastAPI application using Uvicorn:**

    ```bash
    uvicorn main:app --reload
    ```

    The `--reload` flag is optional but recommended for development, as it automatically reloads the server when code changes are detected.

2.  **Access the application:**

    Once the server is running, open your web browser and navigate to:

    ```
    http://127.0.0.1:8000
    ```

    You should see the Prompt Splitter interface.

