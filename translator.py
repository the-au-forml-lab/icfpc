english =   list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n")
ascii =     list("!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~")

encoding_dict = {english[i]: ascii[i] for i in range(len(english))}
decoding_dict = {ascii[i]: english[i] for i in range(len(ascii))}

msg = ""

# Decoding Message
print(''.join(decoding_dict.get(char, char) for char in msg))

# Encoding Message
print(''.join(encoding_dict.get(char, char) for char in msg))