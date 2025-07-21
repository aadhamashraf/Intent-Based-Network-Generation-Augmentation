# Intent-Based-Network-Generation-Augmentation

A comprehensive toolkit for generating, augmenting, analyzing, and evaluating advanced intent-based networking (IBN) datasets tailored for 5G/3GPP research. The system combines modular data synthesis, extensive augmentation options, expert-grade LLM-driven evaluation, and in-depth dataset analytics.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/aadhamashraf/Intent-Based-Network-Generation-Augmentation.git
cd Intent-Based-Network-Generation-Augmentation

# Setup environment (recommended)
python scripts/setup_environment.py

# Or manual setup
pip install -r requirements.txt
python -m spacy download en_core_web_md

# Generate your first dataset
python src/main.py --num_records 100 --use_paraphrasing --paraphrase_ratio 0.3
```

## Features

- **Advanced Intent Generation**: Sophisticated 3GPP-compliant network intent generation
- **Multi-Modal Augmentation**: 11+ augmentation techniques including LLM-based methods
- **Expert Evaluation**: LLM-powered evaluation with domain expertise
- **Comprehensive Analytics**: Statistical and linguistic dataset analysis
- **Research-Grade Quality**: Publication-ready datasets with detailed metadata
- **Production Ready**: Docker support, API server, and comprehensive testing
- **Extensible Architecture**: Plugin-based augmentation and constraint systems

## Project Structure

```
├── src/                          # Main source code
│   ├── Intents_Generators/       # Intent generation components
│   ├── Evaluation/               # Evaluation and analysis tools
│   ├── augmentation_utils.py     # Text augmentation utilities
│   ├── config.py                 # Configuration and CLI arguments
│   └── main.py                   # Main execution script
├── tests/                        # Test suite
├── scripts/                      # Utility scripts
├── docker/                       # Docker configuration
├── notebooks/                    # Jupyter notebooks
├── data/                         # Data files and datasets
├── docs/                         # Documentation
├── LICENSE                       # MIT License
├── setup.py                      # Package setup
├── Makefile                      # Build automation
└── README.md                     # This file
```

## Installation

### Option 1: Automated Setup (Recommended)
```bash
git clone https://github.com/aadhamashraf/Intent-Based-Network-Generation-Augmentation.git
cd Intent-Based-Network-Generation-Augmentation
python scripts/setup_environment.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_md

# Install package in development mode
pip install -e .
```

### Option 3: Docker Setup
```bash
# Build and run with Docker Compose
cd docker
docker-compose up ibn-toolkit

# Or build manually
docker build -f docker/Dockerfile -t ibn-toolkit .
docker run -v $(pwd)/output:/app/output ibn-toolkit
```

### Optional: LLM Evaluation Setup
```bash
# Install Ollama for advanced evaluation
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

# Using Make commands
make generate                    # Generate sample dataset
make quick-test                  # Quick test with 10 records
make full-test                   # Full pipeline test
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

### API Usage

```bash
# Start API server
python scripts/api_server.py

# Or with Docker
docker-compose up ibn-api

# Generate intents via API
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"num_records": 10, "use_llm_synthesis": false}'
```

### Jupyter Notebook

```bash
# Start Jupyter server
docker-compose up ibn-jupyter

# Or locally
jupyter notebook notebooks/
```

## 🧪 Testing

```bash
make test                        # Run all tests
python -m pytest tests/ -v      # Detailed test output
make lint                        # Code quality checks
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

## 🔧 Development

```bash
make dev-setup                   # Setup development environment
make format                      # Format code
make build                       # Build package
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
