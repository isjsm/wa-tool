import os
import time
import webbrowser
from urllib.parse import quote
from colorama import init, Fore, Style

# --- (تهيئة Colorama) ---
init(autoreset=True)

# --- وظائف الواجهة الرسومية ---

def clear_screen():
    """تنظيف شاشة الطرفية."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """طباعة شعار الأداة بشكل احترافي."""
    banner = """
███╗   ███╗ ██████╗ ███╗   ██╗██╗  ██╗██╗   ██╗    ██████╗ ██████╗  ██████╗ 
████╗ ████║██╔═══██╗████╗  ██║██║ ██╔╝╚██╗ ██╔╝    ██╔══██╗██╔══██╗██╔═══██╗
██╔████╔██║██║   ██║██╔██╗ ██║█████╔╝  ╚████╔╝     ██║  ██║██████╔╝██║   ██║
██║╚██╔╝██║██║   ██║██║╚██╗██║██╔═██╗   ╚██╔╝      ██║  ██║██╔══██╗██║   ██║
██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██╗   ██║       ██████╔╝██║  ██║╚██████╔╝
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝       ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
    """
    print(Fore.CYAN + Style.BRIGHT + banner)
    print(Fore.GREEN + Style.BRIGHT + " " * 20 + "--- WhatsApp Messenger Tool ---")
    print(Fore.YELLOW + Style.BRIGHT + " " * 24 + "By: Monky D Dragon")
    print("-" * 70)

def print_info(message):
    """طباعة رسالة معلوماتية."""
    print(Fore.BLUE + Style.BRIGHT + f"[INFO] {message}")

def print_success(message):
    """طباعة رسالة نجاح."""
    print(Fore.GREEN + Style.BRIGHT + f"[SUCCESS] {message}")

def print_warning(message):
    """طباعة رسالة تحذير."""
    print(Fore.YELLOW + f"[WARNING] {message}")

def print_error(message):
    """طباعة رسالة خطأ."""
    print(Fore.RED + Style.BRIGHT + f"[ERROR] {message}")

def get_input(prompt):
    """الحصول على مدخلات من المستخدم بشكل منسق."""
    return input(Fore.MAGENTA + Style.BRIGHT + f"   └──> {prompt}")

# --- الوظائف الأساسية للأداة ---

def main_menu():
    """عرض القائمة الرئيسية والحصول على اختيار المستخدم."""
    print_info("Choose the target type:")
    print("   [1] Send to a Person (Private Number)")
    print("   [2] Send to a Group (Using Group ID)")
    print("   [0] Exit")
    
    while True:
        choice = get_input("Enter your choice [1, 2, or 0]: ")
        if choice in ['1', '2', '0']:
            return choice
        print_error("Invalid choice. Please try again.")

def get_target_details(choice):
    """الحصول على تفاصيل الهدف (رقم أو معرف مجموعة)."""
    if choice == '1':
        target = get_input("Enter the target phone number (e.g., +966...): ")
    else: # choice == '2'
        print_info("How to get the Group ID:")
        print("   1. Open WhatsApp Web in your browser.")
        print("   2. Open the target group.")
        print("   3. The Group ID is in the URL (e.g., 1234567890@g.us)")
        target = get_input("Enter the Group ID: ")
    return target

def run_tool():
    """الدالة الرئيسية التي تدير تدفق عمل الأداة."""
    clear_screen()
    print_banner()
    
    print_warning("This tool uses the WhatsApp account currently logged into your browser.")
    print_warning("The 'sending number' is determined by your active WhatsApp Web session.")
    print("-" * 70)

    choice = main_menu()
    if choice == '0':
        print_info("Exiting tool. Goodbye!")
        return

    target = get_target_details(choice)
    message = get_input("Enter the message to send: ")
    
    while True:
        try:
            count = int(get_input("How many times to open the chat?: "))
            if count > 0: break
            print_error("Please enter a number greater than zero.")
        except ValueError:
            print_error("Invalid input. Please enter a valid number.")

    # ترميز الرسالة بشكل آمن
    encoded_message = quote(message)

    print_warning("\nProcess will start now. You MUST press SEND manually for each message.")
    input(Fore.CYAN + "Press ENTER to begin...")

    for i in range(count):
        print_info(f"Opening chat #{i + 1} of {count}...")
        
        if choice == '1':
            url = f"https://web.whatsapp.com/send?phone={target}&text={encoded_message}"
        else: # choice == '2'
            url = f"https://web.whatsapp.com/accept?code={target.replace('@g.us', '')}"
            if i == 0:
                print_warning("For groups, you must paste the message manually.")

        try:
            webbrowser.open(url)
            print_success(f"Chat #{i + 1} opened. Please send the message.")
        except Exception as e:
            print_error(f"Could not open browser: {e}")
            break
        
        if i < count - 1:
            input(Fore.YELLOW + "   Press ENTER for the next message...")
        time.sleep(1)

    print_success("\nProcess finished!")

# --- نقطة بداية تشغيل البرنامج ---
if __name__ == "__main__":
    try:
        run_tool()
    except KeyboardInterrupt:
        print_error("\n\nProcess interrupted by user. Exiting.")
