# LLM Tester

This project is designed for testing and evaluating Large Language Models (LLMs) across various tasks and scenarios. It includes components for running local and online LLM tests, as well as evaluating their performance on specific benchmarks like mathematical problems.

## Project Structure

- `LLM Tester/`: Contains the core LLM testing framework, including:
    - `LLM Ranking.md`: Documentation or results related to LLM rankings.
    - `main.py`: Main script for running LLM tests or evaluations.
    - `training_data.npz`: Data used for training or evaluation.
    - `Hexagon_Ball Coding/`: Sub-project likely involving coding challenges or specific tasks for LLMs.
        - `Local/`: Scripts for testing locally hosted LLMs.
        - `Online/`: Scripts for interacting with online LLM APIs (e.g., ChatGPT, Claude, Gemini).

- `Testing_LLMs/`: Dedicated directory for specific LLM evaluation benchmarks.
    - `Math500/`: Evaluation results and scripts for mathematical problem-solving tasks.
        - `DeepSeek-R1-Distill-Qwen-7B/`: Results and testing scripts for the DeepSeek-R1-Distill-Qwen-7B model on Math500.
        - `Math500_Qwen2.5-14B/`: Results and testing scripts for the Qwen2.5-14B model on Math500.

## Getting Started

To get a local copy up and running, follow these steps:

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AashishH15/LLM-Tester.git
   cd LLM-Tester
   ```
2. Install necessary Python packages (specific requirements may vary per sub-project, check individual directories for `requirements.txt` files):
   ```bash
   pip install -r requirements.txt # If a global requirements.txt exists
   ```

### Running Tests

Refer to the specific sub-directories (`LLM Tester/Hexagon_Ball Coding/Local/`, `LLM Tester/Hexagon_Ball Coding/Online/`, `Testing_LLMs/Math500/`) for detailed instructions on how to run individual tests and evaluations.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

[Specify your license here, e.g., MIT License]

## README made by Gemini 2.5-Flash