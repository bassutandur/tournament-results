-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create new database tournament, drop it if already exissts
DROP DATABASE tournament;
CREATE DATABASE tournament;

-- connect to tournament database
\c tournament

--Create tables for tournament
CREATE TABLE players(player_id SERIAL primary key, player_name TEXT);

CREATE TABLE matches(match_id SERIAL primary key, winner SERIAL references players(player_id),
												loser SERIAL references players(player_id));

-- Create view for the standings
CREATE VIEW standings AS
	SELECT players.player_id,players.player_name,
	(SELECT count(matches.winner)
		FROM matches
		WHERE players.player_id = matches.winner)
		AS total_wins,
	(SELECT count(matches.match_id)
		FROM matches
		WHERE players.player_id = matches.winner
		OR players.player_id = matches.loser)
		AS total_matches
	FROM players
	ORDER BY total_wins DESC, total_matches DESC;