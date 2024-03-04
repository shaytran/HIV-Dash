# Milestone 2 Reflection

### Tab 1
Tab 1 is called **HIV Indicator Trends by Country and Year** and it displays a line chart that represents a chosen HIV indicator (ie. `Estimated rate of annual AIDS-related deaths (per 100,000 population)`) values over a certain amount of years for up to 4 different countries. There is a drop-down menu that allows users to choose their HIV indicator and the countries of interests, and there is a slider to let the users choose a year range. A legend will appear to indicate the countries as well. There are some exception cases and handling like when choosing more than 4 countries, the tab will prompt the user to limit the number of countries before producing a chart. 

One thing that has not been addressed is showing some warning or message for when there is no data of a chosen indicator retrieved for a country within a specific year range. The line for that country would just not appear in the chart. What could be implemented is some sort of message to let them know that there is no data available for ther chosen criteria. For our prototype, there is aren't any components that are not working as intended in its current state.

The tab does well in creating the necessary components of the chart like the axis and the legend, but it sometimes the range is not in the most optimal state when representing many countries. This could be adjusted to make the chart look more intuitive. Additionally, some aesthetics could be improved to make the tab look more interesting and engaging. 

### Tab 2
Tab 2 is called **HIV Indicator map**, it showcases the global spread of a chosen HIV indicator in the chosen year. How it accomplishes this goal is through displaying a world wide map in the natural earth projection, the value of the chosen indicator will overlay on top of each country as a colored circle using the Viridis color scale, and the size of the colored circle will increase with larger indicator value. The user can choose the indicator through the drop down menu underneath the tab title, and the year through the slide bar underneath the map.

Some limitations related to `Tab 2` at the moment are that the zoom in feature of the map is still quite difficult to work with, so I'm hoping if there is a way to create an additional slider that can allow an easier zoom in and zoom out user exeperience. In addition, the tab does not have a feature that can display the global spread of a chosen indicator across time automatically. For example, if users want to check the global spread of an indicator across multiple years right now, they will need to manually click through each year on the slidebar. Therefore, if I can incorporate some sort of animation feature, that will be helpful for users to visulize the trend of a chosen indicator more clearly.

Outside the limitations, some future improvements that can be made would be to decide whether Viridis is the appropriate color scale for the indicator color circle, check if there are any additional interactive features that can add useful information to the end users, and create a better design of the user interface.   

### Tab 3

Tab 3 is called **HIV Summary Statistics** and it returns a table of up to 10 selected countries for a given indicator. It also allows the user to select a year or a range of years and will return common summary statistics like min max, mean, and the count of null values for that indicator. The current capabilities are that as you increase the number of countries, the table presented will grow. However, for visual purposes, a limitation has been set to only display up to 10 countries. I decided to put this measure in place for ease of reading and general comparison purposes. Currently, the table is also sorted alphabetically and will keep growing in descending alphabeletical order. It is fairly straightforward to use, and just provides a quick light-weight ability to compare and contrast different countries in a more numerical fashion.

The current limitations are that depending on the specific combinations of indicator, country, and selection of year range, we can end up into situations where there is simply no data available from our data set, and thus, the table will appear empty. Perhaps, it may be better to show these as NA or NULL if no data is available. Additionally, I think that although the set-up 'works', there are still some improvements that could be made with respect to design. The table is a bit bland, it may be worthwhile exploring other color schemes for the table but to ensure that we are not too distracting from the overall messages. 

Other improvements may include: adding alternative means of sortings, and additional summary statistics. With respect to sorting, it currently only sorts alphabetically, but it may also be worth exploring sorting by other columns either in desc or asc order. For summary statistics, it is also worth looking into other statistics that help give more information on the countries.

### Conclusions

Overall, our project is well underway. What we have done here is to sketch out generally what the app will look like and its initial deployment. We will continue to reiterate over the design and development process and take into consideration feedback from instructors, TAs, and peers to further improve our project. We hope you enjoyed our initial deployment of our app!
