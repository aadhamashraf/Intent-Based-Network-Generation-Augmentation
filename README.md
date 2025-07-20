# Intent-Based-Network-Generation-Augmentation

A comprehensive toolkit for generating, augmenting, analyzing, and evaluating advanced intent-based networking (IBN) datasets tailored for 5G/3GPP research. The system combines modular data synthesis, extensive augmentation options, expert-grade LLM-driven evaluation, and in-depth dataset analytics.

## Features

- **Advanced Intent Generation**: Sophisticated 3GPP-compliant network intent generation
- **Multi-Modal Augmentation**: 11+ augmentation techniques including LLM-based methods
- **Expert Evaluation**: LLM-powered evaluation with domain expertise
- **Comprehensive Analytics**: Statistical and linguistic dataset analysis
- **Research-Grade Quality**: Publication-ready datasets with detailed metadata

## Project Structure

```
├── src/                          # Main source code
│   ├── Intents_Generators/       # Intent generation components
│   ├── Evaluation/               # Evaluation and analysis tools
│   ├── augmentation_utils.py     # Text augmentation utilities
│   ├── config.py                 # Configuration and CLI arguments
│   └── main.py                   # Main execution script
├── data/                         # Data files and datasets
├── LICENSE                       # MIT License
└── README.md                     # This file
```

## Installation

1. Clone the repository:
```bash
https://github.com/aadhamashraf/Intent-Based-Network-Generation-Augmentation.git
cd Intent-Based-Network-Generation-Augmentation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

3. Install Ollama (for LLM evaluation):
```bash
# Follow instructions at https://ollama.ai/
ollama pull mistral
```

## 🚀 Quick Start

### Basic Usage

```bash
# Generate 1000 intent records with basic augmentation
python src/main.py --num_records 1000 --use_paraphrasing --paraphrase_ratio 0.3

# Generate with multiple augmentation techniques
python src/main.py \
    --num_records 5000 \
    --use_paraphrasing --paraphrase_ratio 0.3 \
    --use_backtranslation --backtranslate_ratio 0.2 \
    --use_synonym_aug --synonym_ratio 0.25 \
    --output_file "my_dataset.csv"
```

### Advanced Usage

```python
from src.Intents_Generators import Advanced3GPPIntentGenerator
from src.augmentation_utils import paraphrase, back_translate

# Initialize generator
generator = Advanced3GPPIntentGenerator(use_llm_synthesis=True)

# Generate intents
intents = generator.generate_batch(1000)

# Apply augmentation
for intent in intents:
    intent.description = paraphrase(intent.description)

# Export
generator.export_to_csv(intents, "dataset.csv")
```

## Evaluation

### LLM-Based Evaluation

```bash
# Run expert LLM evaluation
python src/Evaluation/LLM_evaluation.py

# Generate evaluation summary
python src/Evaluation/evaluation_summarizer.py evaluated_dataset.jsonl
```

### Statistical Analysis

```bash
# Run comprehensive dataset analysis
python src/Evaluation/base_evaluation.py
```

## Configuration Options

### Augmentation Techniques

| Technique | Flag | Description |
|-----------|------|-------------|
| Paraphrasing | `--use_paraphrasing` | T5-based paraphrasing |
| Back Translation | `--use_backtranslation` | EN↔FR translation |
| Synonym Replacement | `--use_synonym_aug` | WordNet synonyms |
| Entity Shuffling | `--use_entity_shuffle` | Token reordering |
| Typo Injection | `--use_typo` | Character-level errors |
| GPT-2 Synthesis | `--use_gpt2_aug` | Neural text generation |
| Contextual Synonyms | `--use_contextual_synonym_aug` | spaCy-based replacement |
| BERT Fill | `--use_bert_fill_aug` | Masked language modeling |
| Adversarial Noise | `--use_adversarial_aug` | Character perturbations |

### Output Formats

- **CSV**: Structured tabular format
- **JSONL**: Line-delimited JSON for streaming
- **JSON**: Complete research dataset with metadata

##  Dataset Quality Metrics

- **Technical Accuracy**: 3GPP compliance and terminology correctness
- **Realism Score**: Real-world deployment feasibility
- **Research Value**: Academic and industrial relevance
- **Linguistic Quality**: Grammar, clarity, and naturalness
- **Diversity Metrics**: Lexical and semantic variety

## Documentation

Detailed documentation for each module:
- [Intent Generators](src/Intents_Generators/README.md)
- [Evaluation Tools](src/Evaluation/README.md)
- [Augmentation Utilities](docs/augmentation.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Adham Ashraf Eltholth**

## 🙏 Acknowledgments

- Dr. Ghada Soliman
- 3GPP standards community
- HuggingFace transformers library
- spaCy NLP library
- Research community in intent-based networking
