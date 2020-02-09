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
            location="",
            filename="",
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
			dict(type="tab", custom_bindings=False),
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
        self._logger.info("Job Scheduler! Message: "+msg)
        return response

    def telegram_bot_info(self):
        token  = self._settings.get(["telegramtoken"])
        url="https://api.telegram.org/bot"+token+"/getMe"
        response = requests.get(url)
        self._logger.info("Job Scheduler! Telegram bot info: "+str(response.json()))
        return response

    def on_event(self, event, payload):
        self._logger.info("Job Scheduler! Event: "+str(event))
        if ( event == "FileSelected" ):
            location = str(payload["origin"])
            filename = str(payload["path"])
            self._logger.info("Job Scheduler! Event: "+str(event)+", File: ",filename)
            self._settings.set(["location"],location)
            self._settings.set(["filename"],filename)
            self._settings.setBoolean(["startenabled"],[True])
            dat = dict(
                loc=self._settings.get(["location"]),
                fn=self._settings.get(["filename"])
            )
            self._logger.info("Job Scheduler! Data: "+str(dat))
            self._settings.save()
        return

    def on_print_progress(self, storage, path, progress):
        msg = path + " " + str(progress)+"%"
        self.telegram(msg)
        return

    def checkjob(self):
        now = datetime.now()
        hr = now.hour
        state = self._printer.get_state_id()
        msg = state + " " + str(now)
        self._logger.info(msg)

        # Avvio all'ora prevista
        if (
            self._settings.get(["startenabled"]) == True and
            self._settings.get(["starttime"]) == str(hr) and
            state == "OPERATIONAL"
        ):
            cmd = self._printer.start_print()
            self.telegram("Stampa avviata: "+str(cmd))

        # Riavvio al mattino
        if (
            self._settings.get(["pauseenabled"]) == True and
            self._settings.get(["pauseday"]) == str(hr) and
            state == "PAUSED"
        ):
            self._printer.resume_print()
            self.telegram("Stampa ripresa")

        # Sospensione alla sera
        if (
            self._settings.get(["pauseenabled"]) == True and
            self._settings.get(["pausenight"]) == str(hr) and
            state == "PRINTING"
        ):
            self._printer.pause_print()
            self.telegram("Stampa sospesa")

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
