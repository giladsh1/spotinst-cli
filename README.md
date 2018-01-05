# spotinst-cli
spotinst-cli is is an interactive command line tool which allows you to to control your spotinst groups and instances.

### Usage  

spotinst-cli has the following flags -
```
  -h, --help            show this help message and exit
  -g GREP, --grep=GREP  text to filter groups by
  -d, --get-data        get groups data
  -s, --get-status      get groups status
  --suspension-status   get groups suspension status
  -u UNGREP, --ungrep=UNGREP
                        text to exclude groups
  -l, --list            show group list and exit
  --min=MIN             update group minimum capacity, must suuply with max
                        and target
  --target=TARGET       update group target capacity, must supply with min and
                        max
  --max=MAX             update group maximum capacity, must supply with min
                        and target
  --scale-up=SCALE_UP   scale up group by X number of instances
  --scale-down=SCALE_DOWN
                        scale down group by X number of instances
  --suspend=SUSPEND     suspend scaling or healing for a group
  --unsuspend=UNSUSPEND
                        unsuspend scaling or healing for a group
  --roll                roll a group, must supply batch-size, and grace-period
  --roll-status         check the status of deployments
  --batch-size=BATCH    roll batch size - must supply with the roll flag
  --grace-period=GRACE  roll grace period - must supply with the roll flag
  --replace-ami=AMI     replace AMI for group
  --replace-health=HEALTH
                        replace health check type for a group
  --user-data=USER_DATA
                        updated user data - supply a file path which contains
                        the user data script (cloud init)
  --get-user-data       fetch the user data script (cloud init)
  --detach-batch        detach all instances for specific batch - choose from
                        a list of batches
  -j, --json            output pure json -- useful for piping into json
                        parsers like jq
  -y, --skip-validation
                        skip prompt validation for non-interactive mode
  -a ACCOUNT, --account=ACCOUNT
                        spotinst account id environment variable label -
                        define an environment variable like
                        spotinst_account_prod="act-asdfasdf" and call with "-a
                        prod"; SpotInst account ids can be found in the web
                        interface under Settings > Account
  -q, --quiet           do not print headers and labels
```

### Multiple Accounts
spotinst-cli can use environment variables to reference multiple provider accounts. Set variables like:

    export spotinst_account_prod="act-asdfasdf"
    export spotinst_account_qa="act-hjklhjkl"
    export spotinst_account_dev="act-zxcvzxcv"

    [user@server:~] $ spotinst-cli -a prod

    Querying spotinst API, hold on...

    ###################################
    Found the following groups:
    ###################################

    +---+-------------------------------+--------------+-----+--------+-----+
    | # | Group name                    | ID           | Min | Target | Max |
    +---+-------------------------------+--------------+-----+--------+-----+
    | 1 | Group-Primary-2.5.30          | sig-adsfadfd | 0   | 0      | 200 |
    | 2 | Group-Secondary-2.5.32        | sig-fddgdfgd | 0   | 0      | 200 |
    | 3 | Group-Standby-2.6.35          | sig-hdfhsfdg | 0   | 52     | 200 |
    | 4 | Web Servers                   | sig-hfhdgdhg | 0   | 0      | 4   |
    | 5 | ECS                           | sig-dfghdfgh | 1   | 8      | 12  |
    +---+-------------------------------+--------------+-----+--------+-----+

SpotInst account ids can be found in the web console under settings/account for each of your accounts. There is currently no way to pull account ids from the SpotInst API.

### Example usage
#### list groups with name filter:
![](docs/list_groups.png)

#### get data:
![](docs/get_data.png)

#### get status:
![](docs/get_status.png)

#### get suspension status:
![](docs/suspension_status.png)

#### update capacity:
![](docs/update_capacity.png)

#### scale up:
![](docs/scale_up.png)

#### replace AMI:
![](docs/replace-ami.png)

#### detach specific batch:
![](docs/detach_batch.png)
