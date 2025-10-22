import flet as ft

from automobile import Automobile
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    txt_aggiungiNuovaAuto = ft.Text(
        value=f"Aggiungi nuova automobile",
        size=16,
        weight=ft.FontWeight.BOLD)

    input_marca = ft.TextField(label="Marca", width=150)
    input_modello = ft.TextField(label="Modello", width=150)
    input_anno = ft.TextField( label="Anno", width=150)
    input_posti = ft.TextField(label="Posti", value="0", text_align=ft.TextAlign.RIGHT, width=100)


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def conferma_automobile(e):
        Automobile.marca = input_marca.value
        Automobile.modello = input_modello.value
        Automobile.anno = input_anno.value
        Automobile.posti = input_posti.value
        # controllo che i valori (data e posti) siano validi
        if int(Automobile.posti) <= 0 or Automobile.anno.isdigit() == False:
            alert.show_alert("❌ Errore: inserisci valori numerici validi per anno e posti.")
        else:
            autonoleggio.aggiungi_automobile(Automobile.marca, Automobile.modello, Automobile.anno, Automobile.posti)
            aggiorna_lista_auto()
        page.update()

    def minus_click(e):
        if int(input_posti.value) > 0:
            input_posti.value = str(int(input_posti.value) - 1)
            page.update()

    def plus_click(e):
        input_posti.value = str(int(input_posti.value) + 1)
        page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    pulsante_conferma_automobile = ft.ElevatedButton("Conferma", on_click=conferma_automobile)

    buttonMinus = ft.IconButton(ft.Icons.REMOVE, on_click=minus_click)
    buttonPlus = ft.IconButton(ft.Icons.ADD, on_click=plus_click)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        txt_aggiungiNuovaAuto,
        ft.Row(spacing=10,
               controls=[input_marca, input_modello, input_anno, buttonMinus, input_posti, buttonPlus, pulsante_conferma_automobile],
               alignment=ft.MainAxisAlignment.CENTER),


        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
