from collections import Counter

import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.power import FTestAnovaPower
from pingouin import power_anova
import statsmodels.stats.multicomp as mc
import scikit_posthocs as sp

data = pd.read_csv("inferential_stats_data/combinedDataFinal_K7.csv")
data1 = pd.read_csv("inferential_stats_data/combinedDataFinal_K7_1.csv")
data2 = pd.read_csv("inferential_stats_data/combinedDataFinal_K7_2.csv")

print(data['Condition'].unique())

def anova_table(aov):
    aov['mean_sq'] = aov[:]['sum_sq']/aov[:]['df']

    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])

    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*aov['mean_sq'][-1]))/(sum(aov['sum_sq'])+aov['mean_sq'][-1])

    cols = ['sum_sq', 'df', 'mean_sq', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
    aov = aov[cols]
    return aov

def calculateStats(item):
    ap = 0
    af = 0
    kp = 0
    kstat = 0
    fstat = 0
    #First generate residuals to feed in for shapiro and levene
    modelData = data[['Condition', item]].copy()
    modelData['Condition'] = modelData['Condition'].map(str)
    model = ols(item + ' ~ C(Condition)', data=modelData).fit()
    #First Shapiro for Conditions: 1, and 2
    assumption1 = False
    stat1, p1 = stats.shapiro(model.resid)
    if p1 >= 0.05:
        assumption1 = True
    print("Shapiro: %.8f" % p1)
    #Then Levene for Conditions 1, and 2
    stat, p = stats.levene(data1[item], data2[item])
    if p >= 0.05:
        lev = True
    print('Levene: %.6f' % p)
    print("Anova")
    fstat, p = stats.f_oneway(data1[item], data2[item])
    ap = p
    af = fstat
    print(fstat, p)
    anovaReject = False
    if p < 0.05:
        print("Reject NULL Hypothesis (YAY)")
        anovaReject = True
    else:
        print("CAN'T reject H0. (OH NO)")
    fstat, p = stats.kruskal(data1[item], data2[item])
    print("Kruskal")
    #Kruskal if no Anova
    print(fstat, p)
    kp = p
    kstat = fstat
    kruskalWallis = False
    if p < 0.05:
        print("Reject NULL Hypothesis (YAY)")
        kruskalWallis = True
    else:
        print("CAN'T reject H0. (OH NO)")
    #Use f statistic to generate power analysis
    aov_table = sm.stats.anova_lm(model, typ=2)
    #print(aov_table)
    sum_sq = aov_table["sum_sq"].tolist()
    effect_size = (sum_sq[0] / (sum_sq[0] + sum_sq[1]))
    print("Power")
    print(effect_size)

    return [p1, p, ap, af, anovaReject, kp, kstat, kruskalWallis, power_anova(eta=effect_size, k=2, n=53), power_anova(eta=effect_size, k=2, power=0.80)]
    #print('alpha: %.4f' % power_anova(eta=effect_size, n=79, k=3, power=0.80, alpha=None))

def frequency():
    items = [data1, data2]
    for item in items:
        print("ITEM")
        words = item["typeOfRelationship"].tolist()

        # print(mean(words), stdev(words), median(words))
        print(Counter(words).keys())  # equals to list(set(words))
        print(Counter(words).values())  # counts the elements' frequency

def fisherExact(contingency):
    print(stats.fisher_exact(contingency))

def chiSquare3(contingency):
    print(stats.chi2_contingency(contingency))

def tukey(item):
    modelData = data[['Condition', item]].copy()
    modelData['Condition'] = modelData['condition'].map(str)

    comp = mc.MultiComparison(modelData[item], modelData['condition'])
    post_hoc_res = comp.tukeyhsd()
    post_hoc_res.summary()
    print(post_hoc_res.summary())

def bonferroni(item):
    modelData = data[['Condition', item]].copy()
    modelData['Condition'] = modelData['Condition'].map(str)

    comp = mc.MultiComparison(modelData[item], modelData['Condition'])
    tbl, a1, a2 = comp.allpairtest(stats.ttest_ind, method="bonf")
    print(tbl)

def dunn(item):
    modeldata1 = data1[item].tolist()
    modeldata2 = data2[item].tolist()
    print(sp.posthoc_dunn([modeldata1, modeldata2], p_adjust ='bonferroni'))

items = ['animacy',
         'anthropomorphism',
         'lesson',
         'transitions',
         'recall',
         'recognition',
         'p_corr_0_meanF0Hz',
         'Proximity_meanF0Hz',
         'Convergence_meanF0Hz',
         'p_corr_0_stdevF0Hz',
         'Proximity_stdevF0Hz',
         'Convergence_stdevF0Hz',
         'p_corr_0_HNR',
         'Proximity_HNR',
         'Convergence_HNR',
         'p_corr_0_localJitter',
         'Proximity_localJitter',
         'Convergence_localJitter',
         'p_corr_0_localabsoluteJitter',
         'Proximity_localabsoluteJitter',
         'Convergence_localabsoluteJitter',
         'p_corr_0_rapJitter',
         'Proximity_rapJitter',
         'Convergence_rapJitter',
         'p_corr_0_ppq5Jitter',
         'Proximity_ppq5Jitter',
         'Convergence_ppq5Jitter',
         'p_corr_0_ddpJitter',
         'Proximity_ddpJitter',
         'Convergence_ddpJitter',
         'p_corr_0_localShimmer',
         'Proximity_localShimmer',
         'Convergence_localShimmer',
         'p_corr_0_localdbShimmer',
         'Proximity_localdbShimmer',
         'Convergence_localdbShimmer',
         'p_corr_0_apq3Shimmer',
         'Proximity_apq3Shimmer',
         'Convergence_apq3Shimmer',
         'p_corr_0_apq5Shimmer',
         'Proximity_apq5Shimmer',
         'Convergence_apq5Shimmer',
         'p_corr_0_apq11Shimmer',
         'Proximity_apq11Shimmer',
         'Convergence_apq11Shimmer',
         'p_corr_0_ddaShimmer',
         'Proximity_ddaShimmer',
         'Convergence_ddaShimmer',
         'p_corr_0_meanPitch',
         'Proximity_meanPitch',
         'Convergence_meanPitch',
         'p_corr_0_maxPitch',
         'Proximity_maxPitch',
         'Convergence_maxPitch',
         'p_corr_0_minPitch',
         'Proximity_minPitch',
         'Convergence_minPitch',
         'p_corr_0_meanIntensity',
         'Proximity_meanIntensity',
         'Convergence_meanIntensity',
         'p_corr_0_maxIntensity',
         'Proximity_maxIntensity',
         'Convergence_maxIntensity',
         'p_corr_0_minIntensity',
         'Proximity_minIntensity',
         'Convergence_minIntensity']

sig = ['animacy',
       'anthropomorphism',
       'p_corr_0_HNR',
       'Proximity_apq11Shimmer',
       'Convergence_meanPitch',
       'Proximity_maxPitch']

for sigItems in sig:
    print(sigItems)
    print(bonferroni(sigItems))
    print(dunn(sigItems))