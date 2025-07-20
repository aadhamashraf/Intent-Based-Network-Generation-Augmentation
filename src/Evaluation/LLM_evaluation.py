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
    Constructs the detailed, multi-faceted evaluation prompt for the LLM.
    This prompt instructs the model to act as a 5G network architect.
    """
    return f"""
You are a senior 5G network architect and AI researcher specializing in Intent-Based Networking (IBN) and 3GPP standards.
Your task is to conduct a meticulous, multi-faceted evaluation of the following generated network intent record.
The record is provided as a complete JSON object.

Critically analyze all fields: the high-level description, the intent type, and especially the deeply nested `parameters`.
Assess the record for technical accuracy, realism, compliance, and internal consistency.

---
INTENT_JSON: "{intent_json_string}"
---

Respond ONLY in a single, well-formed JSON format with the following structure.
Provide scores on a 1-10 scale where 1 is poor and 10 is excellent.

{{
  "overall_assessment": {{
    "overall_quality_score": "A numerical score from 1-10, representing your holistic evaluation of the sample.",
    "executive_summary": "A brief, one-sentence summary of the intent's quality and primary strengths or weaknesses."
  }},
  "core_technical_evaluation": {{
    "technical_accuracy_score": "1-10. How correct are the technologies, parameters, and values from a 5G architecture perspective?",
    "realism_and_implementability_score": "1-10. Does this intent represent a realistic, real-world operational scenario?",
    "3gpp_compliance_score": "1-10. How well does the intent align with relevant 3GPP (e.g., Rel-16/17) and ETSI NFV standards?",
    "internal_consistency_score": "1-10. Are the parameters within the intent logically consistent?",
    "research_value_score": "1-10. How novel, complex, or insightful is this generated sample for research?"
  }},
  "linguistic_evaluation": {{
    "intent_clarity_score": "1-10. How clear and unambiguous is the intent's 'description' field?",
    "terminology_accuracy_score": "1-10. Is the technical terminology in the 'description' used correctly?",
    "linguistic_naturalness_score": "1-10. How human-like is the phrasing in the 'description'?"
  }},
  "weakness_analysis": {{
    "primary_weakness_category": "Select one from: 'Technical Inaccuracy', 'Lack of Realism', 'Internal Inconsistency', 'Vague Description', 'None'.",
    "detailed_issues_detected": [
      {{
        "issue": "A concise description of a specific problem found.",
        "location": "The JSON path to the problematic field (e.g., 'parameters.qos_parameters.packet_delay_budget').",
        "severity": "High, Medium, or Low"
      }}
    ]
  }},
  "enhancement_recommendations": {{
    "suggested_modifications": [
      {{
        "location": "The JSON path to the field that needs changing.",
        "recommendation": "A specific, actionable suggestion for improvement."
      }}
    ],
    "generator_logic_feedback": "Broader advice on how the data generation logic itself could be improved."
  }}
}}
"""

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


