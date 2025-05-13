import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_csv('data/ingredients_onehot.csv')

# 2. Áp dụng Apriori
frequent_itemsets = apriori(df, min_support=0.02, use_colnames=True)

# 3. Sinh tất cả Association Rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

# 4. Lọc luật mạnh: confidence >= 0.6 và lift > 1
strong_rules = rules[(rules['confidence'] >= 0.6) & (rules['lift'] > 1)]


strong_rules = strong_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
strong_rules.to_csv('data/strong_rules.csv', index=False)

