import pandas as pd
import scipy 
import numpy as np


before = pd.read_csv("final_before.csv")
after = pd.read_csv("final_after.csv")



# normalize everybody's person id by stripping whitespace, consistent case
before["Person ID"] = before["Person ID"].astype(str).str.strip().str.lower()
after["Person ID"] = after["Person ID"].astype(str).str.strip().str.lower()


#rename columns
before = before.rename(columns={"Total (anxiety)": "Total"})
after = after.rename(columns={"Total (anxiety)": "Total"})


merged = pd.merge(before[["Person ID","Total"]], 
after[["Person ID","Total"]],
on="Person ID",
how="inner",
suffixes= ("_pre","_post")
)


# "Series " data type
total_pre = merged["Total_pre"]
total_post = merged["Total_post"]

# Compute mean total STAI scores for each person
mean_total_pre_stai_score = total_pre.mean()
mean_total_post_stai_score = total_post.mean()

print("="*100)
print("Mean for Total Pre STAI Scores: ",mean_total_pre_stai_score)
print("Mean for Total Post STAI Scores: ",mean_total_post_stai_score)

# Compute Std. Dev for pre and post scores 
total_pre_std = total_pre.std()
total_post_std= total_post.std()

print("Std. Dev for Total Pre STAI Scores: ",total_pre_std)
print("Std. Dev for Total Post STAI Scores: ",total_post_std)

# Do the Paired T Test, print out T and P value
result = scipy.stats.ttest_rel(total_pre,total_post)

print("="*100)
print("T value:",result.statistic)
print("P value:",result.pvalue)

# Calculate the confidence interval
confidence_interval = result.confidence_interval(confidence_level=0.95)
print("95% confidence interval for mean change in STAI score:",confidence_interval.low,"to",confidence_interval.high)

# finding the percent of participants who showed reduction
print("="*100)
total_participants = len(merged)
decreased_change_count = 0
change_for_each_participant = []
for i in range(total_participants):
    change = merged["Total_post"].iloc[i] - merged["Total_pre"].iloc[i]
    change_for_each_participant.append(change)
    if change<0:
        decreased_change_count+=1

percent_participants_who_showed_reduction = decreased_change_count/total_participants
print(f"The % of Participants whose STAI scores reduced: {percent_participants_who_showed_reduction:.4f} out of {total_participants} people")

# finding Cohen's d
change = total_post-total_pre
cohens_d = change.mean() / change.std(ddof=1)
print("Cohen's d (paired):",cohens_d)

    