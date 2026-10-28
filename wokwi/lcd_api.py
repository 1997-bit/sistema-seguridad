"""Provides an API for talking to HD44780 compatible character LCDs."""
import time


class LcdApi:
    """ Implementa la API para la comunicación con pantallas LCD de caracteres compatibles con
    HD44780.
    Esta clase solo sabe qué comandos enviar a la pantalla LCD, pero no cómo enviarlos.
    El método de envío se gestiona mediante clases derivadas.
    """

    # Los siguientes nombres de constantes se tomaron del archivo de cabecera lcd.h de avrlib.
    # Sin embargo, cambié las definiciones de números de bits a máscaras de bits.
    # # Conjunto de comandos del controlador LCD
    LCD_CLR = 0x01
    LCD_HOME = 0x02
    LCD_ENTRY_MODE = 0x04
    LCD_ENTRY_INC = 0x02
    LCD_ENTRY_SHIFT = 0x01
    LCD_ON_CTRL = 0x08
    LCD_ON_DISPLAY = 0x04
    LCD_ON_CURSOR = 0x02
    LCD_ON_BLINK = 0x01
    LCD_MOVE = 0x10
    LCD_MOVE_DISP = 0x08
    LCD_MOVE_RIGHT = 0x04
    LCD_FUNCTION = 0x20
    LCD_FUNCTION_8BIT = 0x10
    LCD_FUNCTION_2LINES = 0x08
    LCD_FUNCTION_10DOTS = 0x04
    LCD_FUNCTION_RESET = 0x30
    LCD_CGRAM = 0x40
    LCD_DDRAM = 0x80
    LCD_RS_CMD = 0
    LCD_RS_DATA = 1
    LCD_RW_WRITE = 0
    LCD_RW_READ = 1

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        if self.num_lines > 4:
            self.num_lines = 4
        self.num_columns = num_columns
        if self.num_columns > 40:
            self.num_columns = 40
        self.cursor_x = 0
        self.cursor_y = 0
        self.implied_newline = False
        self.backlight = True
        self.display_off()
        self.backlight_on()
        self.clear()
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)
        self.hide_cursor()
        self.display_on()

    def clear(self):
        """ Borra la pantalla LCD y mueve el cursor a la esquina superior izquierda.."""
        self.hal_write_command(self.LCD_CLR)
        self.hal_write_command(self.LCD_HOME)
        self.cursor_x = 0
        self.cursor_y = 0

    def show_cursor(self):
        """ Hace que el cursor se haga visible.."""
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY |
                               self.LCD_ON_CURSOR)

    def hide_cursor(self):
        """ Hace que el cursor se oculte."""
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)

    def blink_cursor_on(self):
        """ Enciende el cursor y lo hace parpadear."""
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY |
                               self.LCD_ON_CURSOR | self.LCD_ON_BLINK)

    def blink_cursor_off(self):
        """ Enciende el cursor y hace que no parpadee (es decir, que se quede fijo)."""
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY |
                               self.LCD_ON_CURSOR)

    def display_on(self):
        """ Enciende (es decir, activa) la pantalla LCD."""
        self.hal_write_command(self.LCD_ON_CTRL | self.LCD_ON_DISPLAY)

    def display_off(self):
        """ Apaga (es decir, deja en negro) la pantalla LCD."""
        self.hal_write_command(self.LCD_ON_CTRL)

    def backlight_on(self):
        """ Enciende la retroiluminación."""
        self.backlight = True
        self.hal_backlight_on()

    def backlight_off(self):
        """ Apaga la retroiluminación."""
        self.backlight = False
        self.hal_backlight_off()

    def move_to(self, cursor_x, cursor_y):
        """ Mueve la posición del cursor a la posición indicada."""
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3f
        if cursor_y & 1:
            addr += 0x40  # Lines 1 & 3 add 0x40
        if cursor_y & 2:
            addr += 0x14  # Lines 2 & 3 add 0x14
        self.hal_write_command(self.LCD_DDRAM | addr)

    def putchar(self, char):
        """ Escribe el carácter indicado en la pantalla LCD en la posición actual del cursor."""
        if char == '\n':
            if self.implied_newline:
                # If we get a newline character just after an implied one, ignore it
                self.implied_newline = False
            else:
                self.cursor_x = self.num_columns
        else:
            self.hal_write_data(ord(char))
            self.cursor_x += 1
        if self.cursor_x >= self.num_columns:
            self.cursor_x = 0
            self.cursor_y += 1
            self.implied_newline = (char != '\n')
        if self.cursor_y >= self.num_lines:
            self.cursor_y = 0
        self.move_to(self.cursor_x, self.cursor_y)

    def putstr(self, string):
        """ Escriba la cadena indicada en la pantalla LCD en la posición actual del cursor."""
        for char in string:
            self.putchar(char)

    def custom_char(self, location, charmap):
        """ Escribe un carácter en una de las 8 ubicaciones CGRAM, disponibles como chr(0) a
        chr(7)."""
        location &= 0x7
        self.hal_write_command(self.LCD_CGRAM | (location << 3))
        time.sleep_us(40)
        for i in range(8):
            self.hal_write_data(charmap[i])
            time.sleep_us(40)
        self.move_to(self.cursor_x, self.cursor_y)

    def hal_backlight_on(self):
        """ Permite que la capa hal encienda la retroiluminación."""
        pass

    def hal_backlight_off(self):
        """ Permite que la capa HAL apague la retroiluminación."""
        pass

    def hal_write_command(self, cmd):
        """ Escribe un comando en la pantalla LCD.."""
        raise NotImplementedError

    def hal_write_data(self, data):
        """ Escribir datos en la pantalla LCD."""
        raise NotImplementedError
