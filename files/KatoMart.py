# coding=utf-8
# v.1.3T beta
import os
import time

def clear_screen():
    os.system("clear||cls")
class Colors:
    """ANSI Escape codes for the console output with colors and rich text.

    How to use: print(f"Total errors this run: {Cores.Red if a > 0 else Cores.Green}{a}")
    Read more also: 
        * https://en.wikipedia.org/wiki/ANSI_escape_code
        * https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
        * https://gist.github.com/arlm/f624561b2cd3f53cb26112f3e48f97cd
        * https://www.ecma-international.org/publications-and-standards/standards/ecma-48/

    Attributes:
        Reset (str): Reset colors.
        Bold (str): Makes text bold.
        Underline (str): Underlines text.
        Red (str): Red foreground text.
        Green (str): Green foreground text.
        Yellow (str): Yellow foreground text.
        Blue (str): Blue foreground text.
        Magenta (str): Magenta foreground text.
        Cyan (str): Cyan foreground text.
        bgRed (str): Red background.
        bgGreen (str): Green background.
        bgYellow (str): Yellow background.
        bgBlue (str): Blue background.
        bgMagenta (str): Magenta background.
        bgCyan (str): Cyan background.
        bgWhite (str): White background.
    """
    
    Reset = '\u001b[0m'
    """Reset colors ANSI Escape code.
    """
    Bold = '\u001b[1m'
    """Makes text bold ANSI Escape code.
    """
    Underline = '\u001b[4m'
    """Underlines text ANSI Escape code.
    """

    Red = '\u001b[31m'
    """Red foreground text ANSI Escape code.
    """
    Green = '\u001b[32m'
    """Green foreground text ANSI Escape code.
    """
    Yellow = '\u001b[33m'
    """Yellow foreground text ANSI Escape code.
    """
    Blue = '\u001b[34m'
    """Blue foreground text ANSI Escape code.
    """
    Magenta = '\u001b[35m'
    """Magenta foreground text ANSI Escape code.
    """
    Cyan = '\u001b[36m'
    """Cyan foreground text ANSI Escape code.
    """

    bgRed = '\u001b[41m'
    """Red background ANSI Escape code.
    """
    bgGreen = '\u001b[42m'
    """Green background ANSI Escape code.
    """
    bgYellow = '\u001b[43m'
    """Yellow background ANSI Escape code.
    """
    bgBlue = '\u001b[44m'
    """Blue background ANSI Escape code.
    """
    bgMagenta = '\u001b[45m'
    """Magenta background ANSI Escape code.
    """
    bgCyan = '\u001b[46m'
    """Cyan background ANSI Escape code.
    """
    bgWhite = '\u001b[47m'
    """White background ANSI Escape code.
    """
clear_screen()


print(f"{Colors.Cyan}(por favor instale as dependências caso esteja usando pela primeira vez após 20/10/21, ignore se já fez 1x){Colors.Reset}")
print(f"{Colors.Green}\tpip install -r requirements.txt{Colors.Reset}\n\n")
soninho_zzz = 5
while soninho_zzz > 0:
    print(f"\r{Colors.Yellow}A execução se resumirá em {soninho_zzz} segundos!{Colors.Reset}", flush=True, end="")
    time.sleep(1)
    soninho_zzz -= 1


import requests
import json
import re

from bs4 import BeautifulSoup
import pytube
import youtube_dl
import m3u8
import random
import string
import sys
import subprocess
import glob
from datetime import datetime

download_success = False

