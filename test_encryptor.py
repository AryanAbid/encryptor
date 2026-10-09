import pygame
from encryptor import decrypt, encrypt, ui

pygame.init()


valid_ciphertext = "gAAAAABqoXiOgAz3Bj6hxgw-Mi2CIU0fh7Km9goVEP8cHGQpSN8nstulWi1d-3NW2q7D0whx_28MrB8iMY7zGYjGmrOAyFWzaYTYh5x1rFWkiPzwgJDcFQiwgM8kn6eM_71vVbjy_yVe"

valid_key = "m_n5hjjgSeIAKU3NAdx-An8nwT4bHOaigVF3KDQm6eg="

invalid_ciphertext = "b'gAAAAABqoXiOgAz3Bj6hxgw-Mi2CIU0fh7Km9goVEP8cHGQpSN8nstulWi1d-3NW2q7D0whx_28MrB8iMY7zGYjGmrOAyFWzaYTYh5x1rFWkiPzwgJDcFQiwgM8kn6eM_71vVbjy_yVe'"

invalid_key = "b'm_n5hjjgSeIAKU3NAdx-An8nwT4bHOaigVF3KDQm6eg='"


def test_encrypt():
    assert encrypt("cat .jpg") == "The file does not exist."


def test_decrypt():
    assert decrypt("cat.jpg", valid_key) == "The file is invalid."


def test_decrypt2():
    assert decrypt("cat.jpg.enc", invalid_key) == "The key is invalid."

def test_ui():
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    assert ui() is None
