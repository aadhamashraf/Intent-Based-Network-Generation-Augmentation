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
import torch
import spacy
from faker import Faker
from deep_translator import GoogleTranslator
from transformers import AutoTokenizer, pipeline, T5Tokenizer, GPT2Tokenizer, GPTNeoForCausalLM, BertTokenizer, BertForMaskedLM
from nltk.corpus import wordnet
import nltk

# Download required NLTK data
try:
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Device set to use {device}")

# Initialize models with error handling
try:
    bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    bert_model = BertForMaskedLM.from_pretrained("bert-base-uncased").to(device)
except Exception as e:
    logger.warning(f"Failed to load BERT model: {e}")
    bert_tokenizer = None
    bert_model = None

try:
    nlp = spacy.load("en_core_web_md")
except Exception as e:
    logger.warning(f"Failed to load spaCy model: {e}")
    nlp = None

try:
    gpt2_tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
    gpt2_tokenizer.pad_token = gpt2_tokenizer.eos_token
    gpt2_model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M").to(device)
except Exception as e:
    logger.warning(f"Failed to load GPT-Neo model: {e}")
    gpt2_tokenizer = None
    gpt2_model = None

try:
    paraphraser = pipeline(
        "text2text-generation",
        model="Vamsi/T5_Paraphrase_Paws",
        tokenizer=T5Tokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws", legacy=False),
        device=0 if device == "cuda" else -1
    )
except Exception as e:
    logger.warning(f"Failed to load T5 paraphraser: {e}")
    paraphraser = None

fake = Faker()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def gpt2_synthesize(text, max_new_tokens=50):
    if not gpt2_model or not gpt2_tokenizer:
        logger.warning("GPT-2 model not available, returning original text")
        return text
        
    try:
        prompt = f"Extend this network intent logically: {text}\nIntent:"

        encoded = gpt2_tokenizer(
            prompt,
            return_tensors='pt',
            truncation=True,
            padding=True
        ).to(device)

        output_ids = gpt2_model.generate(
            input_ids=encoded["input_ids"],
            attention_mask=encoded["attention_mask"],
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.9,
            pad_token_id=gpt2_tokenizer.eos_token_id
        )

        generated = gpt2_tokenizer.decode(output_ids[0], skip_special_tokens=True)
        continuation = generated.replace(prompt, "").strip()

        return text + " " + continuation if continuation else text

    except Exception as e:
        logger.warning(f"GPT generation failed: {e}")
        return text


def contextual_synonym_augment(text):
    """Replace one word with a contextually similar one using spaCy word vectors."""
    if not nlp:
        logger.warning("spaCy model not available, returning original text")
        return text
        
    doc = nlp(text)
    words = [token.text for token in doc if token.has_vector and not token.is_stop and token.is_alpha]
    if not words:
        return text

    target_word = random.choice(words)
    similar_words = sorted(
        [(w.text, doc.vocab[target_word].similarity(w.vector)) for w in nlp.vocab if w.has_vector and w.is_lower and w.is_alpha],
        key=lambda x: -x[1]
    )

    for new_word, _ in similar_words:
        if new_word != target_word and len(new_word) > 2:
            return text.replace(target_word, new_word, 1)
    return text


def mask_fill_augment(text):
    """Randomly mask a word and let BERT predict a replacement."""
    if not bert_model or not bert_tokenizer:
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
    if not paraphraser:
        logger.warning("T5 paraphraser not available, returning original text")
        return text
        
    for attempt in range(retries):
        try:
            result = paraphraser(f"paraphrase: {text}", max_length=256, do_sample=True,
                                 top_k=120, top_p=0.95, num_return_sequences=1)
            return result[0]['generated_text']
        except Exception as e:
            logger.warning(f"Paraphrasing failed (attempt {attempt+1}): {e}")
    return text
