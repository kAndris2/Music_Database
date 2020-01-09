import os
import urllib.request, json 

def correct_filenames(directory, ext):

    def isweblink(item):
        search = [".com", ".co", ".info", ".net", ".org", ".me", ".us", ".biz", ".com.co", ".com.uk",
					".net.co", ".eu", ".in", ".uk", ".site", ".net16.net", ".hu", ".xxx", ".asia", ".name",
					".nom.co", ".co.uk", ".org.uk", ".me.uk", ".mx", ".com.mx", ".tw", ".com.tw", ".org.tw",
					".co.in", ".net.in", ".org.in", ".firm.in", ".gen.in", ".ind.in", ".nz", ".co.nz", ".net.nz",
					".org.nz", ".ac", ".ag", ".am", ".at", ".be", ".bz", ".cc", ".ch", ".cx", ".cz", ".de", ".fm",
					".gs", ".hn", ".io", ".jp", ".la", ".lc", ".li", ".mn", ".ms", ".nl", ".nu", ".pl", ".sc", ".sg",
					".sh", ".tk", ".tv", ".vc", ".ws", ".pm", "www.", ".mobi", ".ly", ".vg", ".cn", ".com.cn", ".net.cn",
					".org.cn", ".tc"]

        for link in search:
            if link in item:
                return True
        return False

    def check_last_char(title):
        if title[-1].isalpha() == False and title[-1] != ")":
            return True
        return False

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

    def correct(mylist, filename):
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
        search = ["x", "feat", "feat.", "Feat", "Feat.", "ft", "Featuring", "featuring", "közr", "közr."]
        for i in range(len(mylist)):
            for item in search:
                if item == mylist[i]:
                    mylist[i] = "ft."
                    
            if "(" not in mylist[i] and mylist[i] != "ft.":
                mylist[i] = mylist[i].capitalize()

        #-Aposztróf javítás----------------------------------------------------------------------------------------------
        starts = ["I", "Can", "Don", "Doesn", "Wouldn", "Couldn", "Ain", "It", "We", "They", 
                "You", "He", "She", "What", "Aren", "Didn", "Hadn", "Hasn", "Haven", "Isn",
                "Let", "Mustn", "Shan", "Shouldn", "That", "There", "Who", "Won"]
        ends = ["m", "ve", "t", "s", "re", "d", "ll"]
        index = -1
        temp = [] 

        for i in range(len(mylist)):
            temp.append(mylist[i])
            if index > -1:
                temp.pop(index)
                index = -1
            if mylist[i] in starts:
                index = i + 1
                if index < len(mylist) and mylist[index].lower() in ends:
                    for item in ends:
                        if mylist[index].lower() == item:
                            temp[index - 1] = f"{mylist[index - 1]}'{item}"
                else:
                    index = -1

        mylist = temp

        #-&-es Előadó név javítás----------------------------------------------------------------------------------------
        for i in range(len(mylist)):
            if "&" in mylist[i] and mylist[i] != "&":
                temp = mylist[i].split("&")
                for n in range(len(temp)):
                    temp[n] = temp[n].capitalize()
                mylist[i] = "&".join(temp)

        #-Kötőjeles cím javítás------------------------------------------------------------------------------------------
        if mylist.count("-") > 1:
            index = []
            for i in range(len(mylist)):
                if mylist[i] == "-":
                    mylist[i] = f"{mylist[i - 1]}-{mylist[i + 1]}"
                    index.append(i-1)
                    index.append(i+1)
                    break
            for i in range(len(index)):
                mylist.pop(index[i] - i)

        #-Kisbetűs szavak-------------------------------------------------------------------------------------------------
        newname = " ".join(mylist)
        lowercase = ["in", "of", "a", "cover)", "to", "és", "or", "by", "is", "for", "on"]
        for i in range(len(mylist)):
            if mylist[i].lower() in lowercase:
                if get_artist(newname).split(" ")[0] != mylist[i] and get_title(newname).split(" ")[0] != mylist[i]:
                    mylist[i] = mylist[i].lower()

        newname = " ".join(mylist)

        print(newname)
        #os.rename(directory + filename, directory + newname + ext)
        #print(f"Artist: {get_artist(newname)}\nTitle: {get_title(newname)}")
        #set_api(get_artist(newname), get_title(newname))

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
 
    if len(data) == 1:
        read_json(data)
    else:
        print(f"[ERROR]: Track not found! '{artist} - {title}'")

def start(link, ext):
    link = link.replace(os.sep, "/")
    link = link + "/"
    if "." not in ext:
        ext = "." + ext
    correct_filenames(link, ext)
    
start(input("Add meg a fájl(ok) elérési útvonalát: "), input("Add meg a fájl(ok) kiterjesztését: "))
#set_api("eiffel 65", "silicon world")
