#define string_shuffle
/// string_shuffle(str)
//
//  Returns a given string with charactars shuffled.
//
//      str         string of text, string
//
/// GMLscripts.com/license
{
    var str,out,len,i;
    str = argument0;
    out = "";
    do {
        len = string_length(str);
        i = floor(random(len))+1;
        out += string_char_at(str,i);
        str = string_delete(str,i,1);
    } until (len <= 1);
    return out;
}