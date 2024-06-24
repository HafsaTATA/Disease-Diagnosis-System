:- dynamic symptomes/1, maladies/1, login/2.

symptomes([
    'fievre',
    'toux_seche',
    'fatigue',
    'maux_de_tete',
    'maux_de_gorge',
    'toux_grasse',
    'essoufflement',
    'perte_du_gout_ou_de_l_odorat',
    'sensibilite_a_la_lumiere',
    'nausees',
    'vomissements',
    'sifflement_respiratoire',
    'maux_de_ventre',
    'diarrhee',
    'rougeurs',
    'demangeaisons',
    'urticaire',
    'nez_qui_coule',
    'etoiles_rouges'
]).


maladies([
    'Grippe',
    'Rhume',
    'Anemie',
    'COVID-19',
    'Migraine',
    'Asthme',
    'Gastro-enterite',
    'Allergie'
]).

symptome('Grippe', ['fievre', 'toux_seche', 'fatigue', 'maux_de_tete']).
symptome('Rhume', ['maux_de_gorge', 'toux_grasse']).
symptome('Anemie', ['fatigue', 'essoufflement']).
symptome('COVID-19', ['fievre', 'toux_seche', 'fatigue', 'perte_du_gout_ou_de_l_odorat', 'essoufflement']).
symptome('Migraine', ['maux_de_tete', 'sensibilite_a_la_lumiere', 'nausees', 'vomissements']).
symptomSe('Asthme', ['toux_seche', 'essoufflement', 'sifflement_respiratoire']).
symptome('Gastro-enterite', ['maux_de_ventre', 'diarrhee', 'vomissements', 'fievre']).
symptome('Allergie', ['rougeurs', 'demangeaisons', 'urticaire', 'nez_qui_coule', 'etoiles_rouges']).


diagnose(Liste) :-
    findall(Disease,(symptome(Disease, Liste)),Result),(Result = [] -> write('') ; write(Result)).


/* Login */
login('user', 'password123').


verify_credentials(User, Password) :-
    login(User, Password), !, write(true).S
verify_credentials(_, _) :-write(false).
