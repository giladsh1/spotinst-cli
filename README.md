# spotinst-cli
spotinst-cli is is an interactive command line tool which allows you to to control your spotinst groups and instances.

### Installation 
```
pip install spotinstcli
```

### Usage  

spotinst-cli has the following flags -
```
  -h, --help                     show this help message and exit
  -a ACCOUNT, --account=ACCOUNT  spotinst account id defined as environment variable
  -g GREP, --grep=GREP           text to filter groups by
  -u UNGREP, --ungrep=UNGREP     text to exclude groups
  -l, --list                     show group list and exit
  -j, --json                     output pure json -- useful for piping into json parsers like jq
  -d, --get-data                 get groups data from spotinst
  -s, --get-status               get groups status  
  --get-health                   get groups health per instance
  --min=MIN                      update group minimum capacity, must supply with max and target
  --target=TARGET                update group target capacity, must supply with min and max
  --max=MAX                      update group maximum capacity, must supply with min and target
  --scale-up=SCALE_UP            scale up group by X number of instances
  --scale-down=SCALE_DOWN        scale down group by X number of instances
  --suspend                      suspend group activities
  --unsuspend                    unsuspend group activities
  --suspension-status            get groups suspension status  
  --roll                         roll a group, must supply batch-size, and grace-period
  --batch-size=BATCH             roll batch size - must supply with the roll flag
  --grace-period=GRACE           roll grace period - must supply with the roll flag
  --replace-ami=AMI              replace AMI for group
  --replace-health=HEALTH        replace the health check type - can be HCS, EC2, ELB
  --set-user-data=USER_DATA      updated user data - supply a file path which contains the user data script (cloud init)
  --get-user-data                fetch the user data script (cloud init)
  --roll-status                  check the status of deployments
  -y, --skip-validation          skip prompt validation for non-interactive mode
```

### Multiple Accounts
spotinst-cli can use environment variables to reference multiple provider accounts.  
Set variables like:

    export spotinst_account_prod="act-asdfasdf"
    export spotinst_account_qa="act-hjklhjkl"
    export spotinst_account_dev="act-zxcvzxcv"

    $> spotinst-cli --account prod

    ====================================================
        Getting groups from Spotisnt, please wait...
    ====================================================
    
    ===================================
        Found the following groups:
    ===================================

    +---+-------------------------------+--------------+-----+--------+-----+
    | # | Group name                    | ID           | Min | Target | Max |
    +---+-------------------------------+--------------+-----+--------+-----+
    | 1 | Group-A                       | sig-adsfadfd | 0   | 0      | 200 |
    | 2 | Group-B                       | sig-fddgdfgd | 0   | 0      | 200 |
    | 3 | Group-C                       | sig-hdfhsfdg | 0   | 52     | 200 |
    | 4 | Web Servers                   | sig-hfhdgdhg | 0   | 0      | 4   |
    | 5 | ECS                           | sig-dfghdfgh | 1   | 8      | 12  |
    +---+-------------------------------+--------------+-----+--------+-----+

SpotInst account ids can be found in the web console under settings/account for each of your accounts.  
There is currently no way to pull account ids from the SpotInst API.  


