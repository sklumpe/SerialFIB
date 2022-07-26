def readProbeTable(path):
    import xml.etree.ElementTree as ET

    tree = ET.parse(path)

    root = tree.getroot()

    print(root.tag)

    # for i in root:
    #     for j in i:
    #         #print(j.tag)
    #         if j.tag=='ProbeTableEntry':
    #             for k in j:
    #                 print(k)

    for tableEntry in root.iter('KVTableEntry'):
        #print(tableEntry.find('Label').text)
        #print(tableEntry.find('Current').text)
        #print(tableEntry.find('Width').text)
        if float(tableEntry.find('KV').text)==30000:


            KVIndex=tableEntry.get('Index')

    dict={}
    for tableEntry in root.iter('ProbeTableEntry'):
        if tableEntry.find('KVIndex').text==KVIndex:
            
            label=tableEntry.find('Label').text
            current=tableEntry.find('Current').text
            diameter=tableEntry.find('Width').text

            dict.update({current:{'name':label,'diameter':diameter,'current':current}})

    return(dict)


def getProbe(defined_current,probe_table):
    dict=readProbeTable(probe_table)
    value=float(defined_current)
    import numpy as np
    diffs=np.zeros(len(dict))
    counter=0
    for i in dict:
        
        diff=value-float(i)
        diff=np.sqrt(diff**2)
        if counter==0:
            label=i
            counter=counter+1
            diff_old=diff
            counter=counter+1
        else:
            if diff_old < diff:
                continue
            elif diff_old > diff:
                label=i
                print(label)

                counter=counter+1
                diff_old=diff
    return(dict[label])



#print(getProbe(1e-09))

 