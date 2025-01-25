#Import libraries
import csv
import pandas as pd
from matplotlib import pyplot as plt

#Read in data from geiger counter
def read_alt_geiger_data(filename):
    """Read the contents of a CSV file into a compound
    list and return the list. Each element in the
    compound list will be a small list that contains
    the values from one row of the CSV file.

    Parameter filename: the name of the CSV file to read
    Return: a list of lists that contain strings
    """
    DATE_TIME_INDEX = 0
    EVENT_INDEX = 1
    COUNT_RATE_INDEX = 3


    #Create empty list for our filedata
    compound_list = []

    #Open our file and read everything to a reader
    with open(filename, "rt") as csv_file:
        reader = csv.reader(csv_file)

        #Skip the first line
        next(reader)   

        #Parse through file one row at a time
        for row_list in reader:

            #Check to see that the event column has the value "Current data values"
            if row_list[EVENT_INDEX] == "Current data values":
                row = []
                row.append(row_list[DATE_TIME_INDEX])
                row.append(row_list[COUNT_RATE_INDEX])

                compound_list.append(row)
 
    return compound_list


#Parse through our data to remove the date and the cpm from the strings
def parse_geiger_data(compound_list):  
    """Function parses through the compound list and removes the 
    Date and the CPM elements from the list
    
    Parameter: compound list of file_data from read_compound_list
    Return: modified compound list
    """
    DATE_TIME_STRING_INDEX = 0
    TIME_STRING_INDEX = 1
    CPM_STRING_INDEX = 1
    CPM_DATA_INDEX = 0

    modified_compound_list = []

    #Loop through the rows and remove necesary extras
    for row in compound_list:

        #Store full date time string
        date_time_string = row[DATE_TIME_STRING_INDEX]

        #Split string and discard date
        time_string = date_time_string.split("  ")[TIME_STRING_INDEX] #Need to modify so that time is broken up by ":"

        #Replace the '.' in the string with ':'
        time_string = time_string.replace(".",":")

        #Store full CPM string
        CPM_string = row[CPM_STRING_INDEX]

        #Split string and discard the CPM
        CPM_data = CPM_string.split(" ")[CPM_DATA_INDEX]

        #Add both to a list and append to our modified compound list
        new_row_list = [time_string,CPM_data]
        modified_compound_list.append(new_row_list)

    return modified_compound_list

def read_altitude_data(filename):
    """Function reads in the file data from the txt file and 
    formats it into a list for later parsing.
    
    Parameters: filename as a string
    Return: compound list of strings
    """
    TIME_INDEX = 0
    ALTITUDE_INDEX = 10

    compound_list = []

    #Open the txt file and read the wanted values form it
    with open(filename, "rt") as text_file:
        
        #Read one line at a time
        for line in text_file:

            #Remove white spacing from the line
            clean_line = line.strip()

            #Split list up based on delimiter
            time_string = clean_line.split(", ")[TIME_INDEX]
            altitude_string = clean_line.split(", ")[ALTITUDE_INDEX]

            #Add both to a list and append to the compound list
            new_line = [time_string,altitude_string]
            compound_list.append(new_line)

    return compound_list

def altitude_time_offset_adjustment(time_string):
    """Function takes the input time string and adjusts the string
    to account for the time offset inherent in the altimeter.
    Params:
        time_string: time in the form 'h:m:s'
    Return:
        adjusted_time_string    
    """
    #IMPORTANT NOTICE: Time adjustment assumes the actual time is 5 hours 
    # BEHIND the altimeter time (see below main for details). This should
    # be checked to verify that it is correct.
    OFFSET = 5

    #Split string by ':' delimiter and extract the hours value
    hour_string = time_string.split(':')[0]
    minute_string = time_string.split(':')[1] 
    second_string = time_string.split(':')[2]
    
    hour_value = int(hour_string) #convert to float for numerical comparison
    
    #For cases where time is still less than 24 hrs
    if (hour_value >= 23):
        hour_value -= OFFSET

    #For cases where it ticks back over to 0
    else:
        hour_value += 23 - OFFSET

    #Convert hour value back into a string and replace the old
    # string
    new_hour_string = str(hour_value)
    adjusted_time_string = new_hour_string + ":" + minute_string + ":" + second_string

    return adjusted_time_string


