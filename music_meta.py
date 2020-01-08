import os
import urllib.request, json 

def correct_filenames(directory, ext):

    def isweblink(item):
        search = [".hu", ".cz", ".pm", ".com", ".ru", ".net", ".org", "www."]
        for link in search:
            if link in item:
                return True
        return False

    def check_last_char(title):
        if title[-1].isalpha() == False and title[-1] != ")":
            return True
        return False

    def correct(mylist, filename):
        """
        def correct_next(table, index, items):
            print(table)
            for item in items:
                if index + 1 != len(table):
                    if table[index + 1].lower() == item:
                        table[index] = f"{table[index]}'{item}"
            #table.pop(index + 1)
            return table
        """

        #-Kiterjesztés levegás-----------------------------------------------------------------------------------------
        mylist[-1] = mylist[-1][:-4]
        
        #-Kötőjel javítás----------------------------------------------------------------------------------------------
        for x, item in enumerate(mylist):
            new_item = ""
            if "-" in item and item != "-":
                for i in range(len(item)):
                    if item[i] != "-":
                        new_item += item[i]
                    else:
                        new_item += " - "
                    mylist[x] = new_item

        mylist = " ".join(mylist).split()

        #-Zárójel igazítás----------------------------------------------------------------------------------------------
        for x, item in enumerate(mylist):
            if "(" in item:
                new_item = ""
                for i in range(len(item)):
                    try:
                        if item[i] == "(" and item[i-1] != " ":
                            new_item += " ("
                        elif item[i-1] == "(" and item[i].islower():
                            new_item += item[i].upper()
                        else:
                            new_item += item[i]
                    except IndexError:
                        print(f"IndexError: '({item[i]})'")
                    mylist[x] = new_item

        mylist = " ".join(mylist).split()

        #-Link törlés--------------------------------------------------------------------------------------------------
        if isweblink(mylist[-1]):
            mylist.pop(-1)

        #-Csak betű/zárójel az utolsó karakter-------------------------------------------------------------------------
        title = " ".join(mylist)
        while check_last_char(title):
            title = title[:-1]

        mylist = title.split()

        #-Capitalize/ft.-----------------------------------------------------------------------------------------------
        search = ["x", "feat", "feat.", "Feat", "Feat.", "ft"]
        # Fel lehet tölteni olyan szavakkal amiket kisbetűsen akarunk
        lowercase = []
        for i in range(len(mylist)):
            for item in search:
                if item == mylist[i]:
                    mylist[i] = "ft."
                    
            if mylist[i] in lowercase:
                mylist[i] = mylist[i].lower()
            elif "(" not in mylist[i] and mylist[i] != "ft.":
                mylist[i] = mylist[i].capitalize()

        #-------------------------------------------------------------------------------------------------------------
        starts = ["I", "Can", "Don", "Doesn", "Wouldn", "Couldn", "Ain", "It", "We", "They", 
                "You", "He", "She", "What", "Aren", "Didn", "Hadn", "Hasn", "Haven", "Isn",
                "Let", "Mustn", "Shan", "Shouldn", "That", "There", "Who", "Won"]
        ends = ["m", "ve", "t", "s", "re", "d", "ll"]
        index = -1
        check = False
        temp = mylist

        for i in range(len(mylist)):
            if mylist[i] in starts:
                if index > -1:
                    temp.pop(index)
                index = i + 1
                if index < len(mylist) and mylist[index].lower in ends:
                    for item in ends:
                        if mylist[index].lower() == item:
                            temp[index - 1] = f"{mylist[index - 1]}'{item}"
                else:
                    index = -1

        #----------------------------------------------------------------------------------------------------------------
        for i in range(len(mylist)):
            if "&" in mylist[i] and mylist[i] != "&":
                temp = mylist[i].split("&")
                for n in range(len(temp)):
                    temp[n] = temp[n].capitalize()
                mylist[i] = "&".join(temp)

        newname = " ".join(mylist)

        print(newname)
        #os.rename(directory + filename, directory + newname + ext)
        get_music_data(newname)

    def get_music_data(string):

        def get_artist(string):
            item = ""
            for i in range(len(string)):
                if string[i] != "-":
                    item += string[i]
                else:
                    item = item[:-1]
                    break

            if "ft." in item:
                item = item.split("ft.")
                return item[0][:-1]
            else:
                return item

        def get_title(string):
            item = ""
            check = False
            for i in range(len(string)):
                if check == True and string[i-1] != "-":
                    item += string[i]
                if string[i] == "-" and string[i+1] == " ":
                    check = True
            
            if "(" in item:
                item = item.split("(")
                return item[0][:-1]
            elif "ft." in item:
                temp = item.split("ft.")
                return temp[0]
            else:
                return item
        
        #print(f"Artist: {get_artist(string)}\nTitle: {get_title(string)}")
        #set_api(get_artist(string), get_title(string))

    for filename in os.listdir(directory):
        if filename.endswith(ext):
            if "_" in filename:
                correct(filename.split("_"), filename)
            else:
                correct(filename.split(" "), filename)

        elif os.path.isdir(directory + filename):
            correct_filenames(directory + filename + "/", ext)

def read_json(mydict):
    for key in mydict:
        if type(mydict[key]) == dict:
            print(f"\n[{key.upper()}]")
            read_json(mydict[key])
        else:
            print(f"{key} : {mydict[key]}")

def set_api(artist, title):
    artist2 = "%20".join(artist.split())
    title2 = "%20".join(title.split())

    api_key = "2f2e1e1617be192a1320a2422b6dcf3b"
    link = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&artist={artist2}&track={title2}&format=json"
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
 
    try:
        if len(data) == 1:
            read_json(data)
        else:
            print(f"Track not found! '{artist} - {title}'")
    except:
        pass

#correct_filenames("C:/Users/andri/Desktop/Codecool/Pyton/Proba/", ".txt")
correct_filenames("E:/Zenék/", ".mp3")
#set_api("eiffel 65", "silicon world")
