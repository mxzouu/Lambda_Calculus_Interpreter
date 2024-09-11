from ast import Not
from numpy import save
import logic
import parsing
import image_maker
import app_functions
import os
import time
import pyfiglet
import keyboard
import shutil
import platform

if platform.system() == 'Windows':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')


welcomeBanner = {
    'en': 'Lambda Calculus Interpreter',
    'fr': 'Interpréteur de Calcul Lambda'
}
goodByeBanner = {
    'en': 'Goodbye!',
    'fr': 'Au revoir!'
}
inputMessage = {
    'en': 'Enter your choice: ',
    'fr': 'Entrez votre choix: '
}

termInputMessage = {
    'en': 'Enter a term: ',
    'fr': 'Entrez un terme: '
}
successMessage = {
    'en': 'Done!',
    'fr': 'succès!'
}
invalidChoiceMessage = {
    'en': 'Invalid choice! Enter your choice: ',
    'fr': 'Choix invalide! Entrez votre choix: '
}

mainMenuOptions = {
    'en': {
        1: 'Run Beta Reduction',
        2: 'Run Interactive Beta Reduction',
        3: 'Arithmetic Operations',
        4: 'Show Numbers',
        5: 'Boolean Expression',
        6: 'Exit'
    },
    'fr': {
        1: 'Exécuter la Réduction Bêta',
        2: 'Exécuter la Réduction Bêta Interactive',
        3: 'Opérations Arithmétiques',
        4: 'Afficher les Nombres',
        5: 'Expression Booléenne',
        6: 'Quitter'
    }
}

arithmetic_operations_options = {
    'en': {
        1: 'Addition',
        2: 'Subtraction',
        3: 'Multiplication',
        4: 'Power',
        5: 'Successor',
        6: 'Predecessor',
        7: 'Back',
    },
    'fr': {
        1: 'Addition',
        2: 'Soustraction',
        3: 'Multiplication',
        4: 'Puissance',
        5: 'Successeur',
        6: 'Prédécesseur',
        7: 'Retour',
    }
}

choice_number_representation= {
'en':{
    1: 'Church Integers',
    2: 'Relative Integers',
    3: 'Back'
},
'fr':{
    1: 'Nombres entiers (représentation de Church)',
    2: 'Nombres relatifs',
    3: 'Retour'
}   
}



boolean_representation= {
'en':{
    1: 'NOT',
    2: 'AND',
    3: 'OR',
    4: 'XOR',
    5: 'IS ZERO',
    6: 'Back'
},
'fr':{
    1: 'NON',
    2: 'ET',
    3: 'OU',
    4: 'OU EXCLUSIF',
    5: 'EST NUL',
    6: 'Retour'
}

}


