import webbrowser
import time
from urllib.parse import quote
from colorama import init, Fore, Style

# --- (تهيئة Colorama) ---
init(autoreset=True)

def print_banner():
    """طباعة شعار الأداة."""
    print(Fore.GREEN + Style.BRIGHT + """
    ===================================================
    |                                                 |
    |  WhatsApp Ultimate Messenger (Termux Fixed)     |
    |                by Manus                         |
    |                                                 |
    ===================================================
    """)
    print(Fore.YELLOW + "Disclaimer: Use this tool responsibly. Spamming can get your number/group banned.")

def get_send_option():
    """الحصول على خيار الإرسال: فردي أم مجموعة."""
    print(Fore.CYAN + "\nChoose an option:")
    print(Fore.WHITE + "1. Send to a Person (Private Number)")
    print(Fore.WHITE + "2. Send to a Group (Using Group ID)")
    
    while True:
        choice = input(Fore.YELLOW + "[-] Your choice (1 or 2): ")
        if choice in ['1', '2']:
            return choice
        else:
            print(Fore.RED + "Invalid choice. Please enter 1 or 2.")

def get_user_input(choice):
    """الحصول على مدخلات المستخدم بناءً على الاختيار."""
    if choice == '1':
        target = input(Fore.YELLOW + "[-] Enter the target WhatsApp number (e.g., +1234567890): ")
    else: # choice == '2'
        print(Fore.MAGENTA + "\nHow to get the Group ID:")
        print("1. Open WhatsApp Web in your browser.")
        print("2. Open the group you want to send messages to.")
        print("3. The Group ID is in the URL. It looks like: 123456789012345678@g.us")
        target = input(Fore.YELLOW + "[-] Enter the Group ID: ")

    message = input(Fore.YELLOW + "[-] Enter the message to send (Arabic supported): ")
    
    while True:
        try:
            count_str = input(Fore.YELLOW + "[-] Enter how many times to open the chat: ")
            count = int(count_str)
            if count > 0:
                return target, message, count
            else:
                print(Fore.RED + "Please enter a number greater than zero.")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid number.")

def open_chat(target, message, count, choice):
    """
    يفتح محادثة واتساب في المتصفح باستخدام رابط URL مباشر.
    هذه الطريقة متوافقة تمامًا مع Termux.
    """
    print(Fore.MAGENTA + "\n[!] Starting the process...")
    print(Fore.RED + Style.BRIGHT + "[IMPORTANT] The script will open the chat. You MUST press SEND manually.")

    # ترميز الرسالة بشكل صحيح لتكون جزءًا من الرابط
    encoded_message = quote(message)

    for i in range(count):
        # بناء الرابط بناءً على الاختيار (فردي أو مجموعة)
        if choice == '1':
            # رابط لإرسال رسالة لرقم شخصي
            url = f"https://web.whatsapp.com/send?phone={target}&text={encoded_message}"
        else: # choice == '2'
            # رابط لإرسال رسالة لمجموعة
            url = f"https://web.whatsapp.com/accept?code={target.replace('@g.us', '')}"
            # ملاحظة: لا يمكن إدراج نص تلقائي في رابط دعوة المجموعة، سيفتح المحادثة فقط
            if i == 0: # طباعة الملاحظة مرة واحدة فقط
                 print(Fore.CYAN + "[INFO] For groups, the script opens the chat, you need to paste the message manually.")


        print(Fore.CYAN + f"\n[*] Preparing to open chat #{i + 1}...")
        
        try:
            # فتح الرابط في المتصفح الافتراضي
            webbrowser.open(url)
            print(Fore.GREEN + f"[+] Chat #{i + 1} opened. Please send the message and then return here.")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Could not open browser: {e}")
            print(Fore.RED + "In Termux, try running 'termux-open-url https://google.com' to test permissions.")
            break
        
        # الانتظار لتأكيد المستخدم قبل المتابعة
        if i < count - 1:
            input(Fore.YELLOW + "    Press ENTER to prepare the next message...")
        
        # فاصل زمني بسيط
        time.sleep(2)

    print(Fore.GREEN + Style.BRIGHT + f"\n[SUCCESS] Process finished. {count} chat(s) were prepared.")

def main():
    """الدالة الرئيسية لتشغيل الأداة."""
    print_banner()
    try:
        choice = get_send_option()
        target, message, count = get_user_input(choice)
        open_chat(target, message, count, choice)
    except KeyboardInterrupt:
        print(Fore.RED + Style.BRIGHT + "\n\n[!] Process interrupted by user. Exiting.")

# --- (نقطة بداية تشغيل البرنامج) ---
if __name__ == "__main__":
    main()
