import csv
import folium
import geopandas

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
    print(world.head()) # we are printing the first some rows and it has headers like pop_est,continent,gdp_md_est,geometry(The shape of the country)
    print(world.loc[0]) #We are printing the first row of the table that has pop_est,continent,gdp_md_est,geometry(The shape of the country)


if __name__ == "__main__":
    create_map("tweet_mood_java.csv", "mood_java.html")