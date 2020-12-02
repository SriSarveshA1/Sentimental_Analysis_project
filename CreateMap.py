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

    print(mood_content[0])


if __name__ == "__main__":
    create_map("tweet_mood_java.csv", "mood_java.html")