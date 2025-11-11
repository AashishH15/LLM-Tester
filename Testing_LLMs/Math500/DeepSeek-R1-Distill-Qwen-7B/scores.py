# Read from the json file and compare the true/questions
import json
import sys

def main():
    with open('Qwen2.5-14B_math500_evaluation_results.json') as f:
        data = json.load(f)
    total = 0
    correct_count = 0
    for item in data:
        total += 1
        if item.get("is_correct") == True:
            correct_count += 1
    accuracy = (correct_count / total) * 100 if total > 0 else 0
    print(f"Total Questions: {total}")
    print(f"Correct Answers: {correct_count}")
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == '__main__':
    main()
