import os
import time
import webbrowser
from urllib.parse import quote
from colorama import init, Fore, Style

# --- (تهيئة Colorama) ---
init(autoreset=True)

# --- وظائف الواجهة الرسومية (UI Functions) ---

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

def print_step(step_num, text):
    """طباعة خطوة من خطوات العملية."""
    print(Fore.BLUE + Style.BRIGHT + f"\n[STEP {step_num}] {text}")

def print_success(message):
    """طباعة رسالة نجاح."""
    print(Fore.GREEN + Style.BRIGHT + f"  [SUCCESS] {message}")

def print_warning(message):
    """طباعة رسالة تحذير."""
    print(Fore.YELLOW + f"  [!] {message}")

def print_error(message):
    """طباعة رسالة خطأ."""
    print(Fore.RED + Style.BRIGHT + f"  [ERROR] {message}")

def get_input(prompt):
    """الحصول على مدخلات من المستخدم بشكل منسق."""
    return input(Fore.MAGENTA + Style.BRIGHT + f"   └──> {prompt}")

def normalize_phone_number(phone):
    """تنسيق رقم الهاتف وإضافة '+' إذا لم تكن موجودة."""
    phone = phone.strip()
    if not phone.startswith('+'):
        return f"+{phone}"
    return phone

# --- الوظائف الأساسية للأداة (Core Functions) ---

def get_sender_number():
    """الحصول على رقم المرسل الذي سيتم استخدامه."""
    print_step(1, "Set the Sending Number")
    print_warning("This number is used to open the correct WhatsApp Web session.")
    print_warning("Make sure you are logged into this account on WhatsApp Web.")
    while True:
        sender = get_input("Enter the number YOU will send from (e.g., 2011...): ")
        if sender.isdigit() and len(sender) > 8:
            return normalize_phone_number(sender)
        print_error("Invalid phone number format. Please enter numbers only.")

def main_menu():
    """عرض القائمة الرئيسية والحصول على اختيار المستخدم."""
    print_step(2, "Choose Target Type")
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
    print_step(3, "Set Target and Message")
    if choice == '1':
        while True:
            target = get_input("Enter the TARGET phone number (e.g., 9665...): ")
            if target.isdigit() and len(target) > 8:
                target = normalize_phone_number(target)
                break
            print_error("Invalid phone number format. Please enter numbers only.")
    else: # choice == '2'
        print_warning("How to get the Group ID:")
        print_warning("1. Open WhatsApp Web > Open the group.")
        print_warning("2. The Group ID is in the URL (e.g., 1234567890@g.us)")
        target = get_input("Enter the Group ID: ")

    message = get_input("Enter the message to send: ")
    
    while True:
        try:
            count = int(get_input("How many times to send the message?: "))
            if count > 0:
                break
            print_error("Please enter a number greater than zero.")
        except ValueError:
            print_error("Invalid input. Please enter a valid number.")
    
    return target, message, count

def run_process(sender_number, target, message, count, choice):
    """تشغيل عملية فتح المتصفح وإرسال الرسائل."""
    print_step(4, "Execution")
    print_warning("Process will start now. You MUST press SEND manually for each message.")
    input(Fore.CYAN + "   Press ENTER to begin...")

    encoded_message = quote(message)

    for i in range(count):
        print(f"\n{Fore.CYAN}>>> Opening chat #{i + 1} of {count}... <<<")
        
        # بناء الرابط بناءً على الاختيار
        if choice == '1':
            # رابط يفتح محادثة مع شخص محدد باستخدام رقم المرسل والمستقبل
            url = f"https://web.whatsapp.com/send/?phone={target}&text={encoded_message}&type=phone_number&app_absent=0"
        else: # choice == '2'
            # رابط يفتح مجموعة (لا يمكن تعبئة النص مسبقًا)
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
            input(Fore.YELLOW + "   ...Press ENTER for the next message...")
        time.sleep(1)

    print_success("\nProcess finished completely!")

# --- نقطة بداية تشغيل البرنامج ---
if __name__ == "__main__":
    clear_screen()
    print_banner()
    try:
        sender_number = get_sender_number()
        choice = main_menu()
        
        if choice == '0':
            print_warning("\nExiting tool. Goodbye!")
        else:
            target, message, count = get_target_details(choice)
            run_process(sender_number, target, message, count, choice)
            
    except KeyboardInterrupt:
        print_error("\n\nProcess interrupted by user. Exiting.")
