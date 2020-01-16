# coding=utf-8

# https://codeload.github.com/Leoborse/Octoprint-job-scheduler/zip/master

#  class octoprint.plugin.SimpleApiPlugin
# http

from __future__ import absolute_import
import octoprint.plugin
import flask

class JobSchedulerPlugin(
        octoprint.plugin.StartupPlugin,
        octoprint.plugin.TemplatePlugin,
        octoprint.plugin.SettingsPlugin,
        octoprint.plugin.AssetPlugin,
        octoprint.plugin.SimpleApiPlugin
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

    def on_api_get(self, request):
        self._logger.info("Job Scheduler! (token %s)" % self._settings.get(["telegramchatid"])
#        https://api.telegram.org/bot<token>/METHOD_NAME
#   POST application/json (except for uploading files)
# {'chat_id':'Integer or String', 'text': 'messaggio'}
#        import requests
#        token = settings.plugins.
#        url = 'https://api.telegram.org/bot'+token+'/sendmessage'
#myobj = {'somekey': 'somevalue'}
#x = requests.post(url, data = myobj)
#print(x.text)
#        import threading
#        method = request.method
#        t = threading.Thread(target=jsonscheduler_handler, args=(method,))
#        t.start()
        self._logger.info("Job Scheduler! (Check todo list)")
        return flask.jsonify(foo="bar")
#        return flask.make_response("Not found", 404)


def jsonscheduler_handler(method):
    import time
    time.sleep(5)
#    self._logger.info("Job Scheduler! (Started: %s)" % method)
    ##### do your response here


def get_implementation_class():
	return JobSchedulerPlugin()

__plugin_name__ = "A Job Scheduler"
__plugin_implementation__ = get_implementation_class()
__plugin_hooks__ = {}
#	"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
#	"octoprint.server.http.routes": __plugin_implementation__.route_hook
