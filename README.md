# 507 Streamlit Demo

## Streamlit Dashboard URL
https://app-dashboard-enhanced-nmmvoupzgpej7kz3rfgwgt.streamlit.app/

## Info Shown in Dashboard
1. Changes in Learning Modality Over Time (Weeks)
    * **Chart Used:** Horizontal Bar
 
In the original repository, this section used a vertical bar chart. However, I felt the x-axis labels were too long even after I removed the timestamp from the date. Thus, I opted for a horizontal bar chart as I felt it was easier on the eye. 

I added toggles for the learning modality in case users may want to focus on a specific chart without visual distractions from the other modality charts. I also added a slider to filter chart dates in case users want to view data from a specific time range.

2. Amount of Operational Schools by Learning Modality (in percent and specific value)
    * **Chart Used:** Pie

Streamlit does not have a built-in method of creating pie charts, so I installed the Plotly package to do so. The pie chart by default only shows percents, so I updated the pie chart to include the specific count of learning modalities. That way, users can view the counts without the need to hover over the pie chart. 

3. Geographical Distribution of Learning Modality in US
    * **Chart Used:** Choropleth Map

The total student count per learning modality per state was obtained using pandas `groupby()` method and then used to create the map. A select box widget was added to allow users to choose a specific learning modality to view on the map. 

4. Distribution of Operational Schools Across States
    * **Chart Used:** Vertical Bar

The total amount of operational schools per state was obtained and then plotted. While some of the x-axis state labels are omitted due to the chart width being too small, users can enlarge the chart by hovering over it and then clicking the fullscreen button that appears on the top right, which will show all the state labels.


## Challenges + Solution
There were issues deploying the app on Streamlit Cloud initially. I realized I did not update the requirements.txt, so I used `pip freeze > requirements.txt` and then pushed the updated file. However, that led to installation errors on Streamlit Cloud while deploying. I solved the issue by undoing the pip freeze and manually adding in packages to the requirements.txt, excluding packages that came with the creation of a new virtual env (venv). 

I believe the issue had stemmed from putting the venv packages inside requirements.txt. Perhaps those packages conflicted with how the deployment process works on Streamlit Cloud.