import csv


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

    cnt=0
    for item in mood_location:  #from the dictionary we are taking the country name and along with that we print how many positive and negative
        print(item,mood_location[item])
        cnt+=1
        if cnt>10:
            break


if __name__ == "__main__":
    create_map("tweet_mood_java.csv", "mood_java.html")