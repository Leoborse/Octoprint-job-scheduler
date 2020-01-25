# coding=utf-8

# https://codeload.github.com/Leoborse/Octoprint-job-scheduler/zip/master

#  class octoprint.plugin.SimpleApiPlugin
# http

from __future__ import absolute_import
import octoprint.plugin
import flask
import requests
from datetime import datetime

class JobSchedulerPlugin(
        octoprint.plugin.StartupPlugin,
        octoprint.plugin.TemplatePlugin,
        octoprint.plugin.SettingsPlugin,
        octoprint.plugin.AssetPlugin,
#        octoprint.plugin.SimpleApiPlugin,
        octoprint.plugin.EventHandlerPlugin
        ):
    def on_after_startup(self):
        self._logger.info("Job Scheduler! Started")

    def get_settings_defaults(self):
        return dict(
            startenabled=True,
            starttime=7,
            pauseenabled=True,
            pauseday=8,
            pausenight=21,
            telegramenabled=True,
            telegramtoken='aaa:bbbbbbbbb....',
            telegramchatid=123456789
        )

    def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

    def get_assets(self):
		return dict(
			js=["js/jobscheduler.js"],
			css=["css/jobscheduler.css"],
            less=[]
		)

    def telegram(self,msg):
#        self._logger.info("Job Scheduler! Telegram sendmessage")
        token  = self._settings.get(["telegramtoken"])
        chatid = self._settings.get(["telegramchatid"])
        url="https://api.telegram.org/bot"+token+"/sendmessage"
        payload = {'chat_id':chatid, 'text': "Jobscheduler: "+msg}
        response = requests.post(url, json=payload)
        return response

    def on_event(self, event, payload):
#        if ( True ):
        if ( event.startswith('Print') ):
            self.telegram(str(event)+" by function")
        return

	def interval(self):
		return 5*60 # 5 minuti

	def check_job(self):
        self.telegram("Job Scheduler! (Timer started)")
#        now = datetime.now()
#        print now.year, now.month, now.day, now.hour, now.minute, now.second

#        import threading
#        method = request.method
        return

# https://codeload.github.com/Leoborse/Octoprint-job-scheduler/zip/master

	def on_after_startup(self):
		RepeatedTimer(self.interval, self.check_job).start()

#    def on_api_get(self, request):

def get_implementation_class():
	return JobSchedulerPlugin()

__plugin_name__ = "A Job Scheduler"
__plugin_implementation__ = get_implementation_class()
__plugin_hooks__ = {}
#	"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
#	"octoprint.server.http.routes": __plugin_implementation__.route_hook
