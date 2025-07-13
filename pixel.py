import pyray as rl
from pyray import Vector2

# Definir las coordenadas de los poligonos
polygons = {
    1: [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)],
    2: [(321, 335), (288, 286), (339, 251), (374, 302)],
    3: [(377, 245), (411, 197), (436, 249)],
    4: [(413, 177), (448, 159), (502, 88), (533, 53), (535, 36), (676, 37), (669, 52), 
        (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), 
        (597, 215), (552, 214), (517, 144), (466, 180)],
    5: [(682, 175), (708, 120), (735, 148), (739, 170)]  # Agujero dentro del poligono 4
}

def draw_filled_polygon(points, color):
    """Dibuja un poligono relleno usando scan-line filling"""
    if len(points) < 3:
        return
    
    # Encontrar limites del poligono
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    
    # Para cada linea horizontal (scan line)
    for y in range(int(min_y), int(max_y) + 1):
        intersections = []
        
        # Encontrar intersecciones con los bordes del poligono
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            
            # Verificar si la linea horizontal intersecta con este borde
            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                # Calcular punto de interseccio
                if p2[1] != p1[1]:  # Evitar divisio por cero
                    x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                    intersections.append(x)
        
        # Ordenar intersecciones
        intersections.sort()
        
        # Dibujar lineas entre pares de intersecciones
        for i in range(0, len(intersections), 2):
            if i + 1 < len(intersections):
                start_x = int(intersections[i])
                end_x = int(intersections[i + 1])
                if start_x != end_x:
                    rl.draw_line(start_x, y, end_x, y, color)

def point_in_polygon(point, polygon):
    """Verifica si un punto esa dentro de un poligono usando ray casting"""
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def main():
    # Configuracion de la ventana
    screen_width = 800
    screen_height = 600
    
    rl.init_window(screen_width, screen_height, "Rellenado de Poligonos")
    rl.set_target_fps(60)
    
    # Crear render texture para guardar como PNG
    render_texture = rl.load_render_texture(screen_width, screen_height)
    
    # Colores para cada poligono
    colors = {
        1: rl.RED,
        2: rl.GREEN,
        3: rl.BLUE,
        4: rl.YELLOW,
        5: rl.WHITE  # El agujero se dibuja en blanco (fondo)
    }
    
    while not rl.window_should_close():
        # Comenzar dibujo
        rl.begin_drawing()
        rl.clear_background(rl.WHITE)
        
        # Comenzar dibujo en render texture
        rl.begin_texture_mode(render_texture)
        rl.clear_background(rl.WHITE)
        
        # Dibujar poligonos 1, 2, 3 normalmente
        for poly_id in [1, 2, 3]:
            draw_filled_polygon(polygons[poly_id], colors[poly_id])
        
        # Dibujar poligono 4
        draw_filled_polygon(polygons[4], colors[4])
        
        # "Borrar" el agujero (poligono 5) dibujandolo en blanco
        draw_filled_polygon(polygons[5], rl.WHITE)
        
        # Dibujar contornos para mejor visualizacion
        for poly_id, points in polygons.items():
            if poly_id == 5:  # El agujero se dibuja con linea negra
                color = rl.BLACK
            else:
                color = rl.BLACK
            
            for i in range(len(points)):
                start = points[i]
                end = points[(i + 1) % len(points)]
                rl.draw_line(start[0], start[1], end[0], end[1], color)
        
        rl.end_texture_mode()
        
        # Dibujar el render texture en la pantalla
        rl.draw_texture_rec(
            render_texture.texture,
            rl.Rectangle(0, 0, screen_width, -screen_height),  # Negative height to flip
            Vector2(0, 0),
            rl.WHITE
        )
        
        # Instrucciones
        rl.draw_text("Presiona ESPACIO para guardar out.png", 10, 10, 20, rl.BLACK)
        rl.draw_text("ESC para salir", 10, 40, 20, rl.BLACK)
        
        # Guardar imagen si se presiona ESPACIO
        if rl.is_key_pressed(rl.KEY_SPACE):
            # Crear una imagen desde el render texture
            image = rl.load_image_from_texture(render_texture.texture)
            rl.image_flip_vertical(image)  # Voltear porque OpenGL tiene Y invertido
            rl.export_image(image, "out.png")
            rl.unload_image(image)
            print("Imagen guardada como out.png")
        
        rl.end_drawing()
    
    # Limpiar recursos
    rl.unload_render_texture(render_texture)
    rl.close_window()

if __name__ == "__main__":
    main()