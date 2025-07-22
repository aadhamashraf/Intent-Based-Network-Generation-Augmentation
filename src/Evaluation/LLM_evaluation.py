# #!/usr/bin/env python3
import subprocess
import json
import pandas as pd
from tqdm import tqdm
import time


INPUT_PATH = "3gpp_research_intents_2025-07-15.csv"
OUTPUT_PATH = "llm_evaluated_samples.jsonl"
LOG_PATH = "evaluation_errors.log"
MODEL = "mistral"         
SAMPLE_SIZE = 10          
RETRY_ATTEMPTS = 2        

def build_evaluation_prompt(intent_json_string: str) -> str:
    """
    Constructs the new detailed evaluation prompt for the LLM.
    This prompt uses the updated evaluation criteria.
    """
    # Extract the description from the JSON for evaluation
    try:
        intent_data = json.loads(intent_json_string)
        text = intent_data.get('description', 'No description available')
        label = intent_data.get('intent_type', 'Unknown')
    except:
        text = intent_json_string
        label = 'Unknown'
    
    return f"""You are an expert in both telecommunications (5G networking) and computational linguistics.
Your task is to critically evaluate the following intent sample and score it across multiple expert criteria.

--- TEXT: "{text}" LABEL: "{label}" ---

Please evaluate and respond with a JSON object containing these fields:

1. grammar_score (1-5): Rate grammar and sentence construction.
2. intent_clarity (1-5): Is the intent of the request unambiguous?
3. domain_relevance (1-5): How appropriate is this text for a 5G intent dataset?
4. linguistic_naturalness (1-5): How human-like and natural is the phrasing?
5. terminology_accuracy (1-5): Are technical terms used correctly (e.g., slices, URLLC, gNB)?
6. hallucination_risk: "None", "Low", "Medium", or "High"
7. label_confidence: How confident are you that the label is correct? (1-5)
8. is_confusing (true/false): Would a model likely misclassify this input?
9. issues_detected: List of critical issues (e.g., "ambiguous phrasing", "domain mismatch", "grammar errors")
10. expert_feedback: Suggest improvement if any.

Respond ONLY with a valid JSON object in this format:
{{
  "grammar_score": 4.5,
  "intent_clarity": 4.0,
  "domain_relevance": 5.0,
  "linguistic_naturalness": 4.2,
  "terminology_accuracy": 4.8,
  "hallucination_risk": "Low",
  "label_confidence": 4.5,
  "is_confusing": false,
  "issues_detected": ["minor grammar issue"],
  "expert_feedback": "Consider rephrasing for better clarity"
}}"""

def evaluate_with_ollama(prompt: str, retries: int = 2) -> dict:
    """
    Sends the prompt to a local Ollama model and retries on timeout.
    """
    timeouts = [512, 1024, 2048] 
    for attempt in range(min(retries + 1, len(timeouts))):
        try:
            result = subprocess.run(
                ["ollama", "run", MODEL, "--format", "json"],
                input=prompt.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeouts[attempt],
                check=True
            )
            return json.loads(result.stdout.decode('utf-8'))
        except subprocess.TimeoutExpired:
            print(f"Timeout on attempt {attempt+1}/{retries+1} ({timeouts[attempt]}s), retrying...")
            time.sleep(5)
        except subprocess.CalledProcessError as e:
            return {"error": f"Ollama process error: {e.stderr.decode('utf-8')}"}
        except json.JSONDecodeError as e:
            raw_response = result.stdout.decode('utf-8') if 'result' in locals() else "No response received"
            return {"error": f"Failed to decode JSON: {e}", "raw_response": raw_response}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}
    return {"error": f"Request failed after {retries + 1} attempts"}

# --- Main Execution ---
print("Starting evaluation prototype...")

try:
    df = pd.read_csv(INPUT_PATH, encoding="utf-8")
    sample_size = min(SAMPLE_SIZE, len(df))
    if sample_size > 0:
        df_sample = df.sample(n=sample_size)
        print(f"Loaded {len(df)} records. Evaluating a random sample of {sample_size}.")
    else:
        print("Input CSV is empty. Exiting.")
        exit()
except FileNotFoundError:
    print(f"Error: Input file not found at '{INPUT_PATH}'")
    exit()
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

evaluated_records = []

with open(LOG_PATH, "w", encoding="utf-8") as log_file:
    for index, row in tqdm(df_sample.iterrows(), total=len(df_sample), desc="Evaluating samples"):
        try:
            parameters_str = row.get("Parameters", "{}")
            if pd.isna(parameters_str):
                parameters_dict = {}
            else:
                parameters_dict = json.loads(parameters_str)

            intent_record = {
                "id": row.get("ID", f"row_{index}"),
                "intent_type": row.get("Intent Type", ""),
                "description": row.get("Description", ""),
                "timestamp": row.get("Timestamp", ""),
                "priority": row.get("Priority", ""),
                "network_slice": row.get("Network Slice"),
                "location": row.get("Location"),
                "parameters": parameters_dict,
                "metadata": {
                    "technical_complexity": row.get("Technical Complexity"),
                    "research_context": row.get("Research Context"),
                    "compliance_standards": row.get("Compliance Standards")
                }
            }

            intent_json_string = json.dumps(intent_record, separators=(',', ':'))
            prompt = build_evaluation_prompt(intent_json_string)

            evaluation_result = evaluate_with_ollama(prompt, retries=RETRY_ATTEMPTS)

            final_record = {
                "original_intent_from_csv": row.to_dict(),
                "llm_evaluation": evaluation_result
            }
            evaluated_records.append(final_record)

            # Log errors for later review
            if "error" in evaluation_result:
                error_log_entry = {
                    "csv_row_index": index,
                    "intent_id": row.get("ID"),
                    "error_details": evaluation_result
                }
                log_file.write(json.dumps(error_log_entry) + "\n")

        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse 'Parameters' JSON in CSV row {index}: {e}"
            print(f"\nWarning: {error_msg}")
            log_file.write(json.dumps({"csv_row_index": index, "error": error_msg}) + "\n")
        except Exception as e:
            error_msg = f"An unexpected error occurred processing row {index}: {e}"
            print(f"\nError: {error_msg}")
            log_file.write(json.dumps({"csv_row_index": index, "error": error_msg}) + "\n")


with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for record in evaluated_records:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print("\n--- Evaluation Complete ---")
print(f"Successfully evaluated and saved {len(evaluated_records)} records to: {OUTPUT_PATH}")
print(f"Errors and failed attempts (if any) are logged in: {LOG_PATH}")
