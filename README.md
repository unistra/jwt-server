# JWT server


Serveur de JSON web token à partir de tickets CAS.

## Objectifs

 - Proposer un service de JWT
 - Permettre d'accéder à quelques données individuelles supplémentaires

## Fonctionnement

### Clés

Le serveur utilise des clés RSA, qui doivent être présentes dans un répertoire `keys` à la racine.
 - `myKey.pem` : clé privée, utilisée pour signer les tokens
 - `myPublic.pem` : clé publique, utilisée pour vérifier les tokens

 Le mot de passe de la clé est déclaré dans le paramètre `RSA_PASSWORD`
 
 ### Déclaration de service
 
 Les services doivent être déclarés pour pouvoir obtenir un token.
 À l'aide de l'interface d'admin ou dans la BDD, il faut renseigner
 le champ `data` de la table `AuthorizedService` avec
 un *JSONField* de la forme :
 ```json
{
    "fields": {
        "username": "uid",
        "affiliations": [
            "eduPersonPrimaryAffiliation",
            "eduPersonAffiliation"
        ],
        "directory_id": "udsDirectoryId",
        "organization": "supannEtablissement"
    },
    "service": "127.0.0.1:8000",
    "conditions": {
        "ldap_filters": [],
        "ldap_must_exist": false
    }
}
```

Le token généré contient alors :

```json
[
    {
        "typ": "JWT",
        "alg": "RS256"
    },
    {
        "token_type": "access",
        "exp": 1593528195,
        "jti": "ead170f3a3dd4c8eb1d10b21f23b4e63",
        "user_id": "not.a.real.uid",
        "iss": "127.0.0.1:8000",
        "sub": "not.a.real.uid",
        "nbf": 1593520995.627925,
        "username": "not.a.real.uid",
        "affiliations": [
            "employee",
            "member",
            "faculty"
        ],
        "directory_id": "01234",
        "organization": "UDS"
    }
]
```

 - `service` correspond à l'adresse autorisée à faire appel aux token
 - `fields` permet de définir les champs remontés depuis le LDAP :
   - la clé est le nom utilisé dans le token, la valeur correspond au champ attendu depuis le LDAP
   - on peut utiliser un champ unique ou la composition de plusieurs champs
   
 ### Personnalisation de l'émetteur

 Il est possible de surcharger l'emetteur du token (champ `iss` du token) en introduisant une clé `issuer` dans le champ `data`.

 ### Ajout de conditions d'accès
 
 Il est possible d'ajouter des conditions supplémentaires en rajoutant un clé `conditions` au champ `data` du service.
 La clé `conditions` peut avoir une sous-clé `ldap_filters` qui est une liste de filtres supplémentaires ajoutés à 
 la requête LDAP. 

 Par exemple :
 ```json
{
    "conditions": {
       "ldap_filters": ["memberOf=cn=group-name,ou=groups,o=org"]
    }
}
```
 Donnera la requête : `(&(uid=username)(memberOf=cm=group-name,ou=groups,o=org)`

 Par défaut, si aucune entrée n'est trouvée dans le LDAP, un token sera tout de même généré. 
 La condition `"ldap_must_exist": true` génèrera une réponse `403 Forbidden`.
 
 ### Vérification de fonctionnement
 
 Une route `/api/service/` permet de générer un token.
 
 En local, vous devriez donc avoir une réponse sur [http://127.0.0.1/api/service/](http://127.0.0.1/api/service/)
 
 ## Développement
 
 ### Exemple de fichier `bin/postactivate`
 
 ```shell script
#!/bin/zsh
# This hook is sourced after this virtualenv is activated.
export DJANGO_SETTINGS_MODULE=jwtserver.settings.dev

export RSA_PASSWORD='iamnotarealpassword'

export JWT_ACCESS_LIFETIME='120'
export JWT_REFRESH_LIFETIME='1'

export LDAP_SERVER='ldap.example.none'
export LDAP_USER='ou=toto,o=annuaire'
export LDAP_PASSWORD='stillnotarealpassword'

export DB_HOST="localhost"
export DB_USER="jwt"
export DB_PWD="jwt"
export DB_NAME="postgres"
```
