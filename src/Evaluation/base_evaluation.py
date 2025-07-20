import pandas as pd
import numpy as np
import re
import random
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import textstat
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# ---- Config ----
DATA_PATH = "3gpp_research_intents_2025-07-15.csv"

LABEL_COLUMN = "Intent Type"
TEXT_COLUMN = "Description"
OUTPUT_MD = "dataset_analysis.md"

# ---- Markdown Buffer ----
md_lines = []

def md_header(title, level=2):
    md_lines.append(f"\n{'#' * level} {title}\n")

def md_line(text=""):
    md_lines.append(str(text))

# ---- Load Dataset ----
def load_dataset(data_path):
    if data_path.endswith(".csv"):
        return pd.read_csv(data_path)
    elif data_path.endswith(".jsonl"):
        return pd.read_json(data_path, lines=True)
    else:
        raise ValueError("Unsupported file format")

df = load_dataset(DATA_PATH)

# ---- Lexical Diversity ----
def lexical_diversity(texts):
    all_words = [w for s in texts for w in s.split()]
    vocab = set(all_words)
    ratios = {
        "unique_sentences": len(set(texts)) / len(texts),
        "unique_tokens": len(vocab),
        "type_token_ratio": len(vocab) / len(all_words)
    }
    unigram = Counter(all_words)
    bigram_vec = CountVectorizer(ngram_range=(2, 2))
    bigram_vec.fit_transform(texts)
    ratios["unique_bigrams"] = len(bigram_vec.get_feature_names_out())
    ratios["rare_word_fraction"] = sum(1 for w in vocab if unigram[w] == 1) / len(vocab)
    return ratios

# ---- TF-IDF Similarity ----
def tfidf_similarity(texts, sample=800):
    vec = TfidfVectorizer(max_features=7000)
    subset = list(texts) if len(texts) <= sample else list(np.random.choice(texts, sample, replace=False))
    tfidf = vec.fit_transform(subset)
    sim_matrix = cosine_similarity(tfidf)
    iu = np.triu_indices_from(sim_matrix, k=1)
    sim_scores = sim_matrix[iu]
    return {
        "mean_tfidf_sim": np.mean(sim_scores),
        "std_tfidf_sim": np.std(sim_scores),
        "min_tfidf_sim": np.min(sim_scores)
    }

# ---- Basic Grammar Heuristic ----
def grammar_and_syntax(texts, sample=500):
    samples = list(texts[:sample])
    grammar_stats = []
    for s in samples:
        errors = 0
        if not s.endswith(('.', '?', '!')): errors += 1
        if re.search(r'\b(\w+)\s+\1\b', s): errors += 1  # repeated word
        if len(s.split()) < 3: errors += 1
        grammar_stats.append(errors)

    pos_tags = [tag for s in samples for (_, tag) in nltk.pos_tag(nltk.word_tokenize(s))]
    pos_dist = Counter(pos_tags)
    return {
        "avg_grammar_errors": np.mean(grammar_stats),
        "median_grammar_errors": np.median(grammar_stats),
        "passive_voice_ratio": sum(1 for s in samples if re.search(r'\b(is|was|were|are|been|being|be) \w+ed\b', s)) / len(samples),
        "pos_diversity": len(pos_dist),
        "most_common_pos": pos_dist.most_common(5)
    }

# ---- Readability ----
def readability_measures(texts):
    return {
        "flesch_reading_ease": np.mean([textstat.flesch_reading_ease(s) for s in texts]),
        "smog_index": np.mean([textstat.smog_index(s) for s in texts]),
        "gunning_fog": np.mean([textstat.gunning_fog(s) for s in texts])
    }

# ---- Semantic Similarity ----
def semantic_similarity_labelwise(df, text_col, label_col):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    results = {}
    labels = df[label_col].unique()
    for label in labels:
        group = df.loc[df[label_col] == label, text_col]
        if len(group) > 500:
            group = group.sample(500)
        emb = model.encode(group.tolist(), convert_to_tensor=True, show_progress_bar=False)
        scores = util.pytorch_cos_sim(emb, emb).cpu().numpy()
        iu = np.triu_indices_from(scores, k=1)
        sim_scores = scores[iu]
        results[label] = {
            "sem_sim_mean": float(np.mean(sim_scores)),
            "sem_sim_std": float(np.std(sim_scores)),
            "sem_sim_min": float(np.min(sim_scores))
        }
    return results

