import signal, sys
import ctypes

from cerver import *
from cerver.http import *

from db import db_mongo_init

from routes.load import load_handler

web_service = None

# end
def end (signum, frame):
	# cerver_stats_print (web_service, False, False)
	http_cerver_all_stats_print (http_cerver_get (web_service))
	cerver_teardown (web_service)
	cerver_end ()
	sys.exit ("Done!")

# GET /
@ctypes.CFUNCTYPE (None, ctypes.c_void_p, ctypes.c_void_p)
def main_handler (http_receive, request):
	http_response_send_file (
		http_receive, HTTP_STATUS_OK,
		b"./examples/http/public/index.html"
	)


def set_routes(http_cerver):

	http_cerver_static_path_add (http_cerver, b"./examples/http/public")

	# GET /api/files
	main_route = http_route_create (REQUEST_METHOD_GET, b"api/files", main_handler)
	http_cerver_route_register (http_cerver, main_route)

	# POST /api/files/load
	load_route = http_route_create (REQUEST_METHOD_POST, b"load", load_handler)
	http_route_set_modifier (load_route, HTTP_ROUTE_MODIFIER_MULTI_PART)
	http_route_child_add (main_route, load_route)

def start ():
	global web_service
	web_service = cerver_create_web (
		b"web-service", 8080, 10
	)

	# main configuration
	cerver_set_alias (web_service, b"web")

	cerver_set_receive_buffer_size (web_service, 4096)
	cerver_set_thpool_n_threads (web_service, 4)
	cerver_set_handler_type (web_service, CERVER_HANDLER_TYPE_THREADS)

	cerver_set_reusable_address_flags (web_service, True)

	# HTTP configuration
	http_cerver = http_cerver_get (web_service)

	# uploads
	http_cerver_set_uploads_path (http_cerver, b"/var/uploads")
	http_cerver_set_uploads_delete_when_done (http_cerver, True)
	http_cerver_set_default_uploads_filename_generator (http_cerver)

	set_routes(http_cerver)

	# start
	cerver_start (web_service)

if __name__ == "__main__":
	signal.signal (signal.SIGINT, end)
	signal.signal (signal.SIGTERM, end)
	signal.signal (signal.SIGPIPE, signal.SIG_IGN)

	cerver_init ()

	cerver_version_print_full ()

	pycerver_version_print_full ()

	if (db_mongo_init ()):
		start ()
