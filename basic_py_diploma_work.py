import requests
import time
from pprint import pprint
import os

app_id = "7722809"
access_token = os.getenv("access_token")
v = "5.126"
URL = "https://api.vk.com/method/"
input_info = input("Who is asking info? Enter either user login or user id, please")
type_of_input = input("What type of information about the user have you just entered? Print 1 for user login and 2 for user id")


class vk_user():
    def __init__(self, input_info, type_of_input):
        self.params = {"access_token": access_token, "v": v}
        self.params['q'] = input_info
        URL_search = URL + "users.search"
        if type_of_input == "1":
            result = requests.get(URL_search, params=self.params)
            self.user_id = result.json()["response"]["items"][0]["id"]
        elif type_of_input == "2":
            self.user_id = input_info
        else:
            print("You have made a mistake in entering data")

    def get_user_group_ids(self):
        params = self.params
        params["user_id"] = self.user_id
        URL_get_groups = URL + "groups.get"
        groups = requests.get(URL_get_groups, params=params)
        return groups.json()["response"]["items"], groups.json()["response"]["count"]

    def get_user_friend_ids(self):
        params = self.params
        params["user_id"] = self.user_id
        URL_get_friends = URL + "friends.get"
        friends = requests.get(URL_get_friends, params=params)
        return friends.json()["response"]["items"]

    def user_groups_members(self, group_id):
        params = self.params
        URL_get_group_members = URL + "groups.getMembers"
        params["group_id"] = group_id
        params["filter"] = "friends"
        group_members = requests.get(URL_get_group_members, params=params)
        group_members_json = group_members.json()["response"]["items"]
        return group_members_json

    def get_group_info(self, group_id):
        params = self.params
        URL_get_group_info = URL + "groups.getById"
        params["group_id"] = group_id
        params["fields"] = "members_count"
        group_info = requests.get(URL_get_group_info, params=params)
        requested_group_info = {}
        requested_group_info["gid"] = group_info.json()["response"][0]["id"]
        requested_group_info["name"] = group_info.json()["response"][0]["name"]
        requested_group_info["members_count"] = group_info.json()["response"][0]["members_count"]
        return requested_group_info


if __name__ == "__main__":
    source_user = vk_user(input_info, type_of_input)
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
