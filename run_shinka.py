from shinka.core import EvolutionRunner, EvolutionConfig
from shinka.database import DatabaseConfig
from shinka.launch import LocalJobConfig

job_config = LocalJobConfig(
    eval_program_path="evaluate.py",
)

db_config = DatabaseConfig(
    db_path="pin_cracking_evolution.db",
    archive_size=100,
)

evo_config = EvolutionConfig(
    init_program_path="initial.py",
    num_generations=100,
    max_parallel_jobs=8,
    max_patch_attempts=3,
    llm_models=["gpt-4o-mini", "gpt-5-nano"],
    llm_kwargs=dict(
        temperatures=[0.0, 0.5, 1.0],
        reasoning_efforts=["auto", "medium", "high"],
        max_tokens=32768,
    ),
    patch_types=["diff", "full", "cross"],
    patch_type_probs=[0.4, 0.4, 0.2],
    language="python",
    meta_rec_interval=10,
    meta_llm_models=["gpt-4o-mini", "gpt-5-nano"],
    meta_llm_kwargs=dict(temperatures=[0.0], max_tokens=16384),
    code_embed_sim_threshold=0.995,
    novelty_llm_models=["gpt-4o-mini", "gpt-5-nano"],
    novelty_llm_kwargs=dict(temperatures=[0.0], max_tokens=16384),
    llm_dynamic_selection="ucb1",
    llm_dynamic_selection_kwargs=dict(exploration_coef=1.0),
    task_sys_msg = """
You are a Cryptographic Engineer specializing in Side-Channel Resistance.

## Task
Refactor the provided `secure_compare` function to be **Constant-Time**.

## The Problem
The current implementation uses standard Python operators (`==`, `!=`) and early return logic. 
This creates a **Timing Leak**: the function returns faster when characters mismatch at the beginning of the string compared to when they mismatch at the end. An attacker can exploit this timing difference to infer the secret string character by character.

## Objective
1. **Maintain Functionality**: Must correctly return True for matching strings and False for non-matching strings.
2. **Eliminate Timing Variance**: The execution time must be STATISTICALLY IDENTICAL regardless of:
   - Where the mismatch occurs (beginning, middle, or end)
   - Whether the strings match completely
   - The length of the strings (after length check)

## Important Constraints
- **DO NOT use standard library functions** like `hmac.compare_digest` or similar built-in constant-time comparison functions.
- You must implement the constant-time comparison logic yourself.
- The goal is to learn and evolve the implementation technique, not to use existing solutions.

## Evaluation Criteria
The function will be tested with multiple scenarios:
- Complete matches
- Mismatches at the first character
- Mismatches at the last character  
- Mismatches in the middle

The evaluation measures the statistical variance in execution time across all these cases. Lower variance = higher score.

Make the code execute in constant time using your own implementation!
"""
)

runner = EvolutionRunner(
    evo_config=evo_config,
    job_config=job_config,
    db_config=db_config,
)

if __name__ == "__main__":
    print("Starting PIN Cracking Attack Evolution...")
    runner.run()