def delete_images(folder):
    if os.path.exists(folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
def moveImages(src, dest):
	for filename in os.listdir(src):
         if os.path.isfile(dest+'/'+filename):
            os.remove(dest+'/'+filename)
         shutil.move(src+"/"+filename, dest)

def return_main_menu():
    image_maker.colors = ['black','blue','green','orange','pink','purple','red','yellow']
    not_pressed = True
    print('Press ENTER to return to the main menu')
    while not_pressed:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('ENTER'):  # if key 'ENTER' is pressed 
                not_pressed = False  # finishing the loop
                clear()
                time.sleep(1)
                logic.image_counter = 0
                image_maker.variables_colors_couple = {}
                break
        except:
            break  # if user pressed a key other than the given key the loop will break
    run_main_menu()

def run_beta_reduction_totale(terme,path='beta_reduction_totale'):
    terme = parsing.parseTerm(terme)
    if logic.recognize_term(terme):
        print(" terme infini detecté")
        return None
    os.makedirs(path, exist_ok=True)# cree le rep si il existe pas, le vide si non
    if len(os.listdir(path)) > 0:
        logic.image_counter = 0
    k=logic.beta_reduction_totale(terme,path)
    print(" le terme obtenu est: "+logic.to_string(k))
    save_image_choice = input('Do you want to save the images? (Y/n): ')
    while save_image_choice not in ['y','n','']:
            save_image_choice = input('Invalid choice. Do you want to save the images? (Y/n): ')
    if save_image_choice == 'y' or save_image_choice=='':
        os.makedirs("./sauvegarde/"+path, exist_ok=True)
        moveImages(path,'./sauvegarde/'+path)
        os.rmdir(path)
    elif save_image_choice=='n':
        delete_images(path)
        os.rmdir(path)

def run_beta_reduction_interactive_totale(terme,path='beta_reduction_interactive_totale'):
    terme = parsing.parseTerm(terme)
    if logic.recognize_term(terme):
        print(" terme infini detecté")
        return None
    os.makedirs(path, exist_ok=True)
    if len(os.listdir(path)) > 0:
        logic.image_counter = 0
    logic.beta_reduction_interactive_totale(terme,path)
    save_image_choice = input('Do you want to save the images? (Y/n): ')
    while save_image_choice not in ['y','n','']:
            save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ')
    if save_image_choice == 'y'or save_image_choice=='':
        os.makedirs("./sauvegarde/"+path, exist_ok=True)
        moveImages(path,'./sauvegarde/'+path)
        os.rmdir(path)
    elif save_image_choice == 'n':
        delete_images(path)
        os.rmdir(path)

def run_show_numbers(path,language='en'):
    os.makedirs(path, exist_ok=True)
    print_menu(choice_number_representation,language)
    choice = int(input(inputMessage[language]))
    while choice not in mainMenuOptions[language]:
        clear()
        print_menu(choice_number_representation,language)
        msg = 'Voici le terme:' if language == 'fr' else 'Here is the term:'
        directory = "./saved/" if language == 'en' else "./sauvegarde/"
        choice = int(input('Invalid choice. Enter your choice: ' if language == 'en' else 'Choix invalide. Entrez votre choix: '))
    if choice ==1:
        clear()
        terme = int(input('Enter a number: ' if language == 'en' else 'Entrez un nombre: '))
        while terme < 0:
            terme = int(input('Enter a number: ' if language == 'en' else 'Entrez un nombre: '))
        t = app_functions.dec_to_church(terme)

        print(msg ,logic.to_string(t))
        logic.captureImage(t,path,'ENTIER'+str(terme),False)
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()

        while save_image_choice not in ['y','n','o', '']:
            save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)

    elif choice==2:
        clear()
        terme = int(input('Enter a number: ' if language == 'en' else 'Entrez un nombre: '))
        t = app_functions.dec_to_lambda_relative_integers(terme)
 
        print(msg,logic.to_string(t))
        logic.captureImage(t,path,'ENTIER-RELATIF#'+'('+str(terme)+')',False)
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','o', '']:
            save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()

        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':

            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
    elif choice==3:
        run_main_menu()

