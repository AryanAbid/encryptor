from pathlib import Path

import pygame
import pyperclip
from cryptography.fernet import Fernet, InvalidToken


def main():
    ui()
  
    
def ui():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    pygame.display.set_caption("Encrypt & Decrypt Files")

    # FONTS
    font = pygame.font.SysFont("Corbel", 30)
    big_font = pygame.font.SysFont("segoeui", 38, bold=True)
    small_font = pygame.font.SysFont("segoeui", 28, bold=True)


    # HOME PAGE
    page = "home"

    text_home = big_font.render(
        "Do you want to 'Encrypt' or 'Decrypt'?",
        True,
        (211, 218, 217)
    )

    encrypt_button = pygame.Rect(150, 380, 200, 60)
    decrypt_button = pygame.Rect(450, 380, 200, 60)

    encrypt_button_text = font.render("Encrypt", True, (211, 218, 217))
    decrypt_button_text = font.render("Decrypt", True, (211, 218, 217))


    # UPLOAD FILE PAGE
    file_upload_text = big_font.render(
        "Drag and Drop the file",
        True,
        (211, 218, 217)
    )

    upload_area = pygame.Rect(300, 380, 200, 60)

    upload_text = font.render(
        "Drag and Drop",
        True,
        (211, 218, 217)
    )


    # COPY KEY
    click_area = pygame.Rect(300, 380, 200, 60)

    copy_button_before = font.render("COPY", True, (211, 218, 217))
    copy_button_after = font.render("COPIED!", True, (211, 218, 217))
    copied = False


    # PASTE KEY
    key_input = ""

    paste_button_before = font.render("PASTE", True, (211, 218, 217))
    paste_button_after = font.render("PASTED!", True, (211, 218, 217))
    pasted = False


    # BACK BUTTON
    back_button = pygame.Rect(690, 520, 100, 60)
    back_button_text = font.render("BACK", True, (211, 218, 217))


    # INTERACTABLE UI LOOP
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # HOME PAGE
            if event.type == pygame.MOUSEBUTTONDOWN and page == "home":
                if encrypt_button.collidepoint(event.pos):
                    copied = False
                    page = "encrypt_file"

                if decrypt_button.collidepoint(event.pos):
                    pasted = False
                    page = "decrypt_file"

            # UPLOAD FILE
            if event.type == pygame.DROPFILE:                
                if page == "encrypt_file":
                    file_path = event.file
                    output = encrypt(file_path)
                    page = "encrypt_output"
                elif page == "decrypt_file":
                    file_path = event.file
                    page = "decrypt_key_input"

            # COPY KEY
            if event.type == pygame.MOUSEBUTTONDOWN and page == "encrypt_output" and click_area.collidepoint(event.pos):
                pyperclip.copy(output)
                copied = True

            # PASTE KEY VIA CTRL + V
            if event.type == pygame.KEYDOWN and page == "decrypt_key_input" and event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                key_input = pyperclip.paste()
                output = decrypt(file_path, key_input)
                pasted = True
                page = "decrypt_output"

            # PASTE KEY BY CLICKING PASTE BUTTON
            if event.type == pygame.MOUSEBUTTONDOWN and page == "decrypt_key_input" and click_area.collidepoint(event.pos):
                key_input = pyperclip.paste()
                output = decrypt(file_path, key_input)
                pasted = True
                page = "decrypt_output"            

            # BACK BUTTON
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                page = "home"

        # HOME PAGE DESIGN
        if page == "home":
            screen.fill((55, 53, 62))

            screen.blit(
                text_home,
                text_home.get_rect(midtop=(400, 150))
            )

            # ENCRYPT BUTTON
            shadow = encrypt_button.move(0, 4)

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                shadow,
                border_radius=12
            )            

            pygame.draw.rect(
                screen,
                (113, 90, 90),
                encrypt_button,
                border_radius=12
            )

            screen.blit(
                encrypt_button_text,
                encrypt_button_text.get_rect(center=encrypt_button.center)
            )

            # DECRYPT BUTTON
            shadow = decrypt_button.move(0, 4)

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                shadow,
                border_radius=12
            )            

            pygame.draw.rect(
                screen,
                (113, 90, 90),
                decrypt_button,
                border_radius=12
            )

            screen.blit(
                decrypt_button_text,
                decrypt_button_text.get_rect(center=decrypt_button.center)
            )

        # UPLOAD PAGE DESIGN
        elif page == "encrypt_file" or page == "decrypt_file":
            screen.fill((55, 53, 62))

            screen.blit(
                file_upload_text,
                file_upload_text.get_rect(midtop=(400, 150))
            )

            # UPLOAD BUTTON
            shadow = upload_area.move(0, 4)

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                shadow,
                border_radius=12
            )    

            pygame.draw.rect(
                screen,
                (113, 90, 90),
                upload_area,
                border_radius=12
            )

            screen.blit(
                upload_text,
                upload_text.get_rect(
                    center=upload_area.center
                )
            )

            # BACK BUTTON
            shadow = back_button.move(0, 4)

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                shadow,
                border_radius=12
            )    

            pygame.draw.rect(
                screen,
                (113, 90, 90),
                back_button,
                border_radius=12
            )

            screen.blit(
                back_button_text,
                back_button_text.get_rect(
                    center=back_button.center
                )
            ) 

        # ENCRYPTED FILE OUTPUT PAGE DESIGN
        elif page == "encrypt_output":
            screen.fill((55, 53, 62))

            message1 = small_font.render(
                "Press 'COPY' to copy your key.",
                True,
                (211, 218, 217)
            )

            message2 = small_font.render(
                "Keep your key safe, without it, you can't decrypt your file.",
                True,
                (211, 218, 217)
            )

            screen.blit(
                message1,
                message1.get_rect(midtop=(400, 150))
            )

            screen.blit(
                message2,
                message2.get_rect(midtop=(400, 225))
            )

            # COPY KEY AREA
            shadow = click_area.move(0, 4)

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                shadow,
                border_radius=12
            )    

            pygame.draw.rect(
                screen,
                (113, 90, 90),
                click_area,
                border_radius=12
            )

            # DYNAMIC COPYING STATUS
            if not copied:
                screen.blit(
                    copy_button_before,
                    copy_button_before.get_rect(
                        center=click_area.center
                    )
                )            
            else:
                screen.blit(
                    copy_button_after,
                    copy_button_after.get_rect(
                        center=click_area.center
                    )
                )     

            # BACK BUTTON
            shadow = back_button.move(0, 4)

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                shadow,
                border_radius=12
            )    

            pygame.draw.rect(
                screen,
                (113, 90, 90),
                back_button,
                border_radius=12
            )

            screen.blit(
                back_button_text,
                back_button_text.get_rect(
                    center=back_button.center
                )
            ) 

        # DECRYPTION KEY INPUT PAGE DESIGN
        elif page == "decrypt_key_input":
            screen.fill((55, 53, 62))

            enter_key_text = small_font.render(
                "Press 'PASTE' to paste your key.",
                True,
                (211, 218, 217)
            )

            screen.blit(
                enter_key_text,
                enter_key_text.get_rect(midtop=(400, 150))
            )

            enter_key_text_alt = small_font.render(
                "Alternatively, CTRL + V anywhere on the page.",
                True,
                (211, 218, 217)
            )

            screen.blit(
                enter_key_text_alt,
                enter_key_text_alt.get_rect(midtop=(400, 225))
            )

            # PASTE KEY LOGIC
            shadow = click_area.move(0, 4)

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                shadow,
                border_radius=12
            )    

            pygame.draw.rect(
                screen,
                (113, 90, 90),
                click_area,
                border_radius=12
            )

            # DYNAMIC PASTING STATUS
            if not pasted:
                screen.blit(
                    paste_button_before,
                    paste_button_before.get_rect(
                        center=click_area.center
                    )
                )            
            else:
                screen.blit(
                    paste_button_after,
                    paste_button_after.get_rect(
                        center=click_area.center
                    )
                ) 

            # BACK BUTTON
            shadow = back_button.move(0, 4)

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                shadow,
                border_radius=12
            )    

            pygame.draw.rect(
                screen,
                (113, 90, 90),
                back_button,
                border_radius=12
            )

            screen.blit(
                back_button_text,
                back_button_text.get_rect(
                    center=back_button.center
                )
            )             

        # DECRYPTED FILE OUTPUT PAGE DESIGN
        elif page == "decrypt_output":
            screen.fill((55, 53, 62))

            message1 = big_font.render(
                output,
                True,
                (211, 218, 217)
            )

            screen.blit(
                message1,
                message1.get_rect(midtop=(400, 150))
            )      

            # BACK BUTTON
            shadow = back_button.move(0, 4)

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                shadow,
                border_radius=12
            )    

            pygame.draw.rect(
                screen,
                (113, 90, 90),
                back_button,
                border_radius=12
            )

            screen.blit(
                back_button_text,
                back_button_text.get_rect(
                    center=back_button.center
                )
            )

        pygame.display.flip()

    pygame.quit()


