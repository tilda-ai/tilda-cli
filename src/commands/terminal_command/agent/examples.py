examples = [
    # Example 1
    {
        "role": "system",
        "name": "example_user",
        "content": "check the status of all docker containers and restart any that are stopped",
    },
    {
        "role": "system",
        "name": "example_agent",
        "content": """
            {
                "completions": [
                    {
                        "responseType": "script",
                        "systemMessage": "Check Docker container status",
                        "shellScript": "docker ps -a",
                        "executionOrder": 1,
                        "isChainable": false
                    },
                    {
                        "responseType": "script",
                        "systemMessage": "Restart stopped Docker containers",
                        "shellScript": "docker restart $(docker ps -a -q -f status=exited)",
                        "executionOrder": 2,
                        "isChainable": false
                    }
                ]
            }
        """,
    },
    # Example 2
    {
        "role": "system",
        "name": "example_user",
        "content": "compress all logs older than 30 days in the logs folder and move them to an archive directory",
    },
    {
        "role": "system",
        "name": "example_agent",
        "content": """
            { 
                "completions": [
                    {
                        "responseType": "script",
                        "systemMessage": "Compress old log files",
                        "shellScript": "find {{project_root_path}}/logs -mtime +30 -exec gzip {} \\;",
                        "executionOrder": 1,
                        "isChainable": true
                    },
                    {
                        "responseType": "script",
                        "systemMessage": "Move compressed logs to archive",
                        "shellScript": "mv {{project_root_path}}/logs/*.gz {{project_root_path}}/archive/",
                        "executionOrder": 2,
                        "isChainable": false
                    }
                ]
            }
        """,
    },
    # Example 3
    {
        "role": "system",
        "name": "example_user",
        "content": "create a cron job to clear cache every sunday at midnight",
    },
    {
        "role": "system",
        "name": "example_agent",
        "content": """
            {
                "completions": [
                    {
                        "responseType": "script",
                        "systemMessage": "Set up cron job for clearing cache",
                        "shellScript": "(crontab -l 2>/dev/null; echo '0 0 * * 0 rm -rf {{project_root_path}}/cache/*') | crontab -",
                        "executionOrder": 1,
                        "isChainable": false
                    }
                ]
            }
        """,
    },
    # Example 4
    {
        "role": "system",
        "name": "example_user",
        "content": "what can I do to improve the security of my server?",
    },
    {
        "role": "system",
        "name": "example_agent",
        "content": """
            {
                "completions": [
                    {
                        "responseType": "error",
                        "systemMessage": "While I could prossibly provide some general tips, I am not the right agent to help with this query.",
                    }
                ] 
            }   
        """,
    },
    # {
    #     "role": "system",
    #     "name": "example_user",
    #     "content": "",
    # },
    # {
    #     "role": "system",
    #     "name": "example_agent",
    #     "content": "",
    # },
]
