import pywhatkit
import time
from colorama import init, Fore, Style
import webbrowser

# --- (Initialize colorama) ---
init(autoreset=True)

def print_banner():
    """Prints the tool's welcome banner."""
    print(Fore.GREEN + Style.BRIGHT + """
    ===================================================
    |                                                 |
    |  WhatsApp Messenger Tool (Termux Compatible)    |
    |                by Dragon                         |
    |                                                 |
    ===================================================
    """)
    print(Fore.YELLOW + "Disclaimer: Use this tool responsibly. Spamming can get your number banned.")

def get_user_input():
    """Gets user input for the target number, message, and count."""
    print(Fore.CYAN + "\nPlease enter the required details:")
    phone_no = input(Fore.YELLOW + "[-] Enter target WhatsApp number (e.g., +1234567890): ")
    message = input(Fore.YELLOW + "[-] Enter the message to send (Arabic supported): ")
    while True:
        try:
            count_str = input(Fore.YELLOW + "[-] Enter how many times to open the chat: ")
            count = int(count_str)
            if count > 0:
                return phone_no, message, count
            else:
                print(Fore.RED + "Please enter a number greater than zero.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid number.")

def open_whatsapp_chat(phone_no, message, count):
    """
    Opens WhatsApp chat in the browser without sending the message automatically.
    This method is compatible with Termux.
    """
    print(Fore.MAGENTA + "\n[!] Starting the process...")
    print(Fore.RED + Style.BRIGHT + "[IMPORTANT] The script will open the chat for you. You must press SEND manually for each message.")
    
    for i in range(count):
        print(Fore.CYAN + f"\n[*] Preparing to open chat #{i + 1}...")
        try:
            # This function generates a URL and opens it. It does not need a GUI.
            pywhatkit.sendwhatmsg_to_group_instantly(phone_no, message, wait_time=0) # We use this as a trick to just open the browser
            
            print(Fore.GREEN + f"[+] Chat #{i + 1} opened in browser. Please press SEND.")
            
            # Ask user to confirm before proceeding to the next one
            if i < count - 1:
                input(Fore.YELLOW + "    Press ENTER to prepare the next message...")

        except webbrowser.Error:
             print(Fore.RED + "[ERROR] Could not open browser. Make sure you have a web browser installed and Termux has permission.")
             print(Fore.RED + "In Termux, run: termux-open-url https://google.com to test.")
             break
        except Exception as e:
            print(Fore.RED + f"[!] An unexpected error occurred: {e}")
            break

    print(Fore.GREEN + Style.BRIGHT + f"\n[SUCCESS] Process finished. {count} chat windows were opened.")

def main():
    """Main function to run the tool."""
    print_banner()
    try:
        phone_no, message, count = get_user_input()
        open_whatsapp_chat(phone_no, message, count)
    except KeyboardInterrupt:
        print(Fore.RED + Style.BRIGHT + "\n\n[!] Process interrupted by user. Exiting.")

# --- (Program entry point) ---
if __name__ == "__main__":
    main()
