import csv
#using CSV: Comma Separated Values
#every row separated by commas, every column separated by new line

def save_to_file(jobs):
    #open a file (if the file doesn't exist --> creates a file)
    #mode = "w" --> we want to write
    file = open("jobs.csv", mode = "w")
    #create a writer --> going to write comma separated values in the file
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Location", "Link"])
    for job in jobs:
        #want only the content and not the names in the dictionary as a list
        # print(list(job.values()))
        writer.writerow(list(job.values()))
    # print(jobs)
    return