from datetime import datetime
import json
import warnings
from urllib.request import urlopen
from bs4 import BeautifulSoup

import pandas as pd
import requests
from tqdm import tqdm

#from xfl_fast_r import raise_html_status_code

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

###################################################################################################################################################################################################################
##
##      Game Participation
##
###################################################################################################################################################################################################################

def get_xfl_game_participation(xfl_api_token:str,game_id:str):
    """
    Retrives the player participation data in a given XFL 3.0 game.

    Parameters
    ----------

    xfl_api_token (str, manditory):
        A valid XFL API token. Must be valid for this function to work.
        
    game_id (str, manditory):
        The game you want all player participation data from. Must be valid for this function to work.
        
    Returns
    ----------
    
    A pandas DataFrame containing all the player participation data in a given XFL 3.0 game.
    """

    #xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    xfl_season = 2023
    #game_id = "FOOTBALL_XFL_2023_2_18_VGS@ARL"
    url = f"https://api.xfl.com/scoring/v3.30/players?game={game_id}&access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['OfficialId']
        #print(f"Player #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'OfficialID':official_id,'game_id':game_id},index=[0])
        row_df['VisOrHome'] = player['VisOrHome']
        row_df['JerseyNum'] = player['JerseyNum']
        row_df['FirstName'] = player['FirstName']
        row_df['LastName'] = player['LastName']
        row_df['LastNameSuffix'] = player['LastNameSuffix']
        row_df['Position'] = player['Position']
        row_df['PositionLongName'] = player['PositionLongName']
        row_df['NAbbrev'] = player['NAbbrev']
        row_df['Height'] = player['Height']
        row_df['Weight'] = player['Weight']
        row_df['DOB'] = player['DOB']
        row_df['POB'] = player['POB']
        
        try:
            row_df['Age'] = player['Age']
        except:
            row_df['Age'] = None

        row_df['Hometown'] = player['Hometown']
        row_df['Country'] = player['Country']
        row_df['CountryCode'] = player['CountryCode']
        row_df['Nickname'] = player['Nickname']
        row_df['InjuryStatus'] = player['InjuryStatus']
        row_df['InjuryDesc'] = player['InjuryDesc']
        try:
            row_df['GfxId'] = player['GfxId']
        except:
            row_df['GfxId'] = None

        row_df['Headshot'] = player['Headshot']
        
        try:
            row_df['IsStarting'] = player['IsStarting']
        except:
            row_df['IsStarting'] = None

        row_df['Initials'] = player['Initials']
        
        try:
            row_df['Scratch'] = player['Scratch']
        except:
            row_df['Scratch'] = None

        row_df['TrackingId'] = player['TrackingId']
        row_df['TeamId'] = player['TeamId']
        row_df['Affiliate'] = player['Affiliate']
        row_df['CloudHeadshotURL'] = player['CloudHeadshotURL']
        row_df['SquadId'] = player['SquadId']
        row_df['College'] = player['College']
        row_df['LeagueStatus'] = player['LeagueStatus']
        try:
            row_df['Participated'] = player['Participated']
        except:
            row_df['Participated'] = None
        main_df = pd.concat([main_df,row_df],ignore_index=True)

    ##main_df = main_df.replace({False:0,True:1},inplace=True)
    main_df.replace({False:0,True:1},inplace=True)
    # if save == True:
        
    #     main_df.to_csv(f'player_info/participation_data/csv/{game_id}.csv',index=False)
    #     main_df.to_parquet(f'player_info/participation_data/parquet/{game_id}.parquet',index=False)

    #     with open(f"player_info/participation_data/json/{game_id}.json", "w+") as f:
    #         f.write(json.dumps(json_data,indent=2))


    return main_df


###################################################################################################################################################################################################################
##
##      Game Stats
##
###################################################################################################################################################################################################################

