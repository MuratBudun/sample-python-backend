# Python Sample Backend

## Development
     
### Create virtual envoriment
```bash
python -m venv .venv
```
### Activate virtual envoriment
- Windows
    ```powershell
    .\.venv\Scripts\activate    
    ```
- macOS/Linux
    ```bash
    source ./.venv/bin/activate    
    ```
### Requirements 
- pip upgrade
   ```bash
   python.exe -m pip install --upgrade pip
   ```
- requirements.txt
    - Install
        ```bash
        pip install -r requirements.txt
        ```
    - Create
        ```bash
        pip freeze > requirements.txt
        ```
### Migration
- upgrade
    ```bash
    alembic upgrade head
    ```
- create revision
    ```bash
    alembic revision --autogenerate -m "init"
    ```
- migrations/env.py
    ```python
    # add your model's MetaData object here
    # for 'autogenerate' support
    # from myapp import mymodel
    # target_metadata = mymodel.Base.metadata
    from services.db import Base
    from models.user import User
    target_metadata = Base.metadata
    ```
- alembic.ini
    ```
    sqlalchemy.url = sqlite:///./sql_app.db
    ```

### Run
- rename the "dev.env" file to ".env" if it is necessary.
```powershell
uvicorn main:app --host 0.0.0.0 --port 8088 --reload
```
- Windows
    ```powershell
    .\run.ps1  
    ```
### Debug Run | main.py
```python
# Debugging
import uvicorn
if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8088)
``` 
### Notes
```bash
    # Disable __pycache__ folder
    PYTHONDONTWRITEBYTECODE=1
```