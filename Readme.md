# Instructions

## 1.Clone the repository

```bash
git clone https://github.com/theGitNoob/simulacion-taller-reparacion.git
```

## 2. Create a virtual environment

```bash
python3 -m venv venv
```

## 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

## 4. Install the dependencies

```bash
pip install -r requirements.txt
```

## 5. Run the application

```bash
python main.py
```

## 6. Compile the project report

```bash
pdflatex -interaction=nonstopmode  informe_simulacion.tex --output-directory=out
rm *.aux *.log *.out *.toc
```
