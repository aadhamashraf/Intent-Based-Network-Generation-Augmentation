# Text Augmentation Techniques

This document provides detailed information about the text augmentation techniques available in the Intent-Based Network Generation Augmentation toolkit.

## Overview

The augmentation system provides 11+ sophisticated techniques for enhancing intent-based networking datasets. These techniques are designed to improve dataset diversity, robustness, and size while maintaining semantic meaning and technical accuracy.

## Available Techniques

### 1. T5-Based Paraphrasing (`paraphrase`)

**Description**: Uses a fine-tuned T5 transformer model to generate paraphrases of intent descriptions.

**Model**: `Vamsi/T5_Paraphrase_Paws`

**Parameters**:
- `max_length`: 256 tokens
- `do_sample`: True
- `top_k`: 120
- `top_p`: 0.95

**Usage**:
```python
from augmentation_utils import paraphrase

original = "Deploy AMF network function with high availability"
paraphrased = paraphrase(original)
# Output: "Implement AMF network component with enhanced reliability"
```

**Pros**:
- High semantic preservation
- Natural language output
- Context-aware transformations

**Cons**:
- Slower processing (2-5 seconds per text)
- Requires GPU for optimal performance
- May occasionally change technical meaning

### 2. Back Translation (`back_translate`)

**Description**: Translates text to French and back to English using Google Translate API.

**Translation Path**: English → French → English

**Parameters**:
- `retries`: 3 attempts
- `source`: 'en' (English)
- `intermediate`: 'fr' (French)

**Usage**:
```python
from augmentation_utils import back_translate

original = "Configure network slice for eMBB service"
back_translated = back_translate(original)
# Output: "Set up network slice for eMBB service"
```

**Pros**:
- Preserves technical meaning
- Introduces natural variations
- Good for improving robustness

**Cons**:
- Requires internet connection
- API rate limits
- May lose nuanced technical details

### 3. Synonym Replacement (`synonym_augment`)

**Description**: Replaces random words with synonyms from WordNet.

**Source**: NLTK WordNet corpus

**Algorithm**:
1. Select random word from text
2. Find synonyms using WordNet
3. Replace with first available synonym

**Usage**:
```python
from augmentation_utils import synonym_augment

original = "Monitor network performance metrics"
augmented = synonym_augment(original)
# Output: "Monitor network execution metrics"
```

**Pros**:
- Fast processing
- Preserves sentence structure
- No external dependencies

**Cons**:
- Limited synonym quality
- May introduce inappropriate substitutions
- Context-unaware replacements

### 4. Entity Shuffling (`entity_shuffle`)

**Description**: Randomly shuffles the order of words in the text.

**Algorithm**:
1. Split text into words
2. Randomly shuffle word order
3. Rejoin into text

**Usage**:
```python
from augmentation_utils import entity_shuffle

original = "Deploy UPF with QoS parameters"
shuffled = entity_shuffle(original)
# Output: "QoS with parameters UPF Deploy"
```

**Pros**:
- Tests model robustness to word order
- Very fast processing
- Useful for adversarial testing

**Cons**:
- Destroys grammatical structure
- May create nonsensical text
- Not suitable for production training

### 5. Typo Injection (`typo_augment`)

**Description**: Introduces character-level typos by swapping adjacent characters.

**Algorithm**:
1. Select random position in text
2. Swap character with next character
3. Return modified text

**Usage**:
```python
from augmentation_utils import typo_augment

original = "Configure security parameters"
typo_text = typo_augment(original)
# Output: "Confiugre security parameters"
```

**Pros**:
- Simulates real-world input errors
- Tests model robustness
- Very fast processing

**Cons**:
- May create unreadable text
- Limited to simple character swaps
- Not linguistically motivated

### 6. GPT-2 Synthesis (`gpt2_synthesize`)

**Description**: Uses GPT-Neo model to generate logical continuations of intent text.

**Model**: `EleutherAI/gpt-neo-125M`

**Parameters**:
- `max_new_tokens`: 50
- `do_sample`: True
- `top_k`: 50
- `top_p`: 0.95
- `temperature`: 0.9

**Usage**:
```python
from augmentation_utils import gpt2_synthesize

original = "Deploy network slice for autonomous vehicles"
extended = gpt2_synthesize(original)
# Output: "Deploy network slice for autonomous vehicles with ultra-low latency requirements and edge computing capabilities"
```

