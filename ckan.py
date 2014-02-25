"""
script for ckan deployments.

test under ubuntu 12.04

must have key access configuration between local and remote host
pre-configure before running this script

"""
from fabric.api import cd, hosts, sudo, local

def install_ckan_from_source():
    sudo("apt-get install python-dev postgresql libpq-dev python-pip python-virtualenv git-core solr-jetty openjdk-6-jdk")
    local("mkdir -p ~/ckan/lib")
    sudo("ln -s ~/ckan/lib /usr/lib/ckan")
    local("mkdir -p ~/ckan/etc/")
    sudo("ln -s ~/ckan/etc  /etc/ckan")

    sudo("mkdir -p /usr/lib/ckan/default")
    sudo("chown `whoami` /usr/lib/ckan/default")
    local("virtualenv --no-site-packages /usr/lib/ckan/default")
    local(". /usr/lib/ckan/default/bin/activate")

    #install the latest stable release of ckan
    local("pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.2#egg=ckan'")

    #install python modules
    local("pip install -r /usr/lib/ckan/default/src/ckan/requirements.txt")

    local("deactivate")
    local(". /usr/lib/ckan/default/bin/activate")

    #setup the DB
    sudo("-u postgres psql -l")
    #create a db user
    sudo("-u postgres createuser -S -D -R -P ckan_default")
    #create a new postgresql database
    sudo("-u postgres createdb -O ckan_default ckan_default -E utf-8")

    #create the default config directory
    sudo("mkdir -p /etc/ckan/default")
    sudo("chown -R `whoami` /etc/ckan/")

    #change ckan directory and create config file
    with cd("/usr/lib/ckan/default/src/ckan"):
        local("paster make-config ckan /etc/ckan/default/development.ini")

    #edit the development.ini file

    #setup solr

    #edit /etc/default/jetty file

    #start solr
    sudo("sudo service jetty start")

    #replace default schema.xml with symlink
    sudo("mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak")
    sudo("ln -s /usr/lib/ckan/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml")

    sudo("service jetty restart")

    with cd("cd /usr/lib/ckan/default/src/ckan"):
        local("paster db init -c /etc/ckan/default/development.ini")

    #symlink the who.ini file
    local("ln -s /usr/lib/ckan/default/src/ckan/who.ini /etc/ckan/default/who.ini")

    #start the server with wsgi server
    with cd("cd /usr/lib/ckan/default/src/ckan"):
        local("paster serve /etc/ckan/default/development.ini")

