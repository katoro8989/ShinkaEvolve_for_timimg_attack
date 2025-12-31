import sys
import os
import time
import statistics
import math
import json
import argparse
import importlib.util

def run_evaluation(program_path: str):
    """
    Evaluate the constant-time implementation by checking for consistent execution time across different inputs.
    """
    with open(program_path, 'r') as f:
        code_content = f.read()
    
    forbidden_patterns = [
        'hmac.compare_digest',
        'secrets.compare_digest',
        'hashlib.compare_digest',
    ]
    
    for pattern in forbidden_patterns:
        if pattern in code_content:
            return 0.0, f"FORBIDDEN: Use of standard library function '{pattern}' is not allowed. You must implement constant-time comparison yourself.", None, None
    
    try:
        spec = importlib.util.spec_from_file_location("candidate_module", program_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        func = module.secure_compare
    except Exception as e:
        return 0.0, f"Syntax/Import Error: {e}", None, None

    SECRET = "SUPER_SECRET_KEY_256"
    
    case_match = SECRET
    
    case_mismatch_first = "X" + SECRET[1:]
    
    case_mismatch_last = SECRET[:-1] + "X"
    
    case_mismatch_mid = SECRET[:len(SECRET)//2] + "X" + SECRET[len(SECRET)//2+1:]

    try:
        if not func(SECRET, case_match):
            return 0.0, "FAILED: Returns False for matching strings.", None, None
        if func(SECRET, case_mismatch_first):
            return 0.0, "FAILED: Returns True for non-matching strings (first char).", None, None
        if func(SECRET, case_mismatch_last):
            return 0.0, "FAILED: Returns True for non-matching strings (last char).", None, None
        if func(SECRET, case_mismatch_mid):
            return 0.0, "FAILED: Returns True for non-matching strings (mid char).", None, None
    except Exception as e:
        return 0.0, f"Runtime Error: {e}", None, None

    ITERATIONS = 5000
    times_match = []
    times_first = []
    times_last = []
    times_mid = []
    
    import gc
    gc.disable()
    
    try:
        for _ in range(ITERATIONS):
            t0 = time.perf_counter_ns()
            func(SECRET, case_match)
            t1 = time.perf_counter_ns()
            times_match.append(t1 - t0)
            
            t0 = time.perf_counter_ns()
            func(SECRET, case_mismatch_first)
            t1 = time.perf_counter_ns()
            times_first.append(t1 - t0)
            
            t0 = time.perf_counter_ns()
            func(SECRET, case_mismatch_last)
            t1 = time.perf_counter_ns()
            times_last.append(t1 - t0)
            
            t0 = time.perf_counter_ns()
            func(SECRET, case_mismatch_mid)
            t1 = time.perf_counter_ns()
            times_mid.append(t1 - t0)
            
    except Exception as e:
        gc.enable()
        return 0.0, f"Error during timing: {e}", None, None
    finally:
        gc.enable()

    all_times = {
        "match": times_match,
        "first": times_first,
        "last": times_last,
        "mid": times_mid,
    }
    
    avg_times = {k: statistics.mean(v) for k, v in all_times.items()}
    
    max_diff = max(avg_times.values()) - min(avg_times.values())
    
    all_measurements = times_match + times_first + times_last + times_mid
    mean_all = statistics.mean(all_measurements)
    stdev_all = statistics.stdev(all_measurements) if len(all_measurements) > 1 else 0
    coefficient_of_variation = (stdev_all / mean_all) if mean_all > 0 else float('inf')
    
    diffs = []
    patterns = list(avg_times.keys())
    for i in range(len(patterns)):
        for j in range(i + 1, len(patterns)):
            diffs.append(abs(avg_times[patterns[i]] - avg_times[patterns[j]]))

    base_score = 50.0

    if max_diff <= 0:
        timing_bonus = 50.0
    else:
        timing_bonus = max(0.0, math.log10(1000.0 / (max_diff + 1.0)) * 15.0)
        timing_bonus = min(timing_bonus, 50.0)

    cv_bonus = 0.0
    if coefficient_of_variation < 0.01:
        cv_bonus = 10.0
    elif coefficient_of_variation < 0.05:
        cv_bonus = 5.0
    elif coefficient_of_variation < 0.1:
        cv_bonus = 2.0
    
    total_score = base_score + timing_bonus + cv_bonus
    total_score = min(total_score, 100.0)

    feedback = f"""
[EVALUATION RESULTS]
Correctness: PASS
Average Execution Times:
  - Match (full):     {avg_times['match']:.2f} ns
  - Mismatch (first): {avg_times['first']:.2f} ns
  - Mismatch (last):  {avg_times['last']:.2f} ns
  - Mismatch (mid):   {avg_times['mid']:.2f} ns

Timing Analysis:
  - Max Time Difference: {max_diff:.2f} ns (Lower is better)
  - Coefficient of Variation: {coefficient_of_variation:.4f} (Lower is better)
  - Standard Deviation: {stdev_all:.2f} ns

Score Breakdown:
  - Base Score (Correctness): {base_score:.2f}
  - Timing Bonus: {timing_bonus:.2f}
  - CV Bonus: {cv_bonus:.2f}
  - Total Score: {total_score:.2f}
    """.strip()
    
    metrics_data = {
        "diff_ns": max_diff,
        "avg_match": avg_times['match'],
        "avg_first": avg_times['first'],
        "avg_last": avg_times['last'],
        "avg_mid": avg_times['mid'],
        "coefficient_of_variation": coefficient_of_variation,
        "stdev": stdev_all,
        "max_diff": max_diff,
    }
    
    return total_score, feedback, metrics_data


def main(program_path: str, results_dir: str):
    score, feedback, metrics_data = run_evaluation(program_path)
    
    os.makedirs(results_dir, exist_ok=True)
    
    metrics = {
        "combined_score": score,
        "public": {
            "score": score,
            "success": (score >= 90.0),
        },
        "private": metrics_data if metrics_data else {},
        "text_feedback": feedback,
    }
    
    metrics_path = os.path.join(results_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    
    is_correct = score > 0.0 and "FAILED" not in feedback and "Error" not in feedback
    correct_payload = {
        "correct": is_correct,
        "error": None if is_correct else feedback,
    }
    correct_path = os.path.join(results_dir, "correct.json")
    with open(correct_path, "w") as f:
        json.dump(correct_payload, f, indent=2)
    
    return {
        "score": score,
        "public": score,
        "text_feedback": feedback,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--program_path", required=True)
    parser.add_argument("--results_dir", required=True)
    args = parser.parse_args()
    
    result = main(args.program_path, args.results_dir)
    print(result["text_feedback"])