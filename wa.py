import os
import time
import webbrowser

# --- حاول استيراد المكتبات المطلوبة ---
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt
    from rich.table import Table
    from rich.spinner import Spinner
    import pyperclip
except ImportError:
    # إذا كانت المكتبات غير مثبتة، اطبع رسالة واضحة واخرج
    print("\nError: Required libraries are not installed.")
    print("Please run this command in Termux first:")
    print("pip install rich pyperclip\n")
    exit()

# --- إعدادات الواجهة ---
console = Console()

def clear_screen():
    """تنظيف شاشة الطرفية."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """طباعة شعار الأداة - متوافق مع كل الإصدارات."""
    title = "[bold green]WhatsApp Automation Tool[/bold green]"
    author = "[yellow]By: Monky D Dragon[/yellow]"
    
    # محاذاة النص يدوياً لضمان التوافق
    width = 40
    centered_title = title.center(width + 18) # (+18) to compensate for rich tags
    centered_author = author.center(width + 18)

    banner_text = f"{centered_title}\n{centered_author}"
    
    # تم إزالة معامل 'justify' بالكامل
    banner_panel = Panel(
        banner_text,
        title="[bold cyan]MW Messenger[/bold cyan]",
        border_style="cyan",
        expand=False
    )
    console.print(banner_panel)

def normalize_phone_number(phone: str) -> str:
    """تنسيق رقم الهاتف وإزالة المسافات وإضافة '+'."""
    phone = phone.strip().replace(" ", "")
    return f"+{phone}" if not phone.startswith('+') else phone

# --- الوظائف الأساسية للأداة ---

def get_target_details():
    """الحصول على تفاصيل الهدف والرسالة من المستخدم."""
    
    table = Table.grid(expand=True)
    table.add_column(style="cyan", justify="right")
    table.add_column(style="white")
    table.add_row("[1]", "  Send to a Person")
    table.add_row("[2]", "  Send to a Group")
    table.add_row("[0]", "  Exit")
    
    console.print(Panel(table, title="[bold blue]STEP 1: Choose Target[/bold blue]", border_style="blue", padding=(1, 2)))
    choice = Prompt.ask("   [bold magenta]└──> Enter your choice[/bold magenta]", choices=["1", "2", "0"], default="1")

    if choice == "0":
        return None

    console.print(Panel("[dim]Enter the target details below.[/dim]", title="[bold blue]STEP 2: Target & Message[/bold blue]", border_style="blue"))
    
    if choice == '1':
        target = Prompt.ask("   [bold magenta]└──> Enter TARGET phone number[/bold magenta]")
        target = normalize_phone_number(target)
    else:
        console.print("[yellow]Hint: Get the Group ID from the group's URL in WhatsApp Web.[/yellow]")
        target = Prompt.ask("   [bold magenta]└──> Enter the Group ID[/bold magenta]")

    message = Prompt.ask("   [bold magenta]└──> Enter the message to send[/bold magenta]")
    count = IntPrompt.ask("   [bold magenta]└──> How many times to send?[/bold magenta]", default=1)
    
    return choice, target, message, count

def confirm_and_run(details):
    """عرض ملخص للتأكيد ثم بدء التنفيذ."""
    if not details:
        console.print("\n[yellow]Exiting tool. Goodbye![/yellow]")
        return

    choice, target, message, count = details
    
    try:
        pyperclip.copy(message)
        copy_status = "✅ [green]Ready to PASTE[/green]"
    except pyperclip.PyperclipException:
        copy_status = "❌ [red]Manual typing needed[/red]"

    summary_table = Table.grid(expand=True)
    summary_table.add_column(style="bold yellow", justify="right")
    summary_table.add_column()
    summary_table.add_row("Target:", f"  [cyan]{target}[/cyan]")
    summary_table.add_row("Messages:", f"  [cyan]{count}[/cyan]")
    summary_table.add_row("Clipboard:", f"  {copy_status}")

    console.print(Panel(summary_table, title="[bold blue]STEP 3: Confirmation[/bold blue]", border_style="blue"))
    
    if Prompt.ask("[bold]   └──> Start the process? (y/n)[/bold]", choices=["y", "n"], default="y") == "n":
        console.print("[yellow]Operation cancelled.[/yellow]")
        return

    # --- بدء التنفيذ ---
    console.rule("[bold green]Execution Started[/bold green]")
    for i in range(count):
        console.print(f"\n[cyan]>>> Opening Chat #{i + 1} of {count}...[/cyan]")
        
        url = f"https://web.whatsapp.com/send/?phone={target}" if choice == '1' else f"https://web.whatsapp.com/accept?code={target.replace('@g.us', '')}"

        try:
            webbrowser.open(url)
            console.print("✅ [green]Browser opened. Go and paste the message now![/green]")
        except Exception as e:
            console.print(f"❌ [bold red]Error opening browser: {e}[/bold red]")
            break
        
        if i < count - 1:
            spinner = Spinner("dots", text=" Waiting for you...")
            with console.status(spinner) as status:
                for _ in range(5):
                    time.sleep(1)
            console.print("[cyan]   ...Preparing next message...[/cyan]")

    console.rule("[bold green]Process Finished[/bold green]")

# --- نقطة بداية تشغيل البرنامج ---
if __name__ == "__main__":
    clear_screen()
    print_banner()
    try:
        details = get_target_details()
        confirm_and_run(details)
    except KeyboardInterrupt:
        console.print("\n\n[bold red]❌ Process interrupted by user. Exiting.[/bold red]")

