# Evaluation Module

This module provides comprehensive evaluation tools for intent-based networking datasets, combining statistical analysis, linguistic assessment, and expert-level LLM evaluation.

## 🏗️ Architecture

```
Evaluation/
├── LLM_evaluation.py           # Expert LLM evaluation system
├── base_evaluation.py          # Statistical and linguistic analysis
├── evaluation_metric.py        # Structured evaluation metrics
├── evaluation_summarizer.py    # Automated report generation
└── README.md                   # This file
```

## 🎯 Core Components

### 1. LLM_evaluation.py - Expert Evaluation System

**Purpose**: Provides expert-level evaluation using local LLM models (Ollama/Mistral)

**Key Features:**
- Multi-faceted technical assessment
- 3GPP compliance verification
- Research value analysis
- Detailed feedback generation
- Structured JSON output

**Evaluation Dimensions:**
- **Technical Accuracy** (1-10): Correctness of 5G technologies and parameters
- **Realism & Implementability** (1-10): Real-world deployment feasibility
- **3GPP Compliance** (1-10): Standards alignment (Rel-16/17, ETSI NFV)
- **Internal Consistency** (1-10): Parameter logical coherence
- **Research Value** (1-10): Academic and industrial relevance
- **Intent Clarity** (1-10): Description clarity and unambiguity
- **Terminology Accuracy** (1-10): Technical term usage correctness
- **Linguistic Naturalness** (1-10): Human-like language quality

**Usage:**
```bash
# Configure input/output paths in the script
INPUT_PATH = "your_dataset.csv"
OUTPUT_PATH = "evaluated_samples.jsonl"
SAMPLE_SIZE = 50  # Number of samples to evaluate

python src/Evaluation/LLM_evaluation.py
```

**Output Format:**
```json
{
  "original_intent_from_csv": {...},
  "llm_evaluation": {
    "overall_assessment": {
      "overall_quality_score": 8.5,
      "executive_summary": "High-quality intent with excellent technical accuracy"
    },
    "core_technical_evaluation": {
      "technical_accuracy_score": 9.0,
      "realism_and_implementability_score": 8.5,
      "3gpp_compliance_score": 9.2,
      "internal_consistency_score": 8.8,
      "research_value_score": 8.0
    },
    "linguistic_evaluation": {...},
    "weakness_analysis": {...},
    "enhancement_recommendations": {...}
  }
}
```

### 2. base_evaluation.py - Statistical Analysis

**Purpose**: Comprehensive statistical and linguistic analysis of datasets

**Analysis Categories:**

#### Lexical Diversity
- Unique sentence ratio
- Type-token ratio
- Unique bigrams count
- Rare word fraction

#### TF-IDF Similarity
- Mean similarity scores
- Distribution analysis
- Duplicate detection

#### Grammar & Syntax
- Grammar error estimation
- POS tag diversity
- Passive voice detection
- Sentence structure analysis

#### Readability Metrics
- Flesch Reading Ease
- SMOG Index
- Gunning Fog Index

#### Semantic Analysis
- Label-wise semantic similarity
- Sentence embedding clustering
- Intent cluster analysis

**Usage:**
```python
# Configure paths in the script
DATA_PATH = "your_dataset.csv"
OUTPUT_MD = "analysis_report.md"

python src/Evaluation/base_evaluation.py
```

**Output**: Detailed Markdown report with visualizations and statistics

### 3. evaluation_metric.py - Structured Metrics

**Purpose**: Provides structured evaluation classes and LLM integration

**Key Classes:**

#### EvaluationMetrics
```python
@dataclass
class EvaluationMetrics:
    technical_accuracy: float
    realism_score: float
    compliance_level: float
    research_value: float
    implementability: float
    overall_quality: float
```

#### DataEvaluator
- LLM-enhanced evaluation system
- Quality threshold management
- Batch evaluation capabilities
- Strength/weakness identification
- Recommendation generation

**Usage:**
```python
from Evaluation.evaluation_metric import DataEvaluator

evaluator = DataEvaluator()
results = evaluator.evaluate_batch(intent_descriptions)
```

### 4. evaluation_summarizer.py - Report Generation

