import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns

sns.set_theme(style="whitegrid")

questionnaire_chooser = {
    "Questionnaire_Shein2026-01-27_07_04_41.csv" : "Shein",
    "Questionnaire_ChromeHearts2026-01-27_07_04_37.csv" : "ChromeHearts",
}

all_scores = []
for q in questionnaire_chooser.keys():
    #print(q)
    data = pd.read_csv(q)
    data = data[:-2]
    data = data.iloc[:, 2:]

    num_tasks = 6
    fig, axes = plt.subplots(2, 3, figsize=(12, 6))
    axes = axes.flatten()  # make it easier to iterate

    for idx, i in enumerate(range(3, 3 + num_tasks)):
        difficulty = data.iloc[:, i]
        possible_answers = range(1, 8)
        counts_dict = (
            difficulty
            .value_counts()
            .reindex(possible_answers, fill_value=0)
            .to_dict()
        )

        # print(f"Task {i-2}")
        # print(f"Mean: {difficulty.mean():.2f}")
        # print(f"Variance: {difficulty.var():.2f}\n")sns.set_theme(style="whitegrid")

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


    plt.suptitle(f"Difficulty Distribution - {questionnaire_chooser[q]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    # print("\n")
    
    score_modifier = 20
    score_coefficient = 2.5
    sus_scores = []
    for index, row in data.iterrows():
        odd_indices = [0, 2, 4, 6, 8]
        even_indices = [1, 3, 5, 7, 9]
        
        for x in range(len(odd_indices)):
            odd_indices[x] += 9
        for x in range(len(even_indices)):
            even_indices[x] += 9      
        total_score = row.iloc[odd_indices].sum() - row.iloc[even_indices].sum()
        sus_score = (score_modifier + total_score) * score_coefficient
        sus_scores.append(sus_score)
    
    all_scores.append(pd.DataFrame({
        "SUS Score": sus_scores,
        "Questionnaire": questionnaire_chooser[q]
    }))
    
# Combine all scores into one DataFrame
all_scores_df = pd.concat(all_scores, ignore_index=True)

# Plot SUS scoresplt.figure(figsize=(10,6))
plt.figure(figsize=(7, 5))

# Boxplot with hue assigned to x (future-proof)
sns.boxplot(
    x="Questionnaire",
    y="SUS Score",
    hue="Questionnaire",
    data=all_scores_df,
    palette="Set2",
    legend=False,
    linewidth=1
)

# Stripplot on top (no hue needed here)
sns.stripplot(
    x="Questionnaire",
    y="SUS Score",
    data=all_scores_df,
    color="black",
    alpha=0.45,
    jitter=True,
    size=4
)

plt.title("SUS Scores by Questionnaire", fontsize=13, pad=10)
plt.ylabel("SUS Score (0-100)", fontsize=11)
plt.xlabel("")

sns.despine(left=True)
plt.grid(axis="y", alpha=0.3)
plt.grid(axis="x", visible=False)
plt.ylim(0, 100)

plt.tight_layout()
plt.show()
