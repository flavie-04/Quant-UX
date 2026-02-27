import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import MaxNLocator
import seaborn as sns

sns.set_theme(style="whitegrid")

q_csv_to_name = {
    "Questionnaire_Shein2026-01-27_07_04_41.csv" : "Shein",
    "Questionnaire_ChromeHearts2026-01-27_07_04_37.csv" : "ChromeHearts",
}

initial_bias_scores = []
all_scores = []
SCORE_MOD = 20
SCORE_COEF = 2.5
NUM_TASKS = 6
HOW_OFTEN_ANS_ORDER = ["Never", "Less then once a month", "At least once a month", "At least once a week", "More then once a week"]
for q_csv_name in q_csv_to_name.keys():
    #print(q_csv_name)
    data = pd.read_csv(q_csv_name)
    data = data[:-2]
    data = data.iloc[:, 2:]
    col_many = data.iloc[:, 0]
    counts_many = (col_many.value_counts().reindex(HOW_OFTEN_ANS_ORDER))
    plt.figure(figsize=(8, 4))
    sns.barplot(
        x=counts_many.index.astype(str),
        hue=counts_many.index.astype(str),
        y=counts_many.values,
        palette="viridis",
        edgecolor="0.2",
        linewidth=0.8,
        legend=False
    )
    plt.title(f"How often do you shop online?", fontsize=14)
    plt.xlabel("")
    plt.xticks(rotation=15, ha="right")
    plt.ylabel("Count")
    plt.grid(axis="y", alpha=0.3)
    sns.despine(left=True, bottom=True)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    
    col_yesno = data.iloc[:, 1]
    counts_yesno = (
        col_yesno
        .astype(str)
        .str.strip()
        .str.capitalize()
        .value_counts()
        .reindex(["Yes", "No"], fill_value=0)
    )
    plt.figure(figsize=(5, 4))
    sns.barplot(
        x=counts_yesno.index,
        hue=counts_yesno.index,
        y=counts_yesno.values,
        palette=["#4CAF50", "#F44336"],
        edgecolor="0.2",
        linewidth=0.8,
        legend=False
    )
    plt.title(f"Have you used {q_csv_to_name[q_csv_name]} before?", fontsize=14)
    plt.xlabel("")
    plt.ylabel("Count")
    plt.grid(axis="y", alpha=0.3)
    sns.despine(left=True, bottom=True)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()
    
    col_binary = data.iloc[:, 2]
    counts_binary = col_binary.value_counts().sort_index()
    plt.figure(figsize=(5, 4))
    sns.barplot(
        x=counts_binary.index.astype(str),
        hue=counts_binary.index.astype(str),
        y=counts_binary.values,
        palette="mako",
        edgecolor="0.2",
        linewidth=0.8,
        legend=False
    )
    plt.title(f"What do you usually shop on?", fontsize=14)
    plt.xlabel("")
    plt.ylabel("Count")
    plt.grid(axis="y", alpha=0.3)
    sns.despine(left=True, bottom=True)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    plt.show()

    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    axes = axes.flatten()  # make it easier to iterate

    for idx, i in enumerate(range(3, 3 + NUM_TASKS)):
        difficulty = data.iloc[:, i]
        possible_answers = range(1, 8)
        counts_dict = (
            difficulty
            .value_counts()
            .reindex(possible_answers, fill_value=0)
            .to_dict()
        )

        print(f"Task {i-2}")
        print(f"Mean: {difficulty.mean():.2f}")
        print(f"Variance: {difficulty.var():.2f}\n")sns.set_theme(style="whitegrid")

        sns.barplot(
            x=list(counts_dict.keys()),
            y=list(counts_dict.values()),
            hue=list(counts_dict.keys()),
            palette="viridis",
            ax=axes[idx],
            edgecolor="0.2",
            linewidth=0.8,
            legend=False
        )

        axes[idx].set_title(
            f"Task {i-2} (Mean: {difficulty.mean():.2f}, Variance: {difficulty.var():.2f})",
            fontsize=11,
            pad=8
        )

        axes[idx].set_xlabel("Difficulty", fontsize=10)
        axes[idx].set_ylabel("Count", fontsize=10)
        axes[idx].set_ylim(0, 25)
        axes[idx].yaxis.set_major_locator(MultipleLocator(5))

        sns.despine(ax=axes[idx], left=True, bottom=True)
        axes[idx].grid(axis="y", alpha=0.3)
        axes[idx].grid(axis="x", visible=False)


    plt.suptitle(f"Difficulty Distribution - {q_csv_to_name[q_csv_name]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    print("\n")
    
    sus_scores = []
    for index, row in data.iterrows():
        odd_indices = [0, 2, 4, 6, 8]
        even_indices = [1, 3, 5, 7, 9]
        
        for x in range(len(odd_indices)):
            odd_indices[x] += 9
        for x in range(len(even_indices)):
            even_indices[x] += 9      
        total_score = row.iloc[odd_indices].sum() - row.iloc[even_indices].sum()
        sus_score = (SCORE_MOD + total_score) * SCORE_COEF
        sus_scores.append(sus_score)
        
    all_scores.append(pd.DataFrame({
        "SUS Score": sus_scores,
        "q_csv_name": q_csv_to_name[q_csv_name]
    }))
    
# Combine all scores into one DataFrame
all_scores_df = pd.concat(all_scores, ignore_index=True)

# print("\nSUS Summary Statistics:\n")
# for name, group in all_scores_df.groupby("q_csv_name"):
#     print(f"{name}:")
#     print(f"  Min:    {group['SUS Score'].min():.2f}")
#     print(f"  25%:    {group['SUS Score'].quantile(0.25):.2f}")
#     print(f"  Median: {group['SUS Score'].median():.2f}")
#     print(f"  75%:    {group['SUS Score'].quantile(0.75):.2f}")
#     print(f"  Max:    {group['SUS Score'].max():.2f}\n")

# Plot SUS scoresplt.figure(figsize=(10,6))
plt.figure(figsize=(7, 5))

# Boxplot with hue assigned to x (future-proof)
sns.boxplot(
    x="q_csv_name",
    y="SUS Score",
    hue="q_csv_name",
    data=all_scores_df,
    palette="Set2",
    legend=False,
    linewidth=1
)

# Stripplot on top (no hue needed here)
sns.stripplot(
    x="q_csv_name",
    y="SUS Score",
    data=all_scores_df,
    color="black",
    alpha=0.45,
    jitter=True,
    size=4
)

plt.title("SUS Scores by q_csv_name", fontsize=13, pad=10)
plt.ylabel("SUS Score (0-100)", fontsize=11)
plt.xlabel("")

sns.despine(left=True)
plt.grid(axis="y", alpha=0.3)
plt.grid(axis="x", visible=False)
plt.ylim(0, 100)

plt.tight_layout()
plt.show()
