Despliegue de un modelo de Machine Learning como API

En esta tarea deberás tomar uno de los modelos de Machine Learning que hayas desarrollado durante el programa de magíster y convertirlo en un producto de datos funcional, accesible mediante una API 
construida con FastAPI y desplegada en Render, siguiendo las buenas prácticas vistas en clases.

El objetivo es que logres empaquetar tu modelo como un servicio de predicción accesible a través de la web, incluyendo pruebas automatizadas desde un cliente y documentación que permita a un tercero 
(en este caso, tu profesor) realizar consultas sin fricción.

Repositorio de referencia: https://github.com/aastroza/producto-de-datos-api a un sitio externo.

Instrucciones Generales

* El trabajo debe entregarse en un repositorio público de GitHub.

* Toda la funcionalidad debe estar documentada en un README.md, incluyendo:

  * Instrucciones para instalar dependencias.
  
  * Cómo ejecutar el servidor localmente.
  
  * Cómo hacer peticiones a la API (ejemplos de payloads).
  
  * Enlace a la API desplegada en Render.

* Se recomienda usar requirements.txt o pyproject.toml para la gestión de dependencias.
  

1. Implementación de la API en FastAPI
   
Construir una API usando FastAPI que:

  * Cargue tu modelo previamente entrenado.
  
  * Exponga al menos un endpoint /predict que reciba datos de entrada en formato JSON.
  
  * Realice la predicción y retorne los resultados al usuario.
  
  * Incluya validaciones básicas con pydantic.

**Entregable**: Código fuente de la API, incluyendo archivo de arranque (main.py), modelo cargado, dependencias y validaciones.

2. Despliegue de la API en Render

Despliega tu API en https://render.com y deja el enlace disponible en el README.

**Entregable**: URL pública de la API funcionando en Render, accesible sin autenticación.

3. Pruebas desde un Cliente Externo
   
Escribe un script (por ejemplo, client.py o client.ipynb) que:

  * Realice al menos tres peticiones distintas a tu API desplegada.
  
  * Muestre los datos enviados y los resultados obtenidos.
  
  * Entregable: Código del cliente + resultados impresos o mostrados en consola/notebook.

4. Test Final del Profesor
   
Enviar una consulta personalizada a tu API desplegada.

Para esto debes:

  * Asegurarte de dejar instrucciones claras en el README.md sobre:
  
  * Cómo se estructura el JSON de entrada.
  
  * Qué valores esperas para cada campo.
  
  * Ejemplos de consultas válidas.

* Tu API debe ser robusta y responder con mensajes claros ante errores.

**Entregable**: Un README bien detallado y una API operativa y funcional al momento de la revisión.

**Evaluación**

* API funcional en FastAPI	30 pts
* Despliegue en Render	20 pts
* Cliente con pruebas automáticas	30 pts
* Test del profesor (instrucciones + API)	20 pts

* Total	100 pts

Recomendaciones

* Reutiliza tu modelo existente, no es necesario reentrenar.

* Puedes usar joblib o pickle para cargar modelos serializados.

* Usa uvicorn como servidor local.

* Prueba localmente con requests, Postman a un sitio externo. o scripts antes de desplegar.

* Usa .env si necesitas manejar variables sensibles (aunque no será necesario si tu modelo es autocontenido).
  