def parse_altitude_list(compound_list):
    """Function parses the compound list of altitude data and removes the ms
    from the time data and the 'Altitude' string from the altitude data
    
    Parameters: compound list of the altitude data
    Returns: modified compound list of usable data
    """
    TIME_INDEX = 0
    ALTITUDE_DATA_INDEX = 1

    modified_compound_list = []

    #Loop through the rows of data and remove necessary items
    for row in compound_list:

        #Remove the miliseconds of the time string
        time_string = row[0].split(".")[TIME_INDEX]

        #Replace time_string with adjusted time string
        adjusted_time_string = altitude_time_offset_adjustment(time_string)

        #Remove the 'Altitude' string from the altitude string
        altitude_data = row[1].split(": ")[ALTITUDE_DATA_INDEX]

        #Add both to a list and append to modified_compound_list
        new_line = [adjusted_time_string,altitude_data]
        modified_compound_list.append(new_line)
    
    return modified_compound_list

def match_data_times(geiger_list,alt_list):
    """Matches the geiger counter and altitude data
    based on their times.
    Params:
        geiger_data: comp list [time,cpm] (str)
        alt_data: comp list [time,altitude] (str)
    Return:
        compound list of geiger_data and alt_data
    """
    #Create new lists
    geiger_data = []
    geiger_time = []
    alt_data = []
    alt_time = []

    #Copy geiger CPM into list geiger_data
    for data in geiger_list:
        geiger_data.append(float(data[1]))

    #Copy geiger time into list
    for time in geiger_list:
        geiger_time.append(time[0])

    #Copy alt time into a list
    for time in alt_list:
        alt_time.append(time[0])

    #Copy alt data into a list
    for data in alt_list:
        alt_data.append(data[1])

    #Convert alt_list into a dictionary
    alt_dict = dict(zip(alt_time,alt_data))

    #Find time values from our altitude data that come close
    # to our geiger time value by +/- a tolerance

    matching_alt_list = []
    
    #Need to add matched values w/ their respective geiger_data
    for time in geiger_time:
        #Split time into H,M,S
        geiger_hr =  int(time.split(":")[0])
        geiger_min = int(time.split(":")[1])
        geiger_sec = int(time.split(":")[2])

        #Debug info
        #print("Geiger_hr: ",geiger_hr)
        #print("Geiger_min: ",geiger_min)
        #print("Geiger_sec: ",geiger_sec)

        #Create dictionary for difference values
        diff_vals = []
        diff_vals_dict = {} 

        found_match = False
        found_one_match = False
        last_index = 0

        while(found_match != True and last_index < len(alt_time)):
            
            #Debug Stuff
            #print("Last Index = ",last_index)
            #print("alt_time at last index: ",alt_time[last_index])
            #print("alt_hr: ",  int(alt_time[last_index].split(":")[0]))
            #print("alt_min: ", int(alt_time[last_index].split(":")[1]))
            #print("alt_sec: ", int(alt_time[last_index].split(":")[2]))

            #Split alt time into values
            alt_hr =  int(alt_time[last_index].split(":")[0])
            alt_min = int(alt_time[last_index].split(":")[1])
            alt_sec = int(alt_time[last_index].split(":")[2])

            #Check to see if the hour and minutes match
            if (geiger_hr == alt_hr and geiger_min == alt_min):
                diff_vals.append(abs(geiger_sec-alt_sec))
                diff_vals_dict[str(abs(geiger_sec-alt_sec))] = alt_time[last_index]
                found_one_match = True
                
            
            elif (geiger_hr == alt_hr):
                if (found_one_match):
                    found_match = True
                    #print("Match Found!")

                    

            last_index += 1

        #Debug stuff
        #print("Len of diff_vals: ",len(diff_vals))

        if (len(diff_vals) > 0):
            #Find the minimum of the different values
            min_value = str(min(diff_vals))
            min_value_time = diff_vals_dict[min_value]

            #Find the altitude data associated with the alt_time
            min_alt_data = alt_dict[min_value_time]

            #Add min_alt_data to matching_alt_list
            matching_alt_list.append(float(min_alt_data))

    #Combine data into one set
    data_set = [geiger_data,matching_alt_list]

    return data_set

