# data_analysis_web_app

Проект для анализа данных csv таблиц, написанный с использованием следующих технологий:
+ HTML
+ CSS
+ JS
+ Boostrap 5
+ Python
+ Pandas
+ plotly
+ ydata-profiling

## Инструкция по запуску
1. [Скачать и установить Python](https://www.python.org/downloads/)
2. Клонировать данный репозиторий: 
```
git clone https://github.com/DogeOk/data_analysis_web_app.git
```
3. Переместиться в каталог репозитория:
```
cd data_analysis_web_app
```
4. (Рекомендуется) Создать виртуальное окружение:
```
python -m venv data_analysis_web_app
```
5. Активировать виртуальное окружение (если было создано):
   - Windows:
   ```
   .\data_analysis_web_app\Scripts\activate
   ```
   - macOS или Linux:
   ```
   source data_analysis_web_app/bin/activate
   ```
6. Установить необходимые пакеты из файла `requirements.txt`:
```
pip install -r requirements.txt
```
7. Запустить проект:
```
python -m flask --app start run
```