def run_boolean_expression(path,language='en'):
    os.makedirs(path, exist_ok=True)
    print_menu(boolean_representation,language)
    choice = int(input(inputMessage[language]))
    while choice not in boolean_representation[language]:
        clear()
        print_menu(boolean_representation)
        choice = int(input(invalidChoiceMessage[language]))
    if choice ==1:
        clear()
        t = app_functions.NOT
        msg = 'Voici le terme:' if language == 'fr' else 'Here is the term:'
        print(msg,logic.to_string(t))
        logic.captureImage(t,path,'NOT',False)
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','o', '']:
                save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            directory = "./saved/" if language == 'en' else "./sauvegarde/"
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
    elif choice==2:
        clear()
        t = app_functions.AND
        msg = 'Voici le terme:' if language == 'fr' else 'Here is the term:'
        print(msg,logic.to_string(t))
        logic.captureImage(t,path,'AND',False)
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','o','']:
                save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            directory = "./saved/" if language == 'en' else "./sauvegarde/"
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
    elif choice==3:
        clear()
        t = app_functions.OR
        msg = 'Voici le terme:' if language == 'fr' else 'Here is the term:'
        print(msg,logic.to_string(t))
        logic.captureImage(t,path,'OR',False)
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','o','']:
                save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            directory = "./saved/" if language == 'en' else "./sauvegarde/"
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
    elif choice ==4:
        clear()
        t = app_functions.XOR
        msg = 'Voici le terme:' if language == 'fr' else 'Here is the term:'
        print(msg,logic.to_string(t))
        logic.captureImage(t,path,'XOR',False)
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','o','']:
                save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            directory = "./saved/" if language == 'en' else "./sauvegarde/"
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)

    elif choice==5:
        clear()
        t = app_functions.IS_ZERO
        msg = 'Voici le terme:' if language == 'fr' else 'Here is the term:'
        print(msg,logic.to_string(t))
        logic.captureImage(t,path,'IS_ZERO',False)
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','o','']:
                save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            directory = "./saved/" if language == 'en' else "./sauvegarde/"
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
    elif choice==6:
        run_main_menu()

    


#------------------------------------------------------------------------------------------------------------------------------------

def print_menu(options, language='en'):
    for key, value in options[language].items():
        print(key, '--', value)

def run_main_menu():
    choice = ''
    language = 'en'
    lang_choice = input('Select language / Sélectionnez la langue (en/fr): ').strip().lower()
    if lang_choice in ['en', 'fr']:
        language = lang_choice

    print(pyfiglet.figlet_format(welcomeBanner[language]))
    print_menu(mainMenuOptions, language)
    try:
        choice = int(input(inputMessage[language]))
    except ValueError:
        clear()
        print_menu(mainMenuOptions, language)

    while choice not in mainMenuOptions[language]:
        choice = int(input(inputMessage[language]))
    if choice == 1:
        clear()
        terme1 = input(termInputMessage[language])
        k=run_beta_reduction_totale(terme1)
        if k!=None:
          clear()
          print(successMessage[language])
        else:
            time.sleep(2)
        return_main_menu()
    elif choice == 2:
        clear()
        terme2 = input(termInputMessage[language])
        v= run_beta_reduction_interactive_totale(terme2)
        if v!=None:
          clear()
          print(successMessage[language])
        else:
            time.sleep(2)
        return_main_menu()
    elif choice == 3:
        clear()
        run_arithmetic_operations_menu()
    elif choice == 4:
        clear()
        run_show_numbers('show_numbers',language)
        return_main_menu()
    elif choice== 5:
        clear()
        run_boolean_expression('boolean expression',language)
        return_main_menu()
    elif choice == 6:
        clear()
        print(goodByeBanner[language])

