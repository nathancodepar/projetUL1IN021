Le projet **Deskmate** consiste à développer un système de surveillance des conditions environnementales intelligent. Ce dispositif embarqué est conçu pour surveiller, traiter et alerter sur les conditions d’un espace intérieur (domicile, bureau, salle de classe, etc.).

L’objectif principal est d’optimiser le confort des occupants. Le système gère des fonctions temporelles (minuteur) et doit garantir que les paramètres ambiants (niveau sonore, température, luminosité) sont compris dans les seuils établis.

Le système permet de soulager l’utilisateur de la surveillance constante de son environnement en assurant un cadre de vie ou de travail sain et agréable pour tous les occupants.


__SCHEMA GENERAL DU PROJET :__

Le cœur du système est le Raspberry Pi. Sa sélection répond à la contrainte d’utiliser au moins un capteur et permet l’intégration facile des modules utilisés. De plus, pour respecter la contrainte d’enregistrement des données dans une base de données, le Raspberry Pi stockera l’historique des mesures, alertes déclenchées et des évènements du minuteur assurant un suivi sur le long terme. Par ailleurs, la contrainte d’utilisation d’un site web est mise en œuvre en configurant le Raspberry Pi comme un serveur. Grâce à son module Wi-Fi, il rend l’interface de contrôle et de visualisation accessible depuis n’importe quel dispositif (téléphone, ordinateur). Enfin, l’interaction avec un humain est gérée à plusieurs niveaux. L’utilisateur peut configurer les seuils critiques et gérer le minuteur via l’interface web.

La figure 1 représente le fonctionnement du Deskmate. Il se compose des éléments suivants:
- __**Capteurs :**__ L’acquisition des données environnementales repose sur trois capteurs principaux: le **Grove - Sound Sensor** (le niveau sonore), le **Grove - Temperature Sensor** (la température) et le **Grove - Light Sensor** (la luminosité)
- __**Raspberry Pi**_
- __**Actionneurs :**__ Un **Grove Buzzer** est utilisé pour les alertes sonores lorsque l’une des limites définies est dépassée.