**Pros**:
- Generates coherent extensions
- Context-aware generation
- Adds technical details

**Cons**:
- May generate incorrect information
- Requires GPU for speed
- Can produce verbose output

### 7. Contextual Synonym Replacement (`contextual_synonym_augment`)

**Description**: Replaces words with contextually similar terms using spaCy word vectors.

**Model**: `en_core_web_md` (spaCy medium English model)

**Algorithm**:
1. Select random word with word vector
2. Find most similar words in vocabulary
3. Replace with contextually appropriate synonym

**Usage**:
```python
from augmentation_utils import contextual_synonym_augment

original = "Optimize network resource allocation"
augmented = contextual_synonym_augment(original)
# Output: "Optimize network resource distribution"
```

**Pros**:
- Context-aware replacements
- Better semantic preservation
- Uses pre-trained embeddings

**Cons**:
- Requires large spaCy model
- Slower than simple synonym replacement
- May still introduce errors

### 8. BERT Masked Fill (`mask_fill_augment`)

**Description**: Masks random words and uses BERT to predict replacements.

**Model**: `bert-base-uncased`

**Algorithm**:
1. Select random word to mask
2. Replace with [MASK] token
3. Use BERT to predict replacement
4. Substitute predicted word

**Usage**:
```python
from augmentation_utils import mask_fill_augment

original = "Configure AMF network function"
augmented = mask_fill_augment(original)
# Output: "Configure core network function"
```

**Pros**:
- Contextually appropriate replacements
- Uses state-of-the-art language model
- Maintains grammatical structure

**Cons**:
- Requires GPU for efficiency
- May change technical meaning
- Limited to single word replacements

### 9. Adversarial Noise (`adversarial_noise`)

**Description**: Introduces small character-level perturbations including insertions, deletions, and substitutions.

**Operations**:
- **Delete**: Remove random character
- **Swap**: Exchange adjacent characters
- **Insert**: Add random character
- **Substitute**: Replace with random character

**Usage**:
```python
from augmentation_utils import adversarial_noise

original = "Monitor network latency"
noisy = adversarial_noise(original)
# Output: "Monitxr network latency" (substitution)
```

**Pros**:
- Tests character-level robustness
- Simulates OCR errors
- Very fast processing

**Cons**:
- May create unreadable text
- Not linguistically motivated
- Can break technical terms

## 🎛️ Configuration and Usage

### Command Line Interface

```bash
# Enable specific augmentation techniques
python src/main.py \
    --use_paraphrasing --paraphrase_ratio 0.3 \
    --use_backtranslation --backtranslate_ratio 0.2 \
    --use_synonym_aug --synonym_ratio 0.25 \
    --use_gpt2_aug --gpt2_ratio 0.15 \
    --num_records 1000
```

### Programmatic Usage

```python
from augmentation_utils import *

# Single technique
text = "Deploy network function"
augmented = paraphrase(text)

# Multiple techniques
techniques = [
    (paraphrase, 0.3),
    (back_translate, 0.2),
    (synonym_augment, 0.25)
]

for technique, ratio in techniques:
    if random.random() < ratio:
        text = technique(text)
```

### Batch Processing

```python
import pandas as pd
from tqdm import tqdm

def augment_dataset(df, techniques):
    augmented_data = []
    
    for _, row in tqdm(df.iterrows(), total=len(df)):
        # Original record
        augmented_data.append(row.to_dict())
        
        # Apply augmentations
        for technique, ratio in techniques:
            if random.random() < ratio:
                augmented_row = row.copy()
                augmented_row['Description'] = technique(row['Description'])
                augmented_row['ID'] = f"AUG_{technique.__name__}_{row['ID']}"
                augmented_data.append(augmented_row.to_dict())
    
    return pd.DataFrame(augmented_data)
```

## 📊 Performance Comparison

| Technique | Speed | Quality | GPU Required | Internet Required |
|-----------|-------|---------|--------------|-------------------|
| Paraphrasing | Slow | High | Recommended | No |
| Back Translation | Medium | Medium | No | Yes |
| Synonym Replacement | Fast | Low | No | No |
| Entity Shuffling | Very Fast | Very Low | No | No |
| Typo Injection | Very Fast | Low | No | No |
| GPT-2 Synthesis | Slow | Medium | Recommended | No |
| Contextual Synonyms | Medium | Medium | No | No |
| BERT Fill | Medium | High | Recommended | No |
| Adversarial Noise | Very Fast | Low | No | No |

