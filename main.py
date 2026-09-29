from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import random


class Juego(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.puntos = 0
        self.vidas = 3
        self.jugando = False

        self.canasta_ancho = dp(110)
        self.canasta_alto = dp(35)
        self.canasta_x = 0
        self.canasta_y = dp(60)

        self.moneda_x = 0
        self.moneda_y = 0
        self.moneda_radio = dp(18)

        self.velocidad = dp(260)

        self.bind(size=self.dibujar)
        Clock.schedule_interval(self.actualizar, 1 / 60)

    def iniciar(self):
        self.puntos = 0
        self.vidas = 3
        self.velocidad = dp(260)
        self.jugando = True

        self.canasta_x = (self.width - self.canasta_ancho) / 2
        self.crear_moneda()
        self.dibujar()

    def crear_moneda(self):
        if self.width <= dp(40):
            return

        self.moneda_x = random.randint(
            int(dp(20)),
            int(self.width - dp(20))
        )
        self.moneda_y = self.height - dp(110)

    def actualizar(self, dt):
        if not self.jugando:
            return

        self.moneda_y -= self.velocidad * dt

        if self.moneda_y <= self.canasta_y + self.canasta_alto:

            atrapada = (
                self.canasta_x <= self.moneda_x <=
                self.canasta_x + self.canasta_ancho
            )

            if atrapada:
                self.puntos += 1
                self.velocidad = dp(260 + (self.puntos // 5) * 25)
                self.crear_moneda()

            elif self.moneda_y < self.canasta_y - dp(20):
                self.vidas -= 1

                if self.vidas <= 0:
                    self.jugando = False
                    App.get_running_app().game_over()
                    return

                self.crear_moneda()

        self.dibujar()
        App.get_running_app().actualizar_marcador()

    def mover_canasta(self, x):
        self.canasta_x = x - self.canasta_ancho / 2

        if self.canasta_x < 0:
            self.canasta_x = 0

        if self.canasta_x + self.canasta_ancho > self.width:
            self.canasta_x = self.width - self.canasta_ancho

        self.dibujar()

    def on_touch_down(self, touch):
        if self.jugando:
            self.mover_canasta(touch.x)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.jugando:
            self.mover_canasta(touch.x)
            return True
        return super().on_touch_move(touch)

    def dibujar(self, *args):
        self.canvas.clear()

        with self.canvas:
            # Fondo
            Color(0.03, 0.05, 0.11, 1)
            Rectangle(pos=self.pos, size=self.size)

            if self.jugando:
                # Moneda
                Color(0.85, 0.45, 0.02, 1)
                Ellipse(
                    pos=(
                        self.moneda_x - self.moneda_radio,
                        self.moneda_y - self.moneda_radio
                    ),
                    size=(
                        self.moneda_radio * 2,
                        self.moneda_radio * 2
                    )
                )

                Color(1, 0.78, 0.05, 1)
                Ellipse(
                    pos=(
                        self.moneda_x - self.moneda_radio + dp(4),
                        self.moneda_y - self.moneda_radio + dp(4)
                    ),
                    size=(
                        (self.moneda_radio - dp(4)) * 2,
                        (self.moneda_radio - dp(4)) * 2
                    )
                )

                # Canasta
                Color(0.08, 0.45, 0.95, 1)
                RoundedRectangle(
                    pos=(self.canasta_x, self.canasta_y),
                    size=(
                        self.canasta_ancho,
                        self.canasta_alto
                    ),
                    radius=[dp(10)]
                )


class AtrapaMonedasApp(App):

    def build(self):
        Window.clearcolor = (0.03, 0.05, 0.11, 1)

        self.juego = Juego()
        self.mostrar_inicio()

        return self.juego

    def label(self, texto, tamano, color=(1, 1, 1, 1)):
        etiqueta = Label(
            text=texto,
            font_size=dp(tamano),
            color=color,
            bold=True,
            size_hint=(1, None),
            height=dp(55),
            halign="center",
            valign="middle"
        )

        etiqueta.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        return etiqueta

    def mostrar_inicio(self):
        self.juego.clear_widgets()

        titulo = self.label(
            "🪙 ATRAPA LAS MONEDAS",
            28,
            (1, 0.78, 0.05, 1)
        )

        titulo.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.70
        }

        self.juego.add_widget(titulo)

        descripcion = self.label(
            "Mueve la canasta con el dedo\n"
            "y atrapa las monedas.",
            18
        )

        descripcion.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.56
        }

        self.juego.add_widget(descripcion)

        boton = Button(
            text="▶  JUGAR",
            font_size=dp(22),
            bold=True,
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.08, 0.45, 0.95, 1),
            size_hint=(None, None),
            size=(dp(220), dp(65)),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.38
            }
        )

        boton.bind(on_release=self.comenzar)

        self.juego.add_widget(boton)

    def comenzar(self, *args):
        self.juego.iniciar()
        self.mostrar_interfaz()

    def mostrar_interfaz(self):
        self.juego.clear_widgets()

        self.marcador = self.label(
            "PUNTOS: 0     VIDAS: ❤️❤️❤️",
            18
        )

        self.marcador.pos_hint = {
            "center_x": 0.5,
            "top": 0.98
        }

        self.juego.add_widget(self.marcador)

    def actualizar_marcador(self):
        if hasattr(self, "marcador"):
            corazones = "❤️" * self.juego.vidas

            self.marcador.text = (
                f"PUNTOS: {self.juego.puntos}     "
                f"VIDAS: {corazones}"
            )

    def game_over(self):
        self.juego.clear_widgets()

        titulo = self.label(
            "GAME OVER",
            38,
            (1, 0.15, 0.18, 1)
        )

        titulo.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.68
        }

        self.juego.add_widget(titulo)

        resultado = self.label(
            f"Puntuación final: {self.juego.puntos}",
            24,
            (1, 0.78, 0.05, 1)
        )

        resultado.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.55
        }

        self.juego.add_widget(resultado)

        boton = Button(
            text="🔄  JUGAR DE NUEVO",
            font_size=dp(20),
            bold=True,
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.1, 0.75, 0.35, 1),
            size_hint=(None, None),
            size=(dp(250), dp(65)),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.38
            }
        )

        boton.bind(on_release=self.comenzar)

        self.juego.add_widget(boton)


if __name__ == "__main__":
    AtrapaMonedasApp().run()
