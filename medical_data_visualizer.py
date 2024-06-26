import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv", header = 0, sep = ',')

# Add 'overweight' column
#Calculating the BMI through vectorized operation and then replacing with 1 or 0 based on whether BMI is >25 using np.where
df['overweight'] = np.where((df['weight']/((df['height']/100)**2) > 25), 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = np.where((df['cholesterol'] > 1), 1, 0)
df['gluc'] = np.where((df['gluc'] > 1), 1, 0)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,id_vars=['cardio'],value_vars=['cholesterol','gluc','smoke','alco','active','overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio','variable','value'],as_index=False).value_counts()
    df_cat = df_cat.rename(columns = {'count': 'total'})

    # Draw the catplot with 'sns.catplot()'

    cat_plot = sns.catplot(data=df_cat, x='variable', y='total', kind='bar', col='cardio' , hue='value')



    # Get the figure for the output
    fig = cat_plot.figure


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data

    heatmap_filter = np.where((df['ap_lo'] <= df['ap_hi']) 
                              & (df['height'] >= df['height'].quantile(0.025)) 
                              & (df['height'] <= df['height'].quantile(0.975))
                              & (df['weight'] >= df['weight'].quantile(0.025))
                              & (df['weight'] <= df['weight'].quantile(0.975)))
    df_heat = df.iloc[heatmap_filter]

    # Calculate the correlation matrix
    corr = df_heat.corr().round(1)

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'

    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f')

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
