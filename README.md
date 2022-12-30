# **Savingz.**

## <b>Description du projet</b>
Les tontines sont des associations collectives qui réunissent des épargnants afin d’investir en commun pour lever
des capitaux. Avec l’avènement des nouvelles technologies, le secteur économique connaît quant à lui de nombreuses mutations. Certaines personnes ont tendance à faire plus confiance aux tontines qu’aux banques ; mais
lorsque ces personnes ne sont plus dans le même environnement que la base tontinière, les choses deviennent
difficiles. Doter des pays comme le Cameroun, où 58% de la population est impliquée dans les tontines d’un
logiciel permettra aux membres de celles-ci de contrôler et d’avoir une meilleure vision de leur investissement
dans la tontine. Le logiciel de gestion de la tontine peut être utilisé à des fins diverses, notamment pour :

- Faciliter l’expérience quotidienne
- Briser les frontières (permettre la participation à des tontines même lointaines)
- Permettre une communication instantanée entre les membres
- Éviter la perte des rapports des réunions précédentes
- Contrôler avec précision les intérêts générés par les prêts
- Suivre l’état financier de tous les membres

<br>

**Page D'accueil**

![Page d'accueil du site Savingz](./core/static/images/Welcome%20to%20Savingz.png)

<br>

**Page D'enregistrement**

![Enregistrement sur Savingz](./core/static/images/Register%20Savingz.png)

<br>

**Page De Connexion**

![Connexion sur Savingz](./core/static/images/login%20Savingz.png)

## <b>Project setup</b>
1. Clonez le dépôt sur votre poste de travail (appareil/machine) en exécutant la commande : <br>

        git clone https://github.com/TedNicos11/Tontine.git

2. Place yourself at the root of the project. <br>
   
        C:\Users\...\Tontine\

        /home/.../Tontine

### **Avant d'exécuter les commandes suivantes, assurez-vous toujours que vous êtes à la racine du projet.**
<br>

3. Configurez l'environnement virtuel du projet à sa racine en exécutant les commandes suivantes : <br>
    `Creation/Installation`

        1. pip install virtualenv
        2. virtualenv .env
   
    `Activation sur Windows`
    
        3. .env\Scripts\activate
   
    `Activation sur Linux/MacOS`
    
        3. source .env/bin/activate

    Pour désactiver l'environnement virtuel déjà activé, tapez simplement `deactivate` dans le terminal, sinon exécutez la commande suivante : <br>

    `Désactivation sous Windows`

        .env\Scripts\deactivate

    `Désactivation sous Linux/MacOS`

        source .env/bin/deactivate

4. Dans l'environnement virtuel créé et activé, "Installez" les packages requis à partir de [requirements.txt](./requirements.txt) en exécutant la commande : <br>

        pip install -r requirements.txt

## <b>Lancement du projet</b>

### **Avant d'exécuter les commandes suivantes, assurez-vous toujours que vous êtes à la racine du projet.**
<br>

5. Migrez les données vers la base de données (`Sqllite` par défaut) : <br>

        python manage.py migrate

6. Exécutez le projet à l'aide de la commande : <br>

        python manage.py runserver

7. Vérifiez que le serveur est en cours d'exécution en allant sur [localhost:8000](http://127.0.0.1:8000) ou [http://127.0.0.1:8000](http://127.0.0.1:8000)

<br>
<small>Prenez plaisir..</small> 😊🖤