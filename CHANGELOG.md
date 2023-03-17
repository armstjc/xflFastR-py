# CHANGELOG : xflFastR-py

## 0.0.1a3 - Second pass on fixing #2

- Attempted a fix on a bug where the following error was raised when installing:
  `ERROR: No matching distribution found for urllib [end of output]`

## 0.0.1a2 - First pass on fixing #2

- Attempted a fix on a bug where the following error was raised when installing:
  `ERROR: No matching distribution found for urllib [end of output]`

## 0.0.1a1 - "最初のステップ" (First Steps)

- Implemented `get_xfl_game_participation()`, a function that allows a programer to get player participation data if they have a valid XFL API token and a valid XFL API game ID.
- Implemented `get_xfl_player_box()`, a function that allows a programer to get player box score data from a XFL 3.0 game if they have a valid XFL API token and a valid XFL API game ID.
- Implemented `get_xfl_team_box()`, a function that allows a programer to get team box score data from a XFL 3.0 game if they have a valid XFL API token and a valid XFL API game ID.
- Implemented `generate_xfl_season_stats()`, a function that allows a programer to get XFL season stats for every XFL player, regardless if they have a valid XFL API token.
- Implemented `get_xfl_pbp()`, a function that allows a programer to get play-by-play data from a XFL 3.0 game if they have a valid XFL API token and a valid XFL API game ID.
- Implemented `get_xfl_rosters()`, a function that allows a programer to get the current XFL rosters if they have a valid XFL API token and a valid XFL API game ID.
- Implemented `get_xfl_standings()`, a function that allows a programer to get the current XFL standings if they have a valid XFL API token and a valid XFL API game ID.
- Implemented `get_xfl_transactions()`, a function that allows a programer to get the current list of roster transactions in a given XFL season.
