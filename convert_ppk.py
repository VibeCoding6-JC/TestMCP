"""
Convert PuTTY PPK v3 to OpenSSH private key format
"""
import base64
import struct

# PPK data dari file devjc.ppk
public_lines = """AAAAB3NzaC1yc2EAAAADAQABAAABAQDLh76jPpWEo6Ylx9DgP04n0T6cvH/cjPR1
58fbsW4HiRs8jiGTztFaXT/GqvFaCdoDHIi0D8qn+KguVYt0FWZU//KSdRxmhAne
A4Hiuv05iqzDp4FTmmvsheeUnhK3BzaezMlHfh7jPFOr32VqRJ9v/2frGMdtLXaV
s3cdh0ui2SlQmwKZOyVwrJ0zCiQ3SDedjBG61B5L/POQNdDEjs4t9mmbSmBMpGVq
uCvRNoRTK83jwgqIjRMZNmwg/f/AKRiFHe7l9kbfBW3LeyYf2j2AE5oE5Ehqmvop
QsxQaCGTFwY54nZhl4KfNPTRi/7FpCF8UO/lpmZPvrNq5XIs45lj"""

private_lines = """AAABAFnxmTvHEohVUb1selA/aaiK/eKCIvcyi233igj6did6XcD7BretNDN89gwz
ywkBRYkOeRMpz2M/rgMb5s7cDicOHQLAIlbjjwDACAxMmk9tiz/DrJFnsr4JxveU
i6y60VaIJYMkpz3AkTFpPgYiYVs7QY9RmgATkU5CyycPfUtvZuH5D8kcuU5zWLfu
LjvHAZiPC4q8FzpOAjGrAUnOj1dAIv5X5YNrzb3qE0DKL3zPjPFPzxoCqLIkWKUU
sQ1YDU+kAkbZP5801PDwM+140SxYIg88tRe3UqFbnQPGQCNVFOz8bakT2PiCZJWM
9jn/WMKFfFK77+uS2jy6rKSSpeEAAACBAOag+roT695Tl7Z+PGl/vvqL+WkJJ4ty
oc/MkiWNOx98E2r+YLi+M0ZEjRwNyMrBlWZmmrg7u5qTk9OTfuz+hocthUAPJi3N
WFm/CbRI6cfQKp3dLqPV7EsUhTM0dVCU3oDLnI+lEMA4cbnCeMUnXNinSqs4yqBj
3y+xAWz7b5+bAAAAgQDh65v0SCxpk3M0bTdSFEiKl40kdkc01QgVHJqS3anoPVID
K3H9ugZnqwpLFZEvZ1hEX0C9QW99v2qaBmwM2fxrwsA2Y5b1FvCyV6wKbJj2w5wi
ON5RXXggIMJ930z1gKQJ4FJb3Bqw96ju77xEbc7n8DYrSYWITIyRyLuB0H5d2QAA
AIBoAyf4ctkiFSGEkI6Xmc1HQrXjqPvNYkKYWeEQhBKS6R5wwTUuo4YuYuGhsUrY
GBrovpvgyyee6Zq9aNVblBeDdu2DveFAfOVCtfndzuhekn1Ejj1HPjjHlWOubvF8
DqG+wxoP95/+MkQoJMaFyRxuL6/9UYRVlVk/c9x0UqhIAg=="""

def read_openssh_string(data, offset):
    length = struct.unpack('>I', data[offset:offset+4])[0]
    return data[offset+4:offset+4+length], offset+4+length

def write_openssh_string(s):
    if isinstance(s, str):
        s = s.encode()
    return struct.pack('>I', len(s)) + s

# Decode base64
pub_data = base64.b64decode(public_lines.replace('\n', ''))
priv_data = base64.b64decode(private_lines.replace('\n', ''))

# Parse public key
offset = 0
key_type, offset = read_openssh_string(pub_data, offset)
e, offset = read_openssh_string(pub_data, offset)
n, offset = read_openssh_string(pub_data, offset)

# Parse private key (PPK format stores: d, p, q, iqmp)
offset = 0
d, offset = read_openssh_string(priv_data, offset)
p, offset = read_openssh_string(priv_data, offset)
q, offset = read_openssh_string(priv_data, offset)
iqmp, offset = read_openssh_string(priv_data, offset)

# Build OpenSSH format private key
import os
check_int = os.urandom(4)

# Private section (unencrypted)
private_section = b''
private_section += check_int + check_int  # Two identical check integers
private_section += write_openssh_string(b'ssh-rsa')
private_section += write_openssh_string(n)
private_section += write_openssh_string(e)
private_section += write_openssh_string(d)
private_section += write_openssh_string(iqmp)
private_section += write_openssh_string(p)
private_section += write_openssh_string(q)
private_section += write_openssh_string(b'devjc@jc-server')  # comment

# Padding
block_size = 8
padding_length = block_size - (len(private_section) % block_size)
if padding_length == block_size:
    padding_length = 0
private_section += bytes(range(1, padding_length + 1))

# Public section  
public_section = write_openssh_string(b'ssh-rsa') + write_openssh_string(e) + write_openssh_string(n)

# Build full key
auth_magic = b'openssh-key-v1\x00'
cipher_name = write_openssh_string(b'none')
kdf_name = write_openssh_string(b'none')
kdf_options = write_openssh_string(b'')
num_keys = struct.pack('>I', 1)
public_key_section = write_openssh_string(public_section)
private_key_section = write_openssh_string(private_section)

full_key = auth_magic + cipher_name + kdf_name + kdf_options + num_keys + public_key_section + private_key_section

# Encode to base64 with proper line breaks
encoded = base64.b64encode(full_key).decode()
lines = [encoded[i:i+70] for i in range(0, len(encoded), 70)]

openssh_key = "-----BEGIN OPENSSH PRIVATE KEY-----\n"
openssh_key += "\n".join(lines)
openssh_key += "\n-----END OPENSSH PRIVATE KEY-----\n"

print(openssh_key)

# Save to file
with open('devops01_openssh.key', 'w') as f:
    f.write(openssh_key)

print("\nKey saved to devops01_openssh.key")
