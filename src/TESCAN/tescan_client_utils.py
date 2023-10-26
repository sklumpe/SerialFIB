

#table=['10 keV; 420 nA', '500 eV; 10 pA', '2 keV; 20 pA', '2 keV; 10 pA Conv', '2 keV; 10 pA UHR', '30 keV; 3uA Katka na image', '30 keV; 3 uA Katka Background 2', '30 keV; 3uA Katka Background 1', '30 keV; 3 uA Katka na spot', '30 keV; 3.75uA', '30 keV; 20pA newApperture', '5 keV; 24 pA', '30 keV; 11 nA na image', '30 keV; 1uA Katka focused', '30 keV; 1uA Katka', '30 keV; Katka 9', '30 keV; Katka 8', '30 keV; Katka 7', '30 keV; Katka 6', '30 keV; Katka 5', '30 keV; 250pA from 100 nA', '1 keV; 10pA', '10 keV; 250 pA', '5 keV; 24 pA MZ', '10 keV; 20 pA', '30 keV; 3uA', '30 keV; 1.8uA', '30 keV; 230 nA', '30 keV; 100 nA', '30 keV; 200pA VB', '5 keV; 1 nA', '10 keV; 5 nA', '15 keV; 4 nA', '30 keV; 5.5 nA', '15 keV; 1 nA', '30 keV; 1uA', '30 keV; 700 nA', '30 keV; 430 nA', '30 keV; 340 nA', '5 keV; 15 nA', '10 keV; 10 nA', '10 keV; 1 nA', '30 keV; 120 nA', '30 keV; 61 nA', '30 keV; 21 nA', '30 keV; 11 nA', '30 keV; 1.1 nA', '30 keV; 330 pA', '30 keV; 50 pA', '30 keV; 200 pA', '30 keV; UHR', '30 keV; 30 pA', '30 keV; 20 pA', '30 keV; 10 pA', '30 keV; 100 pA', '30 keV; 20pA newApperture', '15 keV; 20 pA', '30 keV; 3 uA K', '30 keV; 3.75 katka focused', '30 keV; 100 nA', '30 keV; 200pA VB', '3 keV; test', '3 keV; 20 pA', '3 keV; 1 nA', '3 keV; 4.5 nA', '3 keV; 9 nA', '3 keV; 25 nA', '1 keV; 340 pA', '2 keV; 20 pA', '2 keV; 10 pA', '30 keV; D600D50 alignment test', '1 keV; 650 pA', '1 keV; 2.5 nA', '5 keV; 24 pA', '5 keV; 40 pA', '5 keV; 110 pA', '5 keV; 70 pA', '5 keV; 500 pA', '5 keV; 1 nA', '5 keV; 2.5 nA', '5 keV; 6 nA', '5 keV; 15 nA', '5 keV; 35 nA', '5 keV; 55 nA', '5 keV; 115 nA', '5 keV; 125 nA', '5 keV; 230 nA', '10 keV; 20 pA', '10 keV; 100 pA', '10 keV; 250 pA', '10 keV; 500 pA', '10 keV; 1 nA', '10 keV; 5 nA', '10 keV; 10 nA', '10 keV; 28 nA', '10 keV; 55 nA', '10 keV; 110 nA', '10 keV; 190 nA', '10 keV; 420 nA', '10 keV; 800 nA', '15 keV; 1 nA', '15 keV; 4 nA', '15 keV; 7.8 nA ', '15 keV; 20 nA', '15 keV; 47 nA', '15 keV; 84nA', '30 keV; UHR', '30 keV; 10 pA', '30 keV; 20 pA', '30 keV; 30 pA', '30 keV; 50 pA', '30 keV; 100 pA', '30 keV; 200 pA', '30 keV; 330 pA', '30 keV; 1.1 nA', '30 keV; 5.5 nA', '30 keV; 11 nA', '30 keV; 21 nA', '30 keV; 61 nA', '30 keV; 230 nA', '30 keV; 340 nA', '30 keV; 430 nA', '30 keV; 700 nA', '30 keV; 1.8uA', '30 keV; 2.3 uA', '30 keV; 4uA', '30 keV; 3.75uA', '30 keV; 1uA', '1 keV; 10pA', '30 keV; 3uA', '30 keV; 120 nA', '1 keV; 5nA', '5 keV; 56 nA', '500 eV; 10 pA']

def read_probeTable(probeTable):
    output_probeTable={}
    for preset in probeTable:
        print(preset)
        voltage=preset.split(';')[0]
        current=preset.split(';')[1]
        print(voltage)
        if voltage in output_probeTable.keys():
            output_probeTable[voltage].append(current)
        else:
            output_probeTable.update({voltage:[current]})
    
    
    return(output_probeTable)

def get_closest_preset(voltage,desired_current,probeTable):
    dict_probeTable=read_probeTable(probeTable)
    currents_at_voltage=dict_probeTable[str(voltage) + ' keV']
    #print(currents_at_voltage)
    difference_start = 1
    for current in currents_at_voltage:
        if current[::-1].startswith('A'):
            print(current)
            try:
                if 'uA' in current:
                    num=current.split('uA')[0]
                    #print(float(num)*1e-03)
                    curr=float(num)*1e-06
                elif 'nA' in current:
                    num=current.split('nA')[0]
                    #print(float(num)*1e03)

                    curr=float(num)*1e-09
                elif 'pA' in current:
                    num=current.split('pA')[0]
                    #print(float(num)*1)
                    curr=float(num)*1e-12
            except:
                print("this is another weird preset")
            difference=desired_current-curr
            #print(curr)
            #print(desired_current)
            #print(difference)


            if abs(difference) < abs(difference_start):
                winner=current
                difference_start=difference

    return(str(voltage) + ' keV;' + winner)
    #return(preset)
#print(read_probeTable(table))
#print(get_closest_preset(30,10,table))