def print_max_altitude_CPM(data_set):
    """ Parses through the data set to find the maximum altitude, then
    matches that value with its accompanying value in the list.

    Params: data_set (list)

    Returns: n/A
    """
    data = {
        "CPM" : data_set[0],
        "Altitude" : data_set[1]
    }

    df = pd.DataFrame(data)

    #Sort our data by altitude
    sorted_df = df.sort_values(by="Altitude", ascending = False)
    print("======================================")
    print("Max Altitude CPM")
    print("======================================")
    print(sorted_df.iloc[1])
    print()

    return

def print_min_altitude_CPM(data_set):
    """ Parses through the data set to find the minimum altitude, then
    matches that value with its accompanying value in the list.

    Params: data_set (list)

    Returns: n/A
    """
    data = {
        "CPM" : data_set[0],
        "Altitude" : data_set[1]
    }

    df = pd.DataFrame(data)

    #Sort our data by altitude
    sorted_df = df.sort_values(by="Altitude", ascending = True)
    print("======================================")
    print("Min Altitude CPM")
    print("======================================")
    print(sorted_df.iloc[1])
    print()

    return

def print_max_CMP_alt(data_set):
    """ Parses through the data set to find the maximum CPM, then
    matches that value with its accompanying value in the list.

    Params: data_set (list)

    Returns: n/A
    """
    data = {
        "CPM" : data_set[0],
        "Altitude" : data_set[1]
    }

    df = pd.DataFrame(data)

    #Sort our data by altitude
    sorted_df = df.sort_values(by="CPM", ascending = False)
    print("======================================")
    print("Max CPM Altitude")
    print("======================================")
    print(sorted_df.iloc[1])
    print()

    return

def print_min_CMP_alt(data_set):
    """ Parses through the data set to find the minimum CPM, then
    matches that value with its accompanying value in the list.

    Params: data_set (list)

    Returns: n/A
    """
    data = {
        "CPM" : data_set[0],
        "Altitude" : data_set[1]
    }

    df = pd.DataFrame(data)

    #Sort our data by altitude
    sorted_df = df.sort_values(by="CPM", ascending = True)
    print("======================================")
    print("Min CPM Altitude")
    print("======================================")
    print(sorted_df.iloc[1])
    print()

    return

def save_data(file_name, data_set):
    """ Saves data to a csv file 
    Params: file_name (string)
            data_set  (list or array)
    
    Return: none
    """
    with open(file_name + ".csv", "w", newline = "") as file:
        writer = csv.writer(file)

        #Write the header
        writer.writerow(["CPM","Altitude(m)"])

        #Write CPM w/ adjacent altitude
        for index, data in enumerate(data_set[0]):
            writer.writerow([data_set[0][index],data_set[1][index]])

    return

def plot_data(geiger_data,alt_data):
    plt.plot(alt_data,geiger_data,'.')
    plt.title("Altitude vs CPM")
    plt.ylabel("Geiger CPM")
    plt.xlabel("Altitude (m) above sea level")
    plt.plot()
    plt.show()

    return

def main():
    #Create compound list of the geiger counter values at specific times
    compound_geiger_list = read_alt_geiger_data("geiger_altitude_data.csv")
    mod_geiger_list = parse_geiger_data(compound_geiger_list)

    #Create compound list of altitude at given times
    compound_alt_list = read_altitude_data("GPSLOG00.txt")
    mod_alt_list = parse_altitude_list(compound_alt_list)

    #Match data to each other
    data_set = match_data_times(mod_geiger_list,mod_alt_list)

    #Plot our data
    plot_data(data_set[0],data_set[1])

    #Save our data to a csv file (do not include type, default CSV file)
    save_data("output",data_set)

    #Find the maximum height and CPM
    print_max_altitude_CPM(data_set)

    #Find the minimum height and CPM
    print_min_altitude_CPM(data_set)

    #Find max CPM altitude
    print_max_CMP_alt(data_set)

    #Find max CPM altitude
    print_min_CMP_alt(data_set)

    return

main()