class NativeVideoGetProtected:
    def __init__(self, download_info) -> None:
        self.video_session = download_info['session']
        self.master_playlist_url = download_info['master_playlist']
        self.get_policy = self.master_playlist_url.split('?', 1)[1]
        self.save_path = download_info['save_path']
        self.high_qual = self.filter_video_quality()
        self.temp_folder = None
        self.finished = False
    
    def video_exists(self):
        if os.path.isfile(self.save_path):
            self.finished = True
            print(f"{Colors.Cyan}\t\tA aula já está presente!!{Colors.Reset}")
            self.cleanup()
        else:
            self.save_video()
    
    def check_save_path(self):
        if len(self.save_path) > 254:
            new_name = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=7)) + ".mp4"
            if not os.path.exists(f"{self.save_path.split('/')[0]}/ev"):
                os.makedirs(f"{self.save_path.split('/')[0]}/ev")
            with open(f"{self.save_path.split('/')[0]}/ev/map.txt", "a", encoding="utf-8") as sv_check:
                sv_check.write(f"{new_name} - {self.save_path}")
            self.save_path = f"{self.save_path.split('/')[0]}/ev/{new_name}"
        else:
            if not os.path.exists(self.save_path[:self.save_path.rfind('/')]):
                os.makedirs(self.save_path[:self.save_path.rfind('/')])
    
    def make_temp_folder(self):
        temp_folder = "_" + ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=7))
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        self.temp_folder = temp_folder
        
    def filter_video_quality(self):
        if "hdnts=" in self.master_playlist_url:
            self.master_playlist_url = self.master_playlist_url.rsplit('?', 1)[0]
        master_content = self.video_session.get(self.master_playlist_url)
        master_loaded = m3u8.loads(master_content.text)
        res = []
        for playlist in master_loaded.playlists:
            res.append(playlist.stream_info.resolution)
        res.sort(reverse=True)
        for playlist in master_loaded.playlists:
            if playlist.stream_info.resolution == res[0]:
                return playlist.uri
    
    def download_playlist_contents(self):
        # TODO: rewrite this whole thing.
        if "hdnts=" in self.master_playlist_url:
            
            hq_content = self.video_session.get(
            f"{self.master_playlist_url[:self.master_playlist_url.rfind('/')]}/{self.high_qual}")
            
            if hq_content.status_code != 200:
                print(f"{Colors.Red}\tNão foi possível obter o conteúdo da playlist, saindo{Colors.Reset}")
                self.cleanup()
                exit(0)
            
            with open(f'{self.temp_folder}/Tdump.m3u8', 'w') as Tdump:
                Tdump.write(hq_content.text)
            
            hq_playlist = m3u8.loads(hq_content.text)
            key = hq_playlist.segments[0].key.uri
            totalSegmentos = hq_playlist.segments[-1].uri.split(".")[0].split("-")[1]
            for segment in hq_playlist.segments:
                print(f"\r\tPlayer NATIVO (novo, sim, demora para baixar as vezes)!"
                    f"Baixando o segmento: {segment.uri.split('.')[0].split('-')[1]}/{totalSegmentos}!",
                        end="", flush=True)
                uri = segment.uri
                frag = self.video_session.get(            
                f"{self.master_playlist_url[:self.master_playlist_url.rfind('/')]}/{self.high_qual.split('/')[0]}/{uri}")
                
                if frag.status_code != 200:
                    print(f"{Colors.Red}\tNão foi possível obter o segmento, saindo{Colors.Reset}")
                    self.cleanup()
                    exit(0)
                
                with open(f"{self.temp_folder}/" + uri.split('?')[0], 'wb') as sfrag:
                    sfrag.write(frag.content)
            
            fragkey = self.video_session.get(
            f"{self.master_playlist_url[:self.master_playlist_url.rfind('/')]}/{self.high_qual.split('/')[0]}/{key}")
            
            if fragkey.status_code != 200:
                print(f"{Colors.Red}\tNão foi possível obter a chave, saindo{Colors.Reset}")
                self.cleanup()
                exit(0)
            
            with open(f"{self.temp_folder}/{key.split('?')[0]}", 'wb') as skey:
                skey.write(fragkey.content)
            
            with open(f'{self.temp_folder}/Tdump.m3u8', 'r') as Tdump, open(f'{self.temp_folder}/dump.m3u8', 'w') as dump:
                for line in Tdump:
                    if "METHOD=AES-128" in line:
                        line = re.sub(r'\"(.+?)\"', f'''"{key.split('?')[0]}"''', line)
                    elif line.startswith("segment"):
                        line = f"{line.split('?')[0]}\n"
                    dump.write(line)
            os.remove(f'{self.temp_folder}/Tdump.m3u8')
            print("")
        
        else:
            hq_content = self.video_session.get(
            f"{self.master_playlist_url[:self.master_playlist_url.rfind('/')]}/{self.high_qual}?{self.get_policy}")
            
            if hq_content.status_code != 200:
                print(f"{Colors.Red}\tNão foi possível obter a playlist mestra, saindo{Colors.Reset}")
                self.cleanup()
                exit(0)
            
            with open(f'{self.temp_folder}/dump.m3u8', 'w') as dump:
                dump.write(hq_content.text)
            hq_playlist = m3u8.loads(hq_content.text)
            key = hq_playlist.segments[0].key.uri
            totalSegmentos = hq_playlist.segments[-1].uri.split(".")[0].split("-")[1]
            for segment in hq_playlist.segments:
                print(f"\r\tPlayer NATIVO (antigo)! Baixando o segmento: {segment.uri.split('.')[0].split('-')[1]}/{totalSegmentos}!",
                    end="", flush=True)
                uri = segment.uri
                frag = self.video_session.get(            
                f"{self.master_playlist_url[:self.master_playlist_url.rfind('/')]}/{self.high_qual.split('/')[0]}/{uri}?{self.get_policy}")
                
                if frag.status_code != 200:
                    print(f"{Colors.Red}\tNão foi possível obter o segmento, saindo{Colors.Reset}")
                    self.cleanup()
                    exit(0)
                
                with open(f"{self.temp_folder}/" + uri, 'wb') as sfrag:
                    sfrag.write(frag.content)
            fragkey = self.video_session.get(
            f"{self.master_playlist_url[:self.master_playlist_url.rfind('/')]}/{self.high_qual.split('/')[0]}/{key}?{self.get_policy}")
            
            if fragkey.status_code != 200:
                print(f"{Colors.Red}\tNão foi possível obter a chave, saindo{Colors.Reset}")
                self.cleanup()
                exit(0)
            
            with open(f"{self.temp_folder}/{key}", 'wb') as skey:
                skey.write(fragkey.content)
            print("")
    
    def save_video(self):
        self.make_temp_folder()
        self.download_playlist_contents()
        self.check_save_path()
        # TODO implement hardware acceleration detection
        # ffmpegcmd = f'ffmpeg -hide_banner -loglevel error -v quiet -stats -allowed_extensions ALL -hwaccel cuda -i {self.temp_folder}/dump.m3u8 -c:v h264_nvenc -n "{self.save_path}"'
        ffmpegcmd = f'ffmpeg -hide_banner -loglevel error -v quiet -stats -allowed_extensions ALL -i {self.temp_folder}/dump.m3u8 -c copy -preset ultrafast -bsf:a aac_adtstoasc "{self.save_path}"'
        print(f"\tSegmentos baixados, gerando o vídeo final em: {Colors.Green}{self.save_path}{Colors.Reset}", flush=True)
        if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
            subprocess.run(ffmpegcmd, shell=True)
        elif sys.platform.startswith('win32'):
            subprocess.run(ffmpegcmd)
        self.finished = True
        self.cleanup()

    def cleanup(self):
        if self.temp_folder is not None:
            for file in glob.glob(f"{self.temp_folder}/*"):
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"{Colors.Red}\tErro ao apagar o arquivo {file}: {e}{Colors.Reset}")
            time.sleep(3)
            try:
                os.rmdir(self.temp_folder)
            except Exception as e:
                print(f"{Colors.Red}\tErro ao apagar a pasta temporária, pode apagar manualmente: {self.temp_folder}{Colors.Reset}")

        global download_success
        download_success = self.finished


