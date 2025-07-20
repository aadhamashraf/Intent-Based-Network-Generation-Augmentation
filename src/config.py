"""
This script defines configurable command-line arguments used to control the generation, augmentation, 
and export of synthetic 5G network intent datasets. Designed to support fine-tuned control over how data 
is augmented, saved, and balanced for research or training purposes.

Supported Augmentation Flags:
------------------------------
--use_paraphrasing              Enable T5-based paraphrasing
--use_backtranslation           Enable EN↔FR backtranslation
--use_synonym_aug               Enable WordNet synonym replacement
--use_entity_shuffle            Shuffle tokens within intent text
--use_typo                      Inject character-level typos
--use_out_of_scope              Introduce unrelated out-of-scope samples
--use_ambiguous                 Inject vague or underspecified samples
--use_gpt2_aug                  Enable GPT-2 (GPT-Neo) logical continuation
--use_contextual_synonym_aug   Replace words using spaCy word vector similarity
--use_bert_fill_aug            Enable BERT-based masked word prediction
--use_adversarial_aug          Add perturbation noise (e.g. insertion, deletion)

Additional Parameters:
-----------------------
--paraphrase_ratio              Percentage of intents to paraphrase
--backtranslate_ratio           Percentage of intents to backtranslate
--synonym_ratio                 Percentage of intents to augment with synonyms
--entity_shuffle_ratio          Percentage to apply token shuffle
--out_of_scope_ratio            Fraction of out-of-scope examples
--ambiguous_ratio               Ratio of ambiguous or vague intents
--typo_ratio                    Ratio of intents with typos
--gpt2_ratio                    Percentage for GPT-2 augmentation
--contextual_syn_ratio          Contextual synonym ratio
--bert_fill_ratio               BERT mask-filling ratio
--adversarial_ratio             Ratio for noisy adversarial perturbation

Output:
--------
--output_file                   Destination CSV file (default: 5g_intents_dataset.csv)
--jsonl_file                    Destination JSONL file (default: 5g_intents_dataset.jsonl)
--metadata_file                 JSON metadata summary file

Usage:
------
python generate_intents.py --use_paraphrasing --paraphrase_ratio 0.3 --num_records 5000

Author:
-------
Adham Ashraf
"""

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate 5G Intent Dataset with augmentation options")
    parser.add_argument("--use_paraphrasing", action="store_true", help="Enable paraphrasing")
    parser.add_argument("--use_backtranslation", action="store_true", help="Enable backtranslation")
    parser.add_argument("--use_synonym_aug", action="store_true", help="Enable synonym augmentation")
    parser.add_argument("--paraphrase_ratio", type=float, default=0.30, help="Ratio for paraphrasing (0-1)")
    parser.add_argument("--backtranslate_ratio", type=float, default=0.20, help="Ratio for backtranslation (0-1)")
    parser.add_argument("--synonym_ratio", type=float, default=0.30, help="Ratio for synonym augmentation (0-1)")
    parser.add_argument("--entity_shuffle_ratio", type=float, default=0.10, help="Ratio for entity shuffling (0-1)")
    parser.add_argument("--out_of_scope_ratio", type=float, default=0.05, help="Ratio for out-of-scope examples (0-1)")
    parser.add_argument("--ambiguous_ratio", type=float, default=0.02, help="Ratio for ambiguous examples (0-1)")
    parser.add_argument("--typo_ratio", type=float, default=0.02, help="Ratio for typo injection (0-1)")
    parser.add_argument("--num_records", type=int, default=3000, help="Number of records to generate")
    parser.add_argument("--output_file", type=str, default="3gpp_research_intents.csv", help="CSV output file")
    parser.add_argument("--jsonl_file", type=str, default="3gpp_research_intents.jsonl", help="JSONL output file")
    parser.add_argument("--metadata_file", type=str, default="metadata.json", help="Metadata output file")
    parser.add_argument("--random_seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--use_gpt2_aug", action="store_true", help="Enable GPT-2-based synthesis")
    parser.add_argument("--gpt2_ratio", type=float, default=0.2, help="Ratio for GPT-2 synthesis (0-1)")
    parser.add_argument("--use_contextual_synonym_aug", action="store_true", help="Enable contextual synonym augmentation")
    parser.add_argument("--contextual_syn_ratio", type=float, default=0.2)

    parser.add_argument("--use_bert_fill_aug", action="store_true", help="Enable BERT mask filling")
    parser.add_argument("--bert_fill_ratio", type=float, default=0.2)

    parser.add_argument("--use_adversarial_aug", action="store_true", help="Enable character-level noise")
    parser.add_argument("--adversarial_ratio", type=float, default=0.2)

    args = parser.parse_args()

    for ratio_arg in ["paraphrase_ratio", "backtranslate_ratio", "synonym_ratio", "entity_shuffle_ratio", "out_of_scope_ratio", "ambiguous_ratio", "typo_ratio", "gpt2_ratio", "contextual_syn_ratio", "bert_fill_ratio", "adversarial_ratio"]:
        value = getattr(args, ratio_arg)
        if not (0.0 <= value <= 1.0):
            parser.error(f"{ratio_arg} must be between 0 and 1")
    if args.num_records <= 0:
        parser.error("num_records must be positive")
    return args
