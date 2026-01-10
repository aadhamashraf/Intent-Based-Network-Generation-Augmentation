"""
This script provides a suite of text augmentation and transformation techniques specifically designed 
for enhancing intent-based natural language datasets, such as used in 3GPP network slicing or IBN scenarios.

Key Functionalities:
---------------------
- **Back Translation**: Uses Google Translate (EN → FR → EN) to generate paraphrased variants.
- **Synonym Augmentation**: Replaces random words with synonyms from WordNet.
- **Typo Injection**: Introduces character-level typos to simulate human errors.
- **Entity Shuffling**: Shuffles the order of words to test robustness.
- **GPT-2-based Synthesis**: Generates logical continuations of intent using GPT-Neo.
- **Contextual Augmentation**: Replaces words with similar terms using spaCy word vectors.
- **Masked Fill Augmentation**: Uses BERT to predict masked word replacements.
- **Adversarial Noise**: Applies small perturbations such as deletion, substitution, or insertion.
- **Paraphrasing**: Employs a T5 model to generate paraphrases of the input intent.

Dependencies:
-------------
- torch, transformers, nltk, spacy, deep_translator, faker
- Pre-trained models from HuggingFace for GPT-Neo, T5, BERT
- English word vectors via `en_core_web_md` spaCy model

Hardware:
---------
- Automatically detects and utilizes GPU if available.

Author:
-------
- Adham Ashraf
"""

import random
import uuid
import json
import csv
import logging
try:
    import torch
except ImportError:
    torch = None

try:
    import spacy
except ImportError:
    nlp = None
    spacy = None

try:
    from faker import Faker
except ImportError:
    Faker = None

try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None

try:
    from transformers import AutoTokenizer, pipeline, T5Tokenizer, GPT2Tokenizer, GPTNeoForCausalLM, BertTokenizer, BertForMaskedLM
except ImportError:
    AutoTokenizer = None
    pipeline = None
    T5Tokenizer = None
    GPT2Tokenizer = None
    GPTNeoForCausalLM = None
    BertTokenizer = None
    BertForMaskedLM = None

try:
    from nltk.corpus import wordnet
    import nltk
except ImportError:
    nltk = None
    wordnet = None

