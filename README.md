# Autoheal
A simple script that auto restart distribute service from power cut or service crash.

# Where it come?
All services will crash after a power cut.When power comes back, services recovery may face these problems:

1. No auto restart and service will not work
2. Service restarts before dependencies getting ready and restart may crash.
2. Service restarts before dependencies getting ready and the service can not work correctly.

What we want is ordered restart.But as more and more services connect together,it's complex to find and maintain a global order. What we provide here is a simple way to deal with th problem.

# How it work?

A centralized restart system may hard to implement,but same effect can be achieved by other method.Let's have a look at how systemd deal with the process dependency at startup time.

Processe dependency is caused by inter-process communication (IPC) in essence. Socket and dbus are two main way of IPC during startup time.What systemd dose are pre-create these sockets and dbus,parallelizd all process and queued the request before corresponding process get ready.The process will be blocked when dependency is not ready and continue work as dependency starts to work and finishes the request.By this way most time no order need to be explicitly pointed out.

Inspired by systemd, we can deal with distribute services restart distributly.Every service checks its directly dependency and start as they are ready.No more global order is needed,different service can restart automatically.Most service are connected by tcp socket or an application layer http protocal,Linux command nc and curl can be used to check these services.

This program Autoheal provide an easy way to generate a script combining checking process liveness,checking dependencies and restarting process together.
# Running

1. Installing the pyyaml dependency

        sudo pip install pyyaml
    
2. Writing conf.yaml as following example:

        nginx:                                                                # process 1
            pname: nginx                                                      # use progess name to check process exist
            script: sudo -u admin /home/admin/cai/bin/nginx-proxy -s restart  # restart the process
        web_service:                                                          # process 2
            pid_file: /home/admin/web_server/conf/.web_server.pid             # use pid file to check process exist
            dep:
                - name: nginx                                                 # check tcp dependency
                  host: 127.0.0.1
                  port: 80
                - name: middleware                                            # check http dependency
                  url: http://middleware.host.com/check.htm
            script: sudo -u admin /home/admin/web_server/bin/startup.sh
  
  3. Generate the restart script:
  
        sh generate.sh >> restart.sh
  
  4. Add a cron task to run restart.sh regularly.You can create a file in /etc/cron.d like this
  
        * * * * * * root sh /home/admin/startup.sh > /dev/null 2>&1
      
    Note about the user privilege to start the process correctly.
