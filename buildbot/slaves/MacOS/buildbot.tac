
from twisted.application import service
from buildslave.bot import BuildSlave

basedir = r'/Users/fraca7/Buildslave'
buildmaster_host = '192.168.1.2'
port = 9989
slavename = 'MacOS'
passwd = file('.passwd', 'rb').readlines()[0].strip()
keepalive = 600
usepty = 1
umask = 0022

application = service.Application('buildslave')
s = BuildSlave(buildmaster_host, port, slavename, passwd, basedir,
               keepalive, usepty, umask=umask)
s.setServiceParent(application)

