#!/usr/bin/env python3
# Unofficial Acunetix CLI version for automation

import subprocess
import sys

# Check if required packages are installed, if not, install them
def check_install_packages():
    try:
        import requests
        import argparse
        import validators
    except ImportError:
        print("Required packages not found. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip3', 'install', 'requests', 'argparse', 'validators'])
        except Exception as e:
            print(f"An error occurred while installing packages: {str(e)}")
            sys.exit(1)

# Check and install required packages
check_install_packages()

# Import installed packages
import requests
import json
import argparse
import validators
import textwrap

requests.packages.urllib3.disable_warnings()

# Config data
config_data = {
    "url": "https://kali",
    "port": 3443,
    "api_key": "ADD-YOUR-API-KEY"
}

# Setting up the target URL
tarurl = f"{config_data['url']}:{config_data['port']}"
headers = {
    "X-Auth": config_data['api_key'],
    "Content-Type": "application/json"
}

def create_scan(target_url, scan_type):
    scan_profile = {
        "full": "11111111-1111-1111-1111-111111111111",
        "high": "11111111-1111-1111-1111-111111111112",
        "weak": "11111111-1111-1111-1111-111111111115",
        "crawl": "11111111-1111-1111-1111-111111111117",
        "xss": "11111111-1111-1111-1111-111111111116",
        "sql": "11111111-1111-1111-1111-111111111113",
    }
    profile_id = scan_profile.get(scan_type, scan_profile['full'])

    def add_task(url=''):
        data = {"address": url, "description": url, "criticality": "30", "scan_speed": "slow", "continuous_mode": "true", "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0", "case_sensitive": "auto", "limit_crawler_scope": "flase"}
        try:
            response = requests.post(tarurl + "/api/v1/targets", data=json.dumps(data), headers=headers, timeout=30, verify=False)
            result = json.loads(response.content)
            return result['target_id']
        except Exception as e:
            print(str(e))
            return

    url = tarurl+"/api/v1/scans"

    print("[*] Running scan on : "+str(target_url))

    data = {
        "target_id": add_task(target_url),
        "profile_id": profile_id,
        "schedule": {"disable": False, "start_date": None, "time_sensitive": False},
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)


def scan_targets_from_file(file_path, scan_type):
    try:
        with open(file_path) as f:
            targets = f.readlines()
        targets = [x.strip() for x in targets]
        for target in targets:
            if validators.url(target):
                create_scan(target, scan_type)
            else:
                print("[!] Invalid URL: "+target)
    except Exception as e:
                print("[!] Error reading file: "+str(e))




def stop_scan(scan_id):
    url = tarurl+"/api/v1/scans/"+str(scan_id)+"/abort"
    response = requests.post(url, headers=headers, verify=False)

    print("[-] Scan stop scan id: "+scan_id)


def stop_specific_scan(target):
    url = tarurl+"/api/v1/scans?q=status:processing;"
    response = requests.get(url, headers=headers, verify=False)
    scans = response.json()["scans"]
    for scan in scans:
        if target == scan["target"]["description"]:
            stop_scan(scan["scan_id"])

def stop_all_scans():
    url = tarurl+"/api/v1/scans?q=status:processing;"
    response = requests.get(url, headers=headers, verify=False)
    scans = response.json()["scans"]
    for scan in scans:
        stop_scan(scan["scan_id"])


if __name__ == "__main__":

    banner = """
                            .,,:;;iiiiii;;:,,.                
                    ,;1tLC088@@@@@@@@@@@@@@880GCLti.         
                    i08@@@@@@@@88888888888888@@@@@@@@8f.       
                    ;@@88888888888888888888888888888888@0,      
                .0@8@@8888888888888888888888888888@@8@0.     
                i@@8L1;;;itC08@8888888888@8GLti;;itG@8@f     
                L 01;ii;:,..:1G@@888888@8L;,..,:;i;;f8@8.    
                0@008@@880Ct;,.;G@88888f,.:ifG088@@8G88@i    
                ,88@@88@@@@@@8Gt1G@88888L1L08@@@@@@8@@@8@f    
                ;@8@8@8GCCLLCG00G8@8888@0G80GCCCGG0@@8@8@    
                i 008Gt1      .L88888880Li:.     ;1f0@08@C    
                i@0ft1t1       ;;L@088@80@       1i1tL8@C    
                i@088@80GGGGG08@@8G88@8G@@80GCCCCG088800@    
                ;@@@88@@@@@@@@@88GG8888C0@@@@@@@@@@8@@8@f    
                ,@8888888888@@@8GGG@888GG088@@8888888888@i    
                .0@@@@@@@@@8008080G@888G8808008@@@@@@@@8@,    
                C8C008800GGG008800@88@00@800CGG088800C80     
                i@CfC,:0888@888LC08880GLC88@@888G:;GfC@t     
                .8@CLC :8@@@@@@81,,;:,,f@@@@@@@L :0LC@8,     
                    t@8LCC..11111;.  ;0G:  ,;i111: 18LL8@f      
                    .0@8CLGt;;;;;:,,iGCGC;,,:;;;;iC8fC@@8.      
                    :8@@GL8@@@@@@800GGGGG08@@@@@@0L0@@@i       
                    :0@@8C088888@@8G00G@@@888880C8@@8i        
                    .f8@8008888888i  t@888888008@@C,         
                        ,L@@8888888@t  C@8888888@@G;           
                        :C@@888888,  i 88888@@Gi             
                            ;C@@@88@:  1@88@@8L;               
                            :L8@@@t  C@@@0f,                 
                                ,1C80.:80Li.
    ╭───────────────────────────────────────────────────────────────────────────────╮
✞ Believe ✞                               BRAIN POWER IS THE MAIN POWER.....

        
➬ Coded By Atif_Alam
╰───────────────────────────────────────────────────────────────────────────────╯
    """

    print(banner)

    if len(sys.argv) < 2:  # Check if no command line arguments are provided
        print("usage: acunetix-cli.py [-h]")

    parser = argparse.ArgumentParser(description="Launch or stop a scan using Acunetix API")
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Start sub-command
    start_parser = subparsers.add_parser("scan", help="Launch a scan use scan -h")
    start_parser.add_argument("-p", "--pipe", action='store_true', help='Read from pipe')
    start_parser.add_argument("-d", "--domain", help="Domain to scan")
    start_parser.add_argument("-f", "--file", help="File containing list of URLs to scan")
    start_parser.add_argument("-t", "--type", choices=["full", "high", "weak", "crawl", "xss", "sql"], default="full",
                        help= textwrap.dedent('''\
                        High Risk Vulnerabilities Scan,
                        Weak Password Scan,
                        Crawl Only,
                        XSS Scan,
                        SQL Injection Scan,
                        Full Scan (by default)'''))

    # Stop sub-command
    stop_parser = subparsers.add_parser("stop", help="Stop a scan")
    stop_parser.add_argument("-d", "--domain", help="Domain of the scan to stop")
    stop_parser.add_argument("-a", "--all", action='store_true', help="Stop all Running Scans")

    args = parser.parse_args()

    if args.action == "scan":
        if args.domain:
            if validators.url(args.domain):
                create_scan(args.domain, args.type)
            else:
                print("[!] Invalid URL: "+args.domain)

        elif args.file:
            scan_targets_from_file(args.file, args.type)

        elif args.pipe:
            input_data = sys.stdin.read().split('\n')
            for url in input_data:
                if validators.url(url):
                    create_scan(url, args.type)

        else:
            print("[!] Must provide either domain or file containing list of targets \nFor Help: acunetix.py scan -h")

    elif args.action == "stop":
        if args.domain:
            stop_specific_scan(args.domain)
        elif args.all == True:
            stop_all_scans()
        else:
            print("[!] Must provide either domain or stop all flag \nFor Help: acunetix.py stop -h")
