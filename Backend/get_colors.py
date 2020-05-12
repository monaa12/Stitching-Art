import math
import pandas as pd

def distanceFromColor(idx,r,g,b,df):
    tr=df.loc[idx]['r']
    tg=df.loc[idx]['g']
    tb=df.loc[idx]['b']
    
    baseDistance = ((r - tr) * (r - tr)) + ((g - tg) * (g - tg)) + ((b - tb) * (b - tb))
    distance = math.sqrt(baseDistance)
    return distance



def matchDMC(redval,greenval,blueval,df):
    distanceList=[]
    
    for idx in range(len(df)):        #elmafroud dmccolourlist da ykon el df bt3na bas sbtha zy ma howa katbo for now
        candidateDist=distanceFromColor(idx,redval,greenval,blueval,df)
        distanceList.append([candidateDist,idx])
            
    distanceList.sort()  #sorting the list in ascending order
    
    #get the values that are closest to RGB value
    dmcl=df.loc[distanceList[0][1]]['floss'] #dmc_code
    dmcR=df.loc[distanceList[0][1]]['r']
    dmcG=df.loc[distanceList[0][1]]['g']
    dmcB=df.loc[distanceList[0][1]]['b']
    dmcH=df.loc[distanceList[0][1]]['hex']
    
    return dmcl,dmcR,dmcG,dmcB,dmcH






def get_colors(image,number_of_colors,show_chart,df):
    
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    plt.imshow(modified_image)
    plt.show()
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    #print(rgb_colors)
    ##########################################
    dmc_colors_code = []
    dmc_colors_hex_labels= []
    for i in range(len(hex_colors)):
        tr=rgb_colors[i][0]
        tg=rgb_colors[i][1]
        tb=rgb_colors[i][2]
        dmcs_code,dmc_r,dmc_g,dmc_b,dmc_h = matchDMC(tr,tg,tb,df)
        dmc_colors_code.append(dmcs_code)
        dmc_colors_hex_labels.append("#"+ dmc_h)    
    print(dmc_colors_hex_labels)
    print(dmc_colors_code)
    
    #########################################
    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
        
        #dmc_pie_chart
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = dmc_colors_code, colors = dmc_colors_hex_labels)
        
