# Uso de Inteligencia Artificial — ES3 (TI3041)

Proyecto: Catálogo Online — Ferretería McHammer
Evaluación: ES3, Unidad 2 (ORM, reportes y formulario de clientes)

<!--
BORRADOR / PLANTILLA — antes de entregar:
1) Reemplaza cada [corchete] por lo que realmente hiciste. No dejes corchetes.
2) Agrega o quita filas según las consultas que de verdad realizaste.
3) La Parte 2 NO puede estar redactada por una IA: escríbela tú, con tus palabras.
4) Verifica que cada fila corresponda a código que existe en el repositorio, porque
   en la revisión se contrasta este archivo con el código.
-->

## Parte 1 — Registro de consultas

| # | Etapa | Prompt enviado a la IA (textual) | Resumen de la respuesta | Qué usé / qué modifiqué |
|---|-------|----------------------------------|-------------------------|--------------------------|
| 1 | 0. Entorno | [pega el prompt literal, ej.: "Tengo un proyecto Django de la ES2; ayúdame a dejar operativo el repo con la BD poblada desde un fixture"] | [1–2 líneas: qué te propuso] | [qué aceptaste tal cual y qué cambiaste: nombre del proyecto, app, ruta del fixture, etc.] |
| 2 | 1. CRUD | [prompt sobre las vistas de crear / editar / eliminar con confirmación] | [resumen] | [qué adaptaste: nombres de campos de tu modelo `Producto` (nombre, categoría, precio, stock, imagen), decorador `user_passes_test`, redirección al catálogo] |
| 3 | 1. CRUD | [prompt sobre el formulario de producto y su template] | [resumen] | [qué cambiaste: `ProductoForm`, validaciones de nombre y precio, labels en español, campos del template] |
| 4 | 2. Reportes | [prompt sobre reporte con `annotate` / `aggregate` por categoría] | [resumen] | [qué ajustaste: `Count`, `Avg`, `Sum`, redondeo del promedio en la vista, totales con `aggregate`] |
| 5 | 2. Reportes | [prompt sobre reporte filtrado con `filter` y `order_by`] | [resumen] | [qué ajustaste: umbral por `GET`, `stock__lte`, orden por stock y nombre, conteo de agotados] |
| 6 | 3. Clientes | [prompt sobre el modelo `ConsultaCliente` y su `ModelForm`] | [resumen] | [qué cambiaste: campos y largos, `SET_NULL` en el producto opcional, `auto_now_add` en la fecha, registro en `/admin`] |
| 7 | 3. Clientes | [prompt sobre validaciones del formulario de contacto] | [resumen] | [qué ajustaste: mínimo de 3 caracteres en el nombre, mínimo de 10 en el mensaje, mensajes de error en español] |
| 8 | 3. Clientes | [prompt sobre la funcionalidad con sesiones] | [resumen] | [qué cambiaste: guardar solo los 3 últimos productos visitados, sin repetidos, y mostrarlos en catálogo y ficha] |
| 9 | 3. Clientes | [prompt sobre pruebas o sobre CSRF] | [resumen] | [qué cambiaste: agregué los tests de correo inválido, campos vacíos y POST sin token CSRF] |
| 10 | Frontend | [prompt sobre estilos / orden de la interfaz, si lo usaste] | [resumen] | [qué cambiaste en `style.css` o en los templates] |

## Parte 2 — Explicación del proceso

<!--
Escribe aquí entre 10 y 20 líneas, en primera persona y con tus palabras.
No copies texto generado por IA. Para que no se te olvide nada, responde estas preguntas
en prosa corrida (no en lista de respuestas):

- ¿Para qué le pediste ayuda a la IA y por qué en esas partes y no en otras?
- ¿Qué respuestas usaste tal cual, sin tocarlas? ¿Por qué te convencieron?
- ¿Qué tuviste que corregir o adaptar (nombres de campos, rutas, validaciones,
  algo que no funcionaba)? ¿Cómo te diste cuenta del error?
- ¿Qué comparaste con la documentación de Django para decidir si lo que te daba
  era correcto?
- ¿Qué aprendiste del ORM (annotate/aggregate/filter) o de los formularios que antes
  no manejabas?
- ¿En qué parte sentiste que la IA no bastaba y tuviste que pensar tú la solución?
-->

[Escribe aquí tu texto personal de 10 a 20 líneas.]
