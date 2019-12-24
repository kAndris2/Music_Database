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

        #-Csak betű/zárójel-------------------------------------------------------------------------------------------
        title = " ".join(mylist)
        while check_last_char(title):
            title = title[:-1]

        mylist = title.split()

        #-Capitalize--------------------------------------------------------------------------------------------------
        for i in range(len(mylist)):
            if "feat" in mylist[i]:
                mylist[i] = "ft."
            elif "ft." in mylist[i]:
                pass
            else:
                if "(" not in mylist[i]:
                    mylist[i] = mylist[i].capitalize()

        newname = " ".join(mylist)
        print(newname)
        os.rename(directory + filename, directory + newname + ext)
        #get_music_data(newname)

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
                return item[0]
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
                return item[0]
            else:
                return item
        
        set_api(get_artist(string), get_title(string))


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

correct_filenames("D:/Gyakran hasznalt/Projectek/Codecool/Python/Proba/", ".txt")
#set_api("eiffel 65", "silicon world")