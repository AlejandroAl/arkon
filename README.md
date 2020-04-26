![Esta es una imagen de ejemplo](https://media-exp1.licdn.com/dms/image/C4E0BAQEvY6yKBPOCTQ/company-logo_200_200/0?e=2159024400&v=beta&t=Te8TxntpUuETCHmGsfls28gDzqdtIvtAaODZUsF01nU)


The project lets us get information about Metrobus CDMX.

```
NOTE:

    To run this project is necesary contain the next requirements:

    * docker-compose
    * docker

```


# Configuration

## First Step

* Go to dir project_ark/collectDataScripts/airflow-dags.

* Copy the two files (ark_dag_metrobus.py,  initial_townHall_Metrobus.py) into:

```
"project_ark/mnt/airflow/dags"
```


## Second Step

* Go to dir -- project_ark/collectDataScripts

* Copy the next files 

  * DataCdmxScripts.py
  * ShapesPoints.py

  into:

```
"project_ark/mnt/airflow/dags/src
```

## Third step

* Go to dir:

```
project_ark/
```

* Execute the next command to start the service :

```
docker-compose -f docker-compose.yml up -d  --build
```

* Execute the next command to stop the service :

```
docker-compose -f docker-compose.yml down
```


After some minute you can go the next endpoints:

* localhost:8081 (iarflow webserver)
* http://localhost:5000/getAvailableUnits (GET Method)
* http://localhost:5000/getlistTownHalls (GET Method)
* http://localhost:5000/metrobusDetailsById?ID= (GET Method)
* http://localhost:5000/metrobusUnitsByTownHall (POST Method)
  * {	"TH":"alcaldia"} (body)

```
NOTE:

If the endpoints dont return value wait to airflow dags finish, they do the ETL processing.
```

Lista de alcaldias:

* Alvaro Obregon
* Azcapotzalco
* Benito Juarez
* Coyoacan
* Cuajimalpa de Morelos
* Cuauhtemoc
* Gustavo A. Madero
* Iztacalco
* Iztapalapa
* La Magdalena Contreras
* Miguel Hidalgo
* Milpa Alta
* Tlahuac
* Tlalpan
* Venustiano Carranza
* Xochimilco