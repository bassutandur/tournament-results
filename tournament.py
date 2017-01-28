#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
	"""Connect to the PostgreSQL database.  Returns a database connection."""
	return psycopg2.connect("dbname=tournament")


def deleteMatches():
	"""Remove all the match records from the database."""
	delete_query = "DELETE FROM matches;"
	db_conn = connect()
	curosr = db_conn.cursor()
	curosr.execute(delete_query)
	db_conn.commit()
	db_conn.close()

def deletePlayers():
	"""Remove all the player records from the database."""
	delete_query = "DELETE FROM players;"
	db_conn = connect()
	cursor = db_conn.cursor()
	cursor.execute(delete_query)
	db_conn.commit()
	db_conn.close()

def countPlayers():
	"""Returns the number of players currently registered."""
	count_query = "SELECT count(*) AS count from players;"
	db_conn = connect()
	curosr = db_conn.cursor()
	curosr.execute(count_query)
	count = curosr.fetchone()
	db_conn.close()
	return count[0]

def registerPlayer(name):
	"""Adds a player to the tournament database.
  
	The database assigns a unique serial id number for the player.  (This
	should be handled by your SQL database schema, not in your Python code.)
  
	Args:
	  name: the player's full name (need not be unique).
	"""
	register_query = ("INSERT INTO players (player_name) VALUES (%s);")
	db_conn = connect()
	cursor = db_conn.cursor()
	cursor.execute(register_query, (name,))
	db_conn.commit()
	db_conn.close()

def playerStandings():
	"""Returns a list of the players and their win records, sorted by wins.

	The first entry in the list should be the player in first place, or a player
	tied for first place if there is currently a tie.

	Returns:
	  A list of tuples, each of which contains (id, name, wins, matches):
		id: the player's unique id (assigned by the database)
		name: the player's full name (as registered)
		wins: the number of matches the player has won
		matches: the number of matches the player has played
	"""
	standings_query = "SELECT * from standings;"
	db_conn = connect()
	cursor = db_conn.cursor()
	cursor.execute(standings_query)
	players_details = cursor.fetchall()
	db_conn.close()
	return players_details

def reportMatch(winner, loser):
	"""Records the outcome of a single match between two players.

	Args:
	  winner:  the id number of the player who won
	  loser:  the id number of the player who lost
	"""
	report_query = ("INSERT INTO matches (winner, loser) values(%s, %s);")
	db_conn = connect()
	cursor = db_conn.cursor()
	cursor.execute(report_query, (winner, loser, ))
	db_conn.commit()
	db_conn.close()

def swissPairings():
	"""Returns a list of pairs of players for the next round of a match.

	Assuming that there are an even number of players registered, each player
	appears exactly once in the pairings.  Each player is paired with another
	player with an equal or nearly-equal win record, that is, a player adjacent
	to him or her in the standings.
  
	Returns:
	  A list of tuples, each of which contains (id1, name1, id2, name2)
		id1: the first player's unique id
		name1: the first player's name
		id2: the second player's unique id
		name2: the second player's name
	"""
	standings = playerStandings()
	num = countPlayers()
	pairings = [] # List of player pairings

	for n in range(num):
		if (n % 2 == 0):
			#Player 1
			player_id1 = standings[n][0]
			player_name1 = standings[n][1]
			#Player 2
			player_id2 = standings[n+1][0]
			player_name2 = standings[n+1][1]
			#Pairing
			players_pair = (player_id1, player_name1, player_id2, player_name2)
			pairings.append(players_pair)
	return pairings

