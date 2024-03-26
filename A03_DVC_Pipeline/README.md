### Repo Structure
```
data-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── __init__.py
│   ├── download.py
│   ├── prepare.py
│   ├── process.py
│   └── evaluate.py
├── dvc.yaml
├── params.yaml
├── README.md
└── .gitignore
```

### Commands
* `dvc init --subdir`
* `dvc add data`
* `git add .gitignore data.dvc`
* `git rm -r --cached 'data\raw'`
* `dvc stage add -n download --force --deps params.yaml -o data/raw --wdir=. "python src/download.py"`