def encrypt(file_name):
    key = Fernet.generate_key()
    f = Fernet(key)

    # OPEN FILE AND READ CONTENTS
    try:
        with open(file_name, "rb") as file:
            contents = file.read()
    except FileNotFoundError:
        return "The file does not exist."

    # ENCRYPT CONTENTS
    encrypted_contents = f.encrypt(contents)

    # CREATE ENCRYPTED FILE
    with open(f"{file_name}.enc", "wb") as file:
        file.write(encrypted_contents)

    # DELETE OLD FILE
    Path(file_name).unlink()

    # RETURN KEY
    return key.decode()


def decrypt(file_name, key):
    # VERIFY KEY
    try:
        f = Fernet(key.encode())
    except (ValueError, TypeError):
        return "The key is invalid."

    # OPEN ENCRYPTED FILE AND COPY CONTENTS
    try:
        with open(file_name, "rb") as file:
            contents = file.read()
    except FileNotFoundError:
        return "The file is invalid."

    # TRY TO DECRYPT FILE WITH KEY
    try:
        decrypted_contents = f.decrypt(contents)
    except InvalidToken:
        return "The file is invalid."

    # RETURN TO ORIGINAL FILE NAME
    file = Path(file_name)

    org_file_name = file_name.replace(".enc", "")
    file.rename(org_file_name)

    # DECRYPT FILE
    with open(org_file_name, "wb") as file:
        file.write(decrypted_contents)

    return "Your file has been decrypted"


if __name__ == "__main__":
    main()
