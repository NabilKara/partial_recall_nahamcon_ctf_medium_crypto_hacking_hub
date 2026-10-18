# Partial Recall

A decryption daemon at a small payments company crashed hard. Before anyone could reboot the box, an
incident responder froze the RAM and dumped it with a cold-boot kit.

It didn't go well. The attacker's own wiper had already scrubbed most of the memory, and all that survived of
the private key material were the upper bits of the two exponents and everything below that has been overwritten.