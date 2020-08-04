# main.py 
#
#
# This file, as well as the subsequent functions (except for mkit_python_api_call, which is an example) are required for use by MKit.
# Each function has sample code.

import json
import mkit
import time
import mkit_rest
import sys
if not hasattr(sys, 'argv'):
    sys.argv  = ['']

import operations

from threading import Thread
from mkit_rest import MKitRestResponse

job_number = 1
configuration = None

#Test thread...
def mkit_python_sample_thread(sso, job_num):
	mkit.log_message("Demoing threading capabilities (you can perform actions in threads, and return an immediate response).");
	mkit.log_message("Count to 1...")
	time.sleep(1)
	mkit.log_message("Count to 2...")
	time.sleep(2)
	mkit.log_message("Count to 3...")
	time.sleep(3)
	mkit.log_message("Done with job " + str(job_num) + " for " + sso)


#This doesn't really do anything, it just shows some of the stuff you can do with MKit calls.
def mkit_python_sample_api_call():
	request = "{\"operation\": \"get_app_info\"}"
	request2 = "{}";

	#Let's pull information about this app/service from the appinfo sub-service.
	#mkit.call allows us to send a message to the given service, and wait for a response.
	mkit.log_message("Calling APIs...")
	result_tuple = mkit.call("ge.dt.mkit.system.service.appinfo", request, None)
	mkit.log_message(result_tuple[0]);

	#mkit.push allows us to simply "push" a message, which means you don't expect a response.
	#mkit.push can accept "*" as a target service, which will mark this as multicast, and send the message to every module on the virtual bus.
	test_binary = bytearray(request, "utf-8")
	mkit.push("*", "{\"val\": \"Hello world!\"}", test_binary)

	#Let's try getting some bootstrapped configuration information (mkit-appconfig.json)...
	result_tuple2 = mkit.call("ge.dt.mkit.core.configurator", "{\"operation\": \"get\", \"type\": \"object\", \"id\": \"configs.ge.dt.mkit.app.seed.python_sample\"}", None)
	mkit.log_message(result_tuple2[0])

	#Only return the JSON part of the tuple [1] would be binary data, if expected from the call.
	return result_tuple[0]

def form_success_rest_response(response_body):
	rest_response = MKitRestResponse()
	rest_response.set_status(200)
	rest_response.set_status_message("OK")
	rest_response.set_body_json(response_body)
	return rest_response.build()

#=======================================================================================================================================
#
#	The below functions are required within your main.py file.
#	The implementation defined below is just for sample purposes only. Please use these functions as you need for you app.
#	See the dt-support user guide located in the Doxygen docs for more information on getting started.
#
#=======================================================================================================================================

#Handle incoming API request (required function in this file).
def mkit_python_incoming_request(source, message, bin):

	mkit.log_message("Incoming request from " + source)
	mkit.log_message("Message: " + message)

	if mkit_rest.is_rest_server(source):
		request_data = json.loads(message)
		response_body = json.loads("{}")
		if request_data["request"]["id"] == "Module 1":
			response_body = request_data

		elif request_data["request"]["id"] == "Module 2":
			response_body = request_data

		elif request_data["request"]["id"] == "getSuggestions":
			result = operations.getSuggestions(request_data["request"]["body_json"]["desc"])
			response_body["data"] = result 
		
		elif request_data["request"]["id"] == "upvote":
			operations.addVotedResult(request_data["request"]["body_json"]["desc"], request_data["request"]["body_json"]["close_note"])
			response_body["data"] = "success" 

		elif request_data["request"]["id"] == "addnote":
			operations.addNote(request_data["request"]["body_json"]["id"], request_data["request"]["body_json"]["note"])
			response_body["data"] = "success"

		elif request_data["request"]["id"] == "removeticket":
			operations.removeTicket(request_data["request"]["body_json"]["id"])
			response_body["data"] = "success"

		elif request_data["request"]["id"] == "updateclousurenote":
			operations.updateClosureNote(request_data["request"]["body_json"]["id"], request_data["request"]["body_json"]["close_note"])
			response_body["data"] = "success"

		elif request_data["request"]["id"] == "addticket":
			operations.addTicket(request_data["request"]["body_json"]["issue"], request_data["request"]["body_json"]["closureNote"])
			response_body["data"] = "success"

		elif request_data["request"]["id"] == "addfile":
			response_body["data"] = "Not supported Yet"
		
		elif request_data["request"]["id"] == "download":
			response_body["data"] = "Not supported Yet"

		result_tuple = (form_success_rest_response(response_body), None)
		mkit.log_message("Returning response tuple......")

	else:
		result_tuple = (None, None)

	return result_tuple

#Startup/initialization function (required function in this file).
def mkit_python_init(name):

	global configuration
	
	mkit.log_message("Getting config from Spring Cloud....")
	#config_tuple = mkit.call("ge.dt.mkit.system.service.cloud_config", "{\"operation\": \"get_config\"}", None)
	#configuration = json.loads(config_tuple[0])
	#mkit.log_message(config_tuple[0])
	mkit.log_message("Initialized Python module!!!!!!!!! The formal name of this module is: " + name)


#Shutdown/cleanup function (required function in this file)..
def mkit_python_shutdown():
	mkit.log_message("Shutting down Python module...")
