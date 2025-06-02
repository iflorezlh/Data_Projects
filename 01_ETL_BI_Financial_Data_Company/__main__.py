import pandas as pd
import requests
import os

def get_alpha_financials(statement, ticker, api_key):

    try:
        url = f'https://www.alphavantage.co/query?function={statement}&symbol={ticker}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()
        print(f'Llamado al {statement} exitoso')

        try:
            df = pd.json_normalize(data['annualReports'])
            return df
        except KeyError:
            print(f"No se encontró 'annualReports' en la respuesta: {data}")
            return pd.DataFrame()
    except Exception as e:
        print(f'Error {e} llamando a la API')
        return pd.DataFrame()


def incremental_csv_writer(df_new, file_path):
    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path, sep=',')
        df_new = pd.concat([df_old, df_new]).drop_duplicates(
            subset=['fiscalDateEnding', 'Ticker'], keep='last'
        )
    df_new.to_csv(file_path, index=False)
    
if __name__ == "__main__":
    
    statements = ['INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW']
    ticker = input("Write the company's ticker: ").upper()
    api_key = "CYR8CFKJA6X64BOR" 

    for statement in statements:
        df = get_alpha_financials(statement, ticker, api_key)
        if not df.empty:
            df['Ticker'] = ticker
            df.replace(to_replace=['None', None], value=0, inplace=True)
            incremental_csv_writer(df, f"{statement}.csv")
        else:
            print(f"No hay datos para guardar para {statement}")