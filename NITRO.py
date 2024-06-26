import os
import random
import requests
import string
import time
from concurrent.futures import ThreadPoolExecutor

class NitroGen:
    def __init__(self):
        self.fileName = "generated.txt"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def slow_type(self, text, sleep_time, new_line=True):
        for char in text:
            print(char, end="", flush=True)
            time.sleep(sleep_time)
        if new_line:
            print()

    def generate_codes(self, amount):
        with open(self.fileName, "w", encoding="utf-8") as txtfile:
            print("Porfavor espera.... / Please wait....")
            time_taken = time.time()
            for _ in range(amount):
                code = "".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16))
                txtfile.write(f"https://discord.gift/{code}\n")
            print(f"Se generarán {amount} código | Tiempo aproximado: {round(time.time() - time_taken, 5)}s")

    def check_code(self, code):
        raw_code = code.strip("\n").strip("https://discord.gift")
        response = self.session.get(f"https://discordapp.com/api/v6/entitlements/gift-codes/{raw_code}?with_application=false&with_subscription_plan=true")
        return response.status_code, code

    def checker(self):
        with ThreadPoolExecutor(max_workers=50) as executor, open(self.fileName, "r", encoding="utf-8") as txtfile:
            futures = [executor.submit(self.check_code, code) for code in txtfile.readlines()]
            for future in futures:
                status_code, code = future.result()
                if status_code == 200:
                    print(f"Funcional | {code}")
                else:
                    print(f"No sirve | {code}")

    def main(self):
        self.clear_screen()
        # Demo message here
        baner = """ _______ _          _____   ____  __  __          _           _                 _   
|__   __| |        |  __ \ / __ \|  \/  |   /\   | |         (_)               | |  
   | |  | |__   ___| |  | | |  | | \  / |  /  \  | |_ __ ___  _ _ __ __ _ _ __ | |_ 
   | |  | '_ \ / _ \ |  | | |  | | |\/| | / /\ \ | | '_ ` _ \| | '__/ _` | '_ \| __|
   | |  | | | |  __/ |__| | |__| | |  | |/ ____ \| | | | | | | | | | (_| | | | | |_ 
   |_|  |_| |_|\___|_____/ \____/|_|  |_/_/    \_\_|_| |_| |_|_|_|  \__,_|_| |_|\__|"""                                               
        print(baner)
              
        amount = int(input("Cuántos códigos quieres generar y verificar? / How many codes do you want generate and check?: "))
        self.generate_codes(amount)
        self.checker()

if __name__ == '__main__':
    Gen = NitroGen()
    Gen.main()

