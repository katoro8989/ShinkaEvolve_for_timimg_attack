# ShinkaEvolve for Timing Attack Mitigation

This repository uses [ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve) to evolve secure, constant-time string comparison implementations that resist timing attacks.

## Overview

Timing attacks are a class of side-channel attacks where an attacker exploits variations in execution time to infer sensitive information. This project demonstrates how evolutionary algorithms, guided by LLMs, can automatically discover and refine constant-time comparison functions that eliminate timing vulnerabilities.

### The Problem

The initial implementation (`initial.py`) contains a vulnerable string comparison function that uses early returns:

```python
def secure_compare(secret: str, input_val: str) -> bool:
    if len(secret) != len(input_val):
        return False
    for i in range(len(secret)):
        if secret[i] != input_val[i]:
            return False  # Early return creates timing leak!
    return True
```

This implementation leaks information through execution time: comparisons that fail early (e.g., first character mismatch) execute faster than those that fail later (e.g., last character mismatch), allowing attackers to infer the secret character-by-character.

### The Solution

Using ShinkaEvolve, we evolve implementations that:
- **Maintain correctness**: Return `True` for matching strings, `False` for non-matching strings
- **Eliminate timing variance**: Execution time is statistically identical regardless of where mismatches occur
- **Avoid standard library functions**: Implement constant-time comparison manually (no `hmac.compare_digest` or similar)

## Project Structure

```
.
├── environment.py      # BlackBoxOracle with timing-vulnerable PIN verification
├── evaluate.py         # Evaluation script that measures timing variance
├── initial.py          # Starting solution (vulnerable implementation)
├── run_shinka.py       # ShinkaEvolve configuration and runner
└── README.md           # This file
```

### Key Files

- **`environment.py`**: Contains a `BlackBoxOracle` class that simulates a timing-vulnerable authentication system. The `attempt_unlock` method leaks timing information by sleeping for 0.05 seconds per character before detecting a mismatch.

- **`evaluate.py`**: Comprehensive evaluation script that:
  - Validates correctness (matching and non-matching cases)
  - Measures execution time across 5000 iterations
  - Tests multiple scenarios (full match, first char mismatch, last char mismatch, mid char mismatch)
  - Calculates timing variance metrics (max difference, coefficient of variation)
  - Scores implementations based on both correctness and timing consistency

- **`initial.py`**: The starting point for evolution - a vulnerable implementation that will be improved by the evolutionary process.

- **`run_shinka.py`**: Configures and launches the ShinkaEvolve evolution process with:
  - Custom system prompts emphasizing constant-time requirements
  - Multiple LLM models for diverse mutations
  - Archive-based knowledge retention
  - Local job execution configuration

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd ShinkaEvolve_for_timimg_attack
```

2. Install ShinkaEvolve as a Python package:

**Using uv (recommended):**
```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv --python 3.11
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install ShinkaEvolve from GitHub
uv pip install git+https://github.com/SakanaAI/ShinkaEvolve.git
```

**Using pip:**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install ShinkaEvolve from GitHub
pip install git+https://github.com/SakanaAI/ShinkaEvolve.git
```

3. Configure your LLM API keys (OpenAI, Anthropic, etc.) as required by ShinkaEvolve. Set environment variables or configure API keys according to your LLM provider's requirements.

## Usage

### ShinkaEvolve as a Python API

ShinkaEvolve can be used as a Python API, similar to `import numpy`. After installing ShinkaEvolve, you can import and use its components directly in your Python code:

```python
from shinka.core import EvolutionRunner, EvolutionConfig
from shinka.database import DatabaseConfig
from shinka.launch import LocalJobConfig

# Configure evolution parameters
evo_config = EvolutionConfig(
    init_program_path="initial.py",
    num_generations=100,
    max_parallel_jobs=8,
    llm_models=["gpt-4o-mini"],
    # ... other configuration options
)

# Configure job execution
job_config = LocalJobConfig(
    eval_program_path="evaluate.py",
)

# Configure database
db_config = DatabaseConfig(
    db_path="evolution.db",
    archive_size=100,
)

# Create and run the evolution
runner = EvolutionRunner(
    evo_config=evo_config,
    job_config=job_config,
    db_config=db_config,
)

runner.run()
```

This project uses ShinkaEvolve programmatically in `run_shinka.py` rather than using the command-line `shinka_launch` tool. This approach provides:
- **Full programmatic control**: Configure everything in Python code
- **Customization**: Easy to modify parameters, add custom logic, or integrate with other tools
- **Reproducibility**: All configuration is in code, making experiments easier to reproduce

### Running Evolution

Start the evolution process:

```bash
python run_shinka.py
```

The evolution will:
1. Start with the vulnerable implementation in `initial.py`
2. Generate candidate solutions using LLM-guided mutations
3. Evaluate each candidate for correctness and timing consistency
4. Select the best performers for the next generation
5. Continue for the configured number of generations (default: 100)

### Evaluation Metrics

The evaluation script scores implementations on:

- **Correctness (50 points)**: Basic functional requirements
- **Timing Bonus (up to 50 points)**: Based on maximum timing difference between test cases
- **Coefficient of Variation Bonus (up to 10 points)**: Rewards low variance in execution times

Total score ranges from 0-100, with higher scores indicating better constant-time properties.

### Monitoring Progress

Results are stored in the database specified in `run_shinka.py` (`pin_cracking_evolution.db` by default). You can monitor the evolution process and view generated solutions through ShinkaEvolve's WebUI or by querying the database directly.

## References

- [ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve): The evolutionary framework used in this project

## License

This project uses ShinkaEvolve, which is licensed under Apache-2.0. Please refer to the [ShinkaEvolve repository](https://github.com/SakanaAI/ShinkaEvolve) for license details.