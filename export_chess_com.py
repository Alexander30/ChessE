#!/usr/bin/env python3

import sys
import argparse
import requests
import os
import re
import logging
import pickle



class ExportChessCom:
    def __init__(self):
        examples = f'''  {sys.argv[0]} -u alexander -t 2012/1-2021/2'''
        self.pgn_file = 'games_from_chess_com.pgn'
        self.pgn_path = os.path.join(os.path.dirname(sys.argv[0]), self.pgn_file)
        #self.logger = logging.Logger()
        logging.basicConfig(level=logging.DEBUG, filename='ExportChessCom.log')
        self._init_parser()
        self.export_games_from_endpoint()

    def _init_parser(self):
        parser = argparse.ArgumentParser(description='testing tool for exporting chess games in pgn from chess.com')
        # parser.add_argument('-d', '--download', help='Download set of games in pgn format for certain period of time')
        parser.add_argument('-u', '--user', help='Set nickname of user from chess.com. Check profile url for getting it', action='store')
        parser.add_argument('-t', '--time', help='Period of time in format: YYYY/MM-YYYY/MM', action='store')
        self.parser = parser.parse_args()

    def execute_arg(self) -> ():
        """
        TODO refactor code to use this method
        :return:
        """
        self.args = self.parser.parse_args()

    def calculate_months_and_execute(self):
        """Parse format into YYYY/MM-YYYY/MM and execute export of games for every month."""
        date_list = re.split('/|-', self.parser.time)
        start_year = int(date_list[0])
        start_month = int(date_list[1])
        end_year = int(date_list[2])
        end_month = int(date_list[3])

        for year in range(start_year, end_year + 1):        # for every year in input
            if year == start_year:
                for month in range(start_month, 13 if year != end_year else end_month + 1):                  #
                    self.download_games_for_year_and_month(year, month)
            else:
                for month in range(1, 13 if year != end_year else end_month + 1):
                    self.download_games_for_year_and_month(year, month)

    def download_games_for_year_and_month(self, year, month):
        logging.info(f'Downloading games for date: {year}/{month}')
        result = requests.get(f'https://api.chess.com/pub/player/{self.parser.user}/games/{year}/{month}/pgn')
        self.store_pgn_in_file(result.text)

    def store_pgn_in_file(self, pgn):
        """Store pgn in file"""
        logging.debug('Adding to file...')
        with open(self.pgn_path, 'a') as file:
            file.write(pgn)
            file.write('\n\n')      # Prevent corrupting pgn format for SCID import
        logging.debug('... done')

    def export_games_from_endpoint(self):
        self.calculate_months_and_execute()
        #self.store_pgn_in_file()
        pass

def main():
    """Script execution entry point: export data from chess.com"""
    print('Hi chess.com')
    ExportChessCom()

    pass

if __name__ == '__main__':
    sys.exit(main())




# TODO: make basic help
#  do downloading games for player in certain timerange

# example for request https://api.chess.com/pub/player/Alexander30/games/2009/10/pgn