import pandas as pd

def wrangle(path):
    temp = pd.read_csv(path)
    dataframe = (temp.
             loc[temp["date"] < '2021-08-12'].
             drop(columns = ['playoff', 'neutral', 'season', 'date']).
             reset_index().
             drop(columns = ['index'])
)
    return dataframe


def initial_correct(path):
    temp = pd.read_csv(path)
    df = (temp.
             loc[temp["date"] < '2021-08-12'].
             drop(columns = ['playoff', 'neutral', 'season']).
             reset_index().
             drop(columns = ['index'])
         )
    correct1 = df.loc[((df['elo_prob1'] > df['elo_prob2']) & (df['score1'] > df['score2']))]
    correct2 = df.loc[((df['elo_prob1'] < df['elo_prob2']) & (df['score1'] < df['score2']))]
    correct_combine = [correct1, correct2]
    initial_correct = pd.concat(correct_combine).sort_values(by=['date']).reset_index()
    return initial_correct


def pitcher_correct(path):
    temp = pd.read_csv(path)
    df = (temp.
             loc[temp["date"] < '2021-08-12'].
             drop(columns = ['playoff', 'neutral', 'season']).
             reset_index().
             drop(columns = ['index'])
         )
    temp1 = df.loc[((df['rating_prob1'] > df['rating_prob2']) & (df['score1'] > df['score2']))]    
    temp2 = df.loc[((df['rating_prob1'] < df['rating_prob2']) & (df['score1'] < df['score2']))]
    correct_combine = [temp1, temp2]
    pitcher_correct = pd.concat(correct_combine).sort_values(by=['date']).reset_index().drop(columns = ['pitcher1_rgs', 'pitcher2_rgs'])
    return pitcher_correct


def only_pitcher(path):
    temp = pd.read_csv(path)
    df = (temp.
             loc[temp["date"] < '2021-08-12'].
             drop(columns = ['playoff', 'neutral', 'season']).
             reset_index().
             drop(columns = ['index'])
         )
    check1 = df.loc[((df['pitcher1_rgs'] < df['pitcher2_rgs']) & (df['score1'] < df['score2']))]   
    check2 = df.loc[((df['pitcher1_rgs'] > df['pitcher2_rgs']) & (df['score1'] > df['score2']))]
    correct_combine = [check1, check2]
    pitcher_correct = pd.concat(correct_combine).sort_values(by=['date']).reset_index().drop(columns = ['pitcher1_rgs', 'pitcher2_rgs'])
    return pitcher_correct



def daily_correct(path):
    temp = pd.read_csv(path)
    df = (temp.
             loc[temp["date"] < '2021-08-12'].
             drop(columns = ['playoff', 'neutral', 'season']).
             reset_index().
             drop(columns = ['index'])
         )
    temp1 = df.loc[((df['rating_prob1'] > df['rating_prob2']) & (df['score1'] > df['score2']))]    
    temp2 = df.loc[((df['rating_prob1'] < df['rating_prob2']) & (df['score1'] < df['score2']))]
    correct_combine = [temp1, temp2]
    pitcher_correct = pd.concat(correct_combine).sort_values(by=['date']).reset_index().drop(columns = ['pitcher1_rgs', 'pitcher2_rgs'])
   
    dates = pitcher_correct['date'].unique()
    counts = pitcher_correct['date'].value_counts()
    daily = pd.DataFrame(counts)
    daily = (daily.
                reset_index().
                sort_values(by=['index']).
                rename(columns = {'date' : 'Correct Guesses'}).
                rename(columns = {'index':'Date',}).
                sort_values(by=['Date'])
           )
    daily = (daily.
             rename(columns = {'date' : 'Correct Guesses'}).
             rename(columns = {'index':'Date',}).
             sort_values(by=['Date']).
             reset_index().
             drop(columns=['index'])
            )
    return daily



def find_team(path, team_name):
    temp = pd.read_csv(path)
    df = (temp.
             loc[temp["date"] < '2021-08-12'].
             drop(columns = ['playoff', 'neutral', 'season']).
             reset_index().
             drop(columns = ['index'])
         )
          
    team_1 = df.loc[df['team1'] == team_name]
    team1 = team_1.rename(columns={'team1':'team', 'rating1_post':'rating'})
    team_2 = df.loc[df['team2'] == team_name]
    team2 = team_2.rename(columns={'team2':'team', 'rating2_post':'rating'})
                 
    home = team1[['date', 'team', 'rating']]
    away = team2[['date', 'team', 'rating']]
    team = pd.concat([home, away])
    team = team.sort_values(by=['date']).reset_index().drop(columns=['index'])
    team['date'] = pd.to_datetime(team['date'])

    return team



def correct(path):
    temp = pd.read_csv(path)
    df = (temp.
             loc[temp["date"] < '2021-08-12'].
             drop(columns = ['playoff', 'neutral', 'season']).
             reset_index().
             drop(columns = ['index'])
)
    temp1 = df.loc[((df['rating_prob1'] > df['rating_prob2']) & (df['score1'] > df['score2']))]    
    temp2 = df.loc[((df['rating_prob1'] < df['rating_prob2']) & (df['score1'] < df['score2']))]
    correct_adj = pd.concat([temp1, temp2])
    dates = correct_adj['date'].unique()
    dicc = correct_adj['date'].value_counts()
    data = pd.DataFrame(dicc)
    data = data.reset_index()
    data.sort_values(by=['index'])
    right = data.rename(columns = {'date' : 'Correct Guesses'})
    right = right.rename(columns = {'index':'Date',})
    right = right.sort_values(by=['Date'])
    right = right.reset_index()
    right = right.drop(columns=['index'])
    right['Date'] = pd.to_datetime(right['Date'])
    
    return right


def find_pitcher(path, pitcher):
    df = pd.read_csv(path)
    dataframe = (df.
             loc[df["date"] < '2021-07-13'].
             drop(columns = ['playoff', 'neutral', 'season']).
             reset_index().
             drop(columns = ['index'])
)
    temp1 = df.loc[df['pitcher1'] == pitcher]
    temp2 = df.loc[df['pitcher2'] == pitcher]
    
    sep1 = temp1[['date', 'pitcher1', 'pitcher1_rgs']]
    sep1 = sep1.rename(columns={'pitcher1':'pitcher', 'pitcher1_rgs':'rating'})
    sep2 = temp2[['date', 'pitcher2', 'pitcher2_rgs']]
    sep2 = sep2.rename(columns={'pitcher2':'pitcher', 'pitcher2_rgs':'rating'})
    
    sep = pd.concat([sep1, sep2])
    sep = sep.sort_values(by=['date']).reset_index().drop(columns=['index'])
    sep['date'] = pd.to_datetime(sep['date'])
    
    return sep