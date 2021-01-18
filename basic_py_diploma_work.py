import os
import json
import requests
import time
from pprint import pprint

APP_ID = "7722809"
ACCEESS_TOKEN = os.getenv("ACCESS_TOKEN")
V = "5.126"
URL = "https://api.vk.com/method/"
INPUT_INFO = input("Who is asking info? Enter either user login or user id, please")
INPUT_TYPE = input("What type of information about the user have you just entered? Print 1 for user login and 2 for user id")

class VkontakteUser():
    def __init__(self, input_info, type_of_input):
        self.params = {"access_token": ACCEESS_TOKEN, "v": V}
        self.params['q'] = input_info
        URL_SEARCH = URL + "users.search"
        if type_of_input == "1":
            result = requests.get(URL_SEARCH, params=self.params)
            self.user_id = result.json()["response"]["items"][0]["id"]
        elif type_of_input == "2":
            self.user_id = type_of_input
        else:
            print("You have made a mistake in entering data")

    def get_user_group_ids(self):
        params = self.params
        params["user_id"] = self.user_id
        URL_GET_GROUPS = URL + "groups.get"
        groups = requests.get(URL_GET_GROUPS, params=params)
        return groups.json()["response"]["items"], groups.json()["response"]["count"]

    def get_user_friend_ids(self):
        params = self.params
        params["user_id"] = self.user_id
        URL_GET_FRIENDS = URL + "friends.get"
        friends = requests.get(URL_GET_FRIENDS, params=params)
        return friends.json()["response"]["items"]

    def user_groups_members(self, group_id):
        params = self.params
        URL_GROUP_MEMBERS = URL + "groups.getMembers"
        params["group_id"] = group_id
        params["filter"] = "friends"
        group_members = requests.get(URL_GROUP_MEMBERS, params=params)
        group_members_json = group_members.json()["response"]["items"]
        return group_members_json

    def get_group_info(self, group_id):
        params = self.params
        URL_GROUP_INFO = URL + "groups.getById"
        params["group_id"] = group_id
        params["fields"] = "members_count"
        group_info = requests.get(URL_GROUP_INFO, params=params)
        requested_group_info = {}
        requested_group_info["gid"] = group_info.json()["response"][0]["id"]
        requested_group_info["name"] = group_info.json()["response"][0]["name"]
        requested_group_info["members_count"] = group_info.json()["response"][0]["members_count"]
        return requested_group_info


if __name__ == "__main__":
    source_user = VkontakteUser(INPUT_INFO, INPUT_TYPE)
    unique_groups = []
    groups, total_number_of_groups = source_user.get_user_group_ids()
    print(f"Your groups currently are being checked on having your friends in subscribers. You will get notifiations on every checked group. In total you have {total_number_of_groups} groups to be checked.")
    for number, group in enumerate(groups):
        friends_in_group = source_user.user_groups_members(group)
        print(f"One of your groups is checked. {total_number_of_groups - number - 1} groups are on queue")
        time.sleep(0.34)
        if len(friends_in_group) == 0:
            result_group_info = source_user.get_group_info(group)
            unique_groups.append(result_group_info)

    print("The analysis is done, thank you for waiting. Unique for you groups are:")
    pprint(unique_groups)

    with open("JSON_test", "w", encoding="utf-8") as f:
    	json.dump(unique_groups, f, ensure_ascii=False, indent=2)

    print("Done")