**Purpose**: Automated analysis and summarization of evaluation results

**Features:**
- Statistical visualization (Orange Labs theme)
- NLP-based feedback summarization
- Interactive charts and plots
- Actionable insights generation

**Visualizations:**
- Score distribution bar charts
- Issue frequency pie charts
- Intent-wise performance heatmaps
- Trend analysis plots

**Usage:**
```bash
python src/Evaluation/evaluation_summarizer.py evaluated_dataset.jsonl
```

**Outputs:**
- `score_statistics.png`: Average evaluation scores
- `top_issues.png`: Most common issues detected
- `intent_heatmap.png`: Performance by intent type
- `feedback_summary.txt`: Summarized expert feedback

## 🔧 Configuration

### LLM Evaluation Settings

```python
# LLM_evaluation.py configuration
MODEL = "mistral"                    # Ollama model name
SAMPLE_SIZE = 10                     # Number of samples to evaluate
RETRY_ATTEMPTS = 2                   # Retry attempts for failed requests
INPUT_PATH = "dataset.csv"           # Input dataset path
OUTPUT_PATH = "evaluated.jsonl"      # Output evaluation path
```

### Statistical Analysis Settings

```python
# base_evaluation.py configuration
LABEL_COLUMN = "Intent Type"         # Label column name
TEXT_COLUMN = "Description"          # Text column name
OUTPUT_MD = "analysis.md"            # Output report path
```

### Visualization Theme

```python
# evaluation_summarizer.py theme
ORANGE = "#FF7900"                   # Primary color
WHITE = "#FFFFFF"                    # Background color
GREY = "#333333"                     # Text color
```

## 📊 Evaluation Metrics

### Quality Thresholds

| Metric | Excellent | Good | Fair | Poor |
|--------|-----------|------|------|------|
| Technical Accuracy | ≥8.5 | 7.0-8.4 | 5.5-6.9 | <5.5 |
| 3GPP Compliance | ≥8.5 | 7.5-8.4 | 6.0-7.4 | <6.0 |
| Research Value | ≥8.0 | 6.5-7.9 | 5.0-6.4 | <5.0 |
| Overall Quality | ≥8.0 | 7.0-7.9 | 5.5-6.9 | <5.5 |

### Statistical Benchmarks

| Metric | Target Range | Interpretation |
|--------|--------------|----------------|
| Type-Token Ratio | 0.6-0.8 | Vocabulary diversity |
| Mean TF-IDF Similarity | 0.1-0.3 | Content uniqueness |
| Flesch Reading Ease | 30-60 | Technical readability |
| Unique Sentence Ratio | >0.95 | Content originality |

## 🚀 Usage Workflows

### Complete Evaluation Pipeline

```bash
# 1. Generate dataset
python src/main.py --num_records 1000 --output_file dataset.csv

# 2. Run LLM evaluation
python src/Evaluation/LLM_evaluation.py

# 3. Generate statistical analysis
python src/Evaluation/base_evaluation.py

# 4. Create summary report
python src/Evaluation/evaluation_summarizer.py evaluated_samples.jsonl
```

### Custom Evaluation

```python
from Evaluation.evaluation_metric import DataEvaluator
from Evaluation.base_evaluation import *

# Load your dataset
df = pd.read_csv("your_dataset.csv")

# Statistical analysis
lexical_stats = lexical_diversity(df["Description"])
similarity_stats = tfidf_similarity(df["Description"])
readability_stats = readability_measures(df["Description"])

# LLM evaluation
evaluator = DataEvaluator()
llm_results = evaluator.evaluate_batch(df["Description"].head(10))

print(f"Lexical Diversity: {lexical_stats}")
print(f"Quality Score: {llm_results['overall_metrics'].overall_quality}")
```

### Batch Processing

```python
import pandas as pd
from tqdm import tqdm

# Process large datasets in chunks
chunk_size = 100
results = []

for chunk in tqdm(pd.read_csv("large_dataset.csv", chunksize=chunk_size)):
    chunk_results = evaluate_chunk(chunk)
    results.extend(chunk_results)
```

## 🔍 Quality Indicators

