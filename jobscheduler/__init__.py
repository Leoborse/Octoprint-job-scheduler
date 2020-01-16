# coding=utf-8

# https://codeload.github.com/Leoborse/Octoprint-job-scheduler/zip/master

#  class octoprint.plugin.SimpleApiPlugin

from __future__ import absolute_import
import octoprint.plugin

class JobSchedulerPlugin(
        octoprint.plugin.StartupPlugin,
        octoprint.plugin.TemplatePlugin,
        octoprint.plugin.SettingsPlugin,
        octoprint.plugin.AssetPlugin):
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
        self._logger.info("Job Scheduler! (Started: %s)" % request.method)
        return flask.jsonify(foo="bar")
#        return flask.make_response("Not found", 404)

def get_implementation_class():
	return JobSchedulerPlugin()

__plugin_name__ = "A Job Scheduler"
__plugin_implementation__ = get_implementation_class()
__plugin_hooks__ = {}
#	"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
#	"octoprint.server.http.routes": __plugin_implementation__.route_hook
