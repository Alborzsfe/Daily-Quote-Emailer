# Daily Quote Emailer

A small Python script that reads recipients from a CSV file and sends each person a randomly selected inspirational quote through Gmail SMTP.

## Security

Credentials are read from environment variables and must never be committed. If a credential has ever appeared in Git history, revoke it before using this project.

## Setup

```bash
git clone https://github.com/Alborzsfe/Daily-Quote-Emailer.git
cd Daily-Quote-Emailer
cp recipients.example.csv recipients.csv
```

Set these environment variables:

- `SMTP_SENDER_EMAIL`: Gmail address used to send messages
- `SMTP_APP_PASSWORD`: a newly generated Gmail App Password
- `RECIPIENTS_CSV`: optional CSV path; defaults to `recipients.csv`

The CSV must contain `name` and `email` columns.

Run once:

```bash
python main.py
```

Use your operating system scheduler or GitHub Actions with repository secrets if you need daily execution. Never put a password directly in a workflow file.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Privacy

`recipients.csv` is ignored by Git because it can contain personal data. Only the anonymized example file belongs in the repository.

## License

MIT
