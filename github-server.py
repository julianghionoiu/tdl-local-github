import http.server
import json
import os
import re
import sys
import time

HOST_NAME = 'localhost'  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9556  # Maybe set this to 9000.

GIT_REPOS_DIR = ""


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        log_info("[POST] You accessed path: %s" % self.path)
        log_debug("[POST] Your request looks like: %s" % self)
        body = self.rfile.read(int(self.headers['Content-Length']))
        # content = convert_raw_http_request_data_to_string(self)
        log_info("[POST] Body: %s" % body)
        self.data_json = json.loads(body)
        if self.path.startswith('/api/v3/orgs/myorg/repos'):
            self.do_POST_user_repos()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

    def do_GET(self):
        log_info("[GET] You accessed path: %s" % self.path)
        log_debug("[GET] Your request looks like: %s" % self)
        if self.path.startswith('/api/v3/repos'):
            self.do_GET_repos()
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "message": "Unknown",
            }))

    def do_GET_repos(self):
        print("Getting repo data")
        repo_name = re.search('\/api\/v3\/repos\/(\w+)\/([\w-]+)', self.path).groups()[1]
        git_path = os.path.abspath(GIT_REPOS_DIR + "/" + repo_name +".git")
        log_info("Git path: " + git_path)
        if os.path.isdir(git_path):
            retval = os.system('git -C %s status' % git_path)
            if retval == 0:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "id": "1234",
                    "clone_url": "file://" + git_path,
                    "html_url": "file://" + git_path.replace(".git", "")
                }))
                return
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "message": "Not found",
            }))

    def do_POST_user_repos(self):
        repo_name = self.data_json['name']
        log_info("Creating repo: %s" % repo_name)
        git_path = os.path.abspath(GIT_REPOS_DIR + "/" + repo_name + ".git")
        log_info("Git path: " + git_path)
        try:
            os.makedirs(git_path)
        except Exception as e:
            errorMessage = "name already exists on this account"
            self.send_response(422, errorMessage)
            self.wfile.write(json.dumps({
                "message": errorMessage,
            }))
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            return

        retval = os.system('git -C %s init' % git_path)
        if retval == 0:
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "id": "1234",
                "clone_url": "file://" + git_path,
                "html_url": "file://" + git_path.replace(".git", "")
            }))
            return
        self.send_error(400, "Not found")
        # self.send_header('Content-type', 'text/json')
        # self.end_headers()


def convert_raw_http_request_data_to_string(request):
    contentLength = int(request.headers.get_all('content-length'))
    return request.rfile.read(contentLength)


def log_debug(message):
    log("[DEBUG] " + message)


def log_info(message):
    log("[INFO] " + message)


def log(message):
    print(time.asctime(), message)


if __name__ == '__main__':
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    GIT_REPOS_DIR = sys.argv[1]
    log_info("Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
log_info("Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
