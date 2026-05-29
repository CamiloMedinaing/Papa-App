from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Base de datos temporal en memoria
agricultores = []


class Agricultor(BaseModel):
    id: int
    cedula: str
    nombre: str
    area: float
    cultivo: str
    inversion: float
    fecha: str
    ubicacion_cultivo: str


@app.get("/", response_class=HTMLResponse)
def inicio():

    filas = ""

    for a in agricultores:
        filas += f"""
        <tr>
            <td>{a['id']}</td>
            <td>{a['cedula']}</td>
            <td>{a['nombre']}</td>
            <td>{a['area']}</td>
            <td>{a['cultivo']}</td>
            <td>${a['inversion']}</td>
            <td>{a['fecha']}</td>
            <td>{a['ubicacion_cultivo']}</td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Sistema Agrícola</title>

<style>

*{{
    margin:0;
    padding:0;
    box-sizing:border-box;
}}

body{{
    font-family:'Segoe UI',sans-serif;
    background:linear-gradient(135deg,#dff6dd,#c8e6c9);
    padding:30px;
}}

.container{{
    max-width:1400px;
    margin:auto;
}}

.card{{
    background:white;
    border-radius:20px;
    padding:30px;
    box-shadow:0 10px 30px rgba(0,0,0,0.15);
}}

h1{{
    text-align:center;
    color:#1b5e20;
    margin-bottom:10px;
}}

.subtitulo{{
    text-align:center;
    color:#555;
    margin-bottom:30px;
}}

.contador{{
    text-align:center;
    font-size:22px;
    font-weight:bold;
    color:#2e7d32;
    margin-bottom:25px;
}}

.form-grid{{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
}}

input{{
    width:100%;
    padding:14px;
    border:1px solid #ccc;
    border-radius:12px;
    font-size:15px;
}}

input:focus{{
    outline:none;
    border-color:#4caf50;
    box-shadow:0 0 10px rgba(76,175,80,.4);
}}

button{{
    width:100%;
    padding:15px;
    border:none;
    border-radius:12px;
    margin-top:20px;
    background:#2e7d32;
    color:white;
    font-size:17px;
    font-weight:bold;
    cursor:pointer;
}}

button:hover{{
    background:#1b5e20;
}}

#mensaje{{
    margin-top:15px;
    text-align:center;
    font-weight:bold;
}}

.error{{
    color:#d32f2f;
}}

.success{{
    color:#2e7d32;
}}

table{{
    width:100%;
    margin-top:30px;
    border-collapse:collapse;
    overflow:hidden;
    border-radius:12px;
}}

th{{
    background:#2e7d32;
    color:white;
}}

th,td{{
    padding:12px;
    text-align:center;
    border:1px solid #ddd;
}}

tr:nth-child(even){{
    background:#f5f5f5;
}}

tr:hover{{
    background:#dcedc8;
}}

@media(max-width:900px){{
    .form-grid{{
        grid-template-columns:1fr;
    }}
}}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h1>🌱 Sistema de Gestión de Agricultores</h1>

<p class="subtitulo">
Registro y control de productores agrícolas
</p>

<div class="contador">
Agricultores registrados: {len(agricultores)}
</div>

<form id="formulario">

<div class="form-grid">

<input type="number" id="id" placeholder="ID" required>

<input type="text" id="cedula" placeholder="Cédula" required>

<input type="text" id="nombre" placeholder="Nombre completo" required>

<input type="text" id="cultivo" placeholder="Cultivo" required>

<input type="number" step="0.01" min="0"
id="area"
placeholder="Área (hectáreas)"
required>

<input type="number" step="0.01" min="0"
id="inversion"
placeholder="Inversión ($)"
required>

<input type="date" id="fecha" required>

<input type="text"
id="ubicacion_cultivo"
placeholder="Ubicación del cultivo"
required>

</div>

<button type="submit">
Guardar Agricultor
</button>

</form>

<div id="mensaje"></div>

<table>

<tr>
<th>ID</th>
<th>Cédula</th>
<th>Nombre</th>
<th>Área</th>
<th>Cultivo</th>
<th>Inversión</th>
<th>Fecha</th>
<th>Ubicación</th>
</tr>

{filas}

</table>

</div>

</div>

<script>

document
.getElementById("formulario")
.addEventListener("submit", async function(e){{

    e.preventDefault();

    let agricultor = {{

        id: parseInt(document.getElementById("id").value),

        cedula: document.getElementById("cedula").value,

        nombre: document.getElementById("nombre").value,

        area: parseFloat(document.getElementById("area").value),

        cultivo: document.getElementById("cultivo").value,

        inversion: parseFloat(document.getElementById("inversion").value),

        fecha: document.getElementById("fecha").value,

        ubicacion_cultivo:
        document.getElementById("ubicacion_cultivo").value
    }};

    if(agricultor.area < 0){{
        document.getElementById("mensaje").innerHTML =
        "<p class='error'>❌ El área no puede ser negativa.</p>";
        return;
    }}

    if(agricultor.inversion < 0){{
        document.getElementById("mensaje").innerHTML =
        "<p class='error'>❌ La inversión no puede ser negativa.</p>";
        return;
    }}

    const respuesta = await fetch("/crear_agricultor", {{
        method:"POST",
        headers:{{
            "Content-Type":"application/json"
        }},
        body:JSON.stringify(agricultor)
    }});

    const datos = await respuesta.json();

    if(datos.error){{
        document.getElementById("mensaje").innerHTML =
        "<p class='error'>❌ "+datos.error+"</p>";
        return;
    }}

    document.getElementById("mensaje").innerHTML =
    "<p class='success'>✅ Agricultor registrado correctamente.</p>";

    setTimeout(() => {{
        location.reload();
    }}, 1000);

}});

</script>

</body>
</html>
"""


@app.post("/crear_agricultor")
def crear_agricultor(agricultor: Agricultor):

    if agricultor.area < 0:
        return {"error": "El área no puede ser negativa"}

    if agricultor.inversion < 0:
        return {"error": "La inversión no puede ser negativa"}

    agricultores.append(agricultor.model_dump())

    return {"mensaje": "Agricultor registrado correctamente"}


@app.get("/agricultores")
def mostrar_agricultores():
    return agricultores