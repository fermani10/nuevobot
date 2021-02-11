import os
import json
import telepotpro
import youtube_dl
from random import randint
from youtubesearchpython import SearchVideos
from multiprocessing import Process

bot  =  telepotpro . Bot ( "https://api.telegram.org/bot1690696524:AAH1pfx5ikQCm7DMr3fA-hX5uPOZyg5GVtQ/Getme" )
class Chat:
	def __init__(self, chat_id, text, msg):
		self.msg = msg

		self.commands = {'/start':self.start, '/music':self.music, 'error':self.error}
		self.chat_id = chat_id

		self.command, self.body_command = self.__getCommandAndBodyOfMsg(text)
		self.valideCommand()
		self.answer()
		pass
	
	def answer(self):
		self.__responseCommand()
		pass

	def __responseCommand(self):
		self.commands[f'{self.command}']()
		pass
	
	def valideCommand(self):
		if self.command not in self.commands:
			self.command = 'error'
		pass

	def __getCommandAndBodyOfMsg(self, msg):
		split_msg = msg.split(' ')
		
		command = split_msg[0]
		body = str()
		for parse in split_msg[1:]:
			body += parse

		return command, body

	def sendMessage(self, msg):
		return bot.sendMessage(self.chat_id, msg, parse_mode='Markdown')
		pass

	def error(self):
		self.sendMessage('‼️ Disculpa! Comando Invalido!\n'+'Prueba : "*/musica* _Nombre de la Musica_"\n'+'o: "*/musica* _musician name - song name_"')
		pass

	## Commands
	def start(self):
		msg = str()
		msg += f"🤖 Hola, {self.msg['from']['first_name']} ! \n\n"
		msg += '📩 Envia: "*/musica* _Nombre de la Musica_"  or\n\n'
		msg += '"*/musica* _musician name - song name_" \n\n'
		msg += "Pedir alguna musica 🎶"

		self.sendMessage(msg)
		pass

	def musica(self):
		if self.body_command != '':

			search = SearchVideos(self.body_command, offset = 1, mode = "json", max_results = 1)
			resultados = json.loads(search.result())

			title = resultados['search_result'][0]['title']
			link = resultados['search_result'][0]['link']
			#video_id = resultados['search_result'][0]['id']

			file_name = title +' - '+str(randint(0,999999))+'.mp3'

			ydl_opts = {
				'outtmpl': './'+file_name,
				'format': 'bestaudio/best',
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '256',
				}],
				'prefer_ffmpeg': True
			}

			self.sendMessage(f"🎵 {title} \n🔗 {link}")#erro aqui
			DownloadingMsg = self.sendMessage('⬇️ Descargando... '+'\n_(this may take a while.)_')

			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				info_dict = ydl.extract_info(link, download=True) 

			bot.sendAudio(self.chat_id,audio=open(file_name,'rb'))
			bot.deleteMessage((self.chat_id, DownloadingMsg['message_id']))
			self.sendMessage( '✅ Sucess!')
			print ("Sucess!")
			os.remove(file_name)
		pass

def main(msg):
	## Create New Chat
	chat_id = msg['chat']['id']
	## Use form to send to user DM
	text_msg = msg['text']
	if msg['chat']['type'] == 'group':
		if '@Noticias123_Bot' in text_msg:
			chat_id = msg['chat']['id']
			text_msg = text_msg.replace('@Noticias123_Bot', '')
			
		else:
			chat_id = msg['from']['id']
	Process(target=Chat, args=(chat_id, text_msg, msg,)).start()
	
	pass

bot.message_loop(main, run_forever=True)