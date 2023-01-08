# ----------------- Dragar Admin CLI ------------------
# guil.lvsq@gmail.com
# --------------------------------------------------
import re
import time
import win32clipboard  # pip install pywin32
import pyautogui
import webbrowser
import googlesheet
import poste_canada
from Couvercle import Couvercle
from gmailApi import compose_draft
from Dragar import Dragar
from Client import Client

# ----------------------------  FOR REFERENCE AUTO-PIP-INSTALL -----------------------
# import subprocess
# import sys
#
# try:
#     import pandas as pd
# except ImportError:
#     subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandas'])
# finally:
#     import pandas as pd
# ------------------------------------------------------------------------------------


class DragarAdmin:
    # pauses setup
    pyautogui.PAUSE = 0.7
    pyautogui.FAILSAFE = True
    courte_pause = 6
    longue_pause = 10

    # program variables & inititialization
    isTestMode = False
    filenameclient = ""
    filenameSubject = ""
    filename_subject_client = ""
    filenamefab = []
    nomClient = ""
    livraisonClient = ""
    nomFichierData = ""
    soumissionPath = ""
    facturePath = ""
    fabPath = []
    couvercle = Couvercle()
    client = Client()
    biz_info = Dragar()
    messageCourriel = []
    actionUtilisateur = "z"

    # ----------------------------------------------------------------------------------------------------------------------
    # setup initial pour enregistrer date
    # ----------------------------------------------------------------------------------------------------------------------
    def stamp_temporel(self):
        is_valid_id = str(self.client.sheet.cell(9, 2).value).isnumeric()

        if not is_valid_id:
            unique_id_file = open(self.biz_info.uniqueIDPath, "r")  # unique id file update
            uniqueid = (int(unique_id_file.read()) + 1) % 99
            unique_id_file.close()

            unique_id_file = open(self.biz_info.uniqueIDPath, "w")
            unique_id_file.write(str(uniqueid))
            unique_id_file.close()
            self.client.sheet.update_cell(9, 2, uniqueid)

        self.client.sheet.update_cell(10, 2, str(self.client.sheet.cell(10, 3).value))
        self.client.sheet.update_cell(11, 2, str(self.client.sheet.cell(11, 3).value))

    # ----------------------------------------------------------------------------------------------------------------------
    # mettre a jour les inventaire et unitees vendues
    # ----------------------------------------------------------------------------------------------------------------------
    def update_stock_and_sold_units(self):
        nb_unique_covers = int(self.client.sheet.cell(1, 3).value)
        for i in range(nb_unique_covers):
            self.couvercle.cover_id = self.client.sheet.cell(i + 1, 4).value
            nb_same_cover = int(self.client.sheet.cell(i + 1, 7).value)
            price_cell = self.client.sheet.cell(31, i + 2).value
            if price_cell is None:
                price_this_cover = "err: get price"
            else:
                price_this_cover = str(price_cell.replace(",", "."))
            googlesheet.add_to_sold_units(self.couvercle.cover_id, nb_same_cover)  # -------------
            if self.couvercle.cover_id[1] == "S":
                googlesheet.std_remove_from_inventory(self.couvercle.cover_id, nb_same_cover)  # -------------
            else:
                googlesheet.log_custom_cover(self.client.order_ID, price_this_cover, self.couvercle.cover_id,
                                             nb_same_cover)  # -------------

    # ----------------------------------------------------------------------------------------------------------------------
    # rename file to order id
    # ----------------------------------------------------------------------------------------------------------------------
    def rename_spreadsheet(self, ss_order_id):
        pyautogui.hotkey('alt', 'f')
        pyautogui.typewrite(['r'])
        pyautogui.typewrite(ss_order_id)
        pyautogui.typewrite(['enter'])
        print("renamed spreadsheet to ", ss_order_id)

    # ----------------------------------------------------------------------------------------------------------------------
    # enregistre les informations du client. Tableur source doit etre en fenetre active
    # ----------------------------------------------------------------------------------------------------------------------
    def recuperer_informations_client_fab(self):
        self.client.nom = self.client.sheet.cell(1, 2).value
        self.client.email = self.client.sheet.cell(2, 2).value
        self.client.livraison = self.client.sheet.cell(3, 2).value
        self.client.fab_email = self.client.sheet.cell(5, 2).value
        self.client.fab_name = self.client.sheet.cell(6, 2).value
        self.client.order_ID = self.client.sheet.cell(4, 1).value
        print("client & fab infos retrieved")
        return [
            self.client.email,
            self.client.nom,
            self.client.livraison,
            self.client.order_ID,
        ]

    # ----------------------------------------------------------------------------------------------------------------------
    # enregistre le fichier PDF d'une feuille de tableur en fenêtre active
    # ----------------------------------------------------------------------------------------------------------------------
    def enregistrer_current_sheet_pdf(self, filename, pathfichier):
        pyautogui.hotkey('alt', 'f')
        pyautogui.hotkey('alt', 'd')
        pyautogui.hotkey('alt', 'p')
        pyautogui.typewrite(['enter'])
        time.sleep(self.longue_pause)
        pyautogui.typewrite(['tab'])
        pyautogui.typewrite(['enter'])
        time.sleep(self.longue_pause)
        pyautogui.typewrite(filename)
        pyautogui.hotkey('alt', 'd')
        pyautogui.typewrite(pathfichier)
        time.sleep(0.5)
        pyautogui.typewrite(['enter'])
        time.sleep(0.7)
        pyautogui.hotkey('alt', 's')
        time.sleep(self.longue_pause)
        print("saved pdf to ", pathfichier)

    # ----------------------------------------------------------------------------------------------------------------------
    # recupere le ID de la spreadsheet en focus via son URL
    # ----------------------------------------------------------------------------------------------------------------------
    def get_client_spreadsheet(self):
        pyautogui.press(['f6'])
        pyautogui.hotkey('ctrl', 'c')
        win32clipboard.OpenClipboard()
        sheet_id_brut = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        self.biz_info.sheet_id = re.match(r'.*\/d\/(.*)\/', sheet_id_brut).groups()[0]
        self.client.sheet = googlesheet.get_worksheet(self.biz_info.sheet_id)
        print("current sheet ID: ", self.biz_info.sheet_id)
        screen_size_x, screen_size_y = pyautogui.size()
        pyautogui.click(screen_size_x / 2, screen_size_y / 2)

    # ----------------------------------------------------------------------------------------------------------------------
    # place le curseur a une position qui n'interfere pas avec les operations automatiques
    # ----------------------------------------------------------------------------------------------------------------------
    def safe_cursor_position(self):
        screen_size_x, screen_size_y = pyautogui.size()
        pyautogui.moveTo(screen_size_x - 1, screen_size_y / 2)
        time.sleep(0.1)

    # ----------------------------------------------------------------------------------------------------------------------
    # compose un courriel pret a envoyer
    # ----------------------------------------------------------------------------------------------------------------------
    def generer_courriel(self, type_document, destinataire):
        print("creating draft: ", type_document, " ", destinataire)
        to = "mock_to"
        email_sujet = "mock_email_subject"
        facture_attach_paths = []
        soumission_attach_paths = []

        # client -------------------------------------------
        if destinataire == "client":
            to = self.client.email
            email_sujet = self.biz_info.email_subject_client + " - " + self.filename_subject_client
            email_produit = self.biz_info.email_product_name
            # composition message
            self.messageCourriel.clear()
            self.messageCourriel.append("Bonjour " + self.client.nom + ", ")
            if type_document == "soumission":
                soumission_attach_paths.append(self.soumissionPath + self.filenameclient)
                self.messageCourriel.append(
                    "\nvoici une soumission correspondant à votre demande de couvercle de drain.\n")
                self.messageCourriel.append('Pour confirmer la commande, svp nous indiquer: \n'
                                            '- Adresse de livraison\n'
                                            '- Mode de paiement (virement interac, virement bancaire, crédit via '
                                            'Paypal / téléphone au besoin)\n '
                                            '- Confirmer les mesures et caractéristiques de la soumission.')
            elif type_document == "facture":
                facture_attach_paths.append(self.facturePath + self.filenameclient)
                self.messageCourriel.append(
                    "\nvoici la confirmation et le reçu d'achat (pièce jointe) pour votre " + email_produit + ".")
                self.messageCourriel.append("\n\nNous vous contacterons prochainement pour vous indiquer "
                                            "les détails de la livraison au " + self.client.livraison + ".")

            # messageCourriel.append("\n\nNous sommes en vacances jusqu'au 6 juin 2021."
            #                        "\nNous vous contacterons dès notre retour pour vous indiquer "
            #                        "les détails de la livraison au " + client.livraison + ".")

            # COVID LIVRAISON --------------------------------------------
            # messageCourriel.append("\nSVP prendre note que le temps de livraison est un peu "
            #                        "plus grand ces jours-ci chez Postes Canada."
            #                        "\nNous effectuons un suivi pour toutes les commandes.")
            # ------------------------------------------------------------

            self.messageCourriel.append("\n\nN'hésitez pas si vous avez des questions.")
            self.messageCourriel.append("\nCordialement,")
            self.messageCourriel.append("\n-Guillaume Lévesque\n")
            self.messageCourriel.append(
                "\n-" + self.biz_info.title + "-\n" + self.biz_info.website + "\n" + self.biz_info.sender)

        # fab --------------------------------------------------
        elif destinataire == "fab":
            to = self.client.fab_email
            if type_document == "PO":
                facture_attach_paths.append(self.fabPath[0] + self.filenamefab[0])
                if self.couvercle.cover_id[1] == "S":
                    facture_attach_paths.append(self.client.shipping_label_path)
                email_sujet = self.filenameSubject + ": " + self.client.nom
                email_produit = self.biz_info.email_product_name
                # composition message
                self.messageCourriel.clear()
                self.messageCourriel.append("Salut " + self.client.fab_name + ",")
                self.messageCourriel.append("\nVoici un PO de " + email_produit + ".")

            elif type_document == "label":
                facture_attach_paths.append(self.client.shipping_label_path)
                email_sujet = self.client.order_ID + " shipping label"
                self.messageCourriel.clear()
                self.messageCourriel.append("Salut Pa,")
                self.messageCourriel.append("\nVoici le shipping label pour la commande " + self.client.order_ID + ".")

            self.messageCourriel.append("\n\nBonne journée,\n-Guillaume\n-Dragar Inc-")

        else:
            print("erreur: destinataire inconnu")
            exit()

        compose_draft(self.biz_info.sender, to, email_sujet, self.messageCourriel,
                      (soumission_attach_paths if type_document == "soumission" else facture_attach_paths))

    # ----------------------------------------------------------------------------------------------------------------------
    # achat etc
    # ----------------------------------------------------------------------------------------------------------------------
    def vente(self, window):
        print("Aller au spreadsheet. Vous avez " + str(self.longue_pause) + " secondes.")
        time.sleep(self.longue_pause)
        self.get_client_spreadsheet()
        self.safe_cursor_position()

        self.facturePath = self.biz_info.facturePath
        self.fabPath.append(self.biz_info.pofabPath)
        self.fabPath.append(self.biz_info.adressePath)
        self.nomFichierData = self.biz_info.nomFichierData

        self.stamp_temporel()
        self.recuperer_informations_client_fab()
        googlesheet.log_client(self.client.nom, self.client.email)
        self.rename_spreadsheet(self.client.order_ID)

        # poste can shipping label
        print("initiating postes canada shipping label")
        self.couvercle.cover_id = self.client.sheet.cell(1, 4).value
        if self.couvercle.cover_id[1] == "S":
            if self.couvercle.cover_id[0] == "R":
                [self.client.shipping_label_path, self.client.shipping_price] = poste_canada.poste_can(
                    self.client.email, self.client.nom,
                    self.client.livraison,
                    self.client.order_ID, "S",
                    weight_lbs="17.5",
                    window=window)
            elif self.couvercle.cover_id[0] == "P":
                [self.client.shipping_label_path, self.client.shipping_price] = poste_canada.poste_can(
                    self.client.email, self.client.nom,
                    self.client.livraison,
                    self.client.order_ID, "S",
                    weight_lbs="10",
                    window=window)
            else:
                print("erreur code couvercle")
                exit()
            if self.client.shipping_price != 0.1:
                googlesheet.write_shipping_price_std(self.biz_info.sheet_id, self.client.shipping_price)
                googlesheet.log_shipping_cost(self.client.shipping_price)
            else:
                print("10 sec to go back to spreadsheet source")
                time.sleep(10)
        # else:
        # googlesheet.save_custom_info_for_future_shipping(client.order_ID, client.email, client.nom, client.livraison)

        # retourner au spreadsheet
        webbrowser.open('https://docs.google.com/spreadsheets/d/' + self.biz_info.sheet_id)
        time.sleep(10)
        screen_size_x, screen_size_y = pyautogui.size()
        pyautogui.click(screen_size_x / 2, screen_size_y / 2)

        # enregistrer pdf fichier client
        print("saving client pdf")
        self.filenameclient = str(self.client.sheet.cell(1, 1).value) + ".pdf"
        self.filename_subject_client = self.client.sheet.cell(1, 1).value
        pyautogui.hotkey('alt', 'down')
        self.enregistrer_current_sheet_pdf(self.filenameclient, self.facturePath)

        # enregistrer pdf PO Fab
        self.filenamefab.append(str(self.client.sheet.cell(2, 1).value) + ".pdf")
        self.filenameSubject = str(self.client.sheet.cell(2, 1).value)
        pyautogui.hotkey('alt', 'down')
        print("saving fab pdf")
        self.enregistrer_current_sheet_pdf(self.filenamefab[0], self.fabPath[0])
        pyautogui.hotkey('alt', 'up')
        pyautogui.hotkey('alt', 'up')

        # prix
        prix_client = self.client.sheet.cell(5, 1).value
        cost_total = self.client.sheet.cell(6, 1).value

        self.update_stock_and_sold_units()  # ---------

        # save repartition
        if self.couvercle.cover_id[1] == "S":
            googlesheet.save_std_sale_repartition(
                self.client.order_ID, re.sub(",", ".", prix_client),
                (re.sub(",", ".", cost_total)))  # ---------

        # generer courriels
        self.generer_courriel("facture", "client")
        self.generer_courriel("PO", "fab")
        webbrowser.open('https://mail.google.com/mail/u/0/#drafts')
        exit()

    # ----------------------------------------------------------------------------------------------------------------------
    # compose un courriel pret a envoyer
    # ----------------------------------------------------------------------------------------------------------------------
    def soumission(self):
        # laisser du temps pour placer la source en fenetre active
        print("Aller au spreadsheet. Vous avez " + str(self.longue_pause) + " secondes.")
        time.sleep(self.longue_pause)
        self.safe_cursor_position()
        self.soumissionPath = self.biz_info.soumissionPath
        self.get_client_spreadsheet()
        self.stamp_temporel()
        self.recuperer_informations_client_fab()
        self.rename_spreadsheet(self.client.order_ID)

        pyautogui.hotkey('ctrl', 'home')
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.hotkey('alt', 'down')
        win32clipboard.OpenClipboard()
        self.filenameclient = "Couvercle de drain " + win32clipboard.GetClipboardData() + ".pdf"
        print('filename', self.filenameclient)
        win32clipboard.CloseClipboard()

        self.enregistrer_current_sheet_pdf(self.filenameclient, self.soumissionPath)
        self.filename_subject_client = self.client.sheet.cell(1, 1).value
        self.generer_courriel("soumission", "client")
        webbrowser.open('https://mail.google.com/mail/u/0/#drafts')
        exit()

    # ----------------------------------------------------------------------------------------------------------------------
    # Terminal Menu principal
    # ----------------------------------------------------------------------------------------------------------------------
    # while actionUtilisateur != 'q':
    #     print("\n---- DRAGAR Menu principal " + biz_info.title + " ----")
    #     print("\ns - Soumission"
    #           "\na - Achat"
    #           "\nl - Label for shipping"
    #           "\nf - Fill clipboard french"
    #           "\nfe - Fill clipboard english"
    #           "\nc - Copy main file"
    #           "\nq - Quitter")
    #     actionUtilisateur = input("opération : ")
    #
    #     # -----------------------------------------------------------------------------------------------------------
    #     # soumission
    #     # -----------------------------------------------------------------------------------------------------------
    #     if actionUtilisateur == 's':
    #         print("soumission...")
    #
    #     # -----------------------------------------------------------------------------------------------------------
    #     # label shipping custom
    #     # -----------------------------------------------------------------------------------------------------------
    #     elif actionUtilisateur == "l":
    #         client.order_ID = input("order id: ")
    #         [email, name, adr, o_id, dim1, dim2, dim3, weight] = googlesheet.get_custom_shipping_info_for_label(
    #             client.order_ID)
    #         [client.shipping_label_path, client.shipping_price] = poste_canada.poste_can(email, name, adr,
    #                                                                                      client.order_ID, "M", dim1,
    #                                                                                      dim2, dim3, weight)
    #         print("label path: ", client.shipping_label_path)
    #         googlesheet.write_shipping_price_custom(client.order_ID, client.shipping_price)
    #         googlesheet.log_shipping_cost(client.shipping_price)
    #         generer_courriel("label", "fab")
    #         webbrowser.open('https://mail.google.com/mail/u/0/#drafts')
    #         exit()
    #
    #     # -----------------------------------------------------------------------------------------------------------
    #     # label shipping custom
    #     # -----------------------------------------------------------------------------------------------------------
    #     elif actionUtilisateur == "c":
    #         googlesheet.copy_source_spreadsheet()
    #         exit()
    #
    #     # -----------------------------------------------------------------------------------------------------------
    #     # clipboard
    #     # -----------------------------------------------------------------------------------------------------------
    #     elif actionUtilisateur == "f":
    #         print("\nfilling french..")
    #         fill_french_clipboard()
    #         print("clipboard filled")
    #         actionUtilisateur = "z"
    #         exit()
    #
    #     elif actionUtilisateur == "fe":
    #         print("\nfilling english..")
    #         fill_english_clipboard()
    #         print("clipboard filled")
    #         actionUtilisateur = "z"
    #         exit()
    #
    #     # -----------------------------------------------------------------------------------------------------------
    #     # achat
    #     # -----------------------------------------------------------------------------------------------------------
    #     elif actionUtilisateur == 'a':
    #         print('achat...')
    #
    #     # -----------------------------------------------------------------------------------------------------------
    #     # quitter
    #     # -----------------------------------------------------------------------------------------------------------
    #     elif actionUtilisateur == 'q':
    #         print("Bonne journée.")
    #         time.sleep(1)
    #
    #     # -----------------------------------------------------------------------------------------------------------
    #     # choix invalide
    #     # -----------------------------------------------------------------------------------------------------------
    #     else:
    #         print("action '" + actionUtilisateur + "' invalide.")
