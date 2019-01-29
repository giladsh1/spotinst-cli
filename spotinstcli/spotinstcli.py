#!/usr/bin/env python

# This tool allows the user to interact with spotinst API
# run the script with the -h flag for help

import spotfunctions
from json import loads as json_loads, dumps as json_dumps
from os import environ
from sys import argv, exit as sys_exit
from os import path
from base64 import b64encode, b64decode


def main(args):
    # main variables
    base_api_path = "https://api.spotinst.io/aws/ec2/group"
    http_method = 'GET'  # set as the default method, and overwrite when necessary
    thread_list = []
    requests_queue = []
    group_placeholder = "__group_id__"
    payload = None
    user_validation = False

    # validate input
    if any([args.min, args.max, args.target]) and not all([args.min, args.max, args.target]):
        spotfunctions.error_and_exit("you must supply max, min and target together!")
    if args.roll and not all([args.batch, args.grace]):
        spotfunctions.error_and_exit("you must supply batch size and grace period with the roll flag!")
    if args.json:
        if args.get_user_data:
            spotfunctions.error_and_exit("user data cannot be printed as a json output!")
    
    # check token
    token = environ.get('spotinst_token')
    if not token:
        spotfunctions.error_and_exit("you must define an environment variable called 'spotinst_token' with a valid token (use export or .bashrc file)!")
    
    # check for Spotinst account
    if args.account:
        environment_var = "spotinst_account_{args.account}".format(**locals())
        account = environ.get(environment_var)
        if account is None:
            spotfunctions.error_and_exit("could not find the environment variable: {environment_var}".format(**locals()))
    else:
        account = None
    
    # get all groups that matches the search
    groups_to_update = spotfunctions.get_groups(base_api_path, token, account, args.grep, args.ungrep, args.json)
    if len(groups_to_update) == 0:
        spotfunctions.error_and_exit("could not find any groups for the search term: {}".format(args.grep))
    spotfunctions.print_all_groups(groups_to_update, args.json, args.list)
    
    # if the list flag was triggered, need to exit
    if args.list:
        sys_exit(0)
    
    # get data request
    if args.data:
        req_uri = "{}/{}".format(base_api_path, group_placeholder)
    
    # get status request
    elif args.status:
        req_uri = "{}/{}/status".format(base_api_path, group_placeholder)
    
    elif args.health_status:
        req_uri = "{}/{}/instanceHealthiness".format(base_api_path, group_placeholder)
    
    # get user data script
    elif args.get_user_data:
        req_uri = "{}/{}".format(base_api_path, group_placeholder)
    
    # get roll status
    elif args.roll_status:
        req_uri = "{}/{}/roll".format(base_api_path, group_placeholder)
    
    # get suspension status
    elif args.suspension:
        req_uri = "{}/{}/suspension".format(base_api_path, group_placeholder)
    
    # suspend / un-suspend equest
    elif any([args.suspend, args.unsuspend]):
        req_uri = "{}/{}/suspension".format(base_api_path, group_placeholder)
        if args.suspend:
            http_method = 'POST'
            payload = json_dumps({"processes": args.suspend})
        elif args.unsuspend:
            http_method = 'DELETE'
            payload = json_dumps({"processes": args.unsuspend})
    
    # scale up / down
    elif any([args.scale_down, args.scale_up]):
        http_method = 'PUT'
        if args.scale_up:
            command = "up"
            adjustment = args.scale_up
        else:
            command = "down"
            adjustment = args.scale_down
        req_uri = "{}/{}/scale/{}\?adjustment={}".format(base_api_path, group_placeholder, command, adjustment)
    
    # set target, max and min
    elif all([args.min, args.target, args.max]):
        http_method = 'PUT'
        payload = json_dumps({ "group": { "capacity": { "target": args.target, "minimum": args.min , "maximum": args.max }}})
        req_uri = "{}/{}".format(base_api_path, group_placeholder)
    
    # roll request
    elif all([args.roll, args.batch, args.grace]):
        http_method = 'PUT'
        req_uri = "{}/{}/roll".format(base_api_path, group_placeholder)
        payload = json_dumps({ "batchSizePercentage" : args.batch, "gracePeriod" : args.grace })
    
    # replace ami and health type
    elif any([args.ami, args.health]):
        http_method = 'PUT'
        req_uri = "{}/{}".format(base_api_path, group_placeholder)
        if args.ami:
            payload = json_dumps({ "group": { "compute": { "launchSpecification": { "imageId": args.ami  }}}})
        else:
            payload = json_dumps({"group": {"compute": {"launchSpecification": {"healthCheckType": args.health}}}})
    
    # replace user data script
    elif args.set_user_data:
        if not path.isfile(args.set_user_data):
            spotfunctions.error_and_exit("{} is not a valid file name!".format(args.set_user_data))
        with open(args.set_user_data, "r") as f:
            user_data_script = f.read()
        user_data_script = b64encode(user_data_script)
        req_uri = "{}/{}".format(base_api_path, group_placeholder)
        http_method = 'PUT'
        payload = json_dumps({ "group": { "compute": { "launchSpecification": { "userData": user_data_script  }}}})
    
    else:
        # user supplied no other choice other than grep / ungrep - exit
        sys_exit(0)
    
    
    # make sure the user wants to continue with the current filter (unless the req type is GET)
    if not user_validation and http_method != 'GET':
        if args.json and not args.skip_validation:
            spotfunctions.error_and_exit("you must supply the -y option for json format")
        if not args.skip_validation:
            if not spotfunctions.prompt_for_conformation():
                print "Existing...\n"
                sys_exit(0)
        else:
            if not args.json:
                print "Found skip validation option, skipping user prompt...\n"
        user_validation = True
        if not args.json:
            spotfunctions.print_message("Updating groups - hold on...")

    # loop through each group and update
    for group, group_values in groups_to_update.iteritems():
        group_id = group_values[0]
        group_req_uri = req_uri.replace(group_placeholder, group_id)
        try:
            spotfunctions.open_thread(thread_list, spotfunctions.query_thread, (requests_queue, group, group_req_uri, token, http_method, payload, account))
        except Exception as e:
            spotfunctions.error_and_exit(e)
    
    # wait for all threads to finish
    for thread in thread_list:
        thread.join()
    
    # print the results
    for result in requests_queue:
        http_method = result[0]
        request_result = result[1]
        request_group = result[2]
        group_result = {"group": request_group, "content": json_loads(request_result.content), "request_status_code": request_result.status_code}
        if args.json:
            print json_dumps(group_result, indent=2, sort_keys=True)
        else:
            spotfunctions.print_header(request_group)
            if request_result.status_code == 200:
                if http_method == 'GET':
                    if not args.get_user_data:
                        print request_result.content
                    else:
                        print b64decode(json_loads(request_result.content)['response']['items'][0]['compute']['launchSpecification']['userData'])
                else:
                    spotfunctions.print_in_color('green', "Update was successful!")
            else:
                try:
                    data = json_loads(request_result.content)
                except:
                    data = None
                    spotfunctions.print_in_color('red', "Error while updating group!\nstatus code: {}".format(request_result.status_code))
                if data is not None:
                    print "request content: {}".format(data['response']['errors'][0]['message'])
    
    if not args.json:
        spotfunctions.print_message("Done executing on all groups! ")


if __name__ == "__main__":
    args = argv[1]
    main(args)