import abc
import json
import pandas as pd


class Parser(object):
    """Abstract class for data parsing to exact attributes (fields)"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, fields):
        self.fields = fields
        self.fields_set = set(fields)

    def parse_process(self, scrapped_file, table_file):
        data = self.parse(scrapped_file)
        self.save_data(table_file, data)

    def save_data(self, table_file, players):
        playersDF = pd.DataFrame.from_dict(players)
        playersDF.to_csv(table_file)

    @abc.abstractmethod
    def parse(self, scrapped_file):
        """
        Override this method for fields extraction from data
        :param data: data can be in any appropriate format
        (text, json or other)
        :return: list of dictionaries where key is
        one of defined fields and value is this field's value
        """

        matches = json.load(open(scrapped_file))
        parsed_player_data = []
        for match in matches:
            for player in match["participants"]:
                achievment = "UNRANKED"
                if ("highestAchievedSeasonTier" in player):
                    achievment = player["highestAchievedSeasonTier"]

                firstTower = False
                if "firstTowerAssist" in player["stats"]:
                    firstTower = player["stats"]["firstTowerAssist"]
                parsed_player_data.append({
                    "name": match["participantIdentities"][player["participantId"]-1]["player"]["summonerName"],
                    "achievment": achievment,
                    "teamId": player["teamId"],
                    "win": player["stats"]["win"],
                    "kills": player["stats"]["kills"],
                    "deaths": player["stats"]["deaths"],
                    "assists": player["stats"]["assists"],
                    "turrets": player["stats"]["turretKills"],
                    "firstBlood": player["stats"]["firstBloodKill"],
                    "firstTower": firstTower,
                    "item0": player["stats"]["item0"],
                    "item1": player["stats"]["item1"],
                    "item2": player["stats"]["item2"],
                    "item3": player["stats"]["item3"],
                    "item4": player["stats"]["item4"],
                    "item5": player["stats"]["item5"],
                    "item6": player["stats"]["item6"]
                })
        return parsed_player_data
