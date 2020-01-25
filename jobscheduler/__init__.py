# coding=utf-8
from __future__ import absolute_import
from octoprint.plugin import RepeatedTimer
import flask
import requests
from datetime import datetime

class JobSchedulerPlugin(
        octoprint.plugin.StartupPlugin,
        octoprint.plugin.TemplatePlugin,
        octoprint.plugin.SettingsPlugin,
        octoprint.plugin.AssetPlugin,
        octoprint.plugin.EventHandlerPlugin
        ):

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
        token  = self._settings.get(["telegramtoken"])
        chatid = self._settings.get(["telegramchatid"])
        url="https://api.telegram.org/bot"+token+"/sendmessage"
        payload = {'chat_id':chatid, 'text': "Jobscheduler: "+msg}
        response = requests.post(url, json=payload)
        return response

    def on_event(self, event, payload):
        if ( event.startswith('Print') ):
            self._logger.info("Job Scheduler! Event: "+str(event))
            self.telegram(str(event))
        return

    def checkjob(self):
        now = datetime.now()
        msg = "Job Scheduler! (Timer action) "+str(now)
        self.telegram(msg)
        return

	def interval(self):
		return 5*60 # 5 minuti

    def on_after_startup(self):
        self._logger.info("Job Scheduler! Started")
        RepeatedTimer(self.interval, self.checkjob).start()

def get_implementation_class():
	return JobSchedulerPlugin()

__plugin_name__ = "A Job Scheduler"
__plugin_implementation__ = get_implementation_class()
__plugin_hooks__ = {}
#	"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
#	"octoprint.server.http.routes": __plugin_implementation__.route_hook
