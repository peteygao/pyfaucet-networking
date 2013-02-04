#define write_bstring
write_ubyte(argument0, string_length(argument1));
write_string(argument0, argument1);

#define write_sstring
write_ushort(argument0, string_length(argument1));
write_string(argument0, argument1);

#define write_istring
write_uint(argument0, string_length(argument1));
write_string(argument0, argument1);

#define read_bstring
length = read_ubyte(argument0);
return read_string(argument0, length);

#define read_sstring
length = read_ushort(argument0);
return read_string(argument0, length);

#define read_istring
length = read_uint(argument0);
return read_string(argument0, length);

#define write_header
/*
  Write the packet fowarding header
  argument0 = Buffer to write to
  argument1 = The gameid
  argument2 = The playerid
*/
// Always clear buffer before writing
buffer_clear(global.udp);
write_ubyte(argument0, FORWARD_PACKET);
//This is the game instance we want our message to be forwarded to.
write_bstring(argument0, argument1);
// Player ID is to make sure the server doesn't send the message back to us
write_bstring(argument0, argument2);

