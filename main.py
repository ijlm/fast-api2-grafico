from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    content = """
    <html>
        <head>
            <title>Diagrama de barras</title>
        </head>
        <body>
            <h1>Ingrese un valor:</h1>
            <form method="post">
                <input type="number" name="value">
                <input type="submit" value="Generar diagrama">
            </form>
            %s
        </body>
    </html>
    """
    return content % ""

@app.post("/", response_class=HTMLResponse)
async def generate_chart(request: Request):
    form = await request.form()
    value = int(form["value"])
    
    # Crear el diagrama de barras
    fig, ax = plt.subplots()
    ax.bar(["Valor"], [value])
    ax.set_ylabel("Valor")
    ax.set_title("Diagrama de barras")
    
    # Guardar el diagrama en un buffer de bytes
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    
    # Convertir el buffer de bytes en una cadena de caracteres base64
    buffer_b64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Mostrar el diagrama en la página web
    content = """
    <html>
        <head>
            <title>Diagrama de barras</title>
        </head>
        <body>
            <h1>Ingrese un valor:</h1>
            <form method="post">
                <input type="number" name="value">
                <input type="submit" value="Generar diagrama">
            </form>
            <img src="data:image/png;base64,%s">
        </body>
    </html>
    """
    return content % buffer_b64

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    