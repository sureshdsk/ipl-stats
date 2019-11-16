import pandas as pd
import numpy as np


class IplStats:
    def __init__(self):
        self.matches = self.deliveries = None

        self.__load_dataset()


    def __load_dataset(self):
        balls = pd.read_csv('data/deliveries.csv')
        self.matches = pd.read_csv('data/matches.csv').drop('umpire3', axis=1)
        self.balls = balls.merge(self.matches, left_on='match_id', right_on='id')

    def get_all_seasons(self):
        seasons = self.matches['season'].unique()
        seasons.sort()
        return seasons

    def _get_chosen_season(self, ipl_year):
        return self.matches[self.matches.season == ipl_year]

    def top_successful_teams(self, season, top_x_teams=4):
        return self.matches[self.matches.season == season].winner.value_counts().nlargest(top_x_teams)

    def most_toss_wins(self, season):
        return self.matches[self.matches.season == season].toss_winner.value_counts().nlargest(1)

    def most_man_of_the_match(self, season):
        return self.matches[self.matches.season == season].player_of_match.value_counts().nlargest(1)

    def toss_win_batting(self, season):
        season = self.matches[self.matches.season == season]
        winner = season['toss_winner'] == season['winner']
        return round(winner.groupby(winner).size() / winner.count() * 100, 2)

    def won_by_highest_margin(self, ipl_year):
        season = self._get_chosen_season(ipl_year)
        return season[self.matches['win_by_runs'] > 0].groupby(['winner'])['win_by_runs'].apply(np.median).sort_values(ascending=False).nlargest(1)

    def location_hosted_max_matches(self, season):
        return self.matches[self.matches.season == season].groupby(['venue'])['id'].count().sort_values(ascending=False).nlargest(1)

    def toss_winner_match_winner(self, ipl_year):
        _matches = self._get_chosen_season(ipl_year)
        ss = _matches['toss_winner'] == _matches['winner']
        return ss.groupby(ss).count()

    def top_team_wins_by_location(self, ipl_year):
        season = self._get_chosen_season(ipl_year)
        top_team = dict(self.top_successful_teams(ipl_year, 1).items())
        top_team_name = next(iter(top_team))
        season = season[season.winner == top_team_name]
        return season.groupby(['winner', 'venue'])['id'].count().sort_values(
            ascending=False).nlargest(1)