# ---- Clustering ----
def intent_cluster_count(texts):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    emb = model.encode(list(texts), show_progress_bar=False)
    clustering = DBSCAN(eps=0.45, min_samples=10, metric='cosine').fit(emb)
    n_clusters = len(set(clustering.labels_)) - (1 if -1 in clustering.labels_ else 0)
    noise = sum(clustering.labels_ == -1)
    return {
        "n_clusters": n_clusters,
        "noise_points": noise,
        "cluster_entropy": -(np.log(n_clusters) if n_clusters > 0 else 0)
    }

# ---- Label Stats ----
def label_stats(df, label_col):
    counts = df[label_col].value_counts()
    total = len(df)
    imbalance = counts.max() / (counts.min() if counts.min() > 0 else 1)
    minority_labels = counts[counts < total * 0.05].index.tolist()
    return {
        "label_counts": counts.to_dict(),
        "label_imbalance_ratio": imbalance,
        "minority_labels": minority_labels
    }

# ---- Duplicates ----
def duplicate_metrics(df, text_col):
    counts = df[text_col].duplicated().sum()
    ratio = counts / len(df)
    return {
        "n_duplicates": counts,
        "dup_ratio": ratio
    }

# ---- OOS/Ambiguity ----
def oos_ambiguity_heuristics(df, label_col, text_col):
    oos = df[df[label_col].str.lower().str.contains("outofscope|oos")]
    ambiguous = df[df[label_col].str.lower().str.contains("ambig")]
    vague_words = ["thing", "stuff", "issue", "it", "whatever"]
    vague_count = sum(any(w in t for w in vague_words) for t in df[text_col])
    return {
        "n_oos": len(oos),
        "n_ambiguous": len(ambiguous),
        "vague_expression_count": vague_count
    }

# ---- Main ----
def main():
    md_header("Dataset Summary")
    md_line(f"- Total records: **{len(df)}**")
    md_line(f"- Columns: `{', '.join(df.columns)}`")

    md_header("Lexical Diversity")
    lexdiv = lexical_diversity(df[TEXT_COLUMN])
    for k, v in lexdiv.items():
        md_line(f"- **{k}**: `{v:.4f}`")

    md_header("TF-IDF Similarity")
    tfidf = tfidf_similarity(df[TEXT_COLUMN])
    for k, v in tfidf.items():
        md_line(f"- **{k}**: `{v:.4f}`")

    md_header("Grammar and Syntax")
    grammar = grammar_and_syntax(df[TEXT_COLUMN])
    for k, v in grammar.items():
        md_line(f"- **{k}**: `{v}`")

    md_header("Readability")
    read = readability_measures(df[TEXT_COLUMN])
    for k, v in read.items():
        md_line(f"- **{k}**: `{v:.2f}`")

    md_header("Semantic Similarity (per Label)")
    sem_by_label = semantic_similarity_labelwise(df, TEXT_COLUMN, LABEL_COLUMN)
    for l, metrics in sem_by_label.items():
        md_line(f"### Label: `{l}`")
        for mk, mv in metrics.items():
            md_line(f"- **{mk}**: `{mv:.4f}`")

    md_header("Clustering Metrics")
    clusters = intent_cluster_count(df[TEXT_COLUMN])
    for k, v in clusters.items():
        md_line(f"- **{k}**: `{v}`")

    md_header("Label Balance")
    lbl_stats = label_stats(df, LABEL_COLUMN)
    md_line(f"- **Imbalance Ratio**: `{lbl_stats['label_imbalance_ratio']:.2f}`")
    md_line(f"- **Minority Labels**: `{lbl_stats['minority_labels']}`")

    md_header("Duplicate Metrics")
    dups = duplicate_metrics(df, TEXT_COLUMN)
    for k, v in dups.items():
        md_line(f"- **{k}**: `{v}`")

    md_header("OOS / Ambiguity / Vagueness")
    oos = oos_ambiguity_heuristics(df, LABEL_COLUMN, TEXT_COLUMN)
    for k, v in oos.items():
        md_line(f"- **{k}**: `{v}`")

    # Write all to Markdown file
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

if __name__ == "__main__":
    main()
