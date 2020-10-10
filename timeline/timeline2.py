from datetime import date
import pandas as pd
import numpy as np
import altair as alt
import random
# alt.renderers.enable('notebook') # if in jupyter

df = pd.read_csv("tasks.csv")

df = pd.DataFrame([{"Initiative":"One", "Task Name": "Milestone A", "Start date": '2017-01-01', "End date":'2017-02-02', "Resource": 'Jack', "Progress %": random.randrange(0,100)},
      {"Initiative":"One", "Task Name": "Milestone B", "Start date": '2018-01-01', "End date":'2018-02-02', "Resource":'Jack', "Progress %": random.randrange(0,100)},
      {"Initiative":"Two", "Task Name": "Milestone A", "Start date": '2017-01-17', "End date":'2017-04-28', "Resource":'Joe', "Progress %": random.randrange(0,100)},
      {"Initiative":"Two", "Task Name": "Milestone B", "Start date": '2017-03-17', "End date":'2017-04-28', "Resource":'Joe', "Progress %": random.randrange(0,100)},
      {"Initiative":"Three", "Task Name": "Milestone A", "Start date": '2017-01-14', "End date":'2017-03-14', "Resource":'John', "Progress %": random.randrange(0,100)},
      {"Initiative":"Three", "Task Name": "Milestone B", "Start date": '2018-01-14', "End date":'2018-03-14', "Resource":'John', "Progress %": random.randrange(0,100)}])



df["Start date"] = pd.to_datetime(df["Start date"])
df["End date"] = pd.to_datetime(df["End date"])

# Use the progress to find how much of the bars should be filled
# (i.e. another end date)
df["progress date"] =  (df["End date"] - df["Start date"]) * df["Progress %"] / 100 + df["Start date"]

# Concatenate the two 
newdf = np.concatenate([df[["Task Name", "Start date", "End date", "Progress %"]].values,  
                        df[["Task Name", "Start date", "progress date", "Progress %"]].values])
newdf = pd.DataFrame(newdf, columns=["Task Name", "Start date", "End date", "Progress %"])

# Reconvert back to datetime
newdf["Start date"] = pd.to_datetime(newdf["Start date"])
newdf["End date"] = pd.to_datetime(newdf["End date"])

# This is the indicator variable (duration vs progress) where the grouping takes place
newdf["progress_"] = np.concatenate([np.ones(len(newdf)//2), np.zeros(len(newdf)//2), ])

# color for first half, color for second half
range_ = {"Initiative": ['#1f77b4', '#5fa0d4',] }
default_range=['#000', '#fff',]
# The stacked bar chart will be our "gantt with progress"
chart = alt.Chart(newdf).mark_bar().encode(
    x=alt.X('Start date', stack=None),
    x2='End date',
    y=alt.Y('Task Name', sort=list(df.sort_values(["End date",
                                                      "Start date"])["Task Name"])*2),
    color=alt.Color('progress_', scale=alt.Scale(range=range_.get("Initiative",default_range)), legend=None)
) 

# Create appropriate labels
newdf["text%"] = newdf["Progress %"].astype(str) + " %"


# And now add those as text in the graph
text = alt.Chart(newdf).mark_text(align='left', baseline='middle', dx=5, color="white",  fontWeight="bold").encode(
    y=alt.Y('Task Name', sort=list(df.sort_values(["End date",
                                                      "Start date"])["Task Name"])*2),
    x=alt.X('Start date'),
    text='text%',
)

# Plot the graph
alt.layer(chart, text).facet(
  row='Initiative'
)