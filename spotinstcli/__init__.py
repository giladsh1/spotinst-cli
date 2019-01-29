#!/usr/bin/env python

from optparse import OptionParser

valid_suspension_types = ["AUTO_SCALE", "AUTO_HEALING", "OUT_OF_STRATEGY","PREVENTIVE_REPLACEMENT","REVERT_PREFERRED", "ALL"]

# function to split parsed option to list by comma
def parser_split(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

# function validate suspension input
def validate_suspension(option, opt, value, parser):
    if value not in valid_suspension_types:
        print "invalid suspension value: '{value}'!\nValid values are: {list}\n".format(value=value, list=", ".join(valid_suspension_types))
        exit()
    # if value is set to ALL pass all process and remove ALL
    if value == 'ALL':
        processes_list = list(valid_suspension_types)
        processes_list.remove("ALL")
        setattr(parser.values, option.dest, processes_list)
    else:
        setattr(parser.values, option.dest, [value])


def main():
    # define help and options
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-a", "--account", action="store", dest="account",
                      help="spotinst account id environment variable label - define an environment variable like "
                           "spotinst_account_prod=\"act-asdfasdf\" and call with \"-a prod\"; "
                           "SpotInst account ids can be found in the web interface under Settings > Account")

    parser.add_option("-g", "--grep", type="string", action="callback", dest="grep", callback=parser_split, default="",
                      help="text to filter groups by")

    parser.add_option("-u", "--ungrep", type="string", action="callback", default="", callback=parser_split,
                      dest="ungrep", help="text to exclude groups")

    parser.add_option("-l", "--list", action="store_true", dest="list", help="show group list and exit")

    parser.add_option("-j", "--json", action="store_true", dest="json",
                      help="output pure json -- useful for piping into json parsers like jq")

    parser.add_option("-d", "--get-data", action="store_true", dest="data", help="get groups config data")

    parser.add_option("-s", "--get-status", action="store_true", dest="status", help="get groups current status")

    parser.add_option("--get-health", action="store_true", dest="health_status", help="get groups health per instance")

    parser.add_option("--min", action="store", dest="min", type=int,
                      help="update group minimum capacity, must suuply with max and target")

    parser.add_option("--target", action="store", dest="target", type=int,
                      help="update group target capacity, must supply with min and max")

    parser.add_option("--max", action="store", dest="max", type=int,
                      help="update group maximum capacity, must supply with min and target")

    parser.add_option("--scale-up", action="store", dest="scale_up", type=int,
                      help="scale up group by X number of instances")

    parser.add_option("--scale-down", action="store", dest="scale_down", type=int,
                      help="scale down group by X number of instances")

    parser.add_option("--suspend", type="string", default=None, action="callback", callback=validate_suspension,
                      dest="suspend", help="suspend scaling or healing for a group")

    parser.add_option("--unsuspend", type="string", default=None, action="callback", callback=validate_suspension,
                      dest="unsuspend", help="unsuspend scaling or healing for a group")

    parser.add_option("--suspension-status", action="store_true", dest="suspension", default="",
                      help="get groups suspension status")

    parser.add_option("--roll", action="store_true", dest="roll",
                      help="roll a group, must supply batch-size, and grace-period")

    parser.add_option("--batch-size", action="store", dest="batch", type=int,
                      help="roll batch size - must supply with the roll flag")

    parser.add_option("--grace-period", action="store", dest="grace", type=int,
                      help="roll grace period - must supply with the roll flag")

    parser.add_option("--replace-ami", action="store", dest="ami", help="replace AMI for group")

    parser.add_option("--replace-health", action="store", dest="health", choices=['EC2', 'ELB', 'HCS'],
                      help="replace health check type - valid options: EC2, ELB, HCS")

    parser.add_option("--set-user-data", action="store", dest="set_user_data",
                      help="updated user data - supply a file path which contains the user data script (cloud init)")

    parser.add_option("--get-user-data", action="store_true", dest="get_user_data",
                      help="fetch the user data script (cloud init)")

    parser.add_option("--roll-status", action="store_true", dest="roll_status", help="check the status of deployments")

    parser.add_option("-y", "--skip-validation", action="store_true", dest="skip_validation",
                      help="skip prompt validation for non-interactive mode")

    (options, _) = parser.parse_args()

    import spotinstcli
    spotinstcli.main(options)

if __name__ == "__main__":
    main()


