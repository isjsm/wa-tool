import pywhatkit
import time
from colorama import init, Fore, Style

# --- (Initialize colorama for colored output) ---
init(autoreset=True)

def print_banner():
    """Prints the tool's welcome banner."""
    print(Fore.GREEN + Style.BRIGHT + """
    ========================================
    |                                      |
    |      WhatsApp Spammer by Dragon         |
    |                                      |
    ========================================
    """)
    print(Fore.YELLOW + "Disclaimer: Please use this tool responsibly. Spamming can get your number banned.")

def get_user_input():
    """Gets the target phone number, message, and count from the user."""
    print(Fore.CYAN + "\nPlease enter the required details:")
    
    # Get phone number with proper instructions
    phone_no = input(Fore.YELLOW + "[-] Enter the target WhatsApp number (e.g., +1234567890): ")
    
    # Get the message (this can be in any language, including Arabic)
    message = input(Fore.YELLOW + "[-] Enter the message you want to send: ")
    
    # Get the number of times to send the message
    while True:
        try:
            count_str = input(Fore.YELLOW + "[-] Enter the number of times to send the message: ")
            count = int(count_str)
            if count > 0:
                return phone_no, message, count
            else:
                print(Fore.RED + "Please enter a number greater than zero.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid number.")

def send_messages(phone_no, message, count):
    """Handles the message sending loop."""
    print(Fore.MAGENTA + "\n[!] Starting the sending process...")
    print(Fore.MAGENTA + "[!] A browser window will open. Please do not close it.")
    print(Fore.MAGENTA + "[!] You may need to scan the QR code if you are not logged into WhatsApp Web.")

    successful_sends = 0
    for i in range(count):
        try:
            # The message to be sent, including the counter
            # The f-string handles any language in the 'message' variable
            full_message = f"{message} - (Message #{i + 1})"
            
            # Send the message instantly
            # wait_time: seconds to wait for the page to load before typing
            # tab_close: closes the tab after sending
            # close_time: seconds to wait before closing the tab
            pywhatkit.sendwhatmsg_instantly(
                phone_no, 
                full_message, 
                wait_time=20,  # Increased to 20s for slower connections
                tab_close=True, 
                close_time=3
            )
            
            print(Fore.GREEN + f"[+] Message #{i + 1} sent successfully!")
            successful_sends += 1
            
            # A 5-second delay between messages to avoid being flagged as spam
            time.sleep(5)

        except Exception as e:
            print(Fore.RED + f"[!] Failed to send message #{i + 1}. Error: {e}")
            print(Fore.RED + "[!] Trying to continue with the next message...")
            time.sleep(5) # Wait before retrying

    print(Fore.CYAN + Style.BRIGHT + "\n--- Process Finished ---")
    print(Fore.GREEN + Style.BRIGHT + f"[SUCCESS] Successfully sent {successful_sends} out of {count} messages.")

def main():
    """Main function to run the tool."""
    print_banner()
    try:
        phone_no, message, count = get_user_input()
        send_messages(phone_no, message, count)
    except KeyboardInterrupt:
        print(Fore.RED + Style.BRIGHT + "\n\n[!] Process interrupted by user. Exiting.")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"\n[ERROR] An unexpected error occurred: {e}")
        print(Fore.RED + "Please check the following:")
        print(Fore.RED + "- Your internet connection.")
        print(Fore.RED + "- The phone number format (must include country code with '+').")
        print(ForeRED + "- That you are logged into WhatsApp Web in your default browser.")

# --- (Program entry point) ---
if __name__ == "__main__":
    main()
