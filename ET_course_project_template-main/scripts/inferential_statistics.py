import numpy as np
from scipy import stats

############# DATA ################
group1 = [
    1.3, 1.4
]
group2 = [
    1.1, 1.2
]
###################################



def cohen_d(x, y):
    # Calculate the means of the two samples
    mean_x = np.mean(x)
    mean_y = np.mean(y)

    # Calculate the standard deviations of the two samples
    std_x = np.std(x, ddof=1)
    std_y = np.std(y, ddof=1)

    # Calculate the pooled standard deviation
    pooled_std = np.sqrt((std_x ** 2 + std_y ** 2) / 2)

    # Calculate Cohen's d
    d = (mean_x - mean_y) / pooled_std
    return d


def two_sample_t_test(x, y):
    t_stat, p_value = stats.ttest_ind(x, y)
    return t_stat, p_value

# Calculate Cohen's d
effect_size = cohen_d(group1, group2)
print(f"Cohen's d: {effect_size}")

# Perform the two-sample t-test
t_stat, p_value = two_sample_t_test(group2, group1)
print(f"t-statistic: {t_stat}, p-value: {p_value}")
