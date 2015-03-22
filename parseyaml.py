__author__ = 'mengxin.liumx'
import yaml

f = open("conf.yaml")
confs = yaml.load(f)
for process in confs:
    print "function start_%s {" % process
    conf = confs[process]
    pid_file = conf.get("pid_file", "")
    if pid_file != "":
        print "    check_process pid %s" % pid_file
    pname = conf.get("pname", "")
    if pname != "":
        print "    check_process pname %s" % pname
    print "    if [ \"$?\" == 0 ]; then \n" \
          "        return 0\n" \
        "    fi"
    if "dep" in conf:
        deps = conf["dep"]
        for dep in deps:
            if "url" in dep:
                print "    check_dep_http %s" % dep["url"]
            else:
                print "    check_dep_tcp %s %s" % (dep["host"], dep["port"])
            print "    if [ \"$?\" == 1 ]; then \n" \
                  "        exit 1\n" \
                  "    fi"

    script = conf["script"]
    print "    " + script
    print "    return $?"
    print "}"
    print "start_%s" % process
