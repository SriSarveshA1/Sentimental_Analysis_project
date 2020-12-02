import csv
import folium
import geopandas
import pandas as pd

def load_csv_file(csv_file):
    content = []
    with open(csv_file) as f:       #we are using the pickle
        reader = csv.DictReader(f)  #we by using the DictReader we are retriving the file from f(using pickle) and storing it in reader
        for row in reader:
            content.append(row)     #Thn we are appearing each row into the content list
    return content


def create_map(csv_file, output_html):
    mood_content = load_csv_file(csv_file) #Loading the csv file into the mood_content

    #Classify each mood_content item in country locations
    mood_location={}     #We are declaring a dictionary that 
    for item in mood_content:
        if item['location'] not in mood_location:
            mood_location[item['location']]={'Positive':0,'Negative':0}
        mood_location[item['location']][item['mood']]+=1   #for each location the mood is counted according to its occurances

    my_map=folium.Map()  #folium is a library that is used to create a Map
    my_map.save(output_html) #And then we are saving that map into the html file
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

    country_names=[]
    moods=[]
    for country in mood_location:
        mood=mood_location[country]['Positive']/(mood_location[country]['Positive']+mood_location[country]['Negative']) #We are calculating the overall postive tweets value pecrcentage
        moods.append(mood)  #And we are appending each mood into the moods list
        country_names.append(country) # And also we are appending each country name into the country_names list

    data_to_plot=pd.DataFrame({'Country':country_names,'Mood':moods})   #We are creating a dataframe inside which we have two columns Country=All country names ,Mood=That says a number of positive tweets of a brand in each country

    folium.Choropleth(               #we are using this folium to color the different parts of a country in a continent
        geo_data=world,
        name='choropleth',
        data=data_to_plot,
        columns=['Country', 'Mood'], #Columns that we are going to pass is Country and mood
        key_on='feature.properties.name',
        fill_color='YlGn',           #Colors are yellow and green
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Mood'
    ).add_to(my_map)

    folium.LayerControl().add_to(my_map)  #we are giving the layer control to the my_map value
    my_map.save(output_html)              #And at last we are saving the my_map into the output.html



if __name__ == "__main__":
    create_map("tweet_mood_java.csv", "mood_java.html")
    create_map("tweet_mood_python.csv", "mood_python.html")