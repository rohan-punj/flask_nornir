from flask import Flask, render_template,request
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.filter import F

app = Flask(__name__)
nr = InitNornir(config_file="config.yaml")


@app.route("/")
def homepage_test():
    return render_template("base.html")


@app.route("/greeting")
def say_hello():
    return "Hello There!"


@app.route("/hosts/inventory")
def get_all_inventory():
    return render_template("inventory.html", my_list=nr.inventory.hosts.values())

@app.route("/runcommand")
def runcommand():
    return render_template("runcommand.html")

@app.route("/all/running")
def get_all_running():
    results = nr.run(task=netmiko_send_command, command_string="show run")
    my_list = [v.result for v in results.values()]
    my_keys = [k for k in results.keys()]
    return render_template("running2.html", my_list=my_list, my_keys=my_keys)

@app.route("/run", methods=["POST"])
def recv_runcommand():
    command=request.form["cmd"]
    results = nr.run(task=netmiko_send_command, command_string=str(command))
    my_list = [v.result for v in results.values()]
    my_keys = [k for k in results.keys()]
    return render_template("running2.html", my_list=my_list, my_keys=my_keys )

@app.route("/all/version")
def get_all_version():
    results = nr.run(task=netmiko_send_command, command_string="show version")
    my_list = [v.genie_parse_output() for v in results.values()]
    return render_template("version.html", my_list=my_list)


@app.route("/hosts/<hostname>/version")
def get_host_version(hostname):
    filtered = nr.filter(F(hostname=hostname))
    results = filtered.run(task=send_command, command="show version")
    my_list = [v.scrapli_response.genie_parse_output() for v in results.values()]
    return render_template("version.html", my_list=my_list)


if __name__ == "__main__":
    app.run(debug=True)