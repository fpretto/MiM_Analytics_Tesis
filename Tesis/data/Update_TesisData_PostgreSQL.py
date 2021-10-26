
from Load_PostgreSQL import PostgreSQL
import json
import psycopg2

class TesisData:
    def __init__(self, etl_data):
        self.etl_data = etl_data
        self.pgEngine = PostgreSQL(self.etl_data)
        self.execution_order = ['league_completeness', 'leagues', 'matches', 'match_stats',
                                'past_performance', 'fp_lk_player_names', 'player_ratings', 'rounds_season',
                                'standings_rounds', 'top_players', 'ABT', 'dash_ft_abt', 'dash_ft_abt_players']

    def update_tesis_data(self):
        for sql_file in self.execution_order:
            print('Executing file: ', sql_file)
            try:
                file = open(self.etl_data['queries']['path'] + self.etl_data['queries'][sql_file], 'r')
                self.pgEngine.cursor.execute(file.read())
                self.pgEngine.conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s" % error)
                self.pgEngine.conn.rollback()

if __name__ == '__main__':

    etl_data = json.load(open('data_config.json'))
    TesisData(etl_data).update_tesis_data()
