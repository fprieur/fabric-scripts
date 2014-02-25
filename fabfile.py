"""Test pour fabric.

Deployment scripts for building on a ckan instance for the ground up.
this is as been testing on ubuntu 12.04

It's using the key-based access configuration for connection to remote host. It must be configure first in order for this script to work.

@author: Fred Prieur
@version: 0.1.0

"""


from fabric.api import env, run, prompt, cd, hosts

def update_drupal_core(old, version):
    """update latest drupal core for billeterie from drupal.org."""
    # ask for unix user
    env.user = prompt("username for remote host : ")
    # create directory for the new drupal core
    run('mkdir -p test-fabric')
    run("echo 'Beginning the update of drupal core'")

    # cd to the new directory and beginning the poutine
    with cd('test-fabric/'):

        # download remote file from drupal.org
        run('wget http://ftp.drupal.org/files/projects/drupal-' +
            version + '.tar.gz')

        # untar and remove the new directory
        run('tar -zxf drupal-' + version + '.tar.gz')
        run('rm drupal-' + version + '.tar.gz')

        # todo: detect the drupalcore to upgrade on server
        # copy current drupal files to new version

        # copy current profile directory to newest
        run('cp -R ' + SERVER_EPLV_URI + '/profiles/eplv' + ' ' +
            'drupal-' + version + '/profiles')

        # copy current modules contrib to newest
        run('cp -R ' + SERVER_EPLV_URI + '/sites/all/modules/contrib' + ' ' +
            'drupal-' + version + '/sites/all/modules')

        # copy current sites directory to newest
        run('cp -R ' + SERVER_EPLV_URI + '/sites' + ' ' +
            'drupal-' + version + '/sites/')

        # copy current .htaccess file to newest directory
        run('cp ' + SERVER_EPLV_URI + '/.htaccess' + ' ' +
            'drupal-' + version + '/.htaccess.a_integer')

        # create symlink from newest core for server eplv uri
        run('ln -s ' + 'drupal-' + version + ' ' +
            "billets.espacepourlavie.dev")

        # todo: check content of the new htaccess