def get_xfl_player_box(xfl_api_token:str,game_id:str,replace_col_names=False):
    """
    Retrives the play-by-play data in a given XFL 3.0 game.

    Parameters
    ----------

    xfl_api_token (str, manditory):
        A valid XFL API token. Must be valid for this function to work.
        
    game_id (str, manditory):
        The game you want all the play-by-play data from. Must be valid for this function to work.

    replace_col_names (bool, optional) = False:
        If ```replace_col_names = True```, the column names for XFL stats will be renamed to more conventional abreviations.
        At this time, setting ```replace_col_names = True``` will raise a NotImplementedError() exception, because the function needs further programing in order for this part of the function to work properly.
        
    Returns
    ----------
    
    A pandas DataFrame containing all the play-by-play data in a given XFL 3.0 game.
    """

    #xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    xfl_season = 2023
    #game_id = "FOOTBALL_XFL_2023_2_18_VGS@ARL"
    url = f"https://api.xfl.com/scoring/v3.30/playerstats?game={game_id}&access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['OfficialId']
        print(f"\nPlayer #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'game_id':game_id,'OfficialID':official_id},index=[0])

        ##############################################################################################################
        ## Game Participation
        ##############################################################################################################
        ## No longer needed.

        ## G        
        # row_df['G'] = 1

        # ## GS
        # try:
        #     row_df['GamesStarted'] = player['GamesStarted']
        # except:
        #     row_df['GamesStarted'] = 0

        ##############################################################################################################
        ## Passing
        ##############################################################################################################
        
        ## COMP
        try:
            row_df['PassComp'] = player['PassComp']
        except:
            row_df['PassComp'] = 0

        ## ATT
        try:
            row_df['PassAtt'] = player['PassAtt']
        except:
            row_df['PassAtt'] = 0

        ## COMP%
        try:
            row_df['PassCompPercent'] = player['PassCompPercent']
        except:
            row_df['PassCompPercent'] = 0
        
        ## PASS_YDS
        try:
            row_df['PassYards'] = player['PassYards']
        except:
            row_df['PassYards'] = 0


        ## PASS_TD
        try:
            row_df['PassTD'] = player['PassTD']
        except:
            row_df['PassTD'] = 0

        ## PASS_INT
        try:
            row_df['PassINT'] = player['PassINT']
        except:
            row_df['PassINT'] = 0

        ## 1st Downs Passing
        try:
            row_df['FirstDownsByPass'] = player['FirstDownsByPass']
        except:
            row_df['FirstDownsByPass'] = 0

        ## 1st Downs Passing Percent
        try:
            row_df['FirstDownPercentOfPasses'] = player['FirstDownPercentOfPasses']
        except:
            row_df['FirstDownPercentOfPasses'] = 0

        ## PASS_LONG
        try:
            row_df['PassYardsLong'] = player['PassYardsLong']
        except:
            row_df['PassYardsLong'] = 0

        ## PASS_LONG_TD
        try:
            row_df['PassYardsLongTD'] = player['PassYardsLongTD']
        except:
            row_df['PassYardsLongTD'] = 0

        ## PASS_YPA
        try:
            row_df['PassYardsPerAtt'] = player['PassYardsPerAtt']
        except:
            row_df['PassYardsPerAtt'] = 0

        ## PASS_YPC
        try:
            row_df['PassYardsPerComp'] = player['PassYardsPerComp']
        except:
            row_df['PassYardsPerComp'] = 0

        ## QBRating (Not NFL, Not CFB)
        try:
            row_df['QBRating'] = player['QBRating']
        except:
            row_df['QBRating'] = 0
        
        ## Sacked
        try:
            row_df['Sacked'] = player['Sacked']
        except:
            row_df['Sacked'] = 0

        ## SackedYards
        try:
            row_df['SackedYards'] = player['SackedYards']
        except:
            row_df['SackedYards'] = 0

        ## SackedYardsAvg
        try:
            row_df['SackedYardsAvg'] = player['SackedYardsAvg']
        except:
            row_df['SackedYardsAvg'] = 0

        ## Pass20YdPlays
        try:
            row_df['Pass20YdPlays'] = player['Pass20YdPlays']
        except:
            row_df['Pass20YdPlays'] = 0

        ## Pass40YdPlays
        try:
            row_df['Pass40YdPlays'] = player['Pass40YdPlays']
        except:
            row_df['Pass40YdPlays'] = 0

        ##############################################################################################################
        ## Rushing
        ##############################################################################################################
        
        ## RUSH
        try:
            row_df['RushAtt'] = player['RushAtt']
        except:
            row_df['RushAtt'] = 0
        
        ## RUSH_YDS
        try:
            row_df['RushYards'] = player['RushYards']
        except:
            row_df['RushYards'] = 0
        
        ## RUSH_AVG
        try:
            row_df['RushYardsAvg'] = player['RushYardsAvg']
        except:
            row_df['RushYardsAvg'] = 0

        ## RUSH_TD
        try:
            row_df['RushTD'] = player['RushTD']
        except:
            row_df['RushTD'] = 0
        
        ## 1st Downs Rushing
        try:
            row_df['FirstDownsByRush'] = player['FirstDownsByRush']
        except:
            row_df['FirstDownsByRush'] = 0

        ## 1st Downs Rushing Percent
        try:
            row_df['FirstDownPercentOfRushes'] = player['FirstDownPercentOfRushes']
        except:
            row_df['FirstDownPercentOfRushes'] = 0
        
        ## RUSH_LONG
        try:
            row_df['RushYardsLong'] = player['RushYardsLong']
        except:
            row_df['RushYardsLong'] = 0

        ## RUSH_LONG_TD
        try:
            row_df['RushYardsLongTD'] = player['RushYardsLongTD']
        except:
            row_df['RushYardsLongTD'] = 0

        ## Rush10YdPlays
        try:
            row_df['Rush10YdPlays'] = player['Rush10YdPlays']
        except:
            row_df['Rush10YdPlays'] = 0

        ## 1st Downs Rushing Percent
        try:
            row_df['Rush20YdPlays'] = player['Rush20YdPlays']
        except:
            row_df['Rush20YdPlays'] = 0

        ##############################################################################################################
        ## Reciving
        ##############################################################################################################

        ## REC_TARGET
        try:
            row_df['RecThrownAt'] = player['RecThrownAt']
        except:
            row_df['RecThrownAt'] = 0

        ## REC
        try:
            row_df['Recs'] = player['Recs']
        except:
            row_df['Recs'] = 0
        
        ## REC_YDS
        try:
            row_df['RecYards'] = player['RecYards']
        except:
            row_df['RecYards'] = 0
        
        ## REC_AVG
        try:
            row_df['RecYardsAvg'] = player['RecYardsAvg']
        except:
            row_df['RecYardsAvg'] = 0

        ## REC_TD
        try:
            row_df['RecTD'] = player['RecTD']
        except:
            row_df['RecTD'] = 0

        ## 1st Downs Reciving
        try:
            row_df['FirstDownsByRec'] = player['FirstDownsByRec']
        except:
            row_df['FirstDownsByRec'] = 0

        ## 1st Downs Reciving Percent
        try:
            row_df['FirstDownPercentOfRecs'] = player['FirstDownPercentOfRecs']
        except:
            row_df['FirstDownPercentOfRecs'] = 0

        ## REC_LONG
        try:
            row_df['RecYardsLong'] = player['RecYardsLong']
        except:
            row_df['RecYardsLong'] = 0

        ## REC_LONG_TD
        try:
            row_df['RecYardsLongTD'] = player['RecYardsLongTD']
        except:
            row_df['RecYardsLongTD'] = 0
        
        ## REC_YAC
        try:
            row_df['RecYardsAfterCatch'] = player['RecYardsAfterCatch']
        except:
            row_df['RecYardsAfterCatch'] = 0

        ## REC_YAC_AVG
        try:
            row_df['RecYardsAfterCatchAvg'] = player['RecYardsAfterCatchAvg']
        except:
            row_df['RecYardsAfterCatchAvg'] = 0

        ## REC_DROPS
        try:
            row_df['RecDropped'] = player['RecDropped']
        except:
            row_df['RecDropped'] = 0

        ## Rec20YdPlays
        try:
            row_df['Rec20YdPlays'] = player['Rec20YdPlays']
        except:
            row_df['Rec20YdPlays'] = 0

        ## Rec40YdPlays
        try:
            row_df['Rec40YdPlays'] = player['Rec40YdPlays']
        except:
            row_df['Rec40YdPlays'] = 0


        ##############################################################################################################
        ## Fumble Stats
        ##############################################################################################################

        ## FUMBLES
        try:
            row_df['Fumbles'] = player['Fumbles']
        except:
            row_df['Fumbles'] = 0

        ## FUMBLES_LOST
        try:
            row_df['FumblesLost'] = player['FumblesLost']
        except:
            row_df['FumblesLost'] = 0

        ## OFF_TD
        try:
            row_df['OffTD'] = player['OffTD']
        except:
            row_df['OffTD'] = 0

        ##############################################################################################################
        ## Misc. Offense
        ##############################################################################################################
        
        ## 1st Downs Total
        try:
            row_df['FirstDowns'] = player['FirstDowns']
        except:
            row_df['FirstDowns'] = 0

        ## 1st Downs Percent
        try:
            row_df['FirstDownPercent'] = player['FirstDownPercent']
        except:
            row_df['FirstDownPercent'] = 0

        ## PAT1PtAttPass
        try:
            row_df['PAT1PtAttPass'] = player['PAT1PtAttPass']
        except:
            row_df['PAT1PtAttPass'] = 0

        ## PAT1PtAttRec
        try:
            row_df['PAT1PtAttRec'] = player['PAT1PtAttRec']
        except:
            row_df['PAT1PtAttRec'] = 0

        ## PAT1PtAttRush
        try:
            row_df['PAT1PtAttRush'] = player['PAT1PtAttRush']
        except:
            row_df['PAT1PtAttRush'] = 0

        ## PAT1PtConvRush
        try:
            row_df['PAT1PtConvRush'] = player['PAT1PtConvRush']
        except:
            row_df['PAT1PtConvRush'] = 0

        ## PAT1PtPctRush
        try:
            row_df['PAT1PtPctRush'] = player['PAT1PtPctRush']
        except:
            row_df['PAT1PtPctRush'] = 0
        
        ## PAT2PtAttPass
        try:
            row_df['PAT2PtAttPass'] = player['PAT2PtAttPass']
        except:
            row_df['PAT2PtAttPass'] = 0

        ## PAT2PtAttRec
        try:
            row_df['PAT2PtAttRec'] = player['PAT2PtAttRec']
        except:
            row_df['PAT2PtAttRec'] = 0

        ## PAT2PtAttRush
        try:
            row_df['PAT2PtAttRush'] = player['PAT2PtAttRush']
        except:
            row_df['PAT2PtAttRush'] = 0

        ## PAT2PtConvRush
        try:
            row_df['PAT2PtConvRush'] = player['PAT2PtConvRush']
        except:
            row_df['PAT2PtConvRush'] = 0

        ## PAT2PtPctRush
        try:
            row_df['PAT2PtPctRush'] = player['PAT2PtPctRush']
        except:
            row_df['PAT2PtPctRush'] = 0
        
        ## PAT3PtAttPass
        try:
            row_df['PAT3PtAttPass'] = player['PAT3PtAttPass']
        except:
            row_df['PAT3PtAttPass'] = 0

        ## PAT3PtAttRec
        try:
            row_df['PAT3PtAttRec'] = player['PAT3PtAttRec']
        except:
            row_df['PAT3PtAttRec'] = 0

        ## PAT3PtAttRush
        try:
            row_df['PAT3PtAttRush'] = player['PAT3PtAttRush']
        except:
            row_df['PAT3PtAttRush'] = 0

        ## PAT3PtConvRush
        try:
            row_df['PAT3PtConvRush'] = player['PAT3PtConvRush']
        except:
            row_df['PAT3PtConvRush'] = 0

        ## PAT3PtPctRush
        try:
            row_df['PAT3PtPctRush'] = player['PAT3PtPctRush']
        except:
            row_df['PAT3PtPctRush'] = 0
        
        ## TotalTD
        try:
            row_df['TotalTD'] = player['TotalTD']
        except:
            row_df['TotalTD'] = 0

        ## TotalYards
        try:
            row_df['TotalYards'] = player['TotalYards']
        except:
            row_df['TotalYards'] = 0

        ##############################################################################################################
        ## Penalty Stats
        ##############################################################################################################

        ## PAT3PtConvRush
        try:
            row_df['Penalties'] = player['Penalties']
        except:
            row_df['Penalties'] = 0

        ## PAT3PtPctRush
        try:
            row_df['PenaltyYards'] = player['PenaltyYards']
        except:
            row_df['PenaltyYards'] = 0

        ##############################################################################################################
        ## Defensive Stats
        ##############################################################################################################

        ## TOTAL
        try:
            row_df['DefTackles'] = player['DefTackles']
        except:
            row_df['DefTackles'] = 0

        ## SOLO
        try:
            row_df['DefSoloTackles'] = player['DefSoloTackles']
        except:
            row_df['DefSoloTackles'] = 0

        ## AST
        try:
            row_df['DefAssistTackles'] = player['DefAssistTackles']
        except:
            row_df['DefAssistTackles'] = 0

        ## QB_HITS
        try:
            row_df['DefQBHits'] = player['DefQBHits']
        except:
            row_df['DefQBHits'] = 0

        ## TFL
        try:
            row_df['DefTacklesForLoss'] = player['DefTacklesForLoss']
        except:
            row_df['DefTacklesForLoss'] = 0

        ## SACKS
        try:
            row_df['DefSacks'] = player['DefSacks']
        except:
            row_df['DefSacks'] = 0
                    
        ## SACK_YDS
        try:
            row_df['DefSackYards'] = player['DefSackYards']
        except:
            row_df['DefSackYards'] = 0

        ## SACK_YDS_AVG
        try:
            row_df['DefSackYardsAvg'] = player['DefSackYardsAvg']
        except:
            row_df['DefSackYardsAvg'] = 0
                                    
        ## INT
        try:
            row_df['DefINT'] = player['DefINT']
        except:
            row_df['DefINT'] = 0

        ## INT_YDS
        try:
            row_df['DefINTReturnYards'] = player['DefINTReturnYards']
        except:
            row_df['DefINTReturnYards'] = 0

        ## INT_AVG
        try:
            row_df['DefINTReturnYardsAvg'] = player['DefINTReturnYardsAvg']
        except:
            row_df['DefINTReturnYardsAvg'] = 0
                                        
        ## INT_TD
        try:
            row_df['DefINTReturnTD'] = player['DefINTReturnTD']
        except:
            row_df['DefINTReturnTD'] = 0
        
        ## INT_LONG
        try:
            row_df['DefINTReturnYardsLong'] = player['DefINTReturnYardsLong']
        except:
            row_df['DefINTReturnYardsLong'] = 0
                              
        ## PD
        try:
            row_df['DefINTReturnYardsLong'] = player['DefINTReturnYardsLong']
        except:
            row_df['DefINTReturnYardsLong'] = 0
                              
        ## FF
        try:
            row_df['DefAssistTackles'] = player['DefAssistTackles']
        except:
            row_df['DefAssistTackles'] = 0
        
        ## FR
        try:
            row_df['DefAssistTackles'] = player['DefAssistTackles']
        except:
            row_df['DefAssistTackles'] = 0

        ##############################################################################################################
        ## Field Goal Stats
        ##############################################################################################################
        
        ## FGA
        try:
            row_df['FGAtt'] = player['FGAtt']
        except:
            row_df['FGAtt'] = 0

        ## FGM
        try:
            row_df['FGMade'] = player['FGMade']
        except:
            row_df['FGMade'] = 0

        ## FG_LONG
        try:
            row_df['FGLong'] = player['FGLong']
        except:
            row_df['FGLong'] = 0

        ## FGA_0_19
        try:
            row_df['FG0To19Att'] = player['FG0To19Att']
        except:
            row_df['FG0To19Att'] = 0

        ## FGM_0_19
        try:
            row_df['FG0To19Made'] = player['FG0To19Made']
        except:
            row_df['FG0To19Made'] = 0

        ## FGM_0_19
        try:
            row_df['FG0To19Made'] = player['FG0To19Made']
        except:
            row_df['FG0To19Made'] = 0

        ## FGA_20_29
        try:
            row_df['FG20To29Att'] = player['FG20To29Att']
        except:
            row_df['FG20To29Att'] = 0

        ## FGM_20_29
        try:
            row_df['FG20To29Made'] = player['FG20To29Made']
        except:
            row_df['FG20To29Made'] = 0
        ## FGA_30_39
        try:
            row_df['FG30To39Att'] = player['FG30To39Att']
        except:
            row_df['FG30To39Att'] = 0

        ## FGM_30_39
        try:
            row_df['FG30To39Made'] = player['FG30To39Made']
        except:
            row_df['FG30To39Made'] = 0

        ## FGA_40_49
        try:
            row_df['FG40To49Att'] = player['FG40To49Att']
        except:
            row_df['FG40To49Att'] = 0

        ## FGM_40_49
        try:
            row_df['FG40To49Made'] = player['FG40To49Made']
        except:
            row_df['FG40To49Made'] = 0

        ## FGA_50_59
        try:
            row_df['FG50PlusAtt'] = player['FG50PlusAtt']
        except:
            row_df['FG50PlusAtt'] = 0

        ## FGM_50_59
        try:
            row_df['FG50PlusMade'] = player['FG50PlusMade']
        except:
            row_df['FG50PlusMade'] = 0

        ##############################################################################################################
        ## Punting Stats
        ##############################################################################################################

        ## PUNTS
        try:
            row_df['Punts'] = player['Punts']
        except:
            row_df['Punts'] = 0

        ## GROSS_PUNT_YDS
        try:
            row_df['PuntGrossYards'] = player['PuntGrossYards']
        except:
            row_df['PuntGrossYards'] = 0

        ## GROSS_PUNT_AVG
        try:
            row_df['PuntGrossYardsAvg'] = player['PuntGrossYardsAvg']
        except:
            row_df['PuntGrossYardsAvg'] = 0

        ## GROSS_PUNT_LONG
        try:
            row_df['PuntGrossYardsLong'] = player['PuntGrossYardsLong']
        except:
            row_df['PuntGrossYardsLong'] = 0

        ## PUNT_TB
        try:
            row_df['PuntTouchbacks'] = player['PuntTouchbacks']
        except:
            row_df['PuntTouchbacks'] = 0

        ## PUNT_INSIDE_20
        try:
            row_df['PuntInside20'] = player['PuntInside20']
        except:
            row_df['PuntInside20'] = 0

        ##############################################################################################################
        ## Punt Return Stats
        ##############################################################################################################
        
        ## PR
        try:
            row_df['PuntRetReturns'] = player['PuntRetReturns']
        except:
            row_df['PuntRetReturns'] = 0

        ## PR_YDS
        try:
            row_df['PuntRetYards'] = player['PuntRetYards']
        except:
            row_df['PuntRetYards'] = 0

        ## PR_AVG
        try:
            row_df['PuntRetYardsAvg'] = player['PuntRetYardsAvg']
        except:
            row_df['PuntRetYardsAvg'] = 0

        ## PR_TD
        try:
            row_df['PuntRetTD'] = player['PuntRetTD']
        except:
            row_df['PuntRetTD'] = 0

        ## PR_LONG
        try:
            row_df['PuntRetYardsLong'] = player['PuntRetYardsLong']
        except:
            row_df['PuntRetYardsLong'] = 0

        ## PR_FC
        try:
            row_df['PuntRetFairCatches'] = player['PuntRetFairCatches']
        except:
            row_df['PuntRetFairCatches'] = 0

        ##############################################################################################################
        ## Kick Return Stats
        ##############################################################################################################
        
        ## KR
        try:
            row_df['KickRetReturns'] = player['KickRetReturns']
        except:
            row_df['KickRetReturns'] = 0

        ## KR_YDS
        try:
            row_df['KickRetYards'] = player['KickRetYards']
        except:
            row_df['KickRetYards'] = 0

        ## KR_AVG
        try:
            row_df['KickRetYardsAvg'] = player['KickRetYardsAvg']
        except:
            row_df['KickRetYardsAvg'] = 0

        ## KR_TD
        try:
            row_df['KickRetTD'] = player['KickRetTD']
        except:
            row_df['KickRetTD'] = 0

        ## KR_LONG
        try:
            row_df['KickRetYardsLong'] = player['KickRetYardsLong']
        except:
            row_df['KickRetYardsLong'] = 0

        ## 'KickRetFairCatches'
        try:
            row_df['KickRetFairCatches'] = player['KickRetFairCatches']
        except:
            row_df['KickRetFairCatches'] = 0

        main_df = pd.concat([main_df,row_df],ignore_index=True)

    try:
        #participation_df = pd.read_parquet(f'player_info/participation_data/parquet/{game_id}.parquet')
        participation_df = get_xfl_game_participation(xfl_api_token,game_id)
        participation_df = participation_df.filter(items=['Season','game_id','OfficialID','TeamId','VisOrHome','JerseyNum','FirstName','LastName','LastNameSuffix','Position','Participated','IsStarting','Scratch'])
    except:
        # return pd.DataFrame()
        raise LookupError(f'Could not get participation data for the following game:\n\t{game_id}\n')

    if len(participation_df) > 0 and len(main_df) >0:

        finished_df = pd.merge(participation_df,main_df,left_on=['Season','game_id','OfficialID'],right_on=['Season','game_id','OfficialID'],how='left')

        del participation_df,main_df

        finished_df[['Participated','IsStarting','Scratch']] = finished_df[['Participated','IsStarting','Scratch']].fillna(0)

        finished_df.loc[finished_df['PassAtt']>=1,'CFB_QBR'] = (((8.4 * finished_df['PassYards']) + (330 * finished_df['PassTD']) + (100 * finished_df['PassComp']) - (200 * finished_df['PassINT'])) / finished_df['PassAtt'])
        ##finished_df.loc[finished_df['PassAtt']>=1,'NFL_QBR'] = ((((finished_df['PassCompPercent'])*5)+()+()+())/6) * 100
        
        ## NFL Passer Rating Calculation
        finished_df['NFL_QBR_A'] = ((finished_df['PassCompPercent']) - 0.3) * 5
        finished_df['NFL_QBR_B'] = ((finished_df['PassYardsPerAtt']) - 3) * 0.25
        finished_df['NFL_QBR_C'] = (finished_df['PassTD']/finished_df['PassAtt']) * 20
        finished_df['NFL_QBR_D'] = 2.375 -(finished_df['PassINT']/finished_df['PassAtt']* 25)

        finished_df.loc[finished_df['NFL_QBR_A'] < 0, 'NFL_QBR_A'] = 0
        finished_df.loc[finished_df['NFL_QBR_A'] > 2.375, 'NFL_QBR_A'] = 2.375
        
        finished_df.loc[finished_df['NFL_QBR_B'] < 0, 'NFL_QBR_B'] = 0
        finished_df.loc[finished_df['NFL_QBR_B'] > 2.375, 'NFL_QBR_B'] = 2.375
        
        finished_df.loc[finished_df['NFL_QBR_C'] < 0, 'NFL_QBR_C'] = 0
        finished_df.loc[finished_df['NFL_QBR_C'] > 2.375, 'NFL_QBR_C'] = 2.375

        finished_df.loc[finished_df['NFL_QBR_D'] < 0, 'NFL_QBR_D'] = 0
        finished_df.loc[finished_df['NFL_QBR_D'] > 2.375, 'NFL_QBR_D'] = 2.375
        

        finished_df['NFL_QBR'] = ((finished_df['NFL_QBR_A'] + finished_df['NFL_QBR_B'] + finished_df['NFL_QBR_C'] + finished_df['NFL_QBR_D'])/6) * 100

        finished_df = finished_df.drop(columns=['NFL_QBR_A','NFL_QBR_B','NFL_QBR_C','NFL_QBR_D'])

        #print(finished_df.columns.values.tolist())
        cols = ['Season', 'game_id', 'OfficialID','TeamId', 'VisOrHome', 'JerseyNum', 'FirstName', 'LastName', 'LastNameSuffix', 'Position', 'Participated', 'IsStarting', 'Scratch',\
        'PassComp', 'PassAtt', 'PassCompPercent', 'PassYards', 'PassTD', 'PassINT', 'FirstDownsByPass', 'FirstDownPercentOfPasses', 'PassYardsLong', 'PassYardsLongTD', \
        'PassYardsPerAtt', 'PassYardsPerComp', 'QBRating', 'CFB_QBR', 'NFL_QBR', 'Sacked', 'SackedYards', 'SackedYardsAvg', 'Pass20YdPlays', 'Pass40YdPlays', \
        'RushAtt', 'RushYards', 'RushYardsAvg', 'RushTD', 'FirstDownsByRush', 'FirstDownPercentOfRushes', 'RushYardsLong', 'RushYardsLongTD', 'Rush10YdPlays', 'Rush20YdPlays', \
        'RecThrownAt', 'Recs', 'RecYards', 'RecYardsAvg', 'RecTD', 'FirstDownsByRec', 'FirstDownPercentOfRecs', 'RecYardsLong', 'RecYardsLongTD', \
        'RecYardsAfterCatch', 'RecYardsAfterCatchAvg', 'RecDropped', 'Rec20YdPlays', 'Rec40YdPlays', 'Fumbles', 'FumblesLost', 'OffTD', 'FirstDowns', 'FirstDownPercent', \
        'PAT1PtAttPass', 'PAT1PtAttRec', 'PAT1PtAttRush', 'PAT1PtConvRush', 'PAT1PtPctRush', 'PAT2PtAttPass', 'PAT2PtAttRec', 'PAT2PtAttRush', 'PAT2PtConvRush', 'PAT2PtPctRush', \
        'PAT3PtAttPass', 'PAT3PtAttRec', 'PAT3PtAttRush', 'PAT3PtConvRush', 'PAT3PtPctRush', 'TotalTD', 'TotalYards', 'Penalties', 'PenaltyYards', \
        'DefTackles', 'DefSoloTackles', 'DefAssistTackles', 'DefQBHits', 'DefTacklesForLoss', 'DefSacks', 'DefSackYards', 'DefSackYardsAvg', \
        'DefINT', 'DefINTReturnYards', 'DefINTReturnYardsAvg', 'DefINTReturnTD', 'DefINTReturnYardsLong', \
        'FGAtt', 'FGMade', 'FGLong', 'FG0To19Att', 'FG0To19Made', 'FG20To29Att', 'FG20To29Made', 'FG30To39Att', 'FG30To39Made', 'FG40To49Att', 'FG40To49Made', 'FG50PlusAtt', 'FG50PlusMade', \
        'Punts', 'PuntGrossYards', 'PuntGrossYardsAvg', 'PuntGrossYardsLong', 'PuntTouchbacks', 'PuntInside20', \
        'PuntRetReturns', 'PuntRetYards', 'PuntRetYardsAvg', 'PuntRetTD', 'PuntRetYardsLong', 'PuntRetFairCatches', \
        'KickRetReturns', 'KickRetYards', 'KickRetYardsAvg', 'KickRetTD', 'KickRetYardsLong','KickRetFairCatches']

        finished_df = finished_df[cols]

        if replace_col_names == True:
            raise NotImplementedError('At this time, get_xfl_player_box() does not currently support renaming column names.')
            print('Replacing column names.')
            finished_df = finished_df.rename(columns={'PassAtt':'ATT','PassComp':'COMP','PassCompPercent':'COMP_PCT','PassYards':'PASS_YDS','PassTD':'PASS_TD','PassINT':'PASS_INT',
                'FirstDownsByPass':'PASS_FIRST_DOWNS','PassYardsLong':'PASS_LONG','PassYardsPerAtt':'PASS_YPA','PassYardsPerComp':'PASS_YPC','Sacked':'SACKED','SackedYards':'SACKED_YDS',
                'Pass20YdPlays':'PASS_20_YDS','Pass40YdPlays':'PASS_40_YDS','RushAtt':'RUSH','RushYards':'RUSH_YDS','RushYardsAvg':'RUSH_AVG','RushTD':'RUSH_TD','FirstDownsByRush':'RUSH_FIRST_DOWNS',
                'RushYardsLong':'RUSH_LONG','Rush10YdPlays':'RUSH_10_YDS','Rush20YdPlays':'RUSH_20_YDS','RecThrownAt':'TARGETS','Recs':'REC','RecYards':'REC_YDS','RecYardsAvg':'REC_AVG',
                'RecTD':'REC_TD','FirstDownsByRec':'REC_FIRST_DOWNS','RecYardsLong':'REC_LONG','RecYardsAfterCatch':'REC_YAC','RecYardsAfterCatchAvg':'REC_YAC_AVG','Rec20YdPlays':'REC_20_YDS',
                'Rec40YdPlays':'REC_40_YDS','Fumbles':'FUMBLES','FumblesLost':'FUMBLES_LOST','FirstDowns':'FIRST_DOWNS','TotalTD':'TOTAL_TD','TotalYards':'TOTAL_YDS','DefTackles':'COMB',
                'DefSoloTackles':'SOLO','DefAssistTackles':'AST'
            })
        
        # #main_df = pd.DataFrame(data=json_data)
        # if save == True:
        #     if len(finished_df) >0:
        #         finished_df.to_csv(f'game_stats/player/raw/csv/{game_id}.csv',index=False)
        #         finished_df.to_parquet(f'game_stats/player/raw/parquet/{game_id}.parquet',index=False)

        #     with open(f"game_stats/player/raw/json/{game_id}.json", "w+") as f:
        #         f.write(json.dumps(json_data,indent=2))

        return finished_df

    else:
        #return pd.DataFrame()
        raise Exception(f'Could not parse game stats info for the following game:\n\t{game_id}\nIt could not be parsed due to a lack of stats and/or participation data.')

def get_xfl_team_box(xfl_api_token:str,game_id:str):
    """
    Retrives the team stats data in a given XFL 3.0 game.

    Parameters
    ----------

    xfl_api_token (str, manditory):
        A valid XFL API token. Must be valid for this function to work.
        
    game_id (str, manditory):
        The game you want all the team stats data from. Must be valid for this function to work.

    Returns
    ----------
    
    A pandas DataFrame containing all the team stats data in a given XFL 3.0 game.
    """

    #xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    xfl_season = 2023
    #game_id = "FOOTBALL_XFL_2023_2_18_VGS@ARL"
    url = f"https://api.xfl.com/scoring/v3.30/teamstats?game={game_id}&access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for team in tqdm(json_data):
        
        official_id = team['OfficialId']
        print(f"{game_id}\tTeamID #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'game_id':game_id,'OfficialID':official_id},index=[0])

        ###############################################################################################################################################################
        ## Team Stats
        ###############################################################################################################################################################
        try:
            row_df['PlaysPerGame'] = team['PlaysPerGame']
        except:
            row_df['PlaysPerGame'] = 0

        try:
            row_df['Points'] = team['Points']
        except:
            row_df['Points'] = 0

        try:
            row_df['DefPointsAgainst'] = team['DefPointsAgainst']
        except:
            row_df['DefPointsAgainst'] = 0

        ###############################################################################################################################################################
        try:
            row_df['YardsPerGame'] = team['YardsPerGame']
        except:
            row_df['YardsPerGame'] = 0
        
        try:
            row_df['DefYardsAgainst'] = team['DefYardsAgainst']
        except:
            row_df['DefYardsAgainst'] = 0
        
        try:
            row_df['PassYardsPerGame'] = team['PassYardsPerGame']
        except:
            row_df['PassYardsPerGame'] = 0

        try:
            row_df['DefPassYardsAgainst'] = team['DefPassYardsAgainst']
        except:
            row_df['DefPassYardsAgainst'] = 0
        try:
            row_df['RushYardsPerGame'] = team['RushYardsPerGame']
        except:
            row_df['RushYardsPerGame'] = 0

        try:
            row_df['DefRushYardsAgainst'] = team['DefRushYardsAgainst']
        except:
            row_df['DefRushYardsAgainst'] = 0

        ###############################################################################################################################################################
        ## This exists in the JSON files, but was blank for week 1
        try:
            row_df['DriveStartYardlineAvg'] = team['DriveStartYardlineAvg']
        except:
            row_df['DriveStartYardlineAvg'] = 0

        ###############################################################################################################################################################
        
        try:
            row_df['FirstDowns'] = team['FirstDowns']
        except:
            row_df['FirstDowns'] = 0

        try:
            row_df['FirstDownsByPass'] = team['FirstDownsByPass']
        except:
            row_df['FirstDownsByPass'] = 0

        try:
            row_df['FirstDownsByPenalty'] = team['FirstDownsByPenalty']
        except:
            row_df['FirstDownsByPenalty'] = 0

        try:
            row_df['FirstDownsByRush'] = team['FirstDownsByRush']
        except:
            row_df['FirstDownsByRush'] = 0

        try:
            row_df['FirstDownPercent'] = team['FirstDownPercent']
        except:
            row_df['FirstDownPercent'] = 0

        try:
            row_df['FirstDownPercentOfPasses'] = team['FirstDownPercentOfPasses']
        except:
            row_df['FirstDownPercentOfPasses'] = 0

        try:
            row_df['FirstDownPercentOfRushes'] = team['FirstDownPercentOfRushes']
        except:
            row_df['FirstDownPercentOfRushes'] = 0
            
        ###############################################################################################################################################################
        
        try:
            row_df['ThirdDownConv'] = team['ThirdDownConv']
        except:
            row_df['ThirdDownConv'] = 0

        try:
            row_df['ThirdDownAtt'] = team['ThirdDownAtt']
        except:
            row_df['ThirdDownAtt'] = 0

        try:
            row_df['ThirdDownPercent'] = team['ThirdDownPercent']
        except:
            row_df['ThirdDownPercent'] = 0
        
        ###############################################################################################################################################################
        
        try:
            row_df['FourthDownConv'] = team['FourthDownConv']
        except:
            row_df['FourthDownConv'] = 0

        try:
            row_df['FourthDownAtt'] = team['FourthDownAtt']
        except:
            row_df['FourthDownAtt'] = 0

        try:
            row_df['FourthDownPercent'] = team['FourthDownPercent']
        except:
            row_df['FourthDownPercent'] = 0

        ###############################################################################################################################################################
        try:
            row_df['Penalties'] = team['Penalties']
        except:
            row_df['Penalties'] = 0

        try:
            row_df['PenaltyYards'] = team['PenaltyYards']
        except:
            row_df['PenaltyYards'] = 0

        try:
            row_df['PenaltiesOffensive'] = team['PenaltiesOffensive']
        except:
            row_df['PenaltiesOffensive'] = 0

        try:
            row_df['PenaltyYardsOffensive'] = team['PenaltyYardsOffensive']
        except:
            row_df['PenaltyYardsOffensive'] = 0

        try:
            row_df['PenaltiesDefensive'] = team['PenaltiesDefensive']
        except:
            row_df['PenaltiesDefensive'] = 0

        try:
            row_df['PenaltyYardsDefensive'] = team['PenaltyYardsDefensive']
        except:
            row_df['PenaltyYardsDefensive'] = 0

        ###############################################################################################################################################################
        try:
            row_df['Turnovers'] = team['Turnovers']
        except:
            row_df['Turnovers'] = 0
        
        ###############################################################################################################################################################
        try:
            row_df['TotalTD'] = team['TotalTD']
        except:
            row_df['TotalTD'] = 0
        
        try:
            row_df['OffTD'] = team['OffTD']
        except:
            row_df['OffTD'] = 0

        try:
            top_seconds = team['TOPSeconds']
            top_min = top_seconds // 60
            top_seconds = top_seconds - (top_min * 60)
            row_df['TOPSeconds'] = top_seconds
            row_df['TOPStrfTime'] = f"{top_min}:{top_seconds}"
            del top_seconds, top_min
        except:
            pass
        ###############################################################################################################################################################
        ## Passing Stats
        ###############################################################################################################################################################

        try:
            row_df['PassComp'] = team['PassComp']
        except:
            row_df['PassComp'] = 0

        try:
            row_df['PassAtt'] = team['PassAtt']
        except:
            row_df['PassAtt'] = 0

        try:
            row_df['PassCompPercent'] = team['PassCompPercent']
        except:
            row_df['PassCompPercent'] = 0

        try:
            row_df['PassYards'] = team['PassYards']
        except:
            row_df['PassYards'] = 0

        try:
            row_df['PassTD'] = team['PassTD']
        except:
            row_df['PassTD'] = 0

        try:
            row_df['PassINT'] = team['PassINT']
        except:
            row_df['PassINT'] = 0
        
        try:
            row_df['PassYardsLong'] = team['PassYardsLong']
        except:
            row_df['PassYardsLong'] = 0

        try:
            row_df['PassYardsLongTD'] = team['PassYardsLongTD']
        except:
            row_df['PassYardsLongTD'] = 0

        try:
            row_df['PassYardsPerAtt'] = team['PassYardsPerAtt']
        except:
            row_df['PassYardsPerAtt'] = 0

        try:
            row_df['PassYardsPerComp'] = team['PassYardsPerComp']
        except:
            row_df['PassYardsPerComp'] = 0

        try:
            row_df['PassYardsAfterCatch'] = team['RecYardsAfterCatch']
        except:
            row_df['PassYardsAfterCatch'] = 0

        try:
            row_df['PassYardsAfterCatchAvg'] = team['RecYardsAfterCatchAvg']
        except:
            row_df['PassYardsAfterCatchAvg'] = 0

        try:
            row_df['RecDropped'] = team['RecDropped']
        except:
            row_df['RecDropped'] = 0
        
        try:
            row_df['Sacked'] = team['Sacked']
        except:
            row_df['Sacked'] = 0
        
        try:
            row_df['SackedYards'] = team['SackedYards']
        except:
            row_df['SackedYards'] = 0

        try:
            row_df['SackedYardsAvg'] = team['SackedYardsAvg']
        except:
            row_df['SackedYardsAvg'] = 0

        try:
            row_df['Pass20YdPlays'] = team['Pass20YdPlays']
        except:
            row_df['Pass20YdPlays'] = 0
        
        try:
            row_df['Pass40YdPlays'] = team['Pass40YdPlays']
        except:
            row_df['Pass40YdPlays'] = 0

        ###############################################################################################################################################################
        ## Rushing Stats
        ###############################################################################################################################################################

        try:
            row_df['RushAtt'] = team['RushAtt']
        except:
            row_df['RushAtt'] = 0

        try:
            row_df['RushTD'] = team['RushTD']
        except:
            row_df['RushTD'] = 0

        try:
            row_df['RushYards'] = team['RushYards']
        except:
            row_df['RushYards'] = 0

        try:
            row_df['RushYardsAvg'] = team['RushYardsAvg']
        except:
            row_df['RushYardsAvg'] = 0

        try:
            row_df['RushYardsLong'] = team['RushYardsLong']
        except:
            row_df['RushYardsLong'] = 0

        try:
            row_df['RushYardsLongTD'] = team['RushYardsLongTD']
        except:
            row_df['RushYardsLongTD'] = 0
        
        try:
            row_df['Rush20YdPlays'] = team['Rush20YdPlays']
        except:
            row_df['Rush20YdPlays'] = 0
        
        try:
            row_df['Rush40YdPlays'] = team['Rush40YdPlays']
        except:
            row_df['Rush40YdPlays'] = 0

        ###############################################################################################################################################################
        ## Conversion Stats
        ###############################################################################################################################################################

        try:
            row_df['PAT1PtAtt'] = team['PAT1PtAtt']
        except:
            row_df['PAT1PtAtt'] = 0
        
        try:
            row_df['PAT1PtConv'] = team['PAT1PtConv']
        except:
            row_df['PAT1PtConv'] = 0
        
        try:
            row_df['PAT1PtPct'] = team['PAT1PtPct']
        except:
            row_df['PAT1PtPct'] = 0

        ###############################################################################################################################################################
        try:
            row_df['PAT1PtAttPass'] = team['PAT1PtAttPass']
        except:
            row_df['PAT1PtAttPass'] = 0
        
        try:
            row_df['PAT1PtConvPass'] = team['PAT1PtConvPass']
        except:
            row_df['PAT1PtConvPass'] = 0
        
        try:
            row_df['PAT1PtPctPass'] = team['PAT1PtPctPass']
        except:
            row_df['PAT1PtPctPass'] = 0

        ###############################################################################################################################################################
        try:
            row_df['PAT1PtAttRush'] = team['PAT1PtAttRush']
        except:
            row_df['PAT1PtAttRush'] = 0
        
        try:
            row_df['PAT1PtConvRush'] = team['PAT1PtConvRush']
        except:
            row_df['PAT1PtConvRush'] = 0
        
        try:
            row_df['PAT1PtPctRush'] = team['PAT1PtPctRush']
        except:
            row_df['PAT1PtPctRush'] = 0

        ###############################################################################################################################################################
        try:
            row_df['PAT2PtAtt'] = team['PAT2PtAtt']
        except:
            row_df['PAT2PtAtt'] = 0
        
        try:
            row_df['PAT2PtConv'] = team['PAT2PtConv']
        except:
            row_df['PAT2PtConv'] = 0

        try:
            row_df['PAT2PtPct'] = team['PAT2PtPct']
        except:
            row_df['PAT2PtPct'] = 0

        ###############################################################################################################################################################
        try:
            row_df['PAT2PtAttPass'] = team['PAT2PtAttPass']
        except:
            row_df['PAT2PtAttPass'] = 0

        try:
            row_df['PAT2PtConvPass'] = team['PAT2PtConvPass']
        except:
            row_df['PAT2PtConvPass'] = 0
        
        try:
            row_df['PAT2PtPctPass'] = team['PAT2PtPctPass']
        except:
            row_df['PAT2PtPctPass'] = 0

        ###############################################################################################################################################################
        try:
            row_df['PAT2PtAttRush'] = team['PAT2PtAttRush']
        except:
            row_df['PAT2PtAttRush'] = 0
        
        try:
            row_df['PAT2PtConvRush'] = team['PAT2PtConvRush']
        except:
            row_df['PAT2PtConvRush'] = 0

        try:
            row_df['PAT2PtPctRush'] = team['PAT2PtPctRush']
        except:
            row_df['PAT2PtPctRush'] = 0

        ###############################################################################################################################################################
        try:
            row_df['PAT3PtAtt'] = team['PAT3PtAtt']
        except:
            row_df['PAT3PtAtt'] = 0
        
        try:
            row_df['PAT3PtConv'] = team['PAT3PtConv']
        except:
            row_df['PAT3PtConv'] = 0

        try:
            row_df['PAT3PtPct'] = team['PAT3PtPct']
        except:
            row_df['PAT3PtPct'] = 0

        ###############################################################################################################################################################
        try:
            row_df['PAT3PtConvPass'] = team['PAT3PtConvPass']
        except:
            row_df['PAT3PtConvPass'] = 0
        
        try:
            row_df['PAT3PtAttPass'] = team['PAT3PtAttPass']
        except:
            row_df['PAT3PtAttPass'] = 0

        try:
            row_df['PAT3PtPctPass'] = team['PAT3PtPctPass']
        except:
            row_df['PAT3PtPctPass'] = 0

        ###############################################################################################################################################################
        try:
            row_df['PAT3PtConvRush'] = team['PAT3PtConvRush']
        except:
            row_df['PAT3PtConvRush'] = 0
        
        try:
            row_df['PAT3PtAttRush'] = team['PAT3PtAttRush']
        except:
            row_df['PAT3PtAttRush'] = 0
        
        try:
            row_df['PAT3PtPctRush'] = team['PAT3PtPctRush']
        except:
            row_df['PAT3PtPctRush'] = 0


        ###############################################################################################################################################################
        ## Fumble Stats
        ###############################################################################################################################################################

        try:
            row_df['Fumbles'] = team['Fumbles']
        except:
            row_df['Fumbles'] = 0
        
        try:
            row_df['FumblesLost'] = team['FumblesLost']
        except:
            row_df['FumblesLost'] = 0

        ###############################################################################################################################################################
        ## Defensive Stats
        ###############################################################################################################################################################

        try:
            row_df['DefTackles'] = team['DefTackles']
        except:
            row_df['DefTackles'] = 0

        try:
            row_df['DefTacklesForLoss'] = team['DefTacklesForLoss']
        except:
            row_df['DefTacklesForLoss'] = 0
        
        try:
            row_df['DefQBHits'] = team['DefQBHits']
        except:
            row_df['DefQBHits'] = 0

        ###############################################################################################################################################################
        try:
            row_df['DefSacks'] = team['DefSacks']
        except:
            row_df['DefSacks'] = 0

        try:
            row_df['DefSackYards'] = team['DefSackYards']
        except:
            row_df['DefSackYards'] = 0
        
        try:
            row_df['DefSackYardsAvg'] = team['DefSackYardsAvg']
        except:
            row_df['DefSackYardsAvg'] = 0

        ###############################################################################################################################################################
        try:
            row_df['DefINT'] = team['DefINT']
        except:
            row_df['DefINT'] = 0
        
        try:
            row_df['DefINTReturnYards'] = team['DefINTReturnYards']
        except:
            row_df['DefINTReturnYards'] = 0
        try:
            row_df['DefINTReturnYardsAvg'] = team['DefINTReturnYardsAvg']
        except:
            row_df['DefINTReturnYardsAvg'] = 0
        
        try:
            row_df['DefINTReturnTD'] = team['DefINTReturnTD']
        except:
            row_df['DefINTReturnTD'] = 0
        
        try:
            row_df['DefINTReturnYardsLong'] = team['DefINTReturnYardsLong']
        except:
            row_df['DefINTReturnYardsLong'] = 0
        
        try:
            row_df['DefPassesDefended'] = team['DefPassesDefended']
        except:
            row_df['DefPassesDefended'] = 0

        ###############################################################################################################################################################
        try:
            row_df['DefFumblesForced'] = team['DefFumblesForced']
        except:
            row_df['DefFumblesForced'] = 0

        try:
            row_df['DefFumblesRecovered'] = team['DefFumblesRecovered']
        except:
            row_df['DefFumblesRecovered'] = 0

        ###############################################################################################################################################################
        ## Field Goal Stats
        ###############################################################################################################################################################
        
        try:
            row_df['Punts'] = team['Punts']
        except:
            row_df['Punts'] = 0
        
        try:
            row_df['PuntGrossYards'] = team['PuntGrossYards']
        except:
            row_df['PuntGrossYards'] = 0
        
        try:
            row_df['PuntGrossYardsAvg'] = team['PuntGrossYardsAvg']
        except:
            row_df['PuntGrossYardsAvg'] = 0

        try:
            row_df['PuntGrossYardsLong'] = team['PuntGrossYardsLong']
        except:
            row_df['PuntGrossYardsLong'] = 0
        
        try:
            row_df['PuntTouchbacks'] = team['PuntTouchbacks']
        except:
            row_df['PuntTouchbacks'] = 0

        try:
            row_df['PuntInside20'] = team['PuntInside20']
        except:
            row_df['PuntInside20'] = 0

        ###############################################################################################################################################################
        ## Field Goal Stats
        ###############################################################################################################################################################
        try:
            row_df['FGAtt'] = team['FGAtt']
        except:
            row_df['FGAtt'] = 0

        try:
            row_df['FGMade'] = team['FGMade']
        except:
            row_df['FGMade'] = 0
        
        try:
            row_df['FGLong'] = team['FGLong']
        except:
            row_df['FGLong'] = 0

        ###############################################################################################################################################################
        ## Kick Return Stats
        ###############################################################################################################################################################

        try:
            row_df['KickRetReturns'] = team['KickRetReturns']
        except:
            row_df['KickRetReturns'] = 0
        
        try:
            row_df['KickRetYards'] = team['KickRetYards']
        except:
            row_df['KickRetYards'] = 0
        
        try:
            row_df['KickRetYardsAvg'] = team['KickRetYardsAvg']
        except:
            row_df['KickRetYardsAvg'] = 0
        
        try:
            row_df['KickRetTD'] = team['KickRetTD']
        except:
            row_df['KickRetTD'] = 0
        
        try:
            row_df['KickRetYardsLong'] = team['KickRetYardsLong']
        except:
            row_df['KickRetYardsLong'] = 0
        
        try:
            row_df['KickRetFairCatches'] = team['KickRetFairCatches']
        except:
            row_df['KickRetFairCatches'] = 0

        ###############################################################################################################################################################
        ## Punt Return Stats
        ###############################################################################################################################################################
        
        try:
            row_df['PuntRetReturns'] = team['PuntRetReturns']
        except:
            row_df['PuntRetReturns'] = 0
        
        try:
            row_df['PuntRetYards'] = team['PuntRetYards']
        except:
            row_df['PuntRetYards'] =  None
        
        try:
            row_df['PuntRetYardsAvg'] = team['PuntRetYardsAvg']
        except:
            row_df['PuntRetYardsAvg'] = 0
        
        try:
            row_df['PuntRetTD'] = team['PuntRetTD']
        except:
            row_df['PuntRetTD'] = 0

        try:
            row_df['PuntRetYardsLong'] = team['PuntRetYardsLong']
        except:
            row_df['PuntRetYardsLong'] = 0

        try:
            row_df['PuntRetFairCatches'] = team['PuntRetFairCatches']
        except:
            row_df['PuntRetFairCatches'] = 0

        main_df = pd.concat([main_df,row_df],ignore_index=True)
        
    # if save == True:
        
    #     if len(main_df) >0:
    #         main_df.to_csv(f'game_stats/team/raw/csv/{game_id}.csv',index=False)
    #         main_df.to_parquet(f'game_stats/team/raw/parquet/{game_id}.parquet',index=False)

    #     with open(f"game_stats/team/raw/json/{game_id}.json", "w+") as f:
    #         f.write(json.dumps(json_data,indent=2))

    return main_df

###################################################################################################################################################################################################################
##
##      Season Stats
##
###################################################################################################################################################################################################################

def generate_xfl_season_stats():
    """
    Retrives the season player stats in a given XFL 3.0 season.

    Parameters
    ----------

    None

    Returns
    ----------
    
    A pandas DataFrame containing all the season player stats data in a given XFL 3.0 season.
    """

    games_df = pd.read_csv('https://raw.githubusercontent.com/armstjc/xfl-2023-data-repository/main/game_stats/player/csv/2023_xfl_player_game_stats.csv')
    games_df = games_df.fillna(0)

    finished_df = pd.DataFrame(games_df.groupby(['Season', 'OfficialID','TeamId', 'FirstName', 'LastName'],as_index=False)\
        ['Participated', 'IsStarting', 'Scratch',
         'PassComp', 'PassAtt',  'PassYards', 'PassTD', 'PassINT', 'FirstDownsByPass','Sacked', 'SackedYards','Pass20YdPlays', 'Pass40YdPlays',
         'RushAtt', 'RushYards', 'RushTD', 'FirstDownsByRush', 'RushYardsLongTD', 'Rush10YdPlays', 'Rush20YdPlays',
         'RecThrownAt', 'Recs', 'RecYards', 'RecTD', 'FirstDownsByRec', 'RecYardsAfterCatch', 'RecDropped', 'Rec20YdPlays', 'Rec40YdPlays', 
         'Fumbles', 'FumblesLost', 'OffTD', 'FirstDowns', 
         'PAT1PtAttPass', 'PAT1PtAttRec', 'PAT1PtAttRush', 'PAT1PtConvRush', 'PAT1PtPctRush', 
         'PAT2PtAttPass', 'PAT2PtAttRec', 'PAT2PtAttRush', 'PAT2PtConvRush', 'PAT2PtPctRush',
         'PAT3PtAttPass', 'PAT3PtAttRec', 'PAT3PtAttRush', 'PAT3PtConvRush', 'PAT3PtPctRush', 
         'TotalTD', 'TotalYards', 'Penalties', 'PenaltyYards',
         'DefTackles', 'DefSoloTackles', 'DefAssistTackles', 'DefQBHits', 'DefTacklesForLoss', 'DefSacks', 'DefSackYards',
         'DefINT', 'DefINTReturnYards', 'DefINTReturnTD', 
         'FGAtt', 'FGMade', 
         'FG0To19Att', 'FG0To19Made', 'FG20To29Att', 'FG20To29Made', 'FG30To39Att', 'FG30To39Made', 'FG40To49Att', 'FG40To49Made', 'FG50PlusAtt', 'FG50PlusMade',
         'Punts', 'PuntGrossYards', 'PuntGrossYardsLong', 'PuntTouchbacks', 'PuntInside20',
         'PuntRetReturns', 'PuntRetYards', 'PuntRetTD', 'PuntRetYardsLong', 'PuntRetFairCatches','KickRetReturns', 
         'KickRetYards', 'KickRetTD', 'KickRetYardsLong','KickRetFairCatches'].sum())

    finished_df.loc[finished_df['PassAtt']>=1, 'PassCompPercent'] = finished_df['PassComp'] / finished_df['PassAtt']
    finished_df.loc[finished_df['PassAtt']>=1, 'FirstDownPercentOfPasses'] = finished_df['FirstDownsByPass'] / finished_df['PassAtt']
    finished_df.loc[finished_df['PassAtt']>=1, 'PASS_YPA'] = finished_df['PassYards'] / finished_df['PassAtt']
    finished_df.loc[finished_df['PassComp']>=1, 'PASS_YPC'] = finished_df['PassYards'] / finished_df['PassComp']

    #PASS_YDS_GM
    finished_df.loc[finished_df['Participated']>=1, 'PASS_YDS_GM'] = finished_df['PassYards'] / finished_df['Participated']

    finished_df.loc[finished_df['PassAtt']>=1,'CFB_QBR'] = (((8.4 * finished_df['PassYards']) + (330 * finished_df['PassTD']) + (100 * finished_df['PassComp']) - (200 * finished_df['PassINT'])) / finished_df['PassAtt'])
    ##finished_df.loc[finished_df['PassAtt']>=1,'NFL_QBR'] = ((((finished_df['PassCompPercent'])*5)+()+()+())/6) * 100
    
    ## NFL Passer Rating Calculation
    finished_df['NFL_QBR_A'] = ((finished_df['PassCompPercent']) - 0.3) * 5
    finished_df['NFL_QBR_B'] = ((finished_df['PASS_YPA']) - 3) * 0.25
    finished_df['NFL_QBR_C'] = (finished_df['PassTD']/finished_df['PassAtt']) * 20
    finished_df['NFL_QBR_D'] = 2.375 -(finished_df['PassINT']/finished_df['PassAtt']* 25)

    finished_df.loc[finished_df['NFL_QBR_A'] < 0, 'NFL_QBR_A'] = 0
    finished_df.loc[finished_df['NFL_QBR_A'] > 2.375, 'NFL_QBR_A'] = 2.375
    
    finished_df.loc[finished_df['NFL_QBR_B'] < 0, 'NFL_QBR_B'] = 0
    finished_df.loc[finished_df['NFL_QBR_B'] > 2.375, 'NFL_QBR_B'] = 2.375
    
    finished_df.loc[finished_df['NFL_QBR_C'] < 0, 'NFL_QBR_C'] = 0
    finished_df.loc[finished_df['NFL_QBR_C'] > 2.375, 'NFL_QBR_C'] = 2.375

    finished_df.loc[finished_df['NFL_QBR_D'] < 0, 'NFL_QBR_D'] = 0
    finished_df.loc[finished_df['NFL_QBR_D'] > 2.375, 'NFL_QBR_D'] = 2.375
    

    finished_df['NFL_QBR'] = ((finished_df['NFL_QBR_A'] + finished_df['NFL_QBR_B'] + finished_df['NFL_QBR_C'] + finished_df['NFL_QBR_D'])/6) * 100

    finished_df = finished_df.drop(columns=['NFL_QBR_A','NFL_QBR_B','NFL_QBR_C','NFL_QBR_D'])

    finished_df.loc[finished_df['Sacked']>=1, 'SackedYardsAvg'] = finished_df['SackedYards'] / finished_df['Sacked']

    finished_df.loc[finished_df['PassAtt']>=1, 'SACKED%'] = finished_df['Sacked'] / (finished_df['PassAtt'] + finished_df['Sacked'])

    finished_df.loc[finished_df['RushAtt']>=1, 'RushYardsAvg'] = finished_df['RushYards'] / finished_df['RushAtt']

    finished_df.loc[finished_df['RushAtt']>=1, 'FirstDownPercentOfRushes'] = finished_df['FirstDownsByRush'] / finished_df['RushAtt']

    finished_df.loc[finished_df['Recs']>=1, 'RecYardsAvg'] = finished_df['RecYards'] / finished_df['Recs']

    finished_df.loc[finished_df['Recs']>=1, 'FirstDownPercentOfRecs'] = finished_df['FirstDownsByRec'] / finished_df['Recs']

    finished_df.loc[finished_df['RecThrownAt']>=1, 'CATCH%'] = finished_df['Recs'] / finished_df['RecThrownAt']

    finished_df.loc[finished_df['Recs']>=1, 'RecYardsAfterCatchAvg'] = finished_df['RecYardsAfterCatch'] / finished_df['Recs']

    finished_df.loc[finished_df['DefSacks']>=1, 'DefSackYardsAvg'] = finished_df['DefSackYards'] / finished_df['DefSacks']

    finished_df.loc[finished_df['DefINT']>=1, 'DefINTReturnYardsAvg'] = finished_df['DefINTReturnYards'] / finished_df['DefINT']

    finished_df.loc[finished_df['FGAtt']>=1, 'FG%'] = finished_df['FGMade'] / finished_df['FGAtt']

    finished_df.loc[finished_df['Punts']>=1, 'PuntGrossYardsAvg'] = finished_df['PuntGrossYards'] / finished_df['Punts']

    finished_df.loc[finished_df['PuntRetReturns']>=1, 'PuntRetYardsAvg'] = finished_df['PuntRetYards'] / finished_df['PuntRetReturns']

    finished_df.loc[finished_df['KickRetReturns']>=1, 'KickRetYardsAvg'] = finished_df['KickRetYards'] / finished_df['KickRetReturns']

    #finished_df = pd.merge(participation_df,main_df,left_on=['Season','game_id','OfficialID'],right_on=['Season','game_id','OfficialID'],how='left')

    max_df =  pd.DataFrame(games_df.groupby(['Season', 'OfficialID','TeamId', 'FirstName', 'LastName'],as_index=False)\
        ['PassYardsLong','RushYardsLong','RecYardsLong','DefINTReturnYardsLong','FGLong','PuntGrossYardsLong','KickRetYardsLong','PuntRetYardsLong'].max())

    finished_df = pd.merge(
        finished_df,
        max_df,
        left_on=['Season', 'OfficialID','TeamId', 'FirstName', 'LastName'],
        right_on=['Season', 'OfficialID','TeamId', 'FirstName', 'LastName'],
        how='left'
    )

    cols = ['Season', 'OfficialID','TeamId', 'FirstName', 'LastName','Participated', 'IsStarting', 'Scratch',\
        'PassComp', 'PassAtt', 'PassCompPercent', 'PassYards', 'PassTD', 'PassINT', 'FirstDownsByPass', 'FirstDownPercentOfPasses', 'PassYardsLong',\
        'PASS_YPA', 'PASS_YPC', 'PASS_YDS_GM', 'CFB_QBR', 'NFL_QBR', 'Sacked', 'SackedYards', 'SackedYardsAvg', 'Pass20YdPlays', 'Pass40YdPlays', \
        'RushAtt', 'RushYards', 'RushYardsAvg', 'RushTD', 'FirstDownsByRush', 'FirstDownPercentOfRushes', 'RushYardsLong',  'Rush10YdPlays', 'Rush20YdPlays', \
        'RecThrownAt', 'Recs', 'RecYards', 'RecYardsAvg', 'RecTD', 'FirstDownsByRec', 'FirstDownPercentOfRecs', 'RecYardsLong', \
        'RecYardsAfterCatch', 'RecYardsAfterCatchAvg', 'RecDropped', 'Rec20YdPlays', 'Rec40YdPlays', 'Fumbles', 'FumblesLost', 'OffTD', 'FirstDowns', \
        'PAT1PtAttPass', 'PAT1PtAttRec', 'PAT1PtAttRush', 'PAT1PtConvRush', 'PAT1PtPctRush', 'PAT2PtAttPass', 'PAT2PtAttRec', 'PAT2PtAttRush', 'PAT2PtConvRush', 'PAT2PtPctRush', \
        'PAT3PtAttPass', 'PAT3PtAttRec', 'PAT3PtAttRush', 'PAT3PtConvRush', 'PAT3PtPctRush', 'TotalTD', 'TotalYards', 'Penalties', 'PenaltyYards', \
        'DefTackles', 'DefSoloTackles', 'DefAssistTackles', 'DefQBHits', 'DefTacklesForLoss', 'DefSacks', 'DefSackYards', 'DefSackYardsAvg', \
        'DefINT', 'DefINTReturnYards', 'DefINTReturnYardsAvg', 'DefINTReturnTD', 'DefINTReturnYardsLong', \
        'FGAtt', 'FGMade', 'FGLong', 'FG0To19Att', 'FG0To19Made', 'FG20To29Att', 'FG20To29Made', 'FG30To39Att', 'FG30To39Made', 'FG40To49Att', 'FG40To49Made', 'FG50PlusAtt', 'FG50PlusMade', \
        'Punts', 'PuntGrossYards', 'PuntGrossYardsAvg', 'PuntGrossYardsLong', 'PuntTouchbacks', 'PuntInside20', \
        'PuntRetReturns', 'PuntRetYards', 'PuntRetYardsAvg', 'PuntRetTD', 'PuntRetYardsLong', 'PuntRetFairCatches', \
        'KickRetReturns', 'KickRetYards', 'KickRetYardsAvg', 'KickRetTD', 'KickRetYardsLong','KickRetFairCatches']

    finished_df = finished_df.reindex(columns=cols)

    # if save == True:
    #     finished_df.to_csv('game_stats/player/csv/2023_xfl_player_season_stats.csv',index=False)
    #     finished_df.to_parquet('game_stats/player/parquet/2023_xfl_player_season_stats.parquet',index=False)

    return finished_df

###################################################################################################################################################################################################################
##
##      Play-by-Play Data
##
###################################################################################################################################################################################################################

def get_xfl_pbp(xfl_api_token:str,game_id:str):
    """
    Retrives the play-by-play data in a given XFL 3.0 game.

    Parameters
    ----------

    xfl_api_token (str, manditory):
        A valid XFL API token. Must be valid for this function to work.
        
    game_id (str, manditory):
        The game you want all the play-by-play data from. Must be valid for this function to work.

    Returns
    ----------
    
    A pandas DataFrame containing all the play-by-play data in a given XFL 3.0 game.
    """
    
    # print(game_id)
    # xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()
    #timezone = pytz.timezone('US/Eastern')
    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    xfl_season = 2023
    #game_id = "FOOTBALL_XFL_2023_2_18_VGS@ARL"
    url = f"https://api.xfl.com/scoring/v3.30/markeractivity?game={game_id}&access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for play in tqdm(json_data):
        
        #official_id = player['OfficialId']
        
        row_df = pd.DataFrame({'Season':xfl_season,'game_id':game_id},index=[0])
        row_df['MarkerId'] = play['MarkerId']
        row_df['MarkerUTC'] = play['MarkerUTC']
        
        try:
            row_df['MarkerLTC'] = play['MarkerLTC']
        except:
            row_df['MarkerLTC'] = None

        # dt = datetime.fromtimestamp(play['MarkerUTC'])
        # row_df['MarkerDateTime'] = dt
        row_df['MarkerDateTime'] = datetime.fromtimestamp(play['MarkerUTC'])
        row_df['MajorType'] = play['MajorType']
        row_df['MinorType'] = play['MinorType']
        row_df['PlayDescriptor'] = play['Descriptor_']
        row_df['PlayComments'] = play['Comments']
        row_df['IsOfficial'] = play['IsOfficial']
        row_df['Quarter'] = play['ETime']['Period']

        try:
            row_df['ClockMinutes'] = play['ETime']['ClockMinutes']
        except:
            ## if it doesn't exist, it means that it is 0
            row_df['ClockMinutes'] = 0
        try:
            row_df['ClockSeconds'] = play['ETime']['ClockSeconds']
        except:
            ## if it doesn't exist, it means that it is 0
            row_df['ClockSeconds'] = 0
        row_df['SourceType'] = play['SourceType']
        row_df['EventId'] = play['EventId']
        row_df['SituationCode'] = play['SituationCode']
        row_df['SourceId'] = play['SourceId']
        row_df['SourceNativeMarkerId'] = play['SourceNativeMarkerId']
        row_df['OfficialCode'] = play['OfficialCode']
        
        try:
            row_df['TimeRemSecTotal'] = play['Properties'][0]['FootballEventContext']['TimeRemSecTotal']
        except:
            row_df['TimeRemSecTotal'] = None

        row_df['TimeRemStr'] = play['Properties'][0]['FootballEventContext']['TimeRemStr']
        
        try:
            ## if it doesn't exist, it means that it is 0
            row_df['VisTimeouts'] = play['Properties'][0]['FootballEventContext']['VisTimeouts']
        except:
            row_df['VisTimeouts'] = 0

        try:
            ## if it doesn't exist, it means that it is 0
            row_df['HomeTimeouts'] = play['Properties'][0]['FootballEventContext']['HomeTimeouts']
        except:
            row_df['HomeTimeouts'] = 0
        
            row_df['BallOn_Side'] = play['Properties'][0]['FootballEventContext']['BallOn']['VisOrHome']
        row_df['BallOn_YardNum'] = play['Properties'][0]['FootballEventContext']['BallOn']['YardNum']
        row_df['DriveNum'] = play['Properties'][0]['FootballEventContext']['DriveNum']
        row_df['PossTeam'] = play['Properties'][0]['FootballEventContext']['PossTeam']
        row_df['LastPlaySummary'] = play['Properties'][0]['FootballEventContext']['LastPlaySummary']
        row_df['LastPlayStatus'] = play['Properties'][0]['FootballEventContext']['LastPlayStatus']

        try:
            for i in play['Participants']:
                row_df[i['Role']] = i['OfficialId']
        except:
            pass

        for i in play['Properties']:
            ########################################################################################################################################################################################
            ## Timeout info (if != Null, this is the teamID for who called a timeout on this play)
            ########################################################################################################################################################################################

            try:
                row_df['FootballTimeoutTeamId'] = i['FootballTimeoutTeamId']
            except:
                pass
            
            ########################################################################################################################################################################################
            ## Down, Distance and Score
            ########################################################################################################################################################################################

            try:
                row_df['FootballStatus'] = i['FootballStatus']
            except:
                pass

            try:
                row_df['Down'] = i['FootballEventContext']['Down']
            except:
                pass
            
            try:
                row_df['Distance'] = i['FootballEventContext']['Distance']
            except:
                pass
            
            try:
                row_df['VisScore'] = i['FootballEventContext']['VisScore']
            except:
                pass

            try:
                row_df['HomeScore'] = i['HomeScore']
            except:
                pass

            ########################################################################################################################################################################################
            ## Play Result, Zone, and Yards gained/lost
            ########################################################################################################################################################################################

            try:
                row_df['FootballPlayResult'] = i['FootballPlayResult']
            except:
                pass

            try:
                row_df['FootballZone'] = i['FootballZone']
            except:
                pass
            
            try:
                row_df['FootballYards'] = i['FootballYards']
            except:
                pass


            ########################################################################################################################################################################################
            ## Drive Summary
            ########################################################################################################################################################################################

            try:
                row_df['Drive_Start_VisOrHome'] = i['FootballDriveSummary']['DriveStart']['VisOrHome']
            except:
                pass

            try:
                row_df['Drive_Start_YardNum'] = i['FootballDriveSummary']['DriveStart']['YardNum']
            except:
                pass

            try:
                row_df['Drive_Plays'] = i['FootballDriveSummary']['Plays']
            except:
                pass

            try:
                row_df['Drive_Yards'] = i['FootballDriveSummary']['Yards']
            except:
                pass

            try:
                row_df['Drive_TOP'] = i['FootballDriveSummary']['TOP']
            except:
                pass

            try:
                row_df['Result'] = i['FootballDriveSummary']['Result']
            except:
                pass

            ########################################################################################################################################################################################
            ## Scoring (on this play specifically)
            ########################################################################################################################################################################################
            
            try:
                row_df['FootballMainScoringPlay'] = i['FootballMainScoringPlay']
            except:
                pass
            
            try:
                row_df['FootballConvAttPts'] = i['FootballConvAttPts']
            except:
                pass

            try:
                row_df['FootballMiscScore_MiscScoreType'] = i['FootballMiscScore']['MiscScoreType']
            except:
                pass

            try:
                row_df['FootballMiscScore_TeamId'] = i['FootballMiscScore']['TeamId']
            except:
                pass

            try:
                row_df['FootballMiscScore_PlayerId'] = i['FootballMiscScore']['PlayerId']
            except:
                pass

            ########################################################################################################################################################################################
            ## Special Teams Yards
            ########################################################################################################################################################################################
            try:
                row_df['FootballKickYards'] = i['FootballKickYards']
            except:
                pass

            try:
                row_df['FootballPuntYards'] = i['FootballPuntYards']
            except:
                pass
          
            try:
                row_df['FootballKickRetYards'] = i['FootballKickRetYards']
            except:
                pass

            try:
                row_df['FootballPuntRetYards'] = i['FootballPuntRetYards']
            except:
                pass

            ########################################################################################################################################################################################
            ## Penalty Info
            ########################################################################################################################################################################################

            try:
                row_df['FootballPenalty_TeamId'] = i['FootballPenalty']['TeamId']
            except:
                pass

            try:
                row_df['FootballPenalty_PlayerId'] = i['FootballPenalty']['PlayerId']
            except:
                pass

            try:
                row_df['FootballPenalty_Yards'] = i['FootballPenalty']['Yards']
            except:
                pass

            try:
                row_df['FootballPenalty_PenaltyResult'] = i['FootballPenalty']['PenaltyResult']
            except:
                pass

            try:
                row_df['FootballPenalty_Description'] = i['FootballPenalty']['Description']
            except:
                pass


            ########################################################################################################################################################################################
            ## Fumble Info
            ########################################################################################################################################################################################

            try:
                row_df['FootballFumble_TeamFumbled'] = i['FootballFumble']['TeamFumbled']
            except:
                pass

            try:
                row_df['FootballFumble_PlayerFumbled'] = i['FootballFumble']['PlayerFumbled']
            except:
                pass

            try:
                row_df['FootballFumble_TeamRecovered'] = i['FootballFumble']['TeamRecovered']
            except:
                pass

            try:
                row_df['FootballFumble_PlayerRecovered'] = i['FootballFumble']['PlayerRecovered']
            except:
                pass

            try:
                row_df['FootballFumble_PlayerForcedFumble'] = i['FootballFumble']['PlayerForcedFumble']
            except:
                pass

            ########################################################################################################################################################################################
            ## Extra yards
            ########################################################################################################################################################################################

            try:
                row_df['FootballExtraYards_IndivOrTeam'] = i['FootballExtraYards']['IndivOrTeam']
            except:
                pass

            try:
                row_df['FootballExtraYards_TeamId'] = i['FootballExtraYards']['TeamId']
            except:
                pass

            try:
                row_df['FootballExtraYards_PlayerId'] = i['FootballExtraYards']['PlayerId']
            except:
                pass

            try:
                row_df['FootballExtraYards_Yards'] = i['FootballExtraYards']['Yards']
            except:
                pass

            ########################################################################################################################################################################################
            ## "Ball Set On" info (TBD on the exact purpose of this stat)
            ########################################################################################################################################################################################

            try:
                row_df['FootballSetBallOn_VisOrHome'] = i['FootballSetBallOn']['VisOrHome']
            except:
                pass

            try:
                row_df['FootballSetBallOn_YardNum'] = i['FootballSetBallOn']['YardNum']
            except:
                pass

        main_df = pd.concat([main_df,row_df],ignore_index=True)
    
    try:
        main_df = main_df.sort_values(by=['MarkerUTC'])
    except:
        print('Could not sort dataframe. This may be because [MarkerUTC] does not exist in this JSON, or the dataframe is empty.')
    
    # if save == True and len(main_df) >0:
    #     main_df.to_csv(f'pbp/single_game/csv/{game_id}.csv',index=False)
    #     main_df.to_parquet(f'pbp/single_game/parquet/{game_id}.parquet',index=False)
    #     with open(f"pbp/single_game/json/{game_id}.json", "w+") as f:
    #         f.write(json.dumps(json_data,indent=2))

    # print(main_df)

    return main_df

###################################################################################################################################################################################################################
##
##      Roster Data
##
###################################################################################################################################################################################################################

def get_xfl_rosters(xfl_api_token:str,season=2023,week=0):
    """
    Retrives the current team rosters in a given XFL 3.0 season.

    Parameters
    ----------

    xfl_api_token (str, manditory):
        A valid XFL API token. Must be valid for this function to work.
        
    season (int, optional) = 2023:
        The season you want all current rosters from. Until the XFL makes it to a second season, this should stay at 2023

    week (int, optional) = 0:
        If ```week != 0``` or ```week != None``` (null), an additional column is added to the dataframe with the inputted value in every row.

        
    Returns
    ----------
    
    A pandas DataFrame containing the current team rosters in a given XFL 3.0 season.
    """
    
    #xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    ## Yes this is bad practice, but there is nothing in their JSON
    ## files to indicate what is what.
    xfl_season = season
    xfl_week = week

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    ## This gets the rosters for all teams, rather than a specific game.
    url = f"https://api.xfl.com/scoring/v3.30/players?access_token={xfl_api_token}"
    response = urlopen(url)
    #raise_html_status_code(response.status_code)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['OfficialId']
        print(f"\nPlayer #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'OfficialID':official_id},index=[0])
        row_df['JerseyNum'] = player['JerseyNum']
        row_df['FirstName'] = player['FirstName']
        row_df['LastName'] = player['LastName']
        row_df['LastNameSuffix'] = player['LastNameSuffix']
        row_df['Position'] = player['Position']
        row_df['PositionLongName'] = player['PositionLongName']
        row_df['NAbbrev'] = player['NAbbrev']
        row_df['Height'] = player['Height']
        row_df['DOB'] = player['DOB']
        row_df['POB'] = player['POB']
        row_df['Hometown'] = player['Hometown']
        row_df['Country'] = player['Country']
        row_df['CountryCode'] = player['CountryCode']
        row_df['Nickname'] = player['Nickname']
        row_df['InjuryStatus'] = player['InjuryStatus']
        row_df['InjuryDesc'] = player['InjuryDesc']
        row_df['Headshot'] = player['Headshot']
        row_df['Initials'] = player['Initials']
        row_df['TeamId'] = player['TeamId']
        row_df['Affiliate'] = player['Affiliate']
        row_df['CloudHeadshotURL'] = player['CloudHeadshotURL']
        row_df['SquadId'] = player['SquadId']
        row_df['College'] = player['College']
        row_df['LeagueStatus'] = player['LeagueStatus']

        main_df = pd.concat([main_df,row_df],ignore_index=True)

    # if save == True:
    #     main_df.to_csv(f'rosters/{xfl_season}_xfl_roster.csv',index=False)
    #     main_df.to_parquet(f'rosters/{xfl_season}_xfl_roster.parquet',index=False)

    #     main_df['Week'] = xfl_week
    #     main_df.to_csv(f'rosters/weekly_rosters/csv/{xfl_season}_{xfl_week}_xfl_roster.csv',index=False)
    #     main_df.to_parquet(f'rosters/weekly_rosters/parquet/{xfl_season}_{xfl_week}_xfl_roster.parquet',index=False)
    #     #urlretrieve(url, filename=f"rosters/weekly_rosters/json/{xfl_season}_{xfl_week}_xfl_roster.json")
    #     with open(f"rosters/weekly_rosters/json/{xfl_season}_{xfl_week}_xfl_roster.json", "w+") as f:
    #         f.write(json.dumps(json_data,indent=2))

    if(xfl_week != 0 and xfl_week != None):
        main_df['Week'] = xfl_week

    return main_df

###################################################################################################################################################################################################################
##
##      Schedule Data
##
###################################################################################################################################################################################################################

def get_xfl_schedule(xfl_api_token:str,season=2023):
    """
    Retrives the league schedule in a given XFL 3.0 season.

    Parameters
    ----------

    xfl_api_token (str, manditory):
        A valid XFL API token. Must be valid for this function to work.
        
    season (int, optional) = 2023:
        The season you want a schedule from. Until the XFL makes it to a second season, this should stay at 2023

    Returns
    ----------
    
    A pandas DataFrame containing the league schedule in a given XFL 3.0 season.
    """

    #xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    ## Yes this is bad practice, but there is nothing in their JSON
    ## files to indicate what is what.
    xfl_season = season

    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    ## This gets the rosters for all teams, rather than a specific game.
    url = f"https://api.xfl.com/scoring/v3.30/scoreboards?access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['EventId']
        #print(f"Player #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'EventId':official_id},index=[0])
        row_df['NowUTC'] = player['NowUTC']
        row_df['NowLTC'] = player['NowLTC']
        row_df['VisitorScore'] = player['VisitorScore']
        row_df['HomeScore'] = player['HomeScore']
        row_df['Period'] = player['Period']
        row_df['ClockMinutes'] = player['ClockMinutes']
        row_df['ClockSeconds'] = player['ClockSeconds']
        row_df['ClockTenths'] = player['ClockTenths']
        row_df['ClockState'] = player['ClockState']
        row_df['VisitorTimeoutsRemaining'] = player['VisitorTimeoutsRemaining']
        row_df['HomeTimeoutsRemaining'] = player['HomeTimeoutsRemaining']
        row_df['VisitorChallengesRemaining'] = player['VisitorChallengesRemaining']
        row_df['HomeChallengesRemaining'] = player['HomeChallengesRemaining']
        #row_df['VisitorPeriodScores'] = player['VisitorPeriodScores']
        for j in range(0,len(player['VisitorPeriodScores'])):
            try:
                row_df[f'VisitorQuarterScore_{j+1}'] = player['VisitorPeriodScores'][j]
            except:
                row_df[f'VisitorQuarterScore_{j+1}'] = None

        for j in range(0,len(player['HomePeriodScores'])):
            try:
                row_df[f'HomeQuarterScore_{j+1}'] = player['HomePeriodScores'][j]
            except:
                row_df[f'HomeQuarterScore_{j+1}'] = None

        #row_df['HomePeriodScores'] = player['HomePeriodScores']
        row_df['EventStatusDetail'] = player['EventStatusDetail']
        row_df['VisitorShots'] = player['VisitorShots']
        row_df['HomeShots'] = player['HomeShots']
        row_df['EventStatus'] = player['EventStatus']
        row_df['OfficialCode'] = player['OfficialCode']
        row_df['PeriodSecondsRemaining'] = player['PeriodSecondsRemaining']
        row_df['PeriodSecondsElapsed'] = player['PeriodSecondsElapsed']
        row_df['PlayClock'] = player['PlayClock']
        row_df['PlayClockTenths'] = player['PlayClockTenths']
        row_df['BallOn'] = player['BallOn']
        row_df['Down'] = player['Down']
        row_df['Distance'] = player['Distance']
        row_df['PossTeam'] = player['PossTeam']
        row_df['DriveNum'] = player['DriveNum']

        main_df = pd.concat([main_df,row_df],ignore_index=True)

    main_df = main_df.sort_values(by=['NowUTC'])

    # if save == True:
        
    #     main_df.to_csv(f'schedule/{xfl_season}_xfl_schedule.csv',index=False)
    #     main_df.to_parquet(f'schedule/{xfl_season}_xfl_schedule.parquet',index=False)


    #     main_df.to_parquet(f'schedule/parquet/{xfl_season}_xfl_schedule.parquet',index=False)
    #     main_df.to_csv(f'schedule/csv/{xfl_season}_xfl_schedule.csv',index=False)
    #     with open(f"schedule/json/{xfl_season}_xfl_schedule.json", "w+") as f:
    #         f.write(json.dumps(json_data,indent=2))

    return main_df

###################################################################################################################################################################################################################
##
##      Standings Data
##
###################################################################################################################################################################################################################

def get_xfl_standings(xfl_api_token:str,season=2023):
    """
    Retrives the current standings in a given XFL 3.0 season.

    Parameters
    ----------

    xfl_api_token (str, manditory):
        A valid XFL API token. Must be valid for this function to work.
        
    season (int, optional) = 2023:
        The season you want standings from. Until the XFL makes it to a second season, this should stay at 2023

    Returns
    ----------
    
    A pandas DataFrame containing the current standings in a given XFL 3.0 season.
    """

    #xfl_api_token = get_xfl_api_token()
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()
    
    xfl_season = season
    #xfl_week = week
    #headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    
    url = f"https://api.xfl.com/scoring/v3.30/standings?access_token={xfl_api_token}"
    response = urlopen(url)
    json_data = json.loads(response.read())
    
    for player in tqdm(json_data):
        
        official_id = player['OfficialId']
        #print(f"Player #{official_id}")
        row_df = pd.DataFrame({'Season':xfl_season,'OfficialID':official_id},index=[0])
        row_df['Rank'] = player['Rank']
        row_df['RankInConference'] = player['RankInConference']
        row_df['RankInDivision'] = player['RankInDivision']
        row_df['GamesPlayed'] = player['GamesPlayed']
        row_df['GamesBack'] = player['GamesBack']
        row_df['ScoreDiff'] = player['ScoreDiff']
        row_df['ScoreFor'] = player['ScoreFor']
        row_df['ScoreAgainst'] = player['ScoreAgainst']
        row_df['RankInWildcard'] = player['RankInWildcard']
        row_df['Streak'] = player['Streak']
        row_df['Last10'] = player['Last10']
        row_df['ClinchIndicator'] = player['ClinchIndicator']
        row_df['ConferenceScoreFor'] = player['ConferenceScoreFor']
        row_df['ConferenceScoreAgainst'] = player['ConferenceScoreAgainst']
        row_df['DivisionScoreFor'] = player['DivisionScoreFor']
        row_df['DivisionScoreAgainst'] = player['DivisionScoreAgainst']
        row_df['City'] = player['City']
        row_df['Mascot'] = player['Mascot']
        row_df['EarnedPoints'] = player['EarnedPoints']
        row_df['Wins'] = player['Wins']
        row_df['Losses'] = player['Losses']
        row_df['Ties'] = player['Ties']
        row_df['WinPct'] = player['WinPct']
        row_df['OTWins'] = player['OTWins']
        row_df['OTLosses'] = player['OTLosses']
        row_df['OTTies'] = player['OTTies']
        row_df['ShootoutWins'] = player['ShootoutWins']
        row_df['ShootoutLosses'] = player['ShootoutLosses']
        row_df['ConferenceWins'] = player['ConferenceWins']
        row_df['ConferenceLosses'] = player['ConferenceLosses']
        row_df['ConferenceTies'] = player['ConferenceTies']
        row_df['ConferenceWinPct'] = player['ConferenceWinPct']
        row_df['DivisionWins'] = player['DivisionWins']
        row_df['DivisionLosses'] = player['DivisionLosses']
        row_df['DivisionTies'] = player['DivisionTies']
        row_df['DivisionWinPct'] = str(player['DivisionWinPct'])
        row_df['RoadEarnedPoints'] = player['RoadEarnedPoints']
        row_df['RoadWins'] = player['RoadWins']
        row_df['RoadLosses'] = player['RoadLosses']
        row_df['RoadTies'] = player['RoadTies']
        row_df['RoadWinPct'] = player['RoadWinPct']
        row_df['RoadOTWins'] = player['RoadOTWins']
        row_df['RoadOTLosses'] = player['RoadOTLosses']
        row_df['RoadOTTies'] = player['RoadOTTies']
        row_df['RoadShootoutWins'] = player['RoadShootoutWins']
        row_df['RoadShootoutLosses'] = player['RoadShootoutLosses']
        row_df['RoadConferenceWins'] = player['RoadConferenceWins']
        row_df['RoadConferenceLosses'] = player['RoadConferenceLosses']
        row_df['RoadConferenceTies'] = player['RoadConferenceTies']
        row_df['RoadConferenceWinPct'] = player['RoadConferenceWinPct']
        row_df['RoadDivisionWins'] = player['RoadDivisionWins']
        row_df['RoadDivisionLosses'] = player['RoadDivisionLosses']
        row_df['RoadDivisionTies'] = player['RoadDivisionTies']
        row_df['RoadDivisionWinPct'] = str(player['RoadDivisionWinPct'])
        row_df['HomeEarnedPoints'] = player['HomeEarnedPoints']
        row_df['HomeWins'] = player['HomeWins']
        row_df['HomeLosses'] = player['HomeLosses']
        row_df['HomeTies'] = player['HomeTies']
        row_df['HomeWinPct'] = player['HomeWinPct']
        row_df['HomeOTWins'] = player['HomeOTWins']
        row_df['HomeOTLosses'] = player['HomeOTLosses']
        row_df['HomeOTTies'] = player['HomeOTTies']
        row_df['HomeShootoutWins'] = player['HomeShootoutWins']
        row_df['HomeShootoutLosses'] = player['HomeShootoutLosses']
        row_df['HomeConferenceWins'] = player['HomeConferenceWins']
        row_df['HomeConferenceLosses'] = player['HomeConferenceLosses']
        row_df['HomeConferenceTies'] = player['HomeConferenceTies']
        row_df['HomeConferenceWinPct'] = player['HomeConferenceWinPct']
        row_df['HomeDivisionWins'] = player['HomeDivisionWins']
        row_df['HomeDivisionLosses'] = player['HomeDivisionLosses']
        row_df['HomeDivisionTies'] = player['HomeDivisionTies']
        row_df['HomeDivisionWinPct'] = str(player['HomeDivisionWinPct'])
        row_df['HockeyOTAndSOLosses'] = player['HockeyOTAndSOLosses']
        row_df['HockeyRegulationAndOTWins'] = player['HockeyRegulationAndOTWins']
        row_df['HockeyRoadOTAndSOLosses'] = player['HockeyRoadOTAndSOLosses']
        row_df['HockeyHomeOTAndSOLosses'] = player['HockeyHomeOTAndSOLosses']

        main_df = pd.concat([main_df,row_df],ignore_index=True)

    # if save == True:
        
    #     main_df.to_csv(f'standings/{xfl_season}_xfl_standings.csv',index=False)
    #     main_df.to_parquet(f'standings/{xfl_season}_xfl_standings.parquet',index=False)


    #     main_df.to_parquet(f'standings/weekly_standings/parquet/{xfl_season}_{xfl_week}_xfl_standings.parquet',index=False)
    #     main_df.to_csv(f'standings/weekly_standings/csv/{xfl_season}_{xfl_week}_xfl_standings.csv',index=False)
    #     with open(f"standings/weekly_standings/json/{xfl_season}_{xfl_week}_xfl_standings.json", "w+") as f:
    #         f.write(json.dumps(json_data,indent=2))

    return main_df

###################################################################################################################################################################################################################
##
##      Transactions Data
##
###################################################################################################################################################################################################################

def get_xfl_transactions(season=2023):
    """
    Retrives the active list of roster transactions from the XFL's website.

    Parameters
    ----------
    
    season (int, optional) = 2023:
        The season you want transactions from. Until the XFL makes it to a second season, this should stay at 2023

    Returns
    ----------
    
    A pandas DataFrame containing roster transactions in a given XFL 3.0 season.
    """
    main_df = pd.DataFrame()
    row_df = pd.DataFrame()

    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    url = f"https://www.xfl.com/xfl-transactions"
    
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,features='lxml')
    
    table_rows = soup.find_all('tr')

    for i in range(1,len(table_rows)):
        t_rows = table_rows[i]
        t_cells = t_rows.find_all('td')
        team_logo_url = t_cells[0].find('img').get('src')
        team_id = ""

        match team_logo_url:
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-st-louis-battlehawks-500x500.png":
                team_id = "STL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-st-louis-battlehawks-500x500.png":
                team_id = "STL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-houston-roughnecks-500x500.png":
                team_id = "HOU"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-houston-roughnecks-500x500.png":
                team_id = "HOU"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-orlando-guardians-500x500.png":
                team_id = "ORL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-orlando-guardians-500x500.png":
                team_id = "ORL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-orlando-guardians-500x500.png.png":
                team_id = "ORL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-orlando-guardians-500x500.png":
                team_id = "SEA"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-seattle-sea-dragons-500x500.png":
                team_id = "SEA"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-vegas-vipers-500x500.png":
                team_id = "VGS"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-vegas-vipers-500x500.png":
                team_id = "VGS"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555935/xfl-prod/logos/logo-vegas-vipers-500x500.png":
                team_id = "VGS"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-arlington-renegades-500x500.png":
                team_id = "ARL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-arlington-renegades-500x500.png":
                team_id = "ARL"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-dc-defenders-500x500.png":
                team_id = "DC"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-dc-defenders-500x500.png":
                team_id = "DC"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100/v1671555934/xfl-prod/logos/logo-san-antonio-brahmas-500x500.png":
                team_id = "SA"
            case "https://res.cloudinary.com/xfl-production/image/upload/c_thumb,w_100,g_face/v1671555934/xfl-prod/logos/logo-san-antonio-brahmas-500x500.png":
                team_id = "SA"
            case _:
                raise ValueError(f'Unhandled Team abreviation: {team_logo_url}')
        
        row_df = pd.DataFrame(columns=['season','team_id','team_logo_url'],data=[[season,team_id,team_logo_url]])
        row_df['date'] = t_cells[1].text
        row_df['player_name'] = t_cells[2].text
        row_df['player_position'] = t_cells[3].text
        row_df['transaction_type'] = t_cells[4].text
        main_df = pd.concat([main_df,row_df],ignore_index=True)

    # print(main_df)
    # if save == True:
    #     main_df.to_csv(f'player_info/transactions/{season}_xfl_transactions.csv',index=False)

    return main_df


if __name__ == "__main__":
    key = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI2M2YyNzM4ZTkyNWEwZjViMjFhMWExNjgiLCJ1bmlxdWVfbmFtZSI6InhmbHdlYnVzZXIiLCJyb2xlIjpbIlhGTFBST0QiLCJQVUJMSUMiLCJYRkxVU0VSIiwiWEZMREVWIiwiWEZMUFJPRCIsIlNDT1JJTkdfUFVTSCIsIlNDT1JJTkdfUkVTVCIsIlhGTFRFU1QiXSwibmJmIjoxNjc5MDQ4MjgyLCJleHAiOjE2NzkzMDc0ODIsImlhdCI6MTY3OTA0ODI4Mn0.4JWPFgWinF5LLZSk9PfoK8QZoBL_93xVFjKwAFckKtemAjjaGz1BLRUtuIMwVlfw3ebFhDWZ4HAHkUYkaV-KcA" ## "firefox" is a placeholder for a valid XFL API key
    game_id = "FOOTBALL_XFL_2023_2_18_ORL@HOU"

    print(get_xfl_game_participation(key,game_id))
    print(get_xfl_player_box(key,game_id))
    print(get_xfl_team_box(key,game_id))
    print(generate_xfl_season_stats())
    print(get_xfl_pbp(key,game_id))
    print(get_xfl_rosters(key))
    print(get_xfl_schedule(key))
    print(get_xfl_standings(key))
    print(get_xfl_transactions())