try:
    if nltk:
        nltk.download('wordnet', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

device = "cuda" if torch and torch.cuda.is_available() else "cpu"

fake = Faker() if Faker else None
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Device set to use {device}")

# Global model cache for lazy loading
_model_cache = {}

def _get_bert_model():
    """Lazy load BERT model."""
    if 'bert' not in _model_cache:
        try:
            if BertTokenizer is None or BertForMaskedLM is None:
                logger.warning("BERT dependencies not available")
                _model_cache['bert'] = (None, None)
                return None, None
            
            bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
            bert_model = BertForMaskedLM.from_pretrained("bert-base-uncased").to(device)
            _model_cache['bert'] = (bert_tokenizer, bert_model)
            logger.info("BERT model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load BERT model: {e}")
            _model_cache['bert'] = (None, None)
    
    return _model_cache['bert']

def _get_spacy_model():
    """Lazy load spaCy model."""
    if 'spacy' not in _model_cache:
        try:
            if spacy is None:
                logger.warning("spaCy not available")
                _model_cache['spacy'] = None
                return None
            
            nlp = spacy.load("en_core_web_md")
            _model_cache['spacy'] = nlp
            logger.info("spaCy model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load spaCy model: {e}")
            _model_cache['spacy'] = None
    
    return _model_cache['spacy']

def _get_gpt2_model():
    """Lazy load GPT-2/GPT-Neo model."""
    if 'gpt2' not in _model_cache:
        try:
            if AutoTokenizer is None or GPTNeoForCausalLM is None:
                logger.warning("GPT-Neo dependencies not available")
                _model_cache['gpt2'] = (None, None)
                return None, None
            
            gpt2_tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
            gpt2_tokenizer.pad_token = gpt2_tokenizer.eos_token
            gpt2_model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M").to(device)
            _model_cache['gpt2'] = (gpt2_tokenizer, gpt2_model)
            logger.info("GPT-Neo model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load GPT-Neo model: {e}")
            _model_cache['gpt2'] = (None, None)
    
    return _model_cache['gpt2']

def _get_paraphraser():
    """Lazy load T5 paraphraser model."""
    if 'paraphraser' not in _model_cache:
        try:
            if pipeline is None or T5Tokenizer is None:
                logger.warning("T5 paraphraser dependencies not available")
                _model_cache['paraphraser'] = None
                return None
            
            paraphraser = pipeline(
                "text2text-generation",
                model="Vamsi/T5_Paraphrase_Paws",
                tokenizer=T5Tokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws", legacy=False),
                device=0 if device == "cuda" else -1
            )
            _model_cache['paraphraser'] = paraphraser
            logger.info("T5 paraphraser loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load T5 paraphraser: {e}")
            _model_cache['paraphraser'] = None
    
    return _model_cache['paraphraser']

def get_augmentation_status():
    """Return status of all augmentation models."""
    return {
        "BERT": bert_model is not None,
        "spaCy": nlp is not None,
        "GPT-Neo": gpt2_model is not None,
        "T5": paraphraser is not None,
        "Device": device
    }


def back_translate(text, retries=3):
    """Backtranslate English text via French with retries."""
    for attempt in range(retries):
        try:
            fr = GoogleTranslator(source='en', target='fr').translate(text)
            en = GoogleTranslator(source='fr', target='en').translate(fr)
            return en
        except Exception as e:
            logger.warning(f"Backtranslation failed (attempt {attempt+1}): {e}")
    return text

def synonym_augment(text):
    """Replace a random word with a synonym using WordNet."""
    if not wordnet:
        logger.warning("WordNet not available, returning original text")
        return text
        
    words = text.split()
    if not words:
        return text
    idx = random.randint(0, len(words) - 1)
    synonyms = wordnet.synsets(words[idx])
    if synonyms:
        lemmas = synonyms[0].lemma_names()
        if lemmas:
            words[idx] = lemmas[0].replace('_', ' ')
    return ' '.join(words)

def typo_augment(text):
    """Inject a simple character swap typo."""
    if len(text) < 5:
        return text
    idx = random.randint(0, len(text) - 2)
    return text[:idx] + text[idx+1] + text[idx] + text[idx+2:]

def entity_shuffle(text):
    """Shuffle the order of words in the text."""
    words = text.split()
    random.shuffle(words)
    return ' '.join(words)

def gpt2_synthesize(text, max_length=100):
    """Generate a continuation using GPT-Neo."""
    gpt2_tokenizer, gpt2_model = _get_gpt2_model()
    
    if gpt2_tokenizer is None or gpt2_model is None:
        logger.warning("GPT-Neo model not available, returning original text")
        return text
    
    try:
        inputs = gpt2_tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
        outputs = gpt2_model.generate(
            inputs["input_ids"],
            max_length=max_length,
            num_return_sequences=1,
            pad_token_id=gpt2_tokenizer.eos_token_id
        )
        return gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        logger.warning(f"GPT-Neo generation failed: {e}")
        return text

# Add missing augmentation functions referenced in main.py
def gpt2_augment(text, max_new_tokens=50):
    """Alias for gpt2_synthesize for consistency."""
    return gpt2_synthesize(text, max_new_tokens)

def bert_fill_augment(text):
    """Alias for mask_fill_augment for consistency."""
    return mask_fill_augment(text)

def adversarial_augment(text):
    """Alias for adversarial_noise for consistency."""
    return adversarial_noise(text)

def entity_shuffle_augment(text):
    """Alias for entity_shuffle for consistency."""
    return entity_shuffle(text)

def contextual_synonym_augment(text):
    """Replace a word with a contextually similar word using spaCy and WordNet."""
    nlp = _get_spacy_model()
    
    if nlp is None:
        logger.warning("spaCy model not available, returning original text")
        return text
    
    doc = nlp(text)
    words = [token.text for token in doc if not token.is_punct and not token.is_space]
    
    if not words:
        return text

    target_word = random.choice(words)
    
    if not wordnet:
        logger.warning("WordNet not available for contextual augmentation, returning original text")
        return text

    # Efficiently find synonyms using WordNet first, then filter/rank if needed
    # Full vocab scan in spaCy is too slow (O(V)). 
    # Fallback to WordNet synonyms but check vector similarity if available
    synsets = wordnet.synsets(target_word)
    if not synsets:
        return text
    
    synonyms = set()
    for syn in synsets:
        for lemma in syn.lemmas():
            if lemma.name() != target_word:
                synonyms.add(lemma.name().replace('_', ' '))
    
    if not synonyms:
        return text
    
    # If we have spaCy vectors, rank by similarity
    target_token = None
    for token in doc:
        if token.text == target_word:
            target_token = token
            break
    
    if target_token and target_token.has_vector:
        # Rank synonyms by vector similarity
        synonym_scores = []
        for syn in synonyms:
            syn_doc = nlp(syn)
            if syn_doc and syn_doc[0].has_vector:
                similarity = target_token.similarity(syn_doc[0])
                synonym_scores.append((syn, similarity))
        
        if synonym_scores:
            # Pick from top 3 most similar
            synonym_scores.sort(key=lambda x: x[1], reverse=True)
            top_syns = [s[0] for s in synonym_scores[:3]]
            replacement = random.choice(top_syns)
        else:
            replacement = random.choice(list(synonyms))
    else:
        replacement = random.choice(list(synonyms))
    
    return text.replace(target_word, replacement, 1)


def mask_fill_augment(text):
    """Randomly mask a word and let BERT predict a replacement."""
    bert_tokenizer, bert_model = _get_bert_model()
    
    if bert_tokenizer is None or bert_model is None:
        logger.warning("BERT model not available, returning original text")
        return text
        
    words = text.split()
    if len(words) < 3:
        return text

    idx = random.randint(0, len(words) - 1)
    original_word = words[idx]
    words[idx] = "[MASK]"
    masked_text = " ".join(words)

    inputs = bert_tokenizer(masked_text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    logits = outputs.logits
    mask_token_index = (inputs.input_ids == bert_tokenizer.mask_token_id).nonzero(as_tuple=True)[1]
    predicted_token_id = logits[0, mask_token_index, :].argmax(axis=-1)
    predicted_token = bert_tokenizer.decode(predicted_token_id)

    words[idx] = predicted_token
    return " ".join(words)

def adversarial_noise(text):
    """Introduce small character-level noise like insertions/deletions/substitutions."""
    if len(text) < 5:
        return text
    idx = random.randint(0, len(text) - 2)
    perturbation_type = random.choice(["delete", "swap", "insert", "substitute"])
    if perturbation_type == "delete":
        return text[:idx] + text[idx+1:]
    elif perturbation_type == "swap":
        return text[:idx] + text[idx+1] + text[idx] + text[idx+2:]
    elif perturbation_type == "insert":
        return text[:idx] + random.choice("abcdefghijklmnopqrstuvwxyz") + text[idx:]
    elif perturbation_type == "substitute":
        return text[:idx] + random.choice("abcdefghijklmnopqrstuvwxyz") + text[idx+1:]
    return text

def paraphrase(text, retries=2):
    """Paraphrase text using a T5 transformer with retries."""
    paraphraser = _get_paraphraser()
    
    if paraphraser is None:
        logger.warning("T5 paraphraser not available, returning original text")
        return text
        
    for attempt in range(retries):
        try:
            result = paraphraser(f"paraphrase: {text}", max_length=256, do_sample=True,
                                 top_k=120, top_p=0.95, num_return_sequences=1)
            return result[0]['generated_text']
        except Exception as e:
            logger.warning(f"Paraphrasing attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                return text
    return text
