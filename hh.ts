def getEmailForInstagramInfluencers():

    instagram_links = [
        "https://www.instagram.com/shalsc?igsh=MWp2ajR0MW9jdndkOA==",
        "https://www.instagram.com/suhanasethiofficial?igsh=MzFsMnBhZTEzYmxn",
        "https://www.instagram.com/arushi.mehra_/",
    ]
    # db = firestore.client()
    # redirectRef = db.collection("redirectUsers")
    # influencersRef = db.collection("influencers")
    instagram_usernames = [link.split("/")[3].split("?")[0] for link in instagram_links]

    print(len(instagram_usernames))

    i = 0

    finalData = [("INSTAGRAM", "EMAIL", "FIRST NAME")]

    for username in instagram_usernames:

        # query = redirectRef.where("username", "==", username)
        # #query = influencersRef.where("influencer", "==", username)

        # docs = query.get()


        # for doc in docs:
        # 	print(username)
        # 	i += 1
        # 	doc_data = doc.to_dict()
        # 	if doc_data["isFollowing"] == True:
        # 		print(doc_data)

        print(f"username: {username}")



        # url = "https://instagram-scraper-2022.p.rapidapi.com/ig/info_username/"
        # url = "https://instagram-scraper-api2.p.rapidapi.com/v1/info"
        url = "https://social-api4.p.rapidapi.com/v1/info"

        # querystring = {"user": username}
        querystring = {"username_or_id_or_url": username}

        # headers = {
        #     "X-RapidAPI-Key": "e84044d9c8mshbbf48b6d2898864p102cfbjsnd2d19beee4cf",
        #     "X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com"
        # }

        # headers = {
        #     "x-rapidapi-key": "8d9b2d89afmsh7d8003d305f3ac8p161af0jsne9eb87477123",
        #     "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
        # }

        headers = {
	        "x-rapidapi-key": "8d9b2d89afmsh7d8003d305f3ac8p161af0jsne9eb87477123",
	        "x-rapidapi-host": "social-api4.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        statusCode = response.status_code
        print(statusCode)
        # print(data)

        # if statusCode == 200 and "user" in data:
        if statusCode == 200 and "data" in data:
            publicEmail = ""
            publicPhone = ""

        #     if "public_email" in data["user"]:
        #         publicEmail = data["user"]["public_email"]

        #     if "public_phone_number" in data["user"]:
        #         publicPhone = data["user"]["public_phone_number"]

        #     finalData.append((username, publicEmail, publicPhone))
        #     print("Username: " + username + " Email: " + publicEmail + " Phone: " + publicPhone)

        # else:
        #     print("Failed: " + username)
            
            if "public_email" in data["data"]:
                publicEmail = data["data"]["public_email"]

            if "public_phone_number" in data["data"]:
                publicPhone = data["data"]["public_phone_number"]

            finalData.append((username, publicEmail, username))
            print("Username: " + username + " Email: " + publicEmail + " Phone: " + publicPhone)
            print()

        else:
            print("Failed: " + username)

    with open("shubham_durex_june11.csv", 'w') as csvfile:
    # with open("shubham_comedy_may29.csv", 'w') as csvfile:
    # with open("plix_may_8.csv", 'w') as csvfile:
    # with open("plix_march_chic_regional_similar_2.csv", 'w') as csvfile:
    # with open("plix_march_chic_regional_3.csv", 'w') as csvfile:
    # with open("plix_gaon_may_1.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(finalData)
    
    print('--------------------------------------------')