class NativeVideoPublic:
    def __init__(self) -> None:
        pass

class EmbeddedVideo:
    def __init__(self, download_info) -> None:
        youtube_dl.utils.std_headers['Referer'] = download_info['referer']
        self.video_url = download_info['video_url']
        self.save_path = download_info['save_path']
        self.finished = False

    def video_exists(self):
        if os.path.isfile(self.save_path):
            self.finished = True
            global download_success
            download_success = self.finished
        else:
            self.save_video()
    
    def check_save_path(self):
        if len(self.save_path) > 254:
            new_name = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=7)) + ".mp4"
            if not os.path.exists(f"{self.save_path.split('/')[0]}/ev"):
                os.makedirs(f"{self.save_path.split('/')[0]}/ev")
            with open(f"{self.save_path.split('/')[0]}/ev/map.txt", "a", encoding="utf-8") as sv_check:
                sv_check.write(f"{new_name} - {self.save_path}")
            self.save_path = f"{self.save_path.split('/')[0]}/ev/{new_name}"
        else:
            if not os.path.exists(self.save_path[:self.save_path.rfind('/')]):
                os.makedirs(self.save_path[:self.save_path.rfind('/')])
    
    def save_video(self):
        self.check_save_path()
        '''ydl_opts = {"format": "best",
            'retries': 8,
            'fragment_retries': 6,
            'quiet': False,
            "outtmpl": self.save_path}'''
        #with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #    ydl.download([self.video_url])
        video = pytube.YouTube([self.video_url])
        video.streams.filter(file_extension='mp4').get_highest_resolution().download(self.save_path) 

        self.finished = True
        global download_success
        download_success = self.finished


def normalize_str(normalize_me):
    return " ".join(re.sub(r'[<>:!"/\\|?*]', '', normalize_me)
                    .replace('\t', '')
                    .replace('\n', '')
                    .replace('.', '')
                    .split(' ')).strip()