## 🎯 Best Practices

### 1. Technique Selection

**For Training Data**:
- Use paraphrasing and back translation
- Avoid entity shuffling and heavy noise
- Focus on semantic preservation

**For Robustness Testing**:
- Include typo injection and adversarial noise
- Test with entity shuffling
- Use various noise levels

**For Data Expansion**:
- Combine multiple techniques
- Use moderate augmentation ratios
- Validate augmented samples

### 2. Ratio Guidelines

| Use Case | Conservative | Moderate | Aggressive |
|----------|-------------|----------|------------|
| Training | 0.1-0.2 | 0.2-0.4 | 0.4-0.6 |
| Testing | 0.05-0.1 | 0.1-0.2 | 0.2-0.3 |
| Research | 0.2-0.3 | 0.3-0.5 | 0.5-0.8 |

### 3. Quality Control

```python
def validate_augmentation(original, augmented):
    """Validate augmented text quality"""
    checks = {
        'length_ratio': len(augmented) / len(original),
        'word_overlap': calculate_word_overlap(original, augmented),
        'semantic_similarity': calculate_similarity(original, augmented)
    }
    
    # Quality thresholds
    if checks['length_ratio'] < 0.5 or checks['length_ratio'] > 2.0:
        return False
    if checks['word_overlap'] < 0.3:
        return False
    if checks['semantic_similarity'] < 0.7:
        return False
    
    return True
```

### 4. Error Handling

```python
def safe_augment(text, technique, retries=3):
    """Safely apply augmentation with fallback"""
    for attempt in range(retries):
        try:
            result = technique(text)
            if validate_augmentation(text, result):
                return result
        except Exception as e:
            logger.warning(f"Augmentation failed (attempt {attempt+1}): {e}")
    
    return text  # Return original if all attempts fail
```

## Hardware Requirements

### Minimum Requirements
- **CPU**: 4 cores, 2.0 GHz
- **RAM**: 8 GB
- **Storage**: 5 GB free space
- **Internet**: For back translation only

### Recommended Requirements
- **CPU**: 8+ cores, 3.0+ GHz
- **RAM**: 16+ GB
- **GPU**: NVIDIA GPU with 8+ GB VRAM
- **Storage**: 20+ GB free space
- **Internet**: Stable connection for API calls

### GPU Acceleration

```python
import torch

# Check GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Configure models for GPU
if device == "cuda":
    # Models will automatically use GPU
    paraphraser = pipeline("text2text-generation", device=0)
else:
    # CPU fallback
    paraphraser = pipeline("text2text-generation", device=-1)
```

## Troubleshooting

### Common Issues

#### 1. Memory Errors
```python
# Reduce batch size
batch_size = 16  # Instead of 64

# Clear GPU cache
torch.cuda.empty_cache()

# Use CPU for memory-intensive operations
device = "cpu"
```

#### 2. API Rate Limits
```python
import time

def rate_limited_back_translate(text):
    try:
        result = back_translate(text)
        time.sleep(0.1)  # Rate limiting
        return result
    except Exception as e:
        logger.warning(f"Rate limit hit: {e}")
        time.sleep(5)  # Longer wait
        return text
```

#### 3. Model Loading Issues
```python
# Download required models
import spacy
import nltk

# spaCy model
spacy.cli.download("en_core_web_md")

# NLTK data
nltk.download('wordnet')
nltk.download('punkt')
```

#### 4. Quality Degradation
```python
# Implement quality gates
def quality_gate(original, augmented):
    similarity = calculate_similarity(original, augmented)
    if similarity < 0.7:
        return original  # Reject poor augmentation
    return augmented
```

## 📚 References

1. Wei, J., & Zou, K. (2019). EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks.
2. Feng, S. Y., et al. (2021). A Survey of Data Augmentation Approaches for NLP.
3. Kumar, V., et al. (2020). Data Augmentation using Pre-trained Transformer Models.
4. Quteineh, H., et al. (2020). Textual Data Augmentation for Efficient Active Learning on Tiny Datasets.
