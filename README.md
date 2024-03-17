# HIV-Dash

HIV/AIDS is a notorious disease that impacts not only the health of infected individuals across the world, but also their lifestyle, their mental health, and overall quality of life. Not all those that are affected have access to sufficient resources for the necessary treatment and care to manage the disease. As data scientists in the health sector, we want to transform our data containing HIV/AIDS statistics across the globe to extract insights to help professionals understand the gap between affected peoples and their access to care.

The HIV dash contains 3 separate tabs that will allow users to extract comprehensive insights about the HIV dataset with 12 indicators (e.g. Estimated mortality rate, estimated infection rate, mother-to-child transmission rate).

[**HEROKU deployment**](https://hiv-dash-8ad3dffed17f.herokuapp.com/)

## Tab 1

Since the dataset covers the period from 2000 to 2022 for numerous countries, the first tab will allow users to visualize the trend of an indicator of choice across up to 4 countries. The resulting plot will show a line graph with each country represented by different colour, and a slider bar at the x-axis that will allow users to expand or limit the range of the years.
![](https://github.com/shaytran/HIV-Dash/blob/main/doc/Sketch/Tab1.png))

## Tab 2

The second tab will show a worldwide map highlighting the spread of an indicator of choice across the world. A color-varying dot will overlay on top of the countries that contain data of the specific indicator, with the more severe countries having a darker color. There is also an animation slider at the x-axis that will allow users to visualize the changing global spread of a specific indicator across time, users can either visualize it by playing through the animation or scrolling through the slider. 
![](https://github.com/shaytran/HIV-Dash/blob/main/doc/Sketch/Tab2.png)

## Tab 3

The third tab will allow users to visualize a direct comparison of a specific indicator between two countries. With simple statistics such as mean, range of a specific indicator for both countries shown in a table like format. Users can toggle the slider bar at the x-axis to visualize the comparison of the statistics across time (Default year will be the most recent year 2022 in the dataset).
![](https://github.com/shaytran/HIV-Dash/blob/main/doc/Sketch/Tab3.png)
