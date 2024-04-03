# # Assignment 3 on DVC and Git

It is recommened to create a virtual environment using venv before proceeding. \
To install the required packages, use the following command `pip install -r requirements.txt`

## ✅ Running the code ✅
Set your parameters in the `params.yaml` file. Then ensure you are in the same directory as this file and run
```
dvc repro
```

> **Please check the `logs` directory for script running logs.**

## Star points!
- Python's inbuilt `concurrent` is leveraged for parallel processing of csv files
- Check 20x the required files (`n_locs`) before downloading *nice* csv files. Otherwise switch to default csv files (pre-downloaded from the archive)
- Input variables boundary and type checks are done in the `download.py` file


## 📊 Reports 📊
- The result $R^2$ scores are shown at the end of the logs output.


## ➕ The Process ➕

### Setting Git and DVC 

```bash
$ dvc init --subdir
$ dvc add data
$ git add .gitignore data.dvc
$ git rm -r --cached 'data\raw' # not logging the (usually large) data files
```

### Configure dvc (local) remote storage
```bash
$ mkdir -p /tmp/dvc_storage
$ dvc remote add --default loc_remote /tmp/dvc_storage # Setting 'loc_remote' as a default remote.
$ git add .dvc/config
$ git commit -m "Configure remote storage loc_remote"
```


### Setup the pipeline
```bash
$ dvc stage add -n download --force -p year -p n_locs -o data/raw --wdir=. "python src/download.py" 
$ dvc stage add -n prepare --force --deps data/raw --deps src/prepare.py -o outputs/processed/ground_truth.csv --wdir=. "python src/prepare.py"
$ dvc stage add -n process --force --deps data/raw --deps src/process.py -o outputs/processed/computed_aggregates.csv --wdir=. "python src/process.py"
$ dvc stage add -n evaluate --force --deps outputs/processed/ground_truth.csv --deps outputs/processed/computed_aggregates.csv --deps src/evaluate.py --wdir=. "python src/evaluate.py"
```

### Visualise the DAG
```bash
$ dvc dag
```

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

### Run the pipeline
```bash
$ dvc repro --no-run-cache --force-downstream
```
```
Running stage 'download':
> python src/download.py
Updating lock file 'dvc.lock'

Running stage 'prepare':
> python src/prepare.py
Updating lock file 'dvc.lock'

Running stage 'process':
> python src/process.py
Updating lock file 'dvc.lock'

Running stage 'evaluate':
> python src/evaluate.py
Updating lock file 'dvc.lock'
```

### Show the experiemnts
```bash
$ dvc exp show --md
```
```
| Experiment  | Created      | year | n_locs | data\raw                             | outputs\processed\computed_aggregates.csv | outputs\processed\generated  |
|-------------|--------------|------|--------|--------------------------------------|-------------------------------------------|------------------------------|
| workspace   | -            | 2012 | 3      | 48f621f2a995a14cd4763a5dac4fd3ba.dir | e8ecd04800ace72e97dba01650cecd1f          | b1120c4d08a162545d8          |
| main        | Mar 31, 2024 | 2011 | 2      | cce8892cc425e351c8be37df222617c3.dir | 7bd7a1664d85ce97ceb0c3d540daa5af          | ed9a07c7e0125ef11dd          |
```

### Compare the experiments
```bash
$ dvc params diff
```

```
Path         Param    HEAD    workspace
params.yaml  n_locs   2       3        
params.yaml  year     2011    2012   
```

### Additional commands to log into Git and DVC
```bash
$ git add 'outputs\processed\.gitignore' dvc.yaml
$ git add dvc.yaml 'outputs\processed\.gitignore'
$ git add dvc.yaml
$ git add * # add the output files also
$ git push
$ dvc push
```
### Ensure experiments are logged 
* [Github repo (Private!)](https://github.com/PoptropicaSahil/CS5830-Big-Data-Lab)
* dvc repo is local!



## 😁 Code-cleanliness! 😁
- Type hints from the `typing` module are leveraged
- All code is pep-8 style formatted using `ruff`, `isort` and `black` as pre-commit hooks


## 📚References 📚
- Git and DVC Documentation


## 🗺 Repo Structure 🗺
```
data-pipeline/
├── data/
│   ├── raw/
│   ├── default/
│   └── .gitignore
├── src/
│   ├── __init__.py
│   ├── download.py
│   ├── prepare.py
│   ├── process.py
│   └── evaluate.py
├── outputs/processed/
│   ├── computed_aggregates.csv
│   └── ground_truth.csv
├── logs/
│   └── logs.log
├── utils/
│   └── logging_config.py
├── venv/
├── .dvc/
├── dvc.yaml
├── dvc.lock
├── params.yaml
├── reqiurements.txt
├── README.md
└── .gitignore
```