### High-Quality Indicators
- Technical accuracy >8.5
- 3GPP compliance >8.5
- Low TF-IDF similarity (<0.2)
- High lexical diversity (>0.7)
- Minimal grammar errors (<1 per text)

### Quality Issues
- **Technical Inaccuracy**: Incorrect 5G parameters or terminology
- **Lack of Realism**: Unrealistic deployment scenarios
- **Internal Inconsistency**: Contradictory parameters
- **Vague Description**: Unclear or ambiguous language
- **Poor Compliance**: Non-standard configurations

### Improvement Recommendations
- **Parameter Validation**: Cross-check 3GPP specifications
- **Realism Enhancement**: Use real-world deployment patterns
- **Consistency Checks**: Validate parameter relationships
- **Language Refinement**: Improve technical clarity
- **Standards Alignment**: Update to latest 3GPP releases

## 📈 Performance Optimization

### LLM Evaluation
- **Timeout Management**: Progressive timeout increases
- **Batch Processing**: Process multiple samples efficiently
- **Error Handling**: Robust retry mechanisms
- **Memory Management**: Stream processing for large datasets

### Statistical Analysis
- **Sampling**: Use representative samples for large datasets
- **Caching**: Cache expensive computations
- **Parallel Processing**: Utilize multiple cores
- **Memory Efficiency**: Process data in chunks

## 🐛 Troubleshooting

### Common Issues

#### LLM Evaluation
```bash
# Ollama not running
ollama serve

# Model not available
ollama pull mistral

# Timeout issues
# Increase timeout values in script
```

#### Statistical Analysis
```python
# Missing dependencies
pip install sentence-transformers textstat nltk

# NLTK data
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
```

#### Memory Issues
```python
# Reduce sample sizes
SAMPLE_SIZE = 50  # Instead of 500

# Use chunked processing
for chunk in pd.read_csv("file.csv", chunksize=1000):
    process_chunk(chunk)
```

## 🔮 Advanced Features

### Custom Evaluation Criteria

```python
# Add custom evaluation dimensions
custom_evaluator = DataEvaluator()
custom_evaluator.quality_thresholds.update({
    'innovation_score': 7.5,
    'deployment_complexity': 6.0
})
```

### Multi-Model Evaluation

```python
# Compare different LLM models
models = ['mistral', 'llama2', 'codellama']
for model in models:
    results = evaluate_with_model(dataset, model)
    compare_results(results)
```

### Temporal Analysis

```python
# Track quality over time
timestamps = df['Timestamp']
quality_scores = df['Quality_Score']
plot_quality_trends(timestamps, quality_scores)
```

## 📚 Research Applications

### Academic Research
- Dataset quality benchmarking
- Augmentation technique comparison
- LLM evaluation validation
- Intent classification studies

### Industrial Applications
- Dataset procurement validation
- Model training data assessment
- Quality assurance automation
- Compliance verification

### Benchmarking Studies
- Cross-dataset comparison
- Evaluation method validation
- Quality metric correlation
- Human-LLM agreement analysis

## 🎯 Best Practices

1. **Sample Representative Data**: Ensure evaluation samples represent the full dataset
2. **Use Multiple Metrics**: Combine statistical and LLM-based evaluation
3. **Validate Thresholds**: Adjust quality thresholds based on use case
4. **Monitor Performance**: Track evaluation consistency over time
5. **Document Results**: Maintain detailed evaluation logs
6. **Iterate Improvements**: Use feedback to enhance generation quality

## 🔧 Customization Guide

### Adding New Metrics

```python
# In evaluation_metric.py
def custom_metric_evaluation(text: str) -> float:
    # Your custom evaluation logic
    return score

# In DataEvaluator class
def evaluate_custom(self, intent: str) -> float:
    return custom_metric_evaluation(intent)
```

### Custom Visualizations

```python
# In evaluation_summarizer.py
def plot_custom_metric(df):
    plt.figure(figsize=(10, 6))
    # Your plotting code
    plt.savefig("custom_metric.png")
```

### Integration with External Tools

```python
# Export to external analysis tools
def export_to_tableau(results):
    # Format for Tableau
    pass

def export_to_powerbi(results):
    # Format for Power BI
    pass
```