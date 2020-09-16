# dump.sh
        dump.sh is a tool to save data to http://dump.sh server, using one of 
        supported tool (curl, PostMan, and etc.). The command is designed to 
        work without user interaction. 


http://dump.sh  [Official websites](http://dump.sh/)

## How to use
```bash
dump.sh (1)                      Dump Shell Manual                  dump.sh (1)


NAME
        dump.sh - Save your command line output.

DESCRIPTION
        dump.sh is a tool to save data to http://dump.sh server, using one of 
        supported tool (curl, PostMan, and etc.). The command is designed to 
        work without user interaction. 

EXAMPLE
        ANONYMOUS POST LOGS:

                $ echo "Hello World" | curl -F '=<-' dump.sh
                  http://dump.sh/rXupAC

                $ curl -F '=@demo.txt' dump.sh
                  http://dump.sh/mh6Cyn

        CREATE/LOGIN USER POST LOGS:
        
                $ echo "Hello World" | curl -F 'USERNAME:PASSWORD=<-' dump.sh
                  http://dump.sh/4DwOCU

                $ curl -F 'USERNAME:PASSWORD=@demo.txt' dump.sh
                  http://dump.sh/vwvqFQ

        LIST USER RECOARDS:

                $ curl dump.sh/testuser/        <<<<<The slash is very important
                  http://dump.sh/rXupAC -- 2020-09-16 16:08:27.208000
                  http://dump.sh/mh6Cyn -- 2020-09-16 15:34:37.260000
                  http://dump.sh/ReKYBv -- 2020-09-16 15:33:57.117000
                  http://dump.sh/4DwOCU -- 2020-09-16 15:33:51.670000
                  http://dump.sh/vwvqFQ -- 2020-09-16 15:33:49.237000
                  http://dump.sh/bgoMC5 -- 2020-09-16 15:33:43.886000

        GET USER LOG:

                $ curl http://dump.sh/rXupAC
                  Hello World

CHANGES
        20200916
            The first release of dump.sh

TODO
        0. Should support delete the LOG.
        1. Shouls support change password.
```
## Deploy && Install 

### File tree
```
.
├── app
│   ├── app.py
│   ├── config.ini
│   ├── LICENSE
│   ├── logger.py
│   ├── logs
│   │   └── runtime.log
│   ├── main.py
│   ├── randomStr.py
│   ├── README.md
│   ├── requirements.txt
│   └── templates
│       ├── index_curl.txt
│       ├── index.html
│       ├── userLogList_curl.html
│       └── userLogList.html
├── Dockerfile
└── dump_sh.yaml
```

### Dockerfile
```Dockerfile
COPY ./app /app
RUN pip install -r requirements.txt
```

### requirements.txt
```bash
[root@ethical-beeps-5 app]# cat requirements.txt
Flask-PyMongo
```

### dump_sh.yaml
```yaml
version: '3.1'

services:

  mongo:
    image: mongo
    container_name: mongodb
    restart: always
    expose:
      - 27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: "root"
      MONGO_INITDB_ROOT_PASSWORD: "MongoDbPassword"

  mongo-express:
    image: mongo-express
    container_name: mongo-express
    restart: always
    ports:
      - 8081:8081
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: "root"
      ME_CONFIG_MONGODB_ADMINPASSWORD: "MongoDbPassword"
      ME_CONFIG_BASICAUTH_USERNAME: "root"
      ME_CONFIG_BASICAUTH_PASSWORD: "MongoLoginBasicAuthPassword"

  web:
    container_name: webcontainer
    build: .
    hostname: dump.sh
    ports:
     - "80:80"
```



### Deploy "docker-compose"
```bash
docker-compose -f dump_sh.yaml up --build -d
```

### "docker ps" output
```bash
[root@ethical-beeps-5 dumpsh_dir]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                         NAMES
7ab7cfe05e0d        dumpsh_dir_web      "/entrypoint.sh /sta…"   10 minutes ago      Up 10 minutes       0.0.0.0:80->80/tcp, 443/tcp   webcontainer
3e48874ecfb9        mongo               "docker-entrypoint.s…"   36 minutes ago      Up 36 minutes       27017/tcp                     mongodb
4b6ff326ede6        mongo-express       "tini -- /docker-ent…"   36 minutes ago      Up 36 minutes       0.0.0.0:8081->8081/tcp        mongo-express
```

Have Fun !!