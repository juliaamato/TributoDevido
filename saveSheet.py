import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from backend import select, connect, disconnect

def get_data_from_db():
    conn = connect()
    
    data = select(conn)

    disconnect(conn)

    df = pd.DataFrame(data, columns=['ID', 'Payment', 'Payment_Method', 'Contract', 'Experience', 'Project', 'Work', 'Description', 'Tags'])
    return df

def insert_data_to_google_sheets(df, spreadsheet_id):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/julia/Documents/Programacao/Projeto Tributo Devido/idyllic-root-439113-t5-9d29fc346aea.json', scope)
    
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(spreadsheet_id).sheet1
    
    existing_data = sheet.get_all_records()
    existing_df = pd.DataFrame(existing_data)

    print("Dados existentes na planilha:")
    print(existing_df)

    if 'ID' in existing_df.columns:
        new_data = df[~df['ID'].isin(existing_df['ID'])]
    else:
        print("A coluna 'ID' não existe no DataFrame existente. Inserindo todos os novos dados.")
        new_data = df

    data_to_insert = new_data.values.tolist()
    
    if data_to_insert:
        sheet.insert_rows(data_to_insert, 2)
        print("Dados inseridos com sucesso.")
    else:
        print("Nenhum dado novo para inserir.")

if __name__ == "__main__":
    data = get_data_from_db()
    spreadsheet_id = '1EXkgDp-SqXBIH6HULlIaXqWTbf-miTm3vO4bNkhrSRM'
    insert_data_to_google_sheets(data, spreadsheet_id)
