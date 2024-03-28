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
* `dvc stage add -n prepare --force --deps data/raw --deps src/prepare.py -o outputs/processed/ground_truth.csv --wdir=. "python src/prepare.py"`
* `dvc stage add -n process --force --deps data/raw --deps src/process.py -o outputs/processed/computed_aggregates.csv --wdir=. "python src/process.py"`
* `dvc stage add -n evaluate --force --deps outputs/processed/ground_truth.csv --deps outputs/processed/computed_aggregates.csv --deps src/evaluate.py --wdir=. "python src/evaluate.py"`
* `dvc dag`


<!--  -->
git add 'outputs\processed\.gitignore' dvc.yaml
git add dvc.yaml 'outputs\processed\.gitignore'
git add dvc.yaml

```
          +----------+
          | download |
          +----------+
          ***        ***
         *              *
       **                **
+---------+           +---------+
| process |           | prepare |
+---------+           +---------+
          ***        ***
             *      *
              **  **
          +----------+
          | evaluate |
          +----------+
```

* `dvc repro`