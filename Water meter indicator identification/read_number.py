import json
def run_read_number():  
# Opening JSON file
    f = open('data.txt')
      
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
      
    # Iterating through the json
    # list

      
    # Closing file
    f.close()
    return data

