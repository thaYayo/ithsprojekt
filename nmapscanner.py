import argparse
import pprint
import os
import json
import nmap


def main():
    '''main program som hanterar argparse för cli commands'''
    parser = argparse.ArgumentParser(description="nmap portscanner")

    subparsers = parser.add_subparsers(dest='command')

    scan_ip = subparsers.add_parser("scan", help= 'scannar ipadress/er.')
    scan_ip.add_argument("ip", type=str, help="Ange ipadress/er som ska skannas", nargs = '+')
    scan_ip.add_argument("-s","--save", help="sparar resultat av scan till .json fil | -s <fil namn>" )
    scan_ip.add_argument("-p","--port",type=str, help="ange portar  | scan <ipadress/er> -p <port>" )


    read_file = subparsers.add_parser("read", help="läser ip adresser från fil")
    read_file.add_argument("file", help="ange fil som ska läsas")

    args = parser.parse_args()

    if args.command == "scan":
        resultat = scan_host(args.ip)
        if args.port:
            resultat = scan_host(args.ip, args.port)
        elif args.save:
            create_file_json(args.save,resultat)
        else:
            resultat = scan_host(args.ip)
        pprint.pprint(resultat)

    if args.command == "read":
        läs_result = scan_fil(args.file)
        pprint.pprint(läs_result)



def scan_host(ipadress, port=None):
    '''skanning av ip adresser med nmap'''
    result = {}

    nm = nmap.PortScanner()
    for ip in ipadress:
        if port:
            scan_result = nm.scan(ip,f"-p {port}")
            result = scan_result
        else:
            scan_result = nm.scan(ip)
            result[ip] = scan_result["scan"][ip]['tcp']

    return result

def create_file_json(filename,resultat):
    '''funktion för att skapa .json fil med  av skanning'''
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(resultat, sort_keys=True, indent=4))
        print(f"File was created: {filename} \n")
    else:
        print(f"File already exists: {filename} \n")

def scan_fil(filename):
    '''läsa av innehåll av fil vars innehåll ska användas som ip adresser och skannar de'''
    file_result = []
    with open(filename, "r") as file:
        for files in file:
            file_result.append(files.strip())
            resultat = scan_host(file_result)
        return resultat


if __name__ == "__main__":
    main()
