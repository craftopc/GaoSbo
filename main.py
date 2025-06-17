import requests
import json

ip = "10.50.100.10"
token = "f793c5576a4e857883d4cc0a0cfaa736"
race_id = "32c9cee6c67f7dda6d93712461071abd"


def get_questions():
    url = f"http://{ip}/api/ct/web/ai_race/race/checkpoints/robot/"
    params = {"token": token, "race_id": race_id}
    res = requests.get(url=url, params=params)
    return json.loads(res.text)


def post_flag(checkpoint_id):
    url = f"http://{ip}/api/ct/web/ai_race/race/flag/robot/"
    data = {
        "token": token,
        "checkpoint_id": checkpoint_id,
        "race_id": race_id,
        "flag": "flag{YFGlUEZ1HYAuAJTDK7Vhlh3HCMw6NDjX}",
    }
    res = requests.post(url=url, json=data)


class Data:
    def __init__(self) -> None:
        self.res: dict = get_questions()

    def get_total(self) -> int:
        return self.res["data"]["total"]

    def get_list(self) -> list:
        return self.res["data"]["list"]

    def get_list_info(self, idx):
        list = self.get_list()
        l = []
        l.append(list[idx]["resource_id"])
        l.append(list[idx]["name"])
        l.append(list[idx]["attachment"][idx]["name"])
        l.append(list[idx]["attachment"][idx]["url"])
        l.append(list[idx]["scene_addresses"][idx]["access_ip"])
        l.append(list[idx]["scene_addresses"][idx]["access_port"])
        # l.append(list[idx]["protocol"])

        return l


if __name__ == "__main__":
    res = Data()
    resource_id, name, attachment_name, attachment_url, ip, port = res.get_list_info(0)
    print(resource_id)
