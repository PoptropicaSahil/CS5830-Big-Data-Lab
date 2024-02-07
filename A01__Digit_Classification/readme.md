# Assingment 1 on Digit Classification

It is recommened to create a virtual environment using venv before proceeding. \
To install the required packages, use the following command `pip install -r requirements.txt`

## Running the code
Ensure you are in the same directory as this file and run
```
python main.py --data_dir (default: "./data") --oversample_rate (default: 2)
```
To run the pytest tests, run `pytest pytests/`. This will run all the files within the pytest directory.


## Additional information
- **Please check the `logs` directory for script running logs and model training logs**
- Plots and figures will be stored in the `plots` directory
- Performance metrics will be stored in the `performance_metrics` directory
- All grading functions are stored in the `grading_tasks` directory

## Reports
- The best model, trained on all orientations, achieves more than 99% accuracy on the holdout set. 
- The confusion matrix shows how numbers such as $2$ and $7$ can have a slight chance of being misclassified as each other. *This is fairly expected due to their similar orientation and shape*
