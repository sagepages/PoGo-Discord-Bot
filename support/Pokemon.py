import pandas as pd
import numpy as np

GREAT_LEAGUE = 15009.9
ULTRA_LEAGUE = 25009.9

pd.set_option('display.float_format', lambda x: '%.3f' % x)

pokemon_stats = pd.read_excel('excel/pokestats.xlsx')
iv_combinations = pd.read_excel('excel/ivPer.xlsx')
cp_multiplier = pd.read_excel('excel/Multiplier.xlsx')
       
pokemon_stats.columns = ['Pokemon', 'Base Attack', 'Base Defense', 'Base Stamina']
pokemon_stats = pokemon_stats.set_index('Pokemon', drop=True)

iv_combinations.columns = ['Attack', 'Defense', 'Stamina']

cp_multiplier.columns = ['CPM', 'Level']


class Pokemon(object):

    def __init__(self, name, attack, defense, stamina):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.stamina = stamina
        self.pokemon_stats = pokemon_stats
        self.iv_combinations = iv_combinations
        self.cp_multiplier = cp_multiplier


    
    def get_selected_info(self):
        
        att_Stat = self.pokemon_stats.loc[self.name, 'Base Attack']
        def_Stat = self.pokemon_stats.loc[self.name, 'Base Defense']
        sta_Stat = self.pokemon_stats.loc[self.name, 'Base Stamina']

        self.iv_combinations['Total Attack'] = att_Stat + self.iv_combinations['Attack']
        self.iv_combinations['Total Defense'] = def_Stat + self.iv_combinations['Defense']
        self.iv_combinations['Total Stamina'] = sta_Stat + self.iv_combinations['Stamina']


    def find_nearest_level_great(self):

        att_column = self.iv_combinations['Total Attack']
        def_column_squared = self.iv_combinations['Total Defense'] ** (0.5)
        sta_column_squared = self.iv_combinations['Total Stamina'] ** (0.5)

        self.iv_combinations['CPM'] = (GREAT_LEAGUE / (att_column * def_column_squared * sta_column_squared)) ** 0.5

        self.iv_combinations = pd.merge_asof(self.iv_combinations.sort_values(['CPM']), cp_multiplier, on='CPM')
        self.iv_combinations = self.iv_combinations.rename(columns={'CPM': 'Approx. CPM'})
    
    def find_nearest_level_ultra(self):

        att_column = self.iv_combinations['Total Attack']
        def_column_squared = self.iv_combinations['Total Defense'] ** (0.5)
        sta_column_squared = self.iv_combinations['Total Stamina'] ** (0.5)

        self.iv_combinations['CPM'] = (ULTRA_LEAGUE / (att_column * def_column_squared * sta_column_squared)) ** 0.5

        self.iv_combinations = pd.merge_asof(self.iv_combinations.sort_values(['CPM']), self.cp_multiplier, on='CPM')
        self.iv_combinations = self.iv_combinations.rename(columns={'CPM': 'Approx. CPM'})

    def find_nearest_cpm(self):

        level_column = self.iv_combinations['Level']
        level_index_column = np.searchsorted(self.cp_multiplier['Level'], level_column)
        cpm_column = self.cp_multiplier['CPM'].iloc[level_index_column]
        cpm_column = cpm_column.reset_index(drop=True)
        self.iv_combinations['Absolute CPM'] = cpm_column

    

    def find_statproduct(self):

        self.iv_combinations['Stat Product Attack'] = self.iv_combinations['Total Attack'] * self.iv_combinations['Absolute CPM']
        self.iv_combinations['Stat Product Defense'] = self.iv_combinations['Total Defense'] * self.iv_combinations['Absolute CPM']
        self.iv_combinations['Stat Product Stamina'] = (self.iv_combinations['Total Stamina'] * self.iv_combinations['Absolute CPM']).astype(int)
        self.iv_combinations['Stat Product'] = (self.iv_combinations['Stat Product Attack'] * 
                                                self.iv_combinations['Stat Product Defense'] * 
                                                self.iv_combinations['Stat Product Stamina'])

        attack = self.iv_combinations['Total Attack']
        defense = self.iv_combinations['Total Defense']
        stamina = self.iv_combinations['Total Stamina']
        CPM = self.iv_combinations['Absolute CPM']

        self.iv_combinations['CP'] = (attack * (defense ** (1/2)) * (stamina **(1/2)) * (CPM ** 2)) / 10

        
    def sortby_statproduct(self):

        self.iv_combinations= self.iv_combinations.sort_values('Stat Product', ascending=False)
        self.iv_combinations = self.iv_combinations.reset_index(drop=True)
    
    def find_user_choice_rank(self):

        self.user_choice_rank = self.iv_combinations[
            (self.iv_combinations['Attack'] == self.attack) & 
            (self.iv_combinations['Defense'] == self.defense) & 
            (self.iv_combinations['Stamina'] == self.stamina)]
        self.rank = sum(self.user_choice_rank.index.values) + 1
        self.level = (self.user_choice_rank['Level'].loc[self.rank - 1]).astype(float)
        self.CP = (self.user_choice_rank['CP'].loc[self.rank - 1]).astype(int)

