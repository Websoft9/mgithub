import configparser
import os


class GithubSystem:

    def get_prop(self, key):
        config = configparser.ConfigParser()
        config.read("meta/mgithub.config", encoding="utf-8")
        mgithub_item = config.items("mgithub")
        for content in mgithub_item:
            if content[0] == key:
                return content[1]
        return False

    def set_prop(self, key, value):
        config = configparser.ConfigParser()
        config.read("meta/mgithub.config")
        config.set("mgithub", key, value)
        with open("meta/mgithub.config", "w") as fw:
            config.write(fw)

