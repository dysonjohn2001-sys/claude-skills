from phg.importers import playbyplay_csv, roster_csv

ROSTER_GAMECHANGER_STYLE = """Number,Name,Position,Bats,Throws,Parent Email
7,"Smith, Jake",SS/P,R,R,parent1@example.com
12,"Hernandez, Marcus",2B,L,R,parent2@example.com
21,"Brooks, Owen",CF,R,R,
"""

ROSTER_SPLIT_NAMES = """first_name,last_name,jersey,positions
Jake,Smith,7,SS
Marcus,Hernandez,12,2B
"""


def test_roster_handles_last_comma_first_and_slash_positions():
    result = roster_csv.parse(ROSTER_GAMECHANGER_STYLE)
    assert result.ok
    assert [p.last_name for p in result.players] == ["Smith", "Hernandez", "Brooks"]
    assert result.players[0].first_name == "Jake"
    assert result.players[0].positions == ["SS", "P"]
    assert result.players[0].guardians[0].email == "parent1@example.com"


def test_roster_handles_split_name_columns():
    result = roster_csv.parse(ROSTER_SPLIT_NAMES)
    assert result.ok
    assert result.players[1].jersey_number == "12"


def test_duplicate_jersey_is_an_error_not_a_warning():
    result = roster_csv.parse("name,jersey\nJake Smith,7\nOwen Brooks,7\n")
    assert not result.ok
    assert any("already used" in message for _, message in result.errors)


def test_roster_without_a_name_column_fails_clearly():
    result = roster_csv.parse("jersey,position\n7,SS\n")
    assert not result.ok
    assert "name column" in result.errors[0][1]


PLAYS_WITH_TIMESTAMPS = """Seq,Inning,Half,Timestamp,Team,Batter,Pitcher,Description,RBI
1,1,top,2026-04-18T10:05:12Z,Riverside Rays,Jake Smith,A. Jones,Jake Smith doubles to left field,1
2,1,top,2026-04-18T10:07:40Z,Riverside Rays,Marcus Hernandez,A. Jones,Marcus Hernandez strikes out swinging,0
3,1,bottom,2026-04-18T10:12:03Z,Northside Owls,B. Carter,Owen Brooks,B. Carter grounds out to Jake Smith,0
"""

PLAYS_NARRATIVE_ONLY = """inning,play
1,Jake Smith singles to right
1,Marcus Hernandez walks
2,Owen Brooks hits a home run to center
"""


def test_plays_reads_timestamps_teams_and_types():
    result = playbyplay_csv.parse(PLAYS_WITH_TIMESTAMPS, our_team_name="Riverside Rays")
    assert result.ok
    assert [p.play_type for p in result.plays] == ["double", "strikeout", "groundout"]
    assert result.plays[0].is_our_offense is True
    assert result.plays[2].is_our_offense is False
    assert result.plays[0].occurred_at is not None
    assert result.plays[0].rbi == 1


def test_fielder_is_pulled_from_the_narrative_on_defensive_plays():
    result = playbyplay_csv.parse(PLAYS_WITH_TIMESTAMPS, our_team_name="Riverside Rays")
    assert result.plays[2].putout_by == ["Jake Smith"]


def test_missing_team_column_flags_rather_than_guesses():
    result = playbyplay_csv.parse(PLAYS_NARRATIVE_ONLY)
    assert result.needs_side_mapping is True


def test_we_bat_in_resolves_the_side_without_a_team_column():
    result = playbyplay_csv.parse(PLAYS_NARRATIVE_ONLY, we_bat_in="top")
    assert result.needs_side_mapping is False
    assert all(p.is_our_offense for p in result.plays)


def test_play_types_are_classified_from_free_text():
    result = playbyplay_csv.parse(PLAYS_NARRATIVE_ONLY, we_bat_in="top")
    assert [p.play_type for p in result.plays] == ["single", "walk", "home_run"]
    assert all(p.inferred_play_type for p in result.plays)


def test_missing_timestamps_are_warned_about():
    result = playbyplay_csv.parse(PLAYS_NARRATIVE_ONLY, we_bat_in="top")
    assert any("no timestamps" in message for _, message in result.warnings)


def test_double_play_wins_over_double():
    play_type, _ = playbyplay_csv.classify("Grounds into a 6-4-3 double play")
    assert play_type == "double_play"


def test_file_without_an_inning_column_fails():
    result = playbyplay_csv.parse("play\nJake Smith singles\n")
    assert not result.ok
