import os
import time
import webbrowser
from urllib.parse import quote

# --- حاول استيراد المكتبات المطلوبة ---
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt
    from rich.table import Table
    from rich.live import Live
    import pyperclip
except ImportError:
    # إذا كانت المكتبات غير مثبتة، اطبع رسالة واضحة واخرج
    print("Error: Required libraries are not installed.")
    print("Please run this command in Termux:")
    print("pip install rich pyperclip")
    exit()

# --- إعدادات الواجهة ---
console = Console()

def clear_screen():
    """تنظيف شاشة الطرفية."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """طباعة شعار الأداة باستخدام Rich."""
    banner_text = "[bold cyan]MW Messenger[/bold cyan]\n[yellow]By: Monky D Dragon[/yellow]"
    
    # تم تغيير 'text_align' إلى 'justify' لحل المشكلة
    banner_panel = Panel(
        banner_text,
        title="[bold green]WhatsApp Automation Tool[/bold green]",
        border_style="green",
        expand=False,
        justify="center"  # <-- هذا هو التعديل الرئيسي
    )
    console.print(banner_panel)

def normalize_phone_number(phone: str) -> str:
    """تنسيق رقم الهاتف وإضافة '+' إذا لم تكن موجودة."""
    phone = phone.strip().replace(" ", "")
    return f"+{phone}" if not phone.startswith('+') else phone

# --- الوظائف الأساسية للأداة ---

def get_target_details():
    """الحصول على تفاصيل الهدف والرسالة من المستخدم."""
    
    # --- اختيار نوع الهدف ---
    table = Table(show_header=False, border_style="dim", box=None)
    table.add_row("[bold cyan][1][/bold cyan]", "Send to a Person")
    table.add_row("[bold cyan][2][/bold cyan]", "Send to a Group")
    table.add_row("[bold red][0][/bold red]", "Exit")
    
    console.print(Panel(table, title="[bold blue]STEP 1: Choose Target[/bold blue]", border_style="blue", padding=(1, 2)))
    choice = Prompt.ask("   [bold magenta]└──> Enter your choice[/bold magenta]", choices=["1", "2", "0"], default="1")

    if choice == "0":
        return None

    # --- إدخال تفاصيل الهدف ---
    console.print(Panel("[dim]Enter the target details below.[/dim]", title="[bold blue]STEP 2: Target & Message[/bold blue]", border_style="blue"))
    
    if choice == '1':
        target = Prompt.ask("   [bold magenta]└──> Enter TARGET phone number[/bold magenta]")
        target = normalize_phone_number(target)
    else: # choice == '2'
        console.print("[yellow]Hint: Get the Group ID from the group's URL in WhatsApp Web.[/yellow]")
        target = Prompt.ask("   [bold magenta]└──> Enter the Group ID[/bold magenta]")

    message = Prompt.ask("   [bold magenta]└──> Enter the message to send[/bold magenta]")
    count = IntPrompt.ask("   [bold magenta]└──> How many times to send?[/bold magenta]", default=1)
    
    return choice, target, message, count

def run_process(details):
    """تشغيل عملية فتح المتصفح وإرسال الرسائل."""
    if not details:
        console.print("\n[yellow]Exiting tool. Goodbye![/yellow]")
        return

    choice, target, message, count = details
    
    # --- نسخ الرسالة إلى الحافظة ---
    try:
        pyperclip.copy(message)
        copy_message = "✅ [green]Message copied to clipboard! Ready to PASTE.[/green]"
    except pyperclip.PyperclipException:
        copy_message = "❌ [red]Could not copy to clipboard. You'll have to type it manually.[/red]"

    # --- بدء التنفيذ ---
    exec_panel = Panel(
        f"Target: [cyan]{target}[/cyan]\n"
        f"Messages: [cyan]{count}[/cyan]\n\n"
        f"[bold yellow]IMPORTANT:[/] You must [u]PASTE[/u] the message and press [u]SEND[/u] manually.\n"
        f"{copy_message}",
        title="[bold blue]STEP 3: Execution[/bold blue]",
        border_style="blue"
    )
    console.print(exec_panel)
    Prompt.ask("[bold cyan]   Press ENTER to begin...[/bold cyan]")

    for i in range(count):
        console.rule(f"[bold]Opening Chat #{i + 1} of {count}[/bold]")
        
        url = f"https://web.whatsapp.com/send/?phone={target}&app_absent=0" if choice == '1' else f"https://web.whatsapp.com/accept?code={target.replace('@g.us', '')}"

        try:
            webbrowser.open(url)
            console.print("✅ [green]Browser opened. Go and paste the message now![/green]")
        except Exception as e:
            console.print(f"❌ [bold red]Error opening browser: {e}[/bold red]")
            break
        
        if i < count - 1:
            # استخدام Live لعرض عداد تنازلي
            with Live(console=console, screen=False, auto_refresh=False) as live:
                for sec in range(5, 0, -1):
                    live.update(f"[dim]   ...Waiting for you... Next message in {sec}s. Press ENTER to skip.[/dim]", refresh=True)
                    time.sleep(1)
            console.print("[cyan]   ...Preparing next message...[/cyan]")

    console.rule("[bold green]Process Finished[/bold green]")

# --- نقطة بداية تشغيل البرنامج ---
if __name__ == "__main__":
    clear_screen()
    print_banner()
    try:
        details = get_target_details()
        run_process(details)
    except KeyboardInterrupt:
        console.print("\n\n[bold red]❌ Process interrupted by user. Exiting.[/bold red]")
