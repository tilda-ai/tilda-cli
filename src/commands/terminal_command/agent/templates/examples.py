examples = [
    {
        "role": "system",
        "name": "example_user",
        "content": "squash all commits",
    },
    {
        "role": "system",
        "name": "example_agent",
        "content": """{
  "completions": [
    {
      "description": "Squashes all commits into one in the current Git branch",
      "content": "git reset --soft $(git rev-list --max-parents=0 HEAD) && git commit --amend --edit",
      "chainable": false,
      "chain_delimiter": null,
      "sudo": false,
      "dangerous": true,
      "interactive": false,
      "order": 1,
      "confidence": 95,
      "sources": [
        "https://git-scm.com/docs/git-reset",
        "https://git-scm.com/docs/git-commit"
      ]
    }
  ]
}""",
    },
]
