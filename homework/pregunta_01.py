# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    def load_data():                                                #? Carga los datos desde csv
        return pd.read_csv("files/input/shipping-data.csv")         #? Lee el archivo
    
    def create_visual_for_shipping_per_warehouse(df):               #? Crea una visualización para el envío por cada almacén
        df = df.copy()
        plt.figure()
        counts = df["Warehouse_block"].value_counts()               #? Cuenta la cantidad de registros por cada bloque de almacén

        counts.plot.bar(                                            #? Dibuja un gráfico de barras con los resultados
            title = "Shipping per Warehouse",                       #? titulo
            xlabel = "warehouse block",                             #? eje x
            ylabel = "Record Count",                                #? eje y
            color = "tab:blue",                                     #? Color barras
            fontsize = 8                                            #? Tamaño  fuente
        )
        
        plt.gca().spines['top'].set_visible(False)                  #? Elimina la línea superior del gráfico
        plt.gca().spines['right'].set_visible(False)                #? Elimina la línea derecha del gráfico

        if not os.path.exists('docs'):                              #? Verifica en la carpeta
            os.makedirs('docs')                                     #? Si no existe, crea la carpeta "docs"

        plt.savefig('docs/shipping_per_warehouse.png')              #? Guarda la figura

    def create_visual_for_shipping_per_mode(df):                    #? visualización modo de envío
        df = df.copy()
        plt.figure()
        counts = df["Mode_of_Shipment"].value_counts()              #? Cuenta los distintos modos de envío

        counts.plot.pie(
            title = "Mode of Shipment",
            wedgeprops = dict(width = 0.35),
            ylabel = "",
            color = ["tab:blue", "tab:orange", "tab:green "],
        )
    if not os.path.exists("docs"):
        os.makedirs("docs")
    
    plt.savefig("docs/mode_of_shipment.png")

    def create_visual_for_average_customer_rating(df):              #? Crea una visualización para la evaluación promedio del cliente
        df = df.copy()
        plt.figure()
                                                                    #? Agrupa por modo de envío y obtiene estadísticas descriptivas
        df = (df[["Mode_of_Shipment", "Customer_rating"]].groupby("Mode_of_Shipment").describe())
        df.columns = df.columns.droplevel()                         #? Elimina el nivel superior del multi-índice de columnas
        df = df[["mean", "min", "max"]]                             #? Selecciona las columnas "mean", "min", y "max" para la visualización

        plt.barh(                                                   #? Dibuja un gráfico de barras horizontal
                y = df.index,                                       #? Usa los índices (modos de envío) en el eje Y
                width = df["max"].values - 1,                       #? Ancho de las barras basado en la diferencia entre el valor máximo y 1
                left = df ["min"].values,
                height = 0.9,
                color = "lightgrey",
                alpha = 0.8                                         #? Transparencia de las barras
            )
        colors = ["tab:green" if value >=3.0
                else "tab:orange" for value in df["mean"].values
        ]

        plt.barh(                                                   #? Dibuja las barras para las calificaciones promedio
            y = df.index.values,
            width = df["mean"]. values - 1,                         #? Ancho de las barras según el valor promedio
            left = df["min"].values,
            color = colors,
            height = 0.5,
            alpha = 1.0
        )
        
        plt.title("Average Customer Rating")
        plt.gca().spines["left"].set_color("gray")
        plt.gca().spines["bottom"].set_color("gray")
        plt.gca().spines["top"].set_visible(False) 
        plt.gca().spines["right"].set_visible(False)

        if not os.path.exists("docs"):
            os.makedirs("docs")

        plt.savefig("docs/average_customer_rating.png")

    def create_visual_for_weight_distribution(df):                  #? Crea una visualización para la distribución del peso             
        df = df.copy()
        plt.figure()
        df["Weight_in_gms"].plot.hist(                              #? Dibuja un histograma para la distribución del peso
            title = "Shipped Weight Distribution",
            color = "tab:orange",
            edgecolor = "white"
        )
        
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        if not os.path.exists("docs"):
            os.makedirs("docs")

        plt.savefig("docs/weight_distribution.png")


    df = load_data()                                                #?Crear las visualizaciones de los df 
    create_visual_for_shipping_per_warehouse(df)
    create_visual_for_shipping_per_mode(df)
    create_visual_for_average_customer_rating(df)
    create_visual_for_weight_distribution(df)

    html = """                                                      #? Inicia la estructura HTML para el dashboard
    <!DOCTYPE html>  #? Define el tipo de documento HTML
<html>  #? Inicia el elemento HTML
    <head>  #? Define la cabecera del documento
        <title>Shipping Dashboard</title>  #? Título del dashboard
    </head>
    <body>  #? Cuerpo del documento HTML
        <h1>Shipping Dashboard</h1>  #? Título principal del dashboard
        <div style = 'width: 45%;float: left;'>  #? Contenedor flotante para la visualización de la izquierda
        <h2>Shipping per Warehouse</h2>  #? Título para el gráfico de "Shipping per Warehouse"
        <img src="shipping_per_warehouse.png" alt="Fig 1">  #? Imagen del gráfico "Shipping per Warehouse"
        <h2>Mode of shipment</h2>  #? Título para el gráfico de "Mode of Shipment"
        <img src="mode_of_shipment.png" alt="Fig 2">  #? Imagen del gráfico "Mode of Shipment"
        </div>  #? Cierra el contenedor flotante de la izquierda
        <div style = 'width: 45%;float: right;'>  #? Contenedor flotante para la visualización de la derecha
        <h2>Average Customer Rating</h2>  #? Título para el gráfico de "Average Customer Rating"
        <img src="average_customer_rating.png" alt="Fig 3">  #? Imagen del gráfico "Average Customer Rating"
        <h2>Weight Distribution</h2>  #? Título para el gráfico de "Weight Distribution"
        <img src="weight_distribution.png" alt="Fig 4">  #? Imagen del gráfico "Weight Distribution"
        </div>  #? Cierra el contenedor flotante de la derecha
        </body>
    </html>
"""  #? Finaliza el contenido HTML
    
    with open("docs/index.html", "w") as file:
        file.write(html)

pregunta_01()