class HotmartClub:
    def __init__(self) -> None:
        clear_screen()
        self.USER_EMAIL = self.get_user_email()
        self.USER_PASSWORD = self.get_user_password()
        self.GET_TOKEN_URL = 'https://api.sparkleapp.com.br/oauth/token'
        self.PRODUCTS_API = \
        'https://api-sec-vlc.hotmart.com/security/oauth/check_token'
        self.HOTMART_API = 'https://api-club.hotmart.com/hot-club-api/rest/v3'
        self.USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/91.0.4472.106 Safari/537.36'
        )
        self.download_course_quantity = 0
        self.count_downloadable_course = 0
        self.course_info = None
        self.course_json = None
        self.course_stats = {'total_modules': 0,
                            'locked_modules': 0,
                            'count_module': 0,
                            'total_lessons': 0,
                            'locked_lessons': 0,
                            'count_lesson': 0,
                            'current_module': None,
                            'current_lesson': None,
                            'current_video': None,
                            'video_seconds': 0}
        self.current_media_name = None
        self.player_auth = {"CloudFront-Policy": "", 
                            "CloudFront-Signature": "", 
                            "CloudFront-Key-Pair-Id": ""}
        self.auth_hotmart = self.create_session()
        self.original_names = self.use_orig_names()
        self.downloadable_courses_list = self.retrieve_downloadable_list()
        self.start_course_download()

    def use_orig_names(self):
        choice = input(f"{Colors.Red}(não recomendado){Colors.Reset} Você gostaria de usar os nomes originais dos vídeos? s/n\n")
        if choice.lower() in ['s', 'si', 'sim', 'ism', 'smi', 'y', 'ye', 'yes', 'yse', 'eys']:
            return True
        else:
            return False
    
    def get_user_email(self) -> str:
        print(f"Qual o seu email da {Colors.Yellow}Hotmart{Colors.Reset}?")
        while True:
            try:
                email = input("email: ")
                if "@" not in email:
                    raise Exception
                else:
                    return email
            except Exception:
                print(f"{Colors.Red}\tOpa, parece que você não entrou um email válido!{Colors.Reset}")
                continue
    
    def get_user_password(self) -> str:
        print(f"Qual a sua senha da {Colors.Yellow}Hotmart{Colors.Reset}?")
        while True:
            try:
                senha = input("senha: ")
                if senha is not None or senha != "":
                    return senha
                else:
                    raise Exception
            except Exception:
                print(f"{Colors.Red}\tOpa, não parece que você informou uma senha válida!{Colors.Reset}")
                continue
    
    def auth_get_token(self) -> str:
        self.auth_hotmart.headers['user-agent'] = self.USER_AGENT
        post_data = {'username': self.USER_EMAIL, 'password': self.USER_PASSWORD,
        'grant_type': 'password'}
        auth_token = self.auth_hotmart.post(self.GET_TOKEN_URL, data=post_data) \
                                .json()['access_token']
        try:
            return auth_token
        except KeyError:
            print(f"{Colors.Red}\tEmail/Senha incorretos! Ou o bot pode estar desatualizado!{Colors.Reset}")
            exit(1)
    
    def create_session(self) -> object:
        self.auth_hotmart = requests.session()
        auth_token = self.auth_get_token()
        self.auth_hotmart.headers.clear()
        headers = {'user-agent': self.USER_AGENT,
                    'authorization': f"Bearer {auth_token}"}
        if self.course_info is not None:
            course_subdomain = self.course_info['resource']['subdomain']
            course_url = f"https://{course_subdomain}.club.hotmart.com"
            headers['origin'] = course_url
            headers['referer'] = course_url
            headers['accept'] = 'application/json, text/plain, */*'
            headers['club'] = course_subdomain
            headers['pragma'] = 'no-cache'
            headers['cache-control'] = 'no-cache'
        self.auth_hotmart.headers.update(headers)
        return self.auth_hotmart
    
    def retrieve_downloadable_list(self) -> None:
        token = self.auth_hotmart.headers['authorization'].split(" ")[1]
        products = self.auth_hotmart.get(self.PRODUCTS_API, 
                                params={'token': token}).json()['resources']
        
        downloadable_courses =[]
        for product in products:
            try:
                if product['resource']['status'] != "ACTIVE" or \
                     "STUDENT" not in product['roles']:
                    continue

                subdomain = product['resource']['subdomain']
                product_url = f'https://{subdomain}.club.hotmart.com'

                self.auth_hotmart.headers['origin'] = product_url
                self.auth_hotmart.headers['referer'] = product_url
                self.auth_hotmart.headers['club'] = subdomain

                course_name = self.auth_hotmart \
                    .get(f'{self.HOTMART_API}/membership?attach_token=false') \
                    .json()['name']

                product['name'] = normalize_str(course_name)

                downloadable_courses.append(product)
            except KeyError:
                continue
        return downloadable_courses

    def start_course_download(self):
        clear_screen()
        print(f"Cursos disponíveis para {Colors.Green}download{Colors.Reset}:")
        for index, course in enumerate(self.downloadable_courses_list, start=1):
            print(f"{index} - {course['name']}")
        while True:
            try:
                download_choice = int(input("Qual curso deseja baixar?"+
                f" {Colors.Cyan}(0 para baixar TODOS!){Colors.Reset}\n")) - 1
                if download_choice > len(self.downloadable_courses_list) or \
                download_choice < -1:

                    raise TypeError
                else:
                    break
            except TypeError:
                print(f"{Colors.Red}{Colors.Bold}Indique um número!{Colors.Reset}")
                continue
        
        if download_choice > -1:
            self.download_course_quantity = 1
            self.course_info = self.downloadable_courses_list[download_choice]
            self.parse_course_info()
        else:
            self.download_course_quantity = len(self.downloadable_courses_list)
            for course in self.downloadable_courses_list:
                self.course_info = course
                self.parse_course_info()

    def count_course_resources(self):
        if not os.path.exists(f"Cursos/{self.course_info['name']}"):
            os.makedirs((f"Cursos/{self.course_info['name']}"))
        for module in self.course_json['modules']:
            self.course_stats['total_modules'] += 1
            if module['locked']:
                with open(f'Cursos/{self.course_info["name"]}/bloq.txt', 'a', encoding="utf-8") as info:
                    info.write(f"(bloqueado) Módulo: {module['name']}\n")
                self.course_stats['locked_modules'] +=1
            else:
                with open(f'Cursos/{self.course_info["name"]}/bloq.txt', 'a', encoding="utf-8") as info:
                    info.write(f"Módulo: {module['name']}\n")
            for lesson in module['pages']:
                self.course_stats['total_lessons'] += 1
                if lesson['locked']:
                    with open(f'Cursos/{self.course_info["name"]}/bloq.txt', 'a', encoding="utf-8") as info:
                        info.write(f"\t(bloqueada) Aula: {lesson['name']}\n")
                    self.course_stats['locked_lessons'] += 1
                else:
                    with open(f'Cursos/{self.course_info["name"]}/bloq.txt', 'a', encoding="utf-8") as info:
                        info.write(f"\tAula: {lesson['name']}\n")

    def retrieve_lesson_info(self, page_hash: str=""):
        lesson_getter = self.auth_hotmart
        return lesson_getter.get(f'{self.HOTMART_API}/page/{page_hash}').json()

    def filter_cookies(self, cookies):
        for cookie in cookies:
            if cookie['path'].endswith("hls/"):
                self.player_auth[cookie['name']] = cookie['value']
    
    def retrieve_native_player_lesson(self, lesson_videos: list=[]):
        for index, media in enumerate(lesson_videos, start=1):
            temp_name = f"{normalize_str(media['mediaName'].rsplit('.', 1)[0])}"
            save_path = f"""Cursos/{self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/{index}. { temp_name if self.original_names else 'parte'}.mp4"""
            video_getter = self.auth_hotmart
            if media['mediaType'] == "VIDEO":
                player = video_getter.get(media['mediaSrcUrl']).text
                info = json.loads(BeautifulSoup(
                                    player, features="html.parser")
                                    .find("script", {"id":"__NEXT_DATA__"}).text)
                self.course_stats['video_seconds'] += info['props']['pageProps']['playerData']['mediaDuration']
                
                self.filter_cookies(info['props']['pageProps']['playerData']['cookies'])

                for asset in info['props']['pageProps']['playerData']['assets']:
                    download_info = {'master_playlist': f"{asset['url']}?Policy={self.player_auth['CloudFront-Policy']}&Signature={self.player_auth['CloudFront-Signature']}&Key-Pair-Id={self.player_auth['CloudFront-Key-Pair-Id']}",
                    'save_path': save_path,
                    'session': self.auth_hotmart}
                    global download_success
                    while not download_success:
                        NativeVideoGetProtected(download_info).video_exists()
                        if not download_success:
                            print(f"\t\t{Colors.Red}Desconectado, redefinindo sessão!{Colors.Reset}")
                            self.auth_hotmart = self.create_session()
                    download_success = False
            
            elif media['mediaType'] == "AUDIO":
                print(f"\r{Colors.Yellow}\t\t(BETA) Download de aúdio, caso não seja salvo por favor se manifeste no telegram{Colors.Reset}", end="", flush=True)
                # TODO
                # Se o link da chave 'url' do objeto no array da chave 'assets' da playerData já for o aúdio o código abaixo funciona
                # DETALHE: Em alguns raros casos os vídeos estão vindo no player antigo, então talvez tenha que filtrar cookie
                # para funcionar nesses casos, eu não tenho acesso em um curso com aúdio então não tenho como verificar isso
                # no caso de player antigo basta colocar ?Policy da cloudfront no final do link igual acontece acima na chave 'master_playlist' do dict 'download_info' (L 528)
                # já no caso do player novo, por enquanto ele está vindo formatado corretamente, não pode alterar nem A nem B no link se não a request se torna inválida (http 403)
                a_text = video_getter.get(media['mediaSrcUrl']).text
                audio_info = json.loads(BeautifulSoup(
                                        a_text, features="html.parser")
                                        .find("script", {"id":"__NEXT_DATA__"}).text)
                #with open("audio_mediasrc.html", "w") as amsrc:
                #    amsrc.write(a_text)
                for asset in audio_info['props']['pageProps']['playerData']['assets']:
                    # resetar a sessão para antes de pegar uma parte é uma boa geralmente, por isso
                    audio_getter = video_getter
                    # ogg não é reconhecido por N players que o pessoal usa, bom evitar
                    if asset['contentType'].lower() == "audio/mp4":
                        if not os.path.isfile(save_path):
                            print(f"\r{Colors.Green}\t\tTudo certo, tentando baixar a aula, por favor aguarde!!{Colors.Reset}                         ", end="", flush=True)
                            audio_file = audio_getter.get(asset['url'])
                            # Aqui já seria o aúdio salvo, tem que ver onde fica o NOME da mídia enviada pelo produtor do curso caso a pessoa opte pelo nome orig
                            # o arg "wb" é para abrir(criar) o arquivo no modo de escrita de bytes, que é o que vem da request feita acima, aúdio
                            if not os.path.exists(f"Cursos/{self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}"):
                                os.makedirs(f"Cursos/{self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}")
                                with open(save_path, "wb") as a_file:
                                    a_file.write(audio_file.content)
                                print(f"\n{Colors.Green}\t\tA aula era um aúdio e foi salva!{Colors.Reset}")
                                # após estar correto, seria bom encadear em um while not 'download_success' para garantir que é salvo e não que tenha alguma desconexão
                        else:
                            print(f"\n{Colors.Cyan}\t\tA aula é um aúdio já presente!!{Colors.Reset}")
    


    def retrieve_embedded_lesson(self, player_html):
        try:
            external_source = None
            page_html = BeautifulSoup(player_html, features="html.parser")
            video_iframe = page_html.findAll("iframe")
            for index, media in enumerate(video_iframe, start=1):
                # TODO Mesmo trecho de aula longa zzz

                file_path = os.path.dirname(os.path.abspath(__file__))
                if not self.original_names:
                    save_path = f"{file_path}/Cursos/{self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/{index}. ext.mp4"
                else:
                    save_path = f"{file_path}/Cursos/{self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/{index}. %(title)s.mp4"

                media_src = media.get("src")
                
                if 'player.vimeo' in media_src:
                    external_source = f"{Colors.Cyan}Vimeo{Colors.Reset}"
                    if "?" in media_src:
                        video_url = media_src.split("?")[0]
                    else:
                        video_url = media_src
                    if video_url[-1] == "/":
                        video_url = video_url.split("/")[-1]

                elif 'vimeo.com' in media_src:
                    external_source = f"{Colors.Cyan}Vimeo{Colors.Reset}"
                    vimeoID = media_src.split('vimeo.com/')[1]
                    if "?" in vimeoID:
                        vimeoID = vimeoID.split("?")[0]
                    video_url = "https://player.vimeo.com/video/" + vimeoID

                elif "wistia" in media_src:
                    # TODO Implementar Wistia
                    external_source = None
                    # fonteExterna = f"{Colors.Yellow}Wistia{Colors.Reset}"
                    # Preciso de um curso que tenha aula do Wistia para ver como tá sendo dado
                    # :( Ajuda noix Telegram: @katomaro
                    input(f"{Colors.bgWhite}{Colors.Red}\tWistia! Entra em contato no Telegram pfv(enter para continuar){Colors.Reset}")

                elif "youtube.com" in media_src or "youtu.be" in media_src:
                    external_source = f"{Colors.Red}YouTube{Colors.Reset}"
                    video_url = media_src

                course_subdomain = self.course_info['resource']['subdomain']

                download_info = {'video_url': video_url,
                'save_path': save_path,
                'referer': f"https://{course_subdomain}.club.hotmart.com/"}

                if external_source is not None:
                    print(f"{Colors.Cyan}\tBaixando aula externa de fonte: {external_source}!")
                    try:
                        EmbeddedVideo(download_info).video_exists()
                    except:
                        print(f"{Colors.Red}\tO vídeo é uma Live Agendada, ou, foi apagado!{Colors.Reset}")
                        with open(f"Cursos/{self.course_info['name']}/erros.txt", "a", encoding="utf-8") as elog:
                            elog.write(f"{video_url} - {self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/{index}. ext.mp4\n")

        except Exception as e:
            print(f"{Colors.Red}\tOu não tem aula externa ou deu algum erro aí, abre issue descrevendo que depois vejo{Colors.Reset}, {e}")

    def save_text(self, content, c_type):
        f_name = 'a'
        f_type = 'a'
        if c_type == 'd':
            f_type = 'ed'
            f_name = 'desc.html'
        elif c_type == 'l':
            f_type = 'el'
            f_name = 'links.html'
        file_path = os.path.dirname(os.path.abspath(__file__))
        lesson_path = f"{file_path}/Cursos/{self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/{f_name}"
            
        
        if len(lesson_path) > 254:
            if not os.path.exists(f"Cursos/{self.course_info['name']}/{f_type}"):
                os.makedirs(f"Cursos/{self.course_info['name']}/{f_type}")
            temp_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            with open(f"Cursos/{self.course_info['name']}/{f_type}/list.txt", "a", encoding="utf-8") as safelist:
                safelist.write(f"{temp_name} = {self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/{f_name}\n")
            lesson_path = f"Cursos/{self.course_info['name']}/{f_type}/{temp_name}.html"

        if not os.path.exists(lesson_path[:lesson_path.rfind('/')]):
            os.makedirs(lesson_path[:lesson_path.rfind('/')])

        if not os.path.isfile(lesson_path):
            if c_type == 'd':
                with open(lesson_path, "w", encoding="utf-8") as desct:
                    desct.write(content)
            elif c_type == 'l':
                for link in content:
                    with open(lesson_path, "a", encoding="utf-8") as linkz:
                        linkz.write(f'''<p><a href="{link['articleUrl']}">{link['articleName']}</a></p>''')

    def save_attachment(self, attachment):
        file_path = os.path.dirname(os.path.abspath(__file__))
        lesson_path = f"{file_path}/Cursos/{self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/Materiais/{normalize_str(attachment['fileName'])[:-3]}.{attachment['fileName'].split('.')[-1]}"
        if len(lesson_path) > 254:
            if not os.path.exists(f"Cursos/{self.course_info['name']}/et"):
                os.makedirs(f"Cursos/{self.course_info['name']}/et")
            temp_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            with open(f"Cursos/{self.course_info['name']}/et/list.txt", "a", encoding="utf-8") as safelist:
                safelist.write(
                    f"{temp_name} = {self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/Materiais/{normalize_str(attachment['fileName'])[:-3]}.{attachment['fileName'].split('.')[-1]}\n")
            lesson_path = f"Cursos/{self.course_info['name']}/et/{temp_name}.{attachment['fileName'].split('.')[-1]}"

        if not os.path.exists(f"Cursos/{self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/Materiais"):
            os.makedirs(f"Cursos/{self.course_info['name']}/{self.course_stats['current_module']}/{self.course_stats['current_lesson']}/Materiais")

        if not os.path.isfile(lesson_path):
            try:
                att_getter = self.auth_hotmart
                anexo = att_getter.get(
                    f"https://api-club.hotmart.com/hot-club-api/rest/v3/attachment/{attachment['fileMembershipId']}/download").json()
                anexo = requests.get(anexo['directDownloadUrl'])
            except KeyError:
                vrum = requests.session()
                vrum.headers.update(self.auth_hotmart.headers)
                lambdaUrl = anexo['lambdaUrl']
                vrum.headers['token'] = anexo['token']
                anexo = requests.get(vrum.get(lambdaUrl).text)
                del vrum
            with open(lesson_path, 'wb') as ann:
                ann.write(anexo.content)
                print(f"{Colors.Green}\t\tAnexo baixado com sucesso ({Colors.bgWhite}{attachment['fileName']}{Colors.Reset}{Colors.Green})!{Colors.Reset}")
        else:
            print(f"{Colors.Green}\t\tAnexo já existente({Colors.bgWhite}{attachment['fileName']}{Colors.Reset}{Colors.Green})!{Colors.Reset}")
    
    
    def goodbye(self):
        with open(f'Cursos/{self.course_info["name"]}/info.txt', 'w', encoding="utf-8") as info:
            info.write(f"""Curso baixado utilizando o Katomart em {datetime.today().strftime("%d/%m/%Y")}!\n
            Ao iniciar o download o curso possuia {self.course_stats['total_modules']} módulos,
            dos quais {self.course_stats['locked_modules']} estavam bloqueados.\n
            Por outro lado, o mesmo possuia {self.course_stats['total_lessons']} aulas,
            das quais {self.course_stats['locked_lessons']} estavam bloqueadas.
            Foram baixados {self.course_stats['video_seconds']} segundos de vídeo nativo da hotmart.""")
    
    def parse_course_info(self):
        self.auth_hotmart = self.create_session()
        self.course_json = self.auth_hotmart.get(
                                    f'{self.HOTMART_API}/navigation').json()
        self.count_course_resources()
        for module in self.course_json['modules']:
            self.course_stats['count_module'] += 1
            self.course_stats['current_module'] = \
            f"{module['moduleOrder']}. {normalize_str(module['name'])}"
            for lesson in module['pages']:
                if self.course_stats['count_lesson'] % 10 == 0:
                    clear_screen()
                self.course_stats['count_lesson'] += 1
                self.course_stats['current_lesson'] = \
                    f"{lesson['pageOrder']}. {normalize_str(lesson['name'])}"
                print(f"Curso {self.count_downloadable_course}/{self.download_course_quantity}: {self.course_info['name']}; Verificando o Módulo {Colors.Cyan}{self.course_stats['count_module']}{Colors.Reset} de {Colors.Blue}{self.course_stats['total_modules']}{Colors.Reset}: {Colors.Cyan}{self.course_stats['current_module']}{Colors.Reset}")
                print(f"\tAula: {Colors.Cyan}{self.course_stats['count_lesson']}{Colors.Reset} de {Colors.Blue}{self.course_stats['total_lessons']}{Colors.Reset}(totais): {Colors.Cyan}{self.course_stats['current_lesson']}{Colors.Reset}")
                lesson_info = self.retrieve_lesson_info(lesson['hash'])
                # video lessons
                try:
                    self.retrieve_native_player_lesson(lesson_info['mediasSrc'])
                except KeyError:
                    try:
                        self.retrieve_embedded_lesson(lesson_info['content'])
                    except KeyError:
                        print(f"{Colors.Yellow}\t\tAula sem vídeo nativo e aparentemente sem aula externa!{Colors.Reset}")
                        with open(f"Cursos/{self.course_info['name']}/erros.txt", "a", encoding="utf-8") as elog:
                            elog.write(f"{self.course_stats['current_module']}/{self.course_stats['current_lesson']} sem conteúdo?\n")
                # lesson descriptions/textual lessons
                try:
                    if lesson_info['content'].strip() != '':
                        self.save_text(lesson_info['content'], 'd')
                        print(f"{Colors.Green}\t\tDescrição encontrada e salva!{Colors.Reset}")
                except KeyError:
                    print(f"{Colors.Yellow}\t\tAula sem Descrição!{Colors.Reset}")
                # Complementary Readings
                try:
                    if lesson_info['complementaryReadings']:
                        self.save_text(lesson_info['complementaryReadings'], 'l')
                        print(f"{Colors.Green}\t\tLinks de leitura complementar encontrados e salvos!{Colors.Reset}")
                except KeyError:
                    print(f"{Colors.Yellow}\t\tAula sem Leitura Complementar!{Colors.Reset}")
                # Attachments
                try:
                    for att in lesson_info['attachments']:
                        print(f"{Colors.Yellow}\t\tTentando baixar o anexo: {Colors.Magenta}{Colors.bgWhite}{att['fileName']}{Colors.Reset}")
                        self.save_attachment(att)
                except KeyError:
                    print(f"{Colors.Yellow}\t\tAula sem Anexos!{Colors.Reset}")
                
                time.sleep(1)

        self.goodbye()


HotmartClub()
