#!/usr/bin/env python
import pyrax
import os
import sys

# upload_file(): Upload a file to a Cloud Files container using PyRax bindings
# PRE: None
# POST: None
# RETURN VALUE: Returns 0 on success and 1 on failure
# NOTES: This is a simple example function.  It initiates all connections
#        internally. As such it is not recommended to be called multiple
#        times; in longer code the authentication configuration only needs
#        to be set once and the cf object should be reused.
def upload_file(src, container, cdn_user, cdn_key, region):
    print "Uploading %s container %s" % (src, container)

    # Configure PyRax authentication
    try:
        # Required on >= Pyrax 1.4
        pyrax.set_setting("identity_type", "rackspace")
        # Please note that you can also pass this a credentials file, so you
        # don't need to pass your key in on the command line.
        pyrax.set_credentials(cdn_user, cdn_key)
    except Exception, e:
        print "!!!!!!! EXCEPTION: Failed to set credentials !!!!! %s" % e
        return 1

    try:
        # Set public to False to use ServiceNet (Untested)
        cf = pyrax.connect_to_cloudfiles(region=region, public=True)
    except Exception, e:
        print "!!!!!!! EXCEPTION: Failed to connect to cloud files !!!!! %s" % e
        return 1

    try:
        container = cf.get_container(container)
        # pyrax.exceptions.NoSuchContainer is a good candidate for a targeted
        # catch, but we're being general for today.
    except Exception, e:
        print "!!!!!!! EXCEPTION: Failed to lookup container !!!!! %s" % e
        return 1

    try:
        # This returns an object for the uploaded file, but it isn't
        # particularly useful in this script.
        container.upload_file(src)
    except Exception, e:
        print "!!!!!!! EXCEPTION: Failed to upload file !!!!! %s" % e
        return 1

    return 0

def main():
    if (len(sys.argv) < 5):
        print "Syntax: cloud-upload <source-file> <target-container> <cdn-user> <cdn-api-key>"
        return 1

    # Recommend looking into argparse for better argument handling.
    return upload_file(src = os.path.normpath(sys.argv[1]),
                       container = sys.argv[2],
                       cdn_user = sys.argv[3],
                       cdn_key = sys.argv[4],
                       region = "DFW")

if __name__ == '__main__':
    sys.exit(main())
