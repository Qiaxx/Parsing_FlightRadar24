import pandas as pd
import glob
import os

def load_all_csv_files(folder_path):
    """Загрузка всех CSV-файлов в папке."""
    csv_files = glob.glob(os.path.join(folder_path, "flights_black_sea_*.csv"))
    df_list = [pd.read_csv(f) for f in csv_files]
    return pd.concat(df_list, ignore_index=True)

def create_daily_report(df):
    """Создание отчёта по авиакомпаниям и моделям."""
    # Преобразуем timestamp в дату
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['date'] = df['timestamp'].dt.date

    # Группировка по дате и авиакомпании
    by_airline = df.groupby(['date', 'airline_name']).size().reset_index(name='num_flights')
    by_model = df.groupby(['date', 'aircraft_model']).size().reset_index(name='num_flights')

    return by_airline, by_model

def save_reports(airline_report, model_report):
    airline_report.to_csv('report_by_airline.csv', index=False)
    model_report.to_csv('report_by_model.csv', index=False)
    print("✅ Витрина сохранена: report_by_airline.csv и report_by_model.csv")

def main():
    folder = '.'  # папка с CSV
    df = load_all_csv_files(folder)
    airline_report, model_report = create_daily_report(df)
    save_reports(airline_report, model_report)

if __name__ == '__main__':
    main()