def run_arithmetic_operations_menu(language='en'):
    path='arithmetic expressions'
    os.makedirs(path, exist_ok=True)
    print_menu(arithmetic_operations_options,language)
    choice = int(input('Enter your choice: ' if language == 'en' else 'Entrez votre choix: '))
    while choice not in arithmetic_operations_options[language]:
        clear()
        print_menu(arithmetic_operations_options)
        msg = 'Voici le terme:' if language == 'fr' else 'Here is the term:'
        directory = "./saved/" if language == 'en' else "./sauvegarde/"
        choice = int(input('Invalid choice. Enter your choice: ' if language == 'en' else 'Choix invalide. Entrez votre choix: '))
    if choice == 1:
        clear()
        print(msg+ logic.to_string(app_functions.ADD))
        logic.captureImage(app_functions.ADD,path,'ADD', False)
        choix=(input("Do you want to try an example? (Y/n) : " if language == 'en' else 'Voulez-vous essayer un exemple? (O/n) : ')).lower()
        while choix not in ['y','n','o','']:
            choix = input('Invalid choice. Do you want to try an example? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous essayer un exemple? (O/n): ').lower()
        if choix=='y' or choix=='' or choix=='o':
            clear()
            print("you are going to try n+m" if language == 'en' else 'vous allez essayer n+m')
            n=int(input("give n : " if language == 'en' else 'donnez n : '))
            m=int(input("give m : " if language == 'en' else 'donnez m : '))
            while n < 0 or m < 0:
                clear()
                print('Relative addition is not possible. Try again.' if language == 'en' else 'L\'addition relative n\'est pas possible. Réessayer.')
                n=int(input("give n : " if language == 'en' else 'donnez n : '))
                m=int(input("give m : " if language == 'en' else 'donnez m : '))
            app_functions.add(app_functions.dec_to_church(n),app_functions.dec_to_church(m))
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','o','']:
            save_image_choice = input('Invalid choice. Do you want to save the images? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':

            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
        return_main_menu()
    elif choice == 2:
        clear()
        print(msg+ logic.to_string(app_functions.SUB))
        logic.captureImage(app_functions.SUB,path,'SUB', False)
        choix=(input("Do you want to try an example? (Y/n) : " if language == 'en' else 'Voulez-vous essayer un exemple? (O/n) : ')).lower()
        while choix not in ['y','n','','o']:
            choix = input('Invalid choice. Do you want to try an example? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous essayer un exemple? (O/n): ').lower()
        if choix=='y' or choix=='' or choix=='o':
            clear()
            print("you are going to try n-m" if language == 'en' else 'vous allez essayer n-m')
            n=int(input("give n : " if language == 'en' else 'donnez n : '))
            m=int(input("give m : " if language == 'en' else 'donnez m : '))
            while m > n:
                clear()
                print('Relative substraction is not possible. Try again.' if language == 'en' else 'La soustraction relative n\'est pas possible. Réessayer.')
                n=int(input("give n : " if language == 'en' else 'donnez n : '))
                m=int(input("give m : " if language == 'en' else 'donnez m : '))
            app_functions.sub(app_functions.dec_to_church(n),app_functions.dec_to_church(m))
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['Y','n','','o']:
            save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
        return_main_menu()
    elif choice == 3:
        clear()
        print(msg+ logic.to_string(app_functions.MUL))
        logic.captureImage(app_functions.MUL,path,'MUL',False)
        choix=(input("Do you want to try an example? (Y/n) : " if language == 'en' else 'Voulez-vous essayer un exemple? (O/n) : ')).lower()
        while choix not in ['y','n','','o']:
            choix = input('Invalid choice. Do you want to try an example? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous essayer un exemple? (O/n): ').lower()
        if choix=='y' or choix=='' or choix=='o':
            clear()
            print("you are going to try n*m" if language == 'en' else 'vous allez essayer n*m')
            n=int(input("give n : " if language == 'en' else 'donnez n : '))
            m=int(input("give m : " if language == 'en' else 'donnez m : '))
            while m < 0 or n < 0:
                clear()
                print('Relative multiplication is not possible. Try again.' if language == 'en' else 'La multiplication relative n\'est pas possible. Réessayer.')
                n=int(input("give n : " if language == 'en' else 'donnez n : '))
                m=int(input("give m : " if language == 'en' else 'donnez m : '))
            app_functions.multiplication(app_functions.dec_to_church(n),app_functions.dec_to_church(m))
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','','o']:
                save_image_choice = input('Invalid choice. Do you want to save the images? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
        return_main_menu()
    elif choice==4:
        clear()
        print(msg+ logic.to_string(app_functions.POW))
        logic.captureImage(app_functions.POW,path,'POWER',False)
        choix=(input("Do you want to try an example? (Y/n) : " if language == 'en' else 'Voulez-vous essayer un exemple? (O/n) : ')).lower()
        while choix not in ['y','n','','o']:
            choix = input('Invalid choice. Do you want to try an example? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous essayer un exemple? (O/n): ').lower()
        if choix=='y' or choix=='' or choix=='o':
            clear()
            print("you are going to try n pow m" if language == 'en' else 'vous allez essayer n puissance m')
            n=int(input("give n : " if language == 'en' else 'donnez n : '))
            m=int(input("give m : " if language == 'en' else 'donnez m : '))
            while m < 0 or n < 0:
                clear()
                print('Relative power is not possible. Try again.' if language == 'en' else 'La puissance relative n\'est pas possible. Réessayer.')
                n=int(input("give n : " if language == 'en' else 'donnez n : '))
                m=int(input("give m : " if language == 'en' else 'donnez m : '))
            app_functions.power(app_functions.dec_to_church(n),app_functions.dec_to_church(m))
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','','o']:
                save_image_choice = input('Invalid choice. Do you want to save the images of the reduction? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
        return_main_menu()
    elif choice==5:
        clear()
        print(msg+ logic.to_string(app_functions.SUCCS))
        logic.captureImage(app_functions.SUCCS,path,'SUCCS',False)
        choix=(input("Do you want to try an example? (Y/n) : " if language == 'en' else 'Voulez-vous essayer un exemple? (O/n) : ')).lower()
        while choix not in ['y','n','','o']:
            choix = input('Invalid choice. Do you want to try an example? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous essayer un exemple? (O/n): ').lower()
        if choix=='y'or choix=='' or choix=='o':
            clear()
            print("you are going to try n+1" if language == 'en' else 'vous allez essayer n+1')
            n=int(input("give n : " if language == 'en' else 'donnez n : '))
            while n<0:
                clear()
                print('Relative integers not possible. Try again.' if language == 'en' else 'Les entiers relatifs ne sont pas possibles. Réessayer.')
                n=int(input("give n : " if language == 'en' else 'donnez n : '))
            app_functions.succ(app_functions.dec_to_church(n))
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','','o']:
                save_image_choice = input('Invalid choice. Do you want to save the images ? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
        return_main_menu()
    elif choice==6:
        clear()
        print(msg+ logic.to_string(app_functions.PRED))
        logic.captureImage(app_functions.PRED,path,'PRED',False)
        choix=(input("Do you want to try an example? (Y/n) : " if language == 'en' else 'Voulez-vous essayer un exemple? (O/n) : ')).lower()
        while choix not in ['y','n','','o']:
            choix = input('Invalid choice. Do you want to try an example? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous essayer un exemple? (O/n): ').lower()
        if choix=='y' or choix=='' or choix=='o':
            clear()
            print("you are going to try n-1" if language == 'en' else 'vous allez essayer n-1')
            n=int(input("give n : " if language == 'en' else 'donnez n : '))
            while n<0:
                clear()
                print('Relative integers not possible. Try again.' if language == 'en' else 'Les entiers relatifs ne sont pas possibles. Réessayer.')
                n=int(input("give n : " if language == 'en' else 'donnez n : '))
            app_functions.predec(app_functions.dec_to_church(n))
        save_image_choice = input('Do you want to save the images? (Y/n): ' if language == 'en' else 'Voulez-vous enregistrer les images? (O/n): ').lower()
        while save_image_choice not in ['y','n','', 'o']:
                save_image_choice = input('Invalid choice. Do you want to save the images? (Y/n): ' if language == 'en' else 'Choix invalide. Voulez-vous enregistrer les images de la réduction? (O/n): ').lower()
        if save_image_choice == 'y' or save_image_choice=='' or save_image_choice=='o':
            os.makedirs(directory+path, exist_ok=True)
            moveImages(path,directory+path)
            os.rmdir(path)
        elif save_image_choice == 'n':
            delete_images(path)
            os.rmdir(path)
        return_main_menu()
    elif choice == 7:
        clear()
        run_main_menu()

run_main_menu()