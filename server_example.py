import pyfaucet, socket, time, random, string, json

"""
pyFaucet Networking Library

Example Server for pyfaucet-networking.

More info at:
https://github.com/peteygao/pyfaucet-networking

Created by: Peter Gao (GMC username 'matrixquare')
Email: me@petergao.com
Twitter: @peteygao

All source code is licensed under GNU LESSER GENERAL PUBLIC LICENSE:
http://opensource.org/licenses/lgpl-3.0.html
"""

"""
Define all shared constants between clients and server:
"""
PING_SERVER=253
COULD_NOT_HOST=254
COULD_NOT_JOIN=255
GAME_LIST_REPLY=101
GET_GAME_LIST=1
HOST_GAME_REPLY=102
HOST_GAME=2
JOIN_REQUEST_REPLY=103
JOIN_REQUEST=3
KEEP_GAME_ALIVE=4
CHAT=5
KEEP_CLIENT_ALIVE=6
FORWARD_PACKET=204

def clean_game_list(games_list):
    """
    This checks games to make sure they are still 'alive' (Received a ping within the last 17 seconds)
    Dead games are removed from the list.
    """
    for game in games_list:
        if game['lastseentime']+17 < time.time():
            del games_list[games_list.index(game)]
    pass

if __name__ == "__main__":
    print "Starting up server"
    udp = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind( ('', 2525) )
    print "Server started, bound to local port 2525"

    games_list = list()
    query = 0
    buf = pyfaucet.buffer()
    resp = pyfaucet.buffer()
    
    while 1:
        msg, (addr, port) = udp.recvfrom( 4096 )
        if msg:
            buf.load(msg)
            msg_code = buf.read_ubyte()
            query += 1

            print "\r\n", "Query #:", query
            print "Remote Address:", (addr, port)
            print "Message Code:", msg_code

            if (msg_code == GET_GAME_LIST):
                clean_game_list(games_list)
                games_list_json = json.dumps(games_list)
                # Write our response packet
                resp.clear()
                resp.write_ubyte(GAME_LIST_REPLY)
                resp.write_sstring(games_list_json)
                udp.sendto( resp, (addr, port) )
                print "Hosted Games: ", len(games_list)

            if (msg_code == HOST_GAME):
                new_game = json.loads(buf.read_sstring())
                uniqueid = ''.join(random.choice(string.letters) for i in xrange(10))
                game_dict = {
                                'gamename': new_game['gamename'],
                                'players': [{'playerid': new_game['gamehostid'], 'playername': new_game['playername'], 'address': (addr, port)}],
                                'playercount': 1,
                                'gamehostid': new_game['gamehostid'],
                                'ip': (addr, port)[0],
                                'port': (addr, port)[1],
                                'lastseentime': time.time(),
                                'uniqueid': uniqueid
                }
                games_list.append(game_dict)
                # Write our response packet
                resp.clear()
                resp.write_ubyte(HOST_GAME_REPLY)
                resp.write_bstring(uniqueid)
                udp.sendto(resp, (addr, port))

            if (msg_code == JOIN_REQUEST):
                uniqueid = buf.read_bstring()
                playerid = buf.read_bstring()
                playername = buf.read_bstring()
                for game in games_list:
                    # Did we find the game?
                    if game['uniqueid']==uniqueid:
                        found = False # By default the user is not already in the game
                        # Resend join data if the player is attempting to join but to the server is already in the game
                        players = list()
                        for player in game['players']:
                            if player['playerid']==playerid:
                                found = True # The user is already in the game
                            else:
                                # Grab the list of players for later
                                players.append({'playername':player['playername'],'playerid':player['playerid']})

                        if found==True:
                            resp.clear()
                            resp.write_ubyte(JOIN_REQUEST_REPLY)
                            resp.write_sstring(json.dumps(players))
                            resp.write_bstring(game['gamehostid'])
                            udp.sendto(resp, (addr, port))
                            break

                        # Check for open slots (less than 4 current players)
                        if len(game['players']) <4:
                            resp.clear()
                            resp.write_ubyte(JOIN_REQUEST)
                            resp.write_bstring(playerid)
                            resp.write_bstring(playername)
                            # Tell all the current players that a new player has joined
                            for player in game['players']:
                                udp.sendto(resp, (player['address'][0], player['address'][1]))

                            # Add this player to the game room
                            games_list[games_list.index(game)]['players'].append({'playerid': playerid, 'playername':playername,'address': (addr, port)})
                            games_list[games_list.index(game)]['playercount'] += 1
                            # Tell this player that he has successfully joined the game
                            resp.clear()
                            resp.write_ubyte(JOIN_REQUEST_REPLY)
                            # Send him the list of all the players already in the room
                            resp.write_sstring(json.dumps(players))
                            resp.write_bstring(game['gamehostid']) # Send the host's playerid
                            udp.sendto(resp, (addr, port))
                            break

            if (msg_code == KEEP_GAME_ALIVE):
                uniqueid = buf.read_bstring()
                found = False
                for game in games_list:
                    if game['uniqueid']==uniqueid:
                        games_list[games_list.index(game)]['lastseentime'] = time.time()
                        found = True
                        break
                if found==False:
                    resp.clear()
                    resp.write_ubyte(COULD_NOT_HOST)
                    udp.sendto(resp, (addr, port))

            if (msg_code == KEEP_CLIENT_ALIVE):
                clean_game_list()
                uniqueid = buf.read_bstring()
                found = False
                for game in games_list:
                    if game['uniqueid']==uniqueid:
                        found = True
                        break
                if found==False:
                    resp.clear()
                    resp.write_ubyte(COULD_NOT_JOIN)
                    udp.sendto(resp, (addr, port))

            if (msg_code == FORWARD_PACKET):
                uniqueid = buf.read_bstring()
                playerid = buf.read_bstring()
                for game in games_list:
                    if game['uniqueid']==uniqueid:
                        for player in game['players']:
                            # Only send to players other than the player that sent this message
                            if player['playerid']!=playerid:
                                udp.sendto(buf[buf.get_readpos():], (player['address'][0], player['address'][1]))
                        break
