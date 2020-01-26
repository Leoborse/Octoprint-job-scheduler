# coding=utf-8


from __future__ import absolute_import
import octoprint.plugin
from octoprint.util import RepeatedTimer
import flask
import requests
from datetime import datetime

class JobSchedulerPlugin(
        octoprint.plugin.StartupPlugin,
        octoprint.plugin.TemplatePlugin,
        octoprint.plugin.SettingsPlugin,
        octoprint.plugin.AssetPlugin,
        octoprint.plugin.EventHandlerPlugin,
        octoprint.plugin.ProgressPlugin,
        octoprint.plugin.SimpleApiPlugin
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

    def get_api_commands(self):
        return dict(
            telegram_bot_info=[],
            telegram_bot_chat=["chat_id"]
        )

    # curl -H "X-Api-Key: 9DF4CEF9B41F42D1A0F95C4D4BDC6FD6" http://localhost:5000/api/plugin/jobscheduler

    def on_api_command(self, command, data):
        response = "{}"
        if command == "telegram_bot_chat":
            parameter = "unset"
            if "parameter" in data:
                parameter = "set"
            self._logger.info("command1 called, parameter is {parameter}".format(**locals()))
        elif command == "telegram_bot_info":
            response = self.telegram_bot_info().json()
        return flask.jsonify(response)

    def on_api_get(self, request):
        response = self.telegram_bot_info().json()
        return flask.jsonify(response)

    def telegram(self,msg):
        response = "disabled"
        if (self._settings.get(["telegramenabled"])):
            token  = self._settings.get(["telegramtoken"])
            chatid = self._settings.get(["telegramchatid"])
            url="https://api.telegram.org/bot"+token+"/sendmessage"
            payload = {'chat_id':chatid, 'text': "Jobscheduler: "+msg}
            response = requests.post(url, json=payload)
            self._logger.info("Job Scheduler! Telegram message: "+msg)
        return response

    def telegram_bot_info(self):
        token  = self._settings.get(["telegramtoken"])
        url="https://api.telegram.org/bot"+token+"/getMe"
        response = requests.get(url)
        self._logger.info("Job Scheduler! Telegram bot info: "+str(response.json()['result']['first_name']))
        return response

    def on_event(self, event, payload):
        if ( event.startswith('Print') ):
            self._logger.info("Job Scheduler! Event: "+str(event))
            self.telegram(str(event))
        return

    def on_print_progress(self, storage, path, progress):
        msg = path + " " + str(progress)
        self.telegram(msg)
        return

    def checkjob(self):
        now = datetime.now()
        hr = now.hour
        state = self._printer.get_state_id()
        self._logger.info(state)
        msg = ""

        # Avvio all'ora prevista
        if (
            self._settings.get(["startenabled"]) and
            self._settings.get(["startenabled"]) == hr and
            state == "Operational"
        ):
            self._printer.resume_print()
            msg = "Stampa avviata"

        # Riavvio al mattino
        if (
            self._settings.get(["pauseenabled"]) and
            self._settings.get(["pauseday"]) == hr and
            state == "Paused"
        ):
            self._printer.resume_print()
            msg = "Stampa ripresa"

        # Sospensione alla sera
        if (
            self._settings.get(["pauseenabled"]) and
            self._settings.get(["pausenight"]) == hr and
            state == "Printing"
        ):
            self._printer.pause_print()
            msg = "Stampa sospesa"

        if ( msg != "" ):
            self.telegram(msg)
            self._logger.info(msg)
        return

    def on_after_startup(self):
        self._logger.info("Job Scheduler! Started")
        # delay in secondi
        delay = 1*60
        RepeatedTimer(delay, self.checkjob).start()

def get_implementation_class():
	return JobSchedulerPlugin()

__plugin_name__ = "A Job Scheduler"
__plugin_implementation__ = get_implementation_class()
__plugin_hooks__ = {}
#	"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
#	"octoprint.server.http.routes": __plugin_implementation__.route_hook
