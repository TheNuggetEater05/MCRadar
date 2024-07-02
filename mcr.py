from multiprocessing.pool import ThreadPool as Pool
from colorama import Fore, Back, Style
import ipaddress
from mcstatus import JavaServer, BedrockServer
import os
from time import gmtime, sleep

TIMESTAMP = f"{gmtime().tm_hour}_{gmtime().tm_min}"

Directory = ""

Threads = {}

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Style.BRIGHT}{Fore.GREEN}MC{Fore.LIGHTGREEN_EX}Radar{Style.RESET_ALL} by J_a.y.d.e.n / TheNuggetEater05")

def get_ips(start, end):
    print(f"{Fore.LIGHTYELLOW_EX}Generating IP list...{Fore.RESET}")

    f = int(ipaddress.IPv4Address(start))
    l = int(ipaddress.IPv4Address(end))

    sleep(2)
    cls()
    return [str(ipaddress.IPv4Address(ip)) for ip in range(f, l + 1)]

def scan_servers(start, end, threads=10, port=25565):
    ip_list = get_ips(start, end)

    def scan(ip):
        try:
            server = JavaServer.lookup(ip, 5)
            status = server.status()
            if status:
                print(f"{Fore.GREEN}{Style.BRIGHT}>> Hit: {ip} | Players: {status.players.online} | MOTD: {status.motd.to_plain()}{Style.RESET_ALL}")
                log = open(rf"{Directory}\{status.version.name}.txt", "a")
                try:
                    log.write(f"{ip} | Players: {status.players.online}/{status.players.max} | MOTD: {status.motd.to_plain()}\n")
                except Exception:
                    log.write(f"{ip} | Players: {status.players.online}/{status.players.max}\n")
            else:
                print(f"{Fore.RED}Failed to connect to: {ip}")
            return 1
        except Exception as e:
            print(f"{Fore.RED}Failed to connect to: {ip}")
            #print(e)
            return 0
        
    pool = Pool(threads)
    print(f"{Fore.YELLOW}Starting threads... (may take a minute!)")
    for ip in ip_list:
        pool.apply_async(scan, (ip,))

    pool.close()
    pool.join()
    return

if __name__ == "__main__":
    print(f"{Style.BRIGHT}{Fore.GREEN}MC{Fore.LIGHTGREEN_EX}Radar{Style.RESET_ALL} by J_a.y.d.e.n / TheNuggetEater05")

    # Set up directories
    Directory = rf"{os.getcwd()}\Servers\{TIMESTAMP}"
    if not os.path.exists(Directory):
        os.makedirs(Directory)

    start_ip = input("Starting IP: ")
    end_ip = input("Ending IP: ")

    num_threads = int(input("Thread count: "))

    scan_servers(start_ip, end_ip, num_threads, 25565)
    print("Finished")
