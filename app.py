
from flask import Flask, current_app, jsonify, request
import pandas as pd
import io



app = Flask(__name__)


def reset_stats():
    current_app.fRevenue = 0.0
    current_app.fExpenses = 0.0
    current_app.fNetRevenue = 0.0
    




@app.route('/')
def list_usage():
    return 'ToDo: Add usage instructions'

@app.route('/reset')
def reset():
    reset_stats()
    return jsonify({"Message": "Transaction data reset"}), 200

@app.route('/report', methods=['GET'])
def report_stats():
    with app.app_context():
        return jsonify(
                { "gross-revenue": current_app.fRevenue,
                "expenses": current_app.fExpenses,
                "net-revenue": current_app.fRevenue-current_app.fExpenses
                }
            ),200
        


@app.route('/transactions', methods=['POST'])
def upload_file():
    with app.app_context():
        if 'file' not in request.files:
            return jsonify({"error": "No file part; Please provide expense file"}), 400
        
        file = request.files['file']
        
        if file:
            # Read the file into a pandas DataFrame
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            dataStore=  pd.read_csv(stream, header=None)
            
            dataStore_cleanedup=dataStore[dataStore[0].notna() & (dataStore[0]!='' )
                                        & dataStore[1].notna() & (dataStore[1]!='')
                                        & dataStore[2].notna() & (dataStore[2]!='')
                                        ]
            
            dataStore_cleanedup.loc[:, 1] = dataStore_cleanedup[1].str.strip()
            uploadSummary=dataStore_cleanedup.groupby(1)[2].sum()
            
            batchRevenue= uploadSummary.get('Income',0) 
            current_app.fRevenue+= batchRevenue
            batchExpense=uploadSummary.get('Expense',0)
            current_app.fExpenses+=batchExpense

            return jsonify({"message": "Data processed succefully",
                            "Revenue_from_curent_upload= " : batchRevenue,
                            "Expense_from_current_upload" : batchExpense,
                            "Net_income_from_current_upload" : batchRevenue-batchExpense,
                            "Total_revenue_so_far" : current_app.fRevenue,
                            "Total_expenses_so_far": current_app.fExpenses,
                            "Net_income_so_far": current_app.fRevenue-current_app.fExpenses
            })
            



if __name__ == '__main__':
    with app.app_context():
        reset_stats()  # Initialize stats
    app.run(host="127.0.0.6", port=5005, debug=True)



# cURL pattern that works C:\Windows\System32\curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@data.csv" http://127.0.0.6:5005/transactions

