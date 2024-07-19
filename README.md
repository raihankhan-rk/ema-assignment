# ema-assignment

## Quick Demo

Check out the Demo of the Sales Development Representative [here](https://www.loom.com/share/9d25035163e64affbdaf71fe7e60a25d?sid=8806edd0-9610-4bf6-8a9b-374eee102a58)


## Run Locally

Clone the project

```bash
  git clone https://github.com/raihankhan-rk/ema-assignment.git
```

Create a Virtual Environment
```bash
  python3 -m venv .venv
  source .venv/bin/activate
```

Install necessary libraries and SDKs

```bash
  pip install -r requirements.txt
```

Run the script to merge the datasets into one

```bash
  python combine_csv.py
```

Add your secret keys in the ```.env.local``` file and rename it to ```.env```

```
OPENAI_API_KEY=
EMAIl_USERNAME=
EMAIL_PASSWORD=
```

Run the AI Agent
```
python agent.py
```

## NOTE
This agent is not conversational yet. So it does not have any context of previous converstaions whatsoever.