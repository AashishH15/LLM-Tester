import json
import requests
import re
import os
from tqdm import tqdm
from datasets import load_dataset

# Define the model name for the file naming
MODEL_NAME = "DeepSeek R1 Distill Qwen 7B"

dataset = load_dataset("HuggingFaceH4/MATH-500")

# Print one example to see the structure
print("Dataset structure example:", dataset["test"][0])

# Setup connection to your local LLM via LM Studio's API
LM_STUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"

import subprocess

def query_local_llm(prompt):
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
    }
    response = requests.post(LM_STUDIO_API_URL, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# Create a prompt template for math problems
def create_prompt(problem):
    return f"""Solve the following math problem step by step:

Problem: {problem}

Show your work and explain each step clearly. 
MAKE SURE YOU Provide the final answer at the end, marked with "Answer: ".
"""

# Function to extract answer from model response
def extract_answer(response_text):
    # Look for an answer preceded by "Answer:" or "answer:", allow for bold and extra chars, capture any text until newline
    answer_match = re.search(r"(?:Answer|answer):\s*\**\s*([^\n]+)(?:\n|$)", response_text, re.IGNORECASE)
    if answer_match:
        extracted_answer = answer_match.group(1).strip()
        if extracted_answer:
            return extracted_answer

    # Look for LaTeX boxed answers
    boxed_match = re.search(r'\\boxed{([^}]+)}', response_text)
    if boxed_match:
        return boxed_match.group(1).strip()

    # Try to extract coordinates
    coord_answer = extract_coordinates(response_text)
    if coord_answer:
        r, theta_denom = coord_answer
        return f"({r}, π/{theta_denom})" # Standardize coordinate output

    return None


# Check if answers are equivalent
def are_answers_equivalent(answer1, answer2):
    # Fix for empty answers
    if not answer1 or not answer2:
        return False

    # Debug output to spot pattern issues
    print(f"Comparing answers:")
    print(f"  Answer1: '{answer1}'") # Print raw answers for debugging
    print(f"  Answer2: '{answer2}'")

    # Extract coordinates for comparison
    coord1 = extract_coordinates(answer1)
    coord2 = extract_coordinates(answer2)
    print(f"  Extracted coordinates Answer1: {coord1}, Answer2: {coord2}")

    if coord1 and coord2:
        r1, theta_denom1 = coord1
        r2, theta_denom2 = coord2

        print(f"  r1: {r1}, theta_denom1: {theta_denom1}")
        print(f"  r2: {r2}, theta_denom2: {theta_denom2}")

        # Compare radius and angle denominator
        if r1 == r2 and theta_denom1 == theta_denom2:
            return True
        else:
            return False  # Explicitly return False if coordinates are extracted but not equivalent

    # Normalize and compare if not coordinates or p-q
    def normalize(text):
        if not text:
            return ""
        # Extract boxed content if present
        boxed_match = re.search(r'\\boxed{(.*?)}', text)
        if boxed_match:
            text = boxed_match.group(1)
        # Remove LaTeX symbols and formatting
        text = re.sub(r'\\left|\\\right', '', text)
        text = re.sub(r'\\text{(.*?)}', r'\1', text)
        text = re.sub(r'\\frac{(.*?)}{(.*?)}', r'\1/\2', text)
        text = re.sub(r'\\pi|π', 'pi', text)
        # Normalize formatting, spaces, and symbols
        text = text.lower().replace(' ', '').replace('$', '')
        return text

    clean1 = normalize(answer1)
    clean2 = normalize(answer2)

    # Debug normalized forms
    print(f"  Normalized1: '{clean1}'")
    print(f"  Normalized2: '{clean2}'")

    # Try exact matching on normalized answers
    if clean1 == clean2:
        return True

    # Check if one answer contains the other - more robust containment check
    if clean1 and clean2 and (clean1 in clean2 or clean2 in clean1):
        return True

    # For numerical fractions like 14/3
    fraction_pattern = r'(\d+)/(\d+)'
    if re.search(fraction_pattern, clean1) and re.search(fraction_pattern, clean2):
        frac1 = re.search(fraction_pattern, clean1)
        frac2 = re.search(fraction_pattern, clean2)
        if frac1 and frac2:
            num1, den1 = int(frac1.group(1)), int(frac2.group(2)) # Corrected denominator access
            num2, den2 = int(frac2.group(1)), int(frac2.group(2))
            return num1 * den2 == num2 * den1

    # For simple numerical answers
    try:
        nums1 = re.findall(r'\d+', clean1)
        nums2 = re.findall(r'\d+', clean2)
        if nums1 and nums2 and nums1 == nums2:
            return True
    except:
        pass

    return False


def extract_coordinates(text):
    """Extract (r,θ) coordinates from text, more robust regex for dataset solutions. Returns (r, theta_denominator)."""
    patterns = [
        r'\(\s*(\d+)\s*,\s*(?:\\pi|pi|π)\s*/?\s*(\d+)?\s*\)',  # Basic coordinate format
        r'\(\s*(\d+)\s*,\s*(?:\\frac{\\pi}{(\d+)}|(\\pi|pi|π))\s*\)', # Fractions and direct pi
        r'polar\s+coordinates.*?\(\s*(\d+)\s*,\s*(?:\\pi|pi|π)\s*/?\s*(\d+)?\s*\)', # Text format
        # Robust patterns for \\boxed and \\left with variations in spacing and commas
        r'\\boxed\{\\left\( *(\d+) *[,\s]* *\\frac\{\\pi\}\{(\d+)\} *\\right\)\}',
        r'\\boxed\{\\left\( *(\d+) *[,\s]* *(\\pi|pi|π) *\\right\)\}', # handles just pi without fraction
        r'\\left\( *(\d+) *[,\s]* *\\frac\{\\pi\}\{(\d+)\} *\\right\)',
        r'\\left\( *(\d+) *[,\s]* *(\\pi|pi|π) *\\right\)', # handles just pi without fraction
        r'\\boxed{\\left\( *(\d+) *\\frac\{\\pi\}\{(\d+)\} *\\right\)}', # No comma, boxed
        r'\\boxed{\\left\( *(\d+) *(\\pi|pi|π) *\\right\)}', # No comma, boxed, just pi
        r'\\left\( *(\d+) *\\frac\{\\pi\}\{(\d+)\} *\\right\)', # No comma, left
        r'\\left\( *(\d+) *(\\pi|pi|π) *\\right\)', # No comma, left, just pi
        # Fallback for simpler formats without LaTeX
        r'\( *(\d+) *[,\s]* *pi */ *(\d+) *\)', # (3, pi/2) format without LaTeX
        r'\( *(\d+) *[,\s]* *pi *\)', # (3, pi) format without LaTeX
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            r_str = match.group(1)
            denom_str = match.group(2) or match.group(4) or match.group(6) or match.group(8) or match.group(10) or match.group(12) or match.group(14) # handles different group indices based on pattern
            if r_str:
                r = int(r_str)
                theta_denom = int(denom_str) if denom_str and denom_str.isdigit() else (2 if 'frac' in pattern.lower() else 1) # Default to 2 if fraction and 1 if direct pi
                return (r, theta_denom)
    return None

# Function to save results incrementally
def save_results(results, model_name):
    filename = f"{model_name}_math500_evaluation_results.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    return filename

# Function to load existing results from file
def load_results(model_name):
    filename = f"{model_name}_math500_evaluation_results.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

# Evaluate the model
results = load_results(MODEL_NAME)
correct_count = 0

# Create results filename with model name
results_filename = f"{MODEL_NAME}_math500_evaluation_results.json"

# Use the dataset properly
start_index = 0
if results:
    start_index = results[-1]["problem_id"] + 1
    print(f"Resuming evaluation from problem {start_index}")
else:
    print("Starting new evaluation")


for i in range(start_index, len(dataset["test"])):
    example = dataset["test"][i]

    # Check if result already exists
    if any(result["problem_id"] == i for result in results):
        print(f"Problem {i+1} already evaluated. Skipping.")
        continue

    # Add debug info
    print(f"\nProcessing example {i+1}/{len(dataset['test'])}, type: {type(example)}")

    problem = example["problem"]
    solution = example["solution"]

    prompt = create_prompt(problem)

    try:
        response = query_local_llm(prompt)

        # Extract the answer from the response
        extracted_answer = extract_answer(response)
        correct_answer = solution

        print(f"  Extracted answer raw: '{extracted_answer}'") # Debug print
        print(f"  Correct answer raw: '{correct_answer}'")   # Debug print

        # Check if the answer is correct
        is_correct = False
        if extracted_answer:
            is_correct = are_answers_equivalent(extracted_answer, correct_answer)
            if is_correct:
                correct_count += 1

        # Create result entry
        result = {
            "problem_id": i,
            "problem": problem,
            "correct_answer": correct_answer,
            "model_response": response,
            "extracted_answer": extracted_answer,
            "is_correct": is_correct
        }

        # Add to results list
        results.append(result)

        # Save the updated results after each problem
        save_results(results, MODEL_NAME)

        print(f"Problem {i+1}/{len(dataset['test'])}: {'✓ Correct' if is_correct else '✗ Incorrect'}")
        print(f"  Model's answer: {extracted_answer}")
        print(f"  Correct answer (excerpt): {correct_answer[:100]}...\n")
        print(f"  Results saved to {results_filename}\n")

    except Exception as e:
        print(f"Error on problem {i}: {str(e)}")
        import traceback
        traceback.print_exc()

print(f"Evaluation complete. Final results saved to {results_filename}")
accuracy = 0
if results: # avoid division by zero
    accuracy = correct_count / len(results) * 100
print(f"Accuracy: {correct_count}/{len(results)} ({accuracy:.2f}%)")
