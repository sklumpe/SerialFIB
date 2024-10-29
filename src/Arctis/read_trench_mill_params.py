#def read_trench_mill_params(file):
#    with open(file,'r') as input_file:#
#
#    
#    return()


def read_trench_mill_params(filename):
    params = {
        "relief_cut_distance": None,
        "relief_cut_width": None
    }
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                if "relief_cut_distance=" in line:
                    # Extract the value after the equal sign and convert to float
                    params["relief_cut_distance"] = float(line.split("=")[1].strip())
                elif "relief_cut_width=" in line:
                    # Extract the value after the equal sign and convert to float
                    params["relief_cut_width"] = float(line.split("=")[1].strip())
                    
        # Check if both parameters were found
        if params["relief_cut_distance"] is None or params["relief_cut_width"] is None:
            print("Warning: One or more parameters not found in the file.")
            
        return params
    
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except ValueError:
        print("Error: Unable to convert parameter value to float.")
        return None
