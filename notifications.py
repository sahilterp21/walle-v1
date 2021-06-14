import pandas as pd

required_agent = {
    "SS": " SS is needed to respond to the situation.",
    "RE": ' Reporter is needed for the job.',
    "PO": " Police Bus needed at the spot.",
    "AM": " Please call an Ambulance.",
    "WT": " Work Truck is required at the location.",
    "FT": " Fire Truck is needed at the earliest."
}

caselets = pd.read_csv('Playtest 4 Caselets - Caselets (2).csv')

def getmessages(token, location):
    location_caselets = caselets[caselets["Grid Location"] == location.upper()]
    if token.lower() == "ss":  # data scientist
        relevant_caselets = (
                    location_caselets[location_caselets["SS"] == "X"]["Code Detail"]).to_list()
    elif token.lower() == "re":  # pio
        relevant_caselets = (
                    location_caselets[location_caselets["RE"] == "X"]["Code Detail"]).to_list()
    elif token.lower() == "wt":  # public works
        relevant_caselets = (
                    location_caselets[location_caselets["WT"] == "X"]["Code Detail"]).to_list()
    elif token.lower() == "po":  # public works
        relevant_caselets = (
                    location_caselets[location_caselets["PO"] == "X"]["Code Detail"]).to_list()
    elif token.lower() == "am":  # public health
        relevant_caselets = (
                    location_caselets[location_caselets["AM"] == "X"]["Code Detail"]).to_list()
    elif token.lower() == "ft":  # public health
        relevant_caselets = (
                    location_caselets[location_caselets["FT"] == "X"]["Code Detail"]).to_list()
    else:
        relevant_caselets = ['Token selection not valid']

    return relevant_caselets

Tokens = ["AM", "RE", "WT", "SS", "FT", "PO"]

def playermove(token, location):
    story = getmessages(token,location)
    if location.upper() not in (caselets.loc[:,"Grid Location"].dropna()).tolist():
        return "Location value is invalid"

    elif len(story) < 1:
        return "No caselets to resolve for supplied token and location combo."

    elif story[0] == "Token selection not valid":
        return "Token selection not valid"
    else:
        message = ''
        for snippet in story:
            #message += snippet
            region = (caselets[caselets["Code Detail"] == snippet]["Region"]).tolist()[0]
            caselet_category = (caselets[caselets["Code Detail"] == snippet]["Caselet Categories"]).tolist()[0]
            resident = (caselets[caselets["Code Detail"] == snippet]["Associated Resident (Residential Caselets Only)"].dropna()).tolist()
            for token in Tokens:
                if ((caselets[caselets["Code Detail"] == snippet][token]).tolist())[0] == "X":
                    if token == "FT" or token == "WT":
                        message +=  caselet_category +" emergency in the region of " + region + " due to: "+ snippet + ((". Resident affected: "+ resident[0]) if len(resident)>0 else "") +". "
                    #message += required_agent[token]
                    elif token == "AM" or token == "PO":
                        message += "Public health assistance needed in the region of "+region+" due to: "+snippet + ". "
                    elif token == "SS":
                        message += "Emergency in the region of " + region + ". " + caselet_category + " due to: " + snippet + ". "
                    elif token == "RE":
                        message += "Special report: " + caselet_category + " emergency in the region of " + region+ ". "
    return message


print(playermove('re', '11m'))

##########CODE ENDS HERE##################################











def asset_neigh_message(token, location):
    token_id = token.upper()
    ident = []
    location_identifier = caselets[caselets["Grid Location"] == location.upper()]
    rel_message = (location_identifier[location_identifier[token_id] == "X"]["Code Detail"]).to_list()
    for i in range(len(rel_message)):
        id_list = caselets[caselets["Code Detail"] == rel_message[i]]
        form_id = id_list["X"].to_list()
        ident.append(form_id[0])
    # print(ident)
    return ident



def getassetmessages(token, location):
    agnt_slct = ["AM", "RE", "WT", "SS", "FT", "PO"]
    location_caselets = caselets[caselets["Grid Location"] == location]["Description"].to_list()
    for i in range(len(agnt_slct)):
        for j in range(0, len(location_caselets)):
            testlist = caselets[caselets["Description"] == location_caselets[j]]
            test_token = (testlist[agnt_slct[i]]).to_list()
            if test_token:
                if test_token[0] == "X":
                    token_sel = agnt_slct[i].lower()
                    loc_caselets = (caselets[caselets["Asset Code"] == location]["Description"] + required_agent[
                        token_sel]).to_list()
                    return loc_caselets
            else:
                return location_caselets



def loadlocations():
    filename = "Locations.csv"
    try:
        file = open(filename, 'r')
    except:
        print('Error: file not found', filename)
        return
    try:
        fileData = file.read().split()
    except:
        print('Error: file cannot be read: ', filename)
    return fileData


def playermove_old(token, location):
    try:

            '''messagelist = getmessages(token, location)
            for i in range(len(messagelist)):
                asset_loc = asset_neigh_message(token, location)
                # print(asset_messages)
                data = {
                    "text": "Neighborhood: " + location + ". " + messagelist[i] + " Location identified as: " + asset_loc[i]
                    # asset added to role's messages
                }
                print(requests.post(token_selection[token], json.dumps(data)))
                time.sleep(1)
            # Call the API HERE <<<<<<
            othertokens = Tokens
            othertokens.remove(token)  # list of tokens not including the one that moved
            messagelist = getmessages(random.choice(othertokens), location)
            for i in range(len(messagelist)):  # --Messages for other roles
                data = {
                    "text": messagelist[i]
                }
                print(requests.post(token_selection[token], json.dumps(data)))
                time.sleep(1)
            return("Neighborhood: " + location + ". " + messagelist[i] + " Location identified as: " + asset_loc[i])'''
    except:
        return "No information available. Select another location token combination"







#print(playermove('am', '4m'))
#print((caselets.loc[:,"Grid Location"].dropna()).tolist())
#print((caselets[caselets["Code Detail"] == 'Residents Trapped']["FT"]).tolist())

