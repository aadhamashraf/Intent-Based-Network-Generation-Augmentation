import pandas as pd

df = pd.read_csv("3gpp_research_intents_2025-09-18.csv")
df['Parameters'].groupby(df['Intent Type']).first().to_markdown("answer.csv")