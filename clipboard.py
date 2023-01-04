import pyperclip
import time

sleep_time = 0.3

texts_to_copy_french = []
texts_to_copy_english = []
# texts_to_copy.append('Je vous conseille de contacter une usine d\'acier inox dans votre secteur et '
#                      'leur demander de fabriquer une plaque percée sur mesure. Le coût sera plus grand, '
#                      'mais dans le cas de votre drain c\'est l\'option la plus sécuritaire.\n')

# texts_to_copy.append('Votre commande est en fabrication. Vous aurez des nouvelles '
#                      'dans les prochains jours concernantl la livraison.')

texts_to_copy_french.append('nous installons 1 poignée car c\'est plus sécuritaire que 2.\n'
                            'En effet, lors de l\'étape initiale du soulèvement du couvercle avec 1 poignée, '
                            'le sol soutient une partie du poid du couvercle.\n'
                            'Ceci aide à diminuer la charge sur le dos dans une position à risque.\n')

texts_to_copy_french.append('votre commande est en voie de production dans les prochains jours ouvrables.\n\n'
                            'Vous aurez des nouvelles dès que c\'est fabriqué et expédié.\n'
                            'N\'hésitez pas si vous avez d\'autres questions.')

texts_to_copy_french.append('Pour confirmer la commande, svp nous indiquer: \n'
                            '- Adresse de livraison\n'
                            '- Mode de paiement (virement interac, virement bancaire, crédit via Paypal / téléphone au besoin)\n'
                            '- Confirmer les mesures et caractéristiques de la soumission.')

# texts_to_copy.append('Je vous invite à visiter https://dragarweb.com '
#                      'pour voir différentes options qui s\'offrent à vous.\n')

# texts_to_copy.append('merci pour le paiement.\n'
#                      'Voici en pièce jointe le reçu d\'achat.\n\n'
#                      'Cordialement,\n')

texts_to_copy_french.append(
    'L\'épaisseur du couvercle est 3/8" avec la surface lisse et 7/16" avec la surface diamantée.\n')

# texts_to_copy.append('Si possible, envoyez-nous une photo du drain sans couvercle.\n'
#                      'Nous pourrons voir la situation et conseiller au besoin.\n')

# texts_to_copy.append('merci pour la photo. SVP confirmer les mesures centre-à-centre du drain '
#                      '(voir pièce jointe pour indications)')

texts_to_copy_french.append('Voici la facture correspondante en pièce jointe.\n'
                            'Pour nous permettre de débuter la production, svp nous indiquer: \n'
                            '- Adresse de livraison\n'
                            '- Mode de paiement (virement interac, crédit via Paypal)\n'
                            '- Confirmer les mesures et caractéristiques du document\n')

texts_to_copy_french.append('Voici les informations pour le virement interac:\n'
                            'Destinataire: interac@dragarweb.com\n'
                            'Montant: XXX.XX\n'
                            'Réponse secrète (si demandée): couvercle\n')

texts_to_copy_french.append('Vous recevrez un courriel de Paypal pour le paiement par crédit.\n'
                            'Il est possible de "payer en tant qu\'invité" sans créer de compte Paypal.\n'
                            'Si ça ne convient pas, un paiement par virement interac est également possible.')

texts_to_copy_english.append('Please let us know the following by email:\n'
                             '- Delivery address\n'
                             '- Payment method (e-interac, credit via Paypal)\n'
                             '- Confirm the measures and specs on the attached bill\n\n'
                             'Here are the information for an e-interac transfer:\n'
                             'Recipient: interac@dragarweb.com\n'
                             'Amount: $252,88\n'
                             'Secret answer (if needed): drain cover'
                             )

texts_to_copy_english.append('Hi xx,\n'
                             'the receipt for your new drain cover is attached to this email.\n\n'
                             'We will contact you in a few days with the delivery details at xx\n'
                             'Let us know if you have any questions.\n\n'
                             'Best regards,'
                             )


def fill_french_clipboard():
    for text in texts_to_copy_french:
        time.sleep(sleep_time)
        pyperclip.copy(text)


def fill_english_clipboard():
    for text in texts_to_copy_english:
        time.sleep(sleep_time)
        pyperclip.